import os
import sys
import xml.etree.ElementTree as ET

from BasicCommands import BasicCommands
from WorkWithModule import WorkWithModule


class StringParser():
    """
    @description: This class parses the text retrieve by Microsoft in order
    to distinguish external commands, internal commands and modules
    """

    def __init__(self, config, text, File, PID):
        # read configuration files
        self.pid = PID
        try:
            max_size = 0
            text = text.lower()
            tree = ET.parse(File)
            root = tree.getroot()
            tp = ''

            for entry in root.findall('entry'):
                score = 0
                entry_name = entry.get('name')
                voice_key = entry.find('key').text
                command_to_apply = entry.find('command').text
                the_linker = entry.find('linker').text
                space_by_plus = entry.find('spacebyplus').text

                key = voice_key.split(' ')
                for j in range(len(key)):
                    score += text.count(key[j])

                if max_size < score:
                    max_size = score
                    do = command_to_apply
                    tp = entry_name
                    linker = the_linker
                    spacebyplus = space_by_plus

            os.system('echo "' + do + '" > /tmp/mama/mama_cmd_' + self.pid)
            if 'modules' in tp:
                # if we find the word "modules", a WorkWithModule class and we pass it we instantiate
                # the folder ie weather, search, ...; the module name weather.sh ie, search.sh and against delivery
                WorkWithModule(do, text, linker, spacebyplus, self.pid)
            elif 'internal' in tp:
                # we execute an internal command, the command is configured
                # and internal / battery, battery is sent to the function
                BasicCommands(config, do, self.pid)
            elif 'external' in tp:
                os.system(do + ' &')
            else:
                os.system('xdotool type "' + do + '"')

            os.system('touch /tmp/mama/mama_stop_' + self.pid)


        except Exception as e:
            message = 'Setup file missing'
            os.system(
                'echo "' + message + '" > /tmp/mama/mama_error_' + self.pid)
            sys.exit(1)
