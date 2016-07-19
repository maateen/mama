import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

# manage the development of the module selection window
class ModuleSelection():
    """
    @description: This class display an fileChooserDialog when the user
    wants to add a new module from the menu of the main window
    """
    def __init__(self):
        w=Gtk.Window()
        dialog = Gtk.FileChooserDialog(_("Choose a file"), w,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        self.module = '-1'
        if response == Gtk.ResponseType.OK:
            self.module=dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def getModule(self):
        """
        @description: return the module selected

        @return: return the path to the executable of the module
        """
        return self.module
