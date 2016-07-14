from workWithModule import workWithModule
from basicCommands import basicCommands
import xml.etree.ElementTree as ET
import os, sys

# Let you run the command associated with a spoken word
class stringParser():
    """
    @description: This class parses the text retrieve by Google in order
    to distinguish external commands, internal commands and modules
    """
    def __init__(self,text,File,PID):
        # read configuration files
        self.pid=PID
        try:
            max = 0
            text=text.lower()
            tree = ET.parse(File)
            root = tree.getroot()
            tp = ''
            # if the dictation mode is activated
            if os.path.exists('/tmp/mama/mama_dictation'):
                for entry in root.findall('entry'):
                    if entry.get('name') == _('internal') and entry.find('command').text == unicode(_('exit dictation mode'),"utf8"):
                        score = 0
                        Type=entry.get('name')
                        Key=entry.find('key').text
                        Command=entry.find('command').text
                        key=Key.split(' ')
                        for j in range(len(key)):
                            score += text.count(key[j])

                        if score == len(key):
                            do = Command
                            tp = Type
                        else:
                            do = text
            else:
                for entry in root.findall('entry'):
                    score = 0
                    Type=entry.get('name')
                    Key=entry.find('key').text
                    Command=entry.find('command').text
                    Linker = entry.find('linker').text
                    Spacebyplus = entry.find('spacebyplus').text

                    key=Key.split(' ')
                    for j in range(len(key)):
                        score += text.count(key[j])

                    if max < score:
                        max = score
                        do = Command
                        tp = Type
                        linker = Linker
                        spacebyplus = Spacebyplus

            do = do.encode('utf8')
            tp = tp.encode('utf8')

            print("key", tp)
            print("command", do)

            os.system('echo "'+do+'" > /tmp/mama/mama_cmd_'+self.pid)
            if _('modules') in tp:
                # if we find the word "modules", a workWithModule class and we pass it we instantiate
                # the folder ie weather, search, ...; the module name weather.sh ie, search.sh and against delivery
                linker = linker.encode('utf8')
                spacebyplus = spacebyplus.encode('utf8')
                wm = workWithModule(do,text,linker,spacebyplus,self.pid)
            elif _('internal') in tp:
                # we execute an internal command, the command is configured
                # and internal / battery, battery is sent to the function
                b = basicCommands(do,self.pid)
            elif _('external') in tp:
                os.system(do+' &')
            else:
                os.system('xdotool type "'+do+'"')

            os.system('> /tmp/mama/mama_stop_'+self.pid)


        except Exception as e:
            message = _('Setup file missing')
            os.system('echo "'+message+'" > /tmp/mama/mama_error_'+self.pid)
            sys.exit(1)
