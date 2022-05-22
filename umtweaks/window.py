import sys
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import Gtk, Gio, GLib, Handy




class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Ultramarine Tweaks")

        self.set_default_size(800, 500)

        headerbar = Gtk.HeaderBar()

        headerbar.set_show_close_button(True)
        headerbar.props.title = "Ultramarine Tweaks"

        headerbar.set_subtitle("Ultimate Linux Tweaks")
        headerbar.set_show_close_button(True)
        self.set_titlebar(headerbar)

        self.set_border_width(10)

        self.hsize_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL)

        self.main_box = Handy.Leaflet()
        self.main_box.set_transition_type(Handy.LeafletTransitionType.SLIDE)

        left_box = self.sidebar()
        right_box = self.main_content()

        self.main_box.add(left_box)
        self.main_box.child_set(left_box, name="sidebar")
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.main_box.add(separator)
        self.main_box.add(right_box)
        self.main_box.child_set(right_box, name="content")
        right_box.props.hexpand = True


        # HOW DO I ADD CONTENT TO SIDEBAR
        # FIXME: META: Please send GTK devs. - Ultramarine Linux Team

        # TODO: Add content to sidebar

        self.add(self.main_box)


    def sidebar(self):
        # Copied over from GNOME Tweaks
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_box.set_size_request(200, -1)
        self.entry = Gtk.SearchEntry(placeholder_text=("Search Tweaks…"))
        if (Gtk.check_version(3, 22, 20) is None):
            self.entry.set_input_hints(Gtk.InputHints.NO_EMOJI)
        #self.entry.connect("search-changed", self._on_search)
        
        self.searchbar = Gtk.SearchBar()
        self.searchbar.add(self.entry)
        self.searchbar.props.hexpand = False
        
        self.searchbar = Gtk.SearchBar()
        self.searchbar.add(self.entry)
        self.searchbar.props.hexpand = False

        self.listbox = Gtk.ListBox()
        self.listbox.get_style_context().add_class("tweak-categories")
        #self.listbox.connect("row-selected", self._on_select_row)
        #self.listbox.set_header_func(self._list_header_func, None)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER,
                          Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.listbox)

        left_box.pack_start(self.searchbar, False, False, 0)
        left_box.pack_start(scroll, True, True, 0)

        self.hsize_group.add_widget(left_box)

        return left_box
    
    def main_content(self):
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box.set_size_request(540, -1)

        self.stack = Gtk.Stack()
        self.stack.get_style_context().add_class("main-container")

        right_box.pack_start(self.stack, True, True, 0)

        return right_box