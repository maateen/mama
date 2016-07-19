import http.client
import json
import os
import sys
import urllib.parse
from os.path import expanduser

import xmltodict
from Listener import Listener
from StringParser import StringParser


class Interface():
    """
    @description: This class start the notifier, then start recording your voice before
    asking Microsoft for the speech-to-text. Then, the result is parsing in order to
    execute the associated action
    """

    def __init__(self, config):
        self.p = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
        self.PID = str(os.getpid())

        # Initialization notifications
        os.system(
            'python3 ' + self.p + 'notifier.py ' + self.PID + ' &')

        # We launch the recorder
        Listener(config, self.PID)
        self.sendto(config)

    def sendto(self, config):
        """
        @function: Send the wav file to Microsoft and start the parser
        """

        # configuration file
        config_file = expanduser('~') + '/.config/mama/mama.xml'
        default = self.p + 'config/' + 'en_EN' + '/default.xml'

        if os.path.exists(config_file):
            config_file = config_file
        else:
            if not os.path.exists(expanduser('~') + '/.config/mama'):
                os.makedirs(expanduser('~') + '/.config/mama')
            if not os.path.exists(
                            expanduser('~') + '/.config/mama/modules'):
                os.system('cp -r ' + self.p + '/modules ' + expanduser(
                    '~') + '/.config/mama')
            if not os.path.exists(default):
                default = self.p + 'config/en_EN/default.xml'

            config_file = default

        print("config file:", config_file)

        host = "https://speech.platform.bing.com"

        params = urllib.parse.urlencode(
            {'grant_type': 'client_credentials',
             'client_id': config['client_id'],
             'client_secret': config['api_key'], 'scope': host})

        headers = {"Content-type": "application/x-www-form-urlencoded"}

        access_token_host = "oxford-speech.cloudapp.net"
        token_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "/token/issueToken")

        # Connecting to server to get the Microsoft Bing Speech API Access Token
        conn = http.client.HTTPSConnection(access_token_host, timeout=10)
        conn.request("POST", token_path, params, headers)
        response = conn.getresponse()
        print(response.status)

        if response.status == 200:

            data = response.read()
            conn.close()
            access_token = data.decode("UTF-8")

            # Decoding the object from json
            decoded_data = json.loads(access_token)
            access_token = decoded_data['access_token']

            # Reading the binary from wave file
            f = open('/tmp/mama/output.wav', 'rb')
            try:
                body = f.read();
            finally:
                f.close()

            headers = {"Content-type": "audio/wav; samplerate=" + str(config[
                                                                          'audio_rate']) + "; sourcerate=" + str(
                config['audio_rate']),
                       "Authorization": "Bearer " + access_token}

            # Connect to server to recognize the wave binary
            conn = http.client.HTTPSConnection("speech.platform.bing.com",
                                               timeout=30)
            conn.request("POST",
                         "/recognize/query?scenarios=ulm&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=en-US&device.os=wp7&version=3.0&format=xml&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66",
                         body, headers)
            response = conn.getresponse()
            print(response.status)

            if response.status == 200:

                data = response.read()
                conn.close()
                result = json.loads(
                    json.dumps(xmltodict.parse(data.decode("UTF-8"))))
                try:
                    text = result['speechbox-root']['results']['result']['name']
                except:
                    text = ''
                print(text)
                os.system("echo '" + text + "' > /tmp/mama/mama_result_" +
                          str(self.PID))

                # parsing the results to find the action
                StringParser(config, text,
                             config_file, self.PID)

            else:
                print(response.reason)
                os.system(
                    'echo "' + response.reason + '" > /tmp/mama/mama_error_' + self.PID)
                sys.exit(1)
        else:
            print(response.reason)
            os.system(
                'echo "' + response.reason + '" > /tmp/mama/mama_error_' + self.PID)
            sys.exit(1)
