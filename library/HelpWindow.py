import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# manage the appearance of the Help window
class HelpWindow():
    """
    @description: Diaplay an help window
    """
    def __init__(self):
        #a  Gtk.AboutDialog
        self.aboutdialog = Gtk.AboutDialog()

        # lists of authors and documenters (will be used later)
        authors = ["Maksudur Rahman Maateen <http://maateen.me/>"]
        documenters = ["Maksudur Rahman Maateen <http://maateen.me/>"]

        # we fill in the aboutdialog
        self.aboutdialog.set_program_name(_("About Mama"))
        self.aboutdialog.set_version("Alpha Version")
        self.aboutdialog.set_copyright("Maksudur Rahman Maateen \xa9 2016")
        self.aboutdialog.set_comments("The aim of this project is to let you use Microsoft powered Bing Speech Recognition API to control your Linux computer. The project is developed in Python3. For note, this is a fork of project google2ubuntu.")
        self.aboutdialog.set_license_type (Gtk.License.GPL_3_0,)
        self.aboutdialog.set_website("https://maateen.github.io/mama/")
        self.aboutdialog.set_website_label("https://maateen.github.io/mama/")
        self.aboutdialog.set_authors(authors)
        self.aboutdialog.set_documenters(documenters)

        # Resetting the window title
        self.aboutdialog.set_title("About Mama")

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        self.aboutdialog.connect("response", self.on_close)
        # show the aboutdialog
        self.aboutdialog.show()

    # destroy the aboutdialog
    def on_close(self, action, parameter):
        """
        @description: function called when the user wants to close the window

        @param: action
            the window to close
        """
        action.destroy()
