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

    def __init__(self, text):
        Gtk.Window.__init__(self)
        self.text = text

    def show_info_message(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   "Info")
        dialog.format_secondary_text(self.text)
        dialog.run()
        print("Info dialog closed")

        dialog.destroy()

    def show_error_message(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL,
                                   "Error")
        dialog.format_secondary_text(self.text)
        dialog.run()
        print("Error dialog closed")

        dialog.destroy()

    def show_warn_message(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL,
                                   "Warning")
        dialog.format_secondary_text(self.text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Warning dialog closed by clicking OK button")
        elif response == Gtk.ResponseType.CANCEL:
            print("Warning dialog closed by clicking CANCEL button")

        dialog.destroy()
