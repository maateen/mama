import sys
from os import system
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import expanduser

sys.path.append(dirname(abspath(__file__)) + '/library')
from Interface import Interface

# Declaring some variables, config{} dict will contain all config info
config = {}
config_file = expanduser('~') + '/.config/mama/mama.conf'
temp_dir = '/tmp/mama/'
has_key = False
has_id = False

# Lets check the existence of temp_dir, create if not
if not exists(temp_dir):
    system("mkdir -p '" + temp_dir + "'")

try:
    with open(config_file, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            field = line.split('=')
            if field[0] == 'audio_chunk':
                self.audio_chunk = int(field[1])
            elif field[0] == 'audio_format':
                self.audio_format = field[1].replace('"', '')
            elif field[0] == 'audio_channels':
                self.audio_channels = int(field[1])
            elif field[0] == 'audio_rate':
                self.audio_rate = int(field[1])
            elif field[0] == 'recording_time':
                self.recording_time = int(field[1])
            elif field[0] == 'client_id':
                self.client_id = field[1].replace('"', '')
            elif field[0] == 'api_key':
                self.api_key = field[1].replace('"', '')

except Exception:
    print("Error reading mama.conf file")

if has_id and has_key:
    # launch the recognition
    Interface(config)
