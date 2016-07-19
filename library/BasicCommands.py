import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from BingTextToSpeech import TextToSpeech
from MessageDialogWindow import MessageDialogWindow
import os, time, subprocess


class BasicCommands():
    """
    @description: Called when the user wants to start an internal command
    for the moment there is 3 internal commands:

    * time
    * clipboard
    * power

    @param config
        A dictionary containing Microsoft Bing Speech API Key and Azure
        client ID, also some other info

    @param text
        name of the function to launch

    @param PID
        the program's pid to synchronize osd notification
    """

    def __init__(self, config, text, PID):
        # according to the received parameter, performs an action
        self.config = config
        self.pid = PID
        if text == 'time':
            self.get_time()
        elif text == 'power':
            self.get_power()
        elif text == 'clipboard':
            self.read_clipboard()
        else:
            error_dialog = MessageDialogWindow("No action found!")
            error_dialog.show_error_message()
            error_dialog.show_all()

    def read_clipboard(self):
        """
        @description: A function to make mama reads the selected
        text
        """
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

        text = clipboard.wait_for_text()
        if text:
            text = text.replace("'", ' ')
            TextToSpeech(self.config, text)
        else:
            TextToSpeech('Nothing in the clipboard')

    def get_time(self):
        """
        @description: a function that let mama read and display
        the current time
        """
        var = time.strftime('%H:%M', time.localtime())
        hour = var.split(':')[0]
        minute = var.split(':')[1]

        message = 'it is' + ' ' + hour + ' ' + 'hour' + ' ' + minute + ' ' + 'minute'
        os.system('echo "' + var + '" > /tmp/mama/mama_display_' + self.pid)
        TextToSpeech(self.config, message, self.pid)

    def get_power(self):
        """
        @description: a function that let mama read and display
        the current power state
        """
        command = "acpi -b"
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if output:
            output = output.decode("utf-8", "strict")[:-1]
            output = output.replace(',', '')
            output = output.split(' ')
        else:
            error_dialog = MessageDialogWindow(error)
            error_dialog.show_error_message()
            error_dialog.show_all()
        # parsing output
        if 'Battery' in output:
            battery_percentage = output[3]
            if len(output) > 4:
                remaining_time = output[4]

                if 'Charging' in output:
                    message = 'Charging' + ', now ' + battery_percentage + ', ' + \
                              remaining_time + ' ' + 'until charged'
                else:
                    message = 'Discharging' + ', now ' + battery_percentage + ', ' \
                                                                              '' + \
                              remaining_time + ' ' + 'remaining'
            else:
                message = 'Not charging, ' + battery_percentage + ' remaining'
        else:
            message = 'battery is not plugged'

        os.system('echo "' + message + '" > /tmp/mama/mama_display_' + self.pid)
        TextToSpeech(self.config, message, self.pid)
