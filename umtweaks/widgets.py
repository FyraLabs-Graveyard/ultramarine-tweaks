import sys
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import Gtk, Gio, GLib, Handy
#rom .window import MainWindow

def main_content():
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box.set_size_request(540, -1)

        stack = Gtk.Stack()
        stack.get_style_context().add_class("main-container")

        right_box.pack_start(stack, True, True, 0)

        return right_box

class MainContent(Gtk.Box):
    def __init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0):
        Gtk.Box.__init__(self, orientation=orientation, spacing=spacing)
        self.set_size_request(540, -1)
        self.stack = Gtk.Stack()
        self.stack.get_style_context().add_class("main-container")

        self.pack_start(self.stack, True, True, 0)



class ListBoxRow(Gtk.ListBoxRow):
    def __init__(self, title, icon_name: str=None, window = None, description: str=None):
        super().__init__()
        # Let's add a fancy box for padding
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_margin_left(10)
        hbox.set_margin_right(10)
        hbox.set_margin_top(10)
        hbox.set_margin_bottom(10)
        label = Gtk.Label(title)
        self.title = title
        if icon_name:
            icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.SMALL_TOOLBAR)
            # Spacing between icon and title
            icon.set_margin_right(10)
            hbox.pack_start(icon, False, False, 0)
        else:
            label.set_margin_left(25)

        hbox.add(label)

        self.add(hbox)
        self.set_activatable(False)
        # map on click
        self.connect("activate", self.select)
        self.connect("focus-in-event", self.select)

        self.test_content = MainContent()
        self.window = window

    def select(self, *args, **kwargs) -> None:
        #print(args)
        #print(kwargs)
        #print("select:", self.title)
        #self.window.main_box.navigate(Handy.NavigationDirection.FORWARD)
        #self.window.main_box.set_visible_child_name(self.title)
        # Get child of self.window.main_box.get_visible_child()
        # which should be a Gtk.Stack
        leaflet: Gtk.Container = self.window.main_box
        box: Gtk.Box = leaflet.get_children()[-1]
        stack: Gtk.Stack = box.get_children()[0]
        # Destroy all children of stack
        for child in stack.get_children():
            stack.remove(child)
        # Add new child to stack
        content = Gtk.Label(f"{self.title} Here")
        stack.add(content)
        stack.show_all()