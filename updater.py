import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys
import json
import urllib.request

# Declaring variables
current_version = 0.1
new_version_info = {}

# This is the github api url of mama release page
host = 'https://api.github.com/repos/maateen/mama/releases'


class MessageDialogWindow(Gtk.Window):
    """
    @description: This class show new stable and pre release message dialog
    To show it on nay page just import the class and then
        win = MessageDialogWindow()
        win.show_stable_release_message()
        win.show_all()
    @param: text
        text will show in the dialog
    """

    def __init__(self, text, url):
        Gtk.Window.__init__(self)
        self.text = text
        self.url = url

    def __install_latest_version(self):
        os.system("unzip /tmp/mama/latest.zip")
        os.system("gksu python3 /tmp/mama/mama/install.py &")
        sys.exit(0)

    def __download_latest_version(self):
        if not os.path.exists("/tmp/mama"):
            os.system("mkdir -p /tmp/mama")
        os.system("wget -O /tmp/mama/latest.zip " + self.url)
        print("Latest version downloaded successfully.")
        self.__install_latest_version()

    def show_pre_release_message(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   "Mama! New beta version available!")
        dialog.format_secondary_text(self.text)
        dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Pre release dialog closed by clicking OK button")
            dialog.destroy()
            self.__download_latest_version()
        elif response == Gtk.ResponseType.CANCEL:
            print("Pre release dialog closed by clicking CANCEL button")
            dialog.destroy()

    def show_stable_release_message(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL,
                                   "Mama! New stable version available!")
        dialog.format_secondary_text(self.text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Stable release dialog closed by clicking OK button")
            dialog.destroy()
            self.__download_latest_version()
        elif response == Gtk.ResponseType.CANCEL:
            print("Stable release dialog closed by clicking CANCEL button")
            dialog.destroy()


# Getting data from github API
try:
    conn = urllib.request.urlopen(host)
    response = conn.read().decode('utf-8')
    info = json.loads(response)

    # Parsing data from info in new_version_info dict
    for key, data in info[0].items():
        if 'assets' == key:
            for new_list in data:
                for x, y in new_list.items():
                    if 'api' in str(y):
                        pass
                    else:
                        new_version_info[x] = y
        elif 'author' in key:
            pass
        elif 'upload' in key:
            pass
        else:
            if 'api' in str(data):
                pass
            else:
                new_version_info[key] = data

    new_version_info['tag_name'] = new_version_info['tag_name'].strip('v')
    published_at = new_version_info['published_at'].split('T')
    new_version_info['published_at'] = published_at[0]
    size = new_version_info['size'] / 1024
    size = str(size).split('.')
    new_version_info['size'] = size[0]
except:
    sys.exit(0)

print(new_version_info)

# Checking first whether any new release is available or not.
if float(new_version_info['tag_name']) > current_version:

    # If the release isn't drafted, then we will proceed
    if not new_version_info['draft']:
        # If the release is stable, then we will show a stable message dialog

        text = "Latest stable version : " + new_version_info[
            'tag_name'] + "\nPublished at : " + new_version_info[
                   'published_at'] + "\n"
        release_notes = "Release notes:\n" + new_version_info['body'] + "\n"
        text2 = "\nAlready " + str(
            new_version_info['download_count']) + " people " \
                                                  "updated " \
                                                  "to this " \
                                                  "version. " \
                                                  "Do you " \
                                                  "want to update? (" \
                                                  "" + new_version_info[
                    'size'] + " KB will be downloaded)"
        if not new_version_info['prerelease']:
            stable_message_dialog = MessageDialogWindow(text + release_notes +
                                                        text2, new_version_info[
                                                            'browser_download_url'])
            stable_message_dialog.show_stable_release_message()
            stable_message_dialog.show_all()
        else:
            pre_message_dialog = MessageDialogWindow(text + release_notes +
                                                     text2, new_version_info[
                                                         'browser_download_url'])
            pre_message_dialog.show_pre_release_message()
            pre_message_dialog.show_all()
    sys.exit(0)
else:
    print("No update available.")
