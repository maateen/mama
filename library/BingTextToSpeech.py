import http.client
import json
import os
import sys
import urllib.parse


class TextToSpeech():
    """
    @description: Let mama to use the Microsoft Bing Text-to-Speech API

    @param config
        A dictionary containing Microsoft Bing Speech API Key and Azure
        client ID, also some other info

    @param text
        the text to read to the user
    """

    def __init__(self, config, text, pid):
        client_id = config['client_id']
        api_key = config['api_key']
        host = "https://speech.platform.bing.com"

        params = urllib.parse.urlencode(
            {'grant_type': 'client_credentials', 'client_id': client_id,
             'client_secret': api_key, 'scope': host})

        headers = {"Content-type": "application/x-www-form-urlencoded"}

        access_token_host = "oxford-speech.cloudapp.net"
        token_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "/token/issueToken")

        # Connecting to server to get the Microsoft Bing Speech API Access Token
        conn = http.client.HTTPSConnection(access_token_host, timeout=10)
        conn.request("POST", token_path, params, headers)
        response = conn.getresponse()

        if response.status == 200:
            data = response.read()
            conn.close()
            access_token = data.decode("UTF-8")

            # Decoding the object from json
            decoded_data = json.loads(access_token)
            access_token = decoded_data['access_token']

            body = "<speak version='1.0' xml:lang='en-us'><voice " \
                   "xml:lang='en-us' xml:gender='Male' name='Microsoft " \
                   "Server Speech Text to Speech Voice (en-US, " \
                   "BenjaminRUS)'>" + text + "</voice></speak>"

            headers = {"Content-type": "application/ssml+xml",
                       "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
                       "Authorization": "Bearer " + access_token,
                       "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
                       "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
                       "User-Agent": "Mama"}

            # Connect to server to synthesize the wave
            conn = http.client.HTTPSConnection("speech.platform.bing.com")
            conn.request("POST", "/synthesize", body, headers)
            response = conn.getresponse()
            print(response.status, response.reason)

            data = response.read()
            conn.close()
            wf = open('/tmp/mama/tts.wav', 'wb')
            wf.write(data)
            wf.close()
            os.system('play /tmp/mama/tts.wav')
            os.system('touch /tmp/mama/mama_stop_' + pid)
            sys.exit(1)
        else:
            os.system(
                'echo "' + response.reason + '" > /tmp/mama/mama_error_' + pid)
            sys.exit(1)
