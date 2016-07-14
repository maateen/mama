from os.path import expanduser
import sys, os, gettext, locale

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/library')
from interface import interface
from localehelper import LocaleHelper

localeHelper = LocaleHelper()
lang = localeHelper.getLocale()

t=gettext.translation('mama',os.path.dirname(os.path.abspath(__file__))+'/i18n/',languages=[lang])
t.install()


# pause media player if necessary
config = expanduser('~')+'/.config/mama/mama.conf'
paused = False
haskey = False
client_id = ''
api_key = ''

try:
    with open(config,"r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            field = line.split('=')
            if field[0] == 'pause' and field[1].replace('"','') != '':
                os.system(field[1].replace('"','')+' &')
                paused = True
            elif field[0] == 'play':
                play_command = field[1].replace('"','')
            elif field[0] == 'client_id' and field[1].replace('"','') != '':
                client_id = field[1].replace('"','')
                hasid = True
            elif field[0] == 'api_key' and field[1].replace('"','') != '':
                api_key = field[1].replace('"','')
                haskey = True

except Exception:
    print("Error reading mama.conf file")

if hasid == True and haskey == True:
    print(client_id, api_key)
    # launch the recognition
    mama = interface(client_id, api_key)

    # restore media player state
    if paused:
        os.system(play_command+' &')
