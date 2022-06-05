import gi
import sys
from .window import MainWindow


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio, GLib, GObject


GObject.threads_init()
class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="org.ultramarinelinux.tweaks"
        )
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(app=self)
        self.window.show_all()

    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about)
        self.add_action(about_action)

    def about(self, action, param):
        about = Gtk.AboutDialog(modal=True, transient_for=self.window)

        about.set_program_name("Ultramarine Tweaks")
        about.set_version("0.1.0")
        about.set_logo_icon_name("ultramarine")
        about.set_copyright("Copyright © 2022 Ultramarine Linux Team")
        about.set_license_type(Gtk.License.MIT_X11)
        about.set_website("https://ultramarine-linux.org")
        about.set_authors([
            "Cappy Ishihara <cappy@cappuchino.xyz>",
            "windowsboy111 <wboy111@outlook.com>",
        ])
        about.connect("response", lambda d, r: about.destroy())
        about.show()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
