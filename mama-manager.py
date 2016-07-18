import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/library')
from MainWindow import MainWindow


class MyApplication(Gtk.Application):
    """
    @description: Initializing the main window for Mama Manager
    """
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MainWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
