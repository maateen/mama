import os
import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MessageDialogWindow(Gtk.Window):
    """
    @description: This class show info, warning and error message dialog
    To show it on nay page just import the class and then
        win = MessageDialogWindow()
        win.show_warn_message()
        win.show_all()
    @param: text
        text will show in the dialog
    """

    def __init__(self):
        Gtk.Window.__init__(self)
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   "Mama! New version Installed Successfully")
        dialog.run()
        print("Info dialog closed")

        dialog.destroy()

# Initializing the parent and directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
print('Parent directory: ' + parent_dir)
target_dir = '/usr/share/mama'
print('Target directory: ' + target_dir)
# Checking target directory existence
if os.path.exists(target_dir):
    print('Target directory exists, so making it empty.')
    os.system("gksu \"rm -rf " + target_dir + "\"")
    os.system("gksu \"mkdir -p " + target_dir + "\"")
else:
    os.system("gksu \"mkdir -p " + target_dir + "\"")
    print('Target directory does not exist, so created.')

# Now copying files and folders
config_dir = parent_dir + '/config'
os.system("gksu \"cp -vr " + config_dir + " " + target_dir + "\"")
library_dir = parent_dir + '/library'
os.system("gksu \"cp -vr " + library_dir + " " + target_dir + "\"")
modules_dir = parent_dir + '/modules'
os.system("gksu \"cp -vr " + modules_dir + " " + target_dir + "\"")
resources_dir = parent_dir + '/resources'
os.system("gksu \"cp -vr " + resources_dir + " " + target_dir + "\"")
os.system("gksu \"cp -v " + parent_dir + "/mama.py" + " " + target_dir + "\"")
os.system(
    "gksu \"cp -v " + parent_dir + "/mama-manager.py" + " " + target_dir + "\"")
os.system(
    "gksu \"cp -v " + parent_dir + "/notifier.py" + " " + target_dir + "\"")

# Now copying desktop launcher
print('Now making desktop launcher.')
if os.path.exists('/usr/share/applications/mama.desktop'):
    os.system("gksu \"rm /usr/share/applications/mama.desktop\"")
    os.system(
        "gksu \"cp -v " + parent_dir + "/mama.desktop" + " /usr/share/applications\"")
else:
    os.system(
        "gksu \"cp -v " + parent_dir + "/mama.desktop" + " /usr/share/applications\"")

if os.path.exists('/usr/share/applications/mama-manager.desktop'):
    os.system("gksu \"rm /usr/share/applications/mama-manager.desktop\"")
    os.system("gksu \"cp -v " + parent_dir + "/mama-manager.desktop" + " "
                                                                     "/usr/share/applications")

print('\n\nInstalled Successfully.\n\n')
win = MessageDialogWindow()
win.show_all()
sys.exit(0)
