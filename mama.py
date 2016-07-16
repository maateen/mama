import sys
from os import system
from os.path import abspath, dirname, exists, expanduser

sys.path.append(dirname(abspath(__file__)) + '/library')
from Interface import Interface

# Declaring some variables, config{} dict will contain all config info
config = {}
config_file = expanduser('~') + '/.config/mama/mama.conf'
temp_dir = '/tmp/mama/'
# pause media player if necessary
config['paused'] = False
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
            if field[0] == 'pause' and field[1].replace('"', '') != '':
                system(field[1].replace('"', '') + ' &')
                config['paused'] = True
            elif field[0] == 'play':
                config['play_command'] = field[1].replace('"', '')
            elif field[0] == 'client_id' and field[1].replace('"', '') != '':
                config['client_id'] = field[1].replace('"', '')
                has_id = True
            elif field[0] == 'api_key' and field[1].replace('"', '') != '':
                config['api_key'] = field[1].replace('"', '')
                has_key = True

except Exception:
    print("Error reading mama.conf file")

if has_id and has_key:
    # launch the recognition
    Interface(config)

    # restore media player state
    if config['paused']:
        system(play_command + ' &')
