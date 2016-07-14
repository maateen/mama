import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from Bingtts import tts
import os, time, subprocess

# Allows to appeal to basic functions
class basicCommands():
    """
    @description: Called when the user wants to start an internal command
    for the moment there is 3 internal commands:

    * time
    * clipboard
    * hour

    @param text
        name of the function to launch

    @param PID
        the program's pid to synchronize osd notification
    """
    def __init__(self,text,PID):
        # according to the received parameter, performs an action
        self.pid = PID
        if text == _('time'):
            self.getTime()
        elif text == _('power'):
            self.getPower()
        elif text == _('clipboard'):
            self.read_clipboard()
        elif text == _('dictation mode'):
            f=open('/tmp/mama/mama_dictation',"w")
            f.close()
        elif text == _('exit dictation mode'):
            os.remove('/tmp/mama/mama_dictation')
        else:
            print("no action found")

    def read_clipboard(self):
        """
        @description: A function to make mama reads the selected
        text
        """
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

        text = clipboard.wait_for_text()
        if text != None:
            text=text.replace("'",' ')
            print("read:", text)
            tts(text)
        else:
            tts(_('Nothing in the clipboard'))

    def getTime(self):
        """
        @description: a function that let mama read and display
        the current timme
        """
        var=time.strftime('%H:%M',time.localtime())
        hour=var.split(':')[0]
        minute=var.split(':')[1]

        message = _('it is')+' '+hour+' '+_('hour')+' '+minute+' '+_('minute')
        os.system('echo "'+var+'" > /tmp/mama/mama_display_'+self.pid)
        print(message)
        tts(message)

    def getPower(self):
        """
        @description: a function that let mama read and display
        the current power state
        """
        command = "acpi -b"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = process.communicate()
        #parsing output
        if output.count('Battery') > 0:
            pcent = output.split(' ')[3]
            rtime = output.split(' ')[4]

            if output.count('Charging') > 0:
                message = _('Charging')+': '+pcent+'\n'+rtime+' '+_('before charging')
            else:
                message = _('Discharging')+': '+pcent+'\n'+rtime+' '+_('remaining')
        else:
            message = _('battery is not plugged')

        os.system('echo "'+message+'" > /tmp/mama/mama_display_'+self.pid)
        tts(message)
