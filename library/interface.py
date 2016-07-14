from os.path import expanduser
import http.client, sys, os, json, urllib.parse, xmltodict
from stringParser import stringParser
from localehelper import LocaleHelper
from listener import listener

# The interface class to start recording and communicating with Google
class interface():
    """
    @description: This class start the osd server, then start recording your voice before
    asking Google for the translation. Then, the result is parsing in order to
    execute the associated action
    """
    def __init__(self, client_id, api_key):
        # make the program able to switch language
        self.p = os.path.dirname(os.path.abspath(__file__)).strip('library')

        localeHelper = LocaleHelper('en_EN')

        self.lang = localeHelper.getLocale()
        # this line can be remove if we modify the config/en_EN to config/en
        #self.lang = self.lang+'_'+self.lang.upper()

        # Initialization notifications
        self.PID = str(os.getpid())
        os.system('rm /tmp/mama/mama_*_'+self.PID+' 2>/dev/null')
        os.system('python3 '+self.p+'library/osd.py '+self.PID+' &')

        # we play a sound to signal the start
        os.system('play '+self.p+'resources/sound.wav &')
        os.system('> /tmp/mama/mama_start_'+self.PID)

        # We launch the recorder
        listener(self.PID)
        self.sendto(client_id, api_key)

    def sendto(self, client_id, api_key):
        """
        @function: Send the wav file to Microsoft and start the parser
        """

        # configuration file
        config = expanduser('~') + '/.config/mama/mama.xml'
        default = self.p +'config/'+self.lang+'/default.xml'

        if os.path.exists(config):
            config_file = config
        else:
            if os.path.exists(expanduser('~') +'/.config/mama') == False:
                os.makedirs(expanduser('~') +'/.config/mama')
            if os.path.exists(expanduser('~') +'/.config/mama/modules') == False:
                os.system('cp -r '+self.p+'/modules '+expanduser('~') +'/.config/mama')
            if os.path.exists(default) == False:
                default = self.p+'config/en_EN/default.xml'

            config_file = default

        print("config file:", config_file)

        clientId = client_id
        clientSecret = api_key
        Host = "https://speech.platform.bing.com"

        params = urllib.parse.urlencode({'grant_type': 'client_credentials', 'client_id': clientId, 'client_secret': clientSecret, 'scope': Host})

        headers = {"Content-type": "application/x-www-form-urlencoded"}

        AccessTokenHost = "oxford-speech.cloudapp.net"
        token_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "/token/issueToken")

        # Connecting to server to get the Microsoft Bing Speech API Access Token
        conn = http.client.HTTPSConnection(AccessTokenHost, timeout=10)
        conn.request("POST", token_path, params, headers)
        response = conn.getresponse()
        print(response.status)

        if response.status == 200:

            data = response.read()
            conn.close()
            accesstoken = data.decode("UTF-8")

            # Decoding the object from json
            ddata = json.loads(accesstoken)
            access_token = ddata['access_token']

            # Reading the binary from wave file
            f = open('output.wav','rb')
            try:
                body = f.read();
            finally:
                f.close()

            headers = {"Content-type": "audio/wav; samplerate=8000",
                        "Authorization": "Bearer " + access_token}

            #Connect to server to recognize the wave binary
            conn = http.client.HTTPSConnection("speech.platform.bing.com", timeout=30)
            conn.request("POST", "/recognize/query?scenarios=ulm&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=en-US&device.os=wp7&version=3.0&format=xml&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66", body, headers)
            response = conn.getresponse()

            if response.status == 200:

                data = response.read()
                conn.close()
                text = json.loads(json.dumps(xmltodict.parse(data.decode("UTF-8"))))
                print(text['speechbox-root']['results']['result']['name'])
                os.system('echo "'+text['speechbox-root']['results']['result']['name']+'" > /tmp/mama/mama_result_'+self.PID)

                # parsing the results to find the action
                sp = stringParser(text,config_file,self.PID)

            else:
                print(response.reason)
                os.system('echo "'+response.reason+'" > /tmp/mama/mama_error_'+self.PID)
                sys.exit(1)
        else:
            print(response.reason)
            os.system('echo "'+response.reason+'" > /tmp/mama/mama_error_'+self.PID)
            sys.exit(1)