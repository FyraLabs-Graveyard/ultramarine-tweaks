import gi
import sys
from .window import MainWindow


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

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

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
