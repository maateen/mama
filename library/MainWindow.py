import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from AddWindow import AddWindow
from SetupWindow import SetupWindow
import os


class MainWindow(Gtk.ApplicationWindow):
    """
    @description: This class display the main window that the user will
    see when he wants to manage his commands
    """

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Mama Manager", application=app)
        self.set_default_size(800, 400)
        self.set_resizable(True)
        self.set_border_width(0)
        self.get_focus()
        self.set_position(Gtk.WindowPosition.CENTER)
        path = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
        self.icon_path = path + 'resources/icons/'
        self.set_default_icon_from_file(path + '/resources/icons.png')

        # get two button to switch between view
        setup_icon = Gtk.Image()
        setup_icon.set_from_file(self.icon_path + 'setup.png')
        button_config = Gtk.ToolButton(icon_widget=setup_icon)
        button_config.set_label("Setup")
        button_config.set_is_important(True)
        button_config.set_tooltip_text('Open setup window')
        button_config.show()
        button_config.connect("clicked", self.change_page, 1)

        button_back = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        button_back.connect("clicked", self.change_page, 0)
        button_cancel = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.change_page, 0)

        # get the main view
        content = AddWindow(button_config)
        label_main = Gtk.Label("main")
        config = SetupWindow(button_back, button_cancel)
        label_config = Gtk.Label("config")

        # create a Gtk.Notebook to store both page
        self.notebook = Gtk.Notebook.new()
        self.notebook.set_show_tabs(False)
        self.notebook.append_page(content.get_grid(), label_main)
        self.notebook.append_page(config.getGrid(), label_config)

        # show
        self.add(self.notebook)
        self.show_all()

    def change_page(self, button, page):
        self.notebook.set_current_page(page)
