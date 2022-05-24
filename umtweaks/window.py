import sys
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import Gtk, Gio, GLib, Handy

from .widgets import ListBoxRow, MainContent, main_content

import umtweaks.modules as modules

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Ultramarine Tweaks")

        self.set_default_size(800, 500)

        headerbar = Gtk.HeaderBar()

        headerbar.set_show_close_button(True)
        headerbar.props.title = "Ultramarine Tweaks"

        headerbar.set_subtitle("Ultimate Linux Tweaks")
        headerbar.set_show_close_button(True)
        self.set_titlebar(self.header_bar())

        #self.set_border_width(10)

        self.hsize_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL)

        self.main_box = Handy.Leaflet()
        self.main_box.set_transition_type(Handy.LeafletTransitionType.SLIDE)

        left_box = self.sidebar()
        right_box = MainContent()

        self.main_box.add(left_box)
        self.main_box.child_set(left_box, name="sidebar")
        self.main_seperator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.main_box.add(self.main_seperator)
        self.main_box.add(right_box)

        self.main_box.child_set(right_box, name="content")
        right_box.props.hexpand = True
        self.main_box.connect("notify::folded", self.csd_update)

        modules.load_modules_to_pages(right_box.stack)

        # FIXME: META: Please send GTK devs. - Ultramarine Linux Team

        # TODO: Add content to sidebar

        # add content to sidebar
        self.back_button = None

        self.add(self.main_box)


    def header_bar(self):
        """A header bar as a Leaflet"""
        header = Handy.Leaflet()
        header.set_transition_type(Handy.LeafletTransitionType.SLIDE)
        header.connect("notify::visible-child", self.csd_update)
        # Check if the leaflet is folded
        #if header.

        left_header = Gtk.HeaderBar()
        left_header.props.show_close_button = False

        self.header_right = Gtk.HeaderBar()
        self.header_right.props.show_close_button = True
        self.header_right.props.hexpand = True

        self.header_right.set_title("Ultramarine Tweaks")

        left_header.get_style_context().add_class("titlebar")
        left_header.get_style_context().add_class("tweak-titlebar-left")
        self.header_right.get_style_context().add_class("titlebar")
        self.header_right.get_style_context().add_class("tweak-titlebar-right")


        #header.bind_property("folded", self.back_button, "visible")

        #self.back_button.hide()

        #self.seperator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)

        #header.add(left_header)
        #header.add(self.seperator)
        header.add(self.header_right)

        return header

    def _on_back_button_clicked(self, widget):
        #print("Back button clicked")
        # We call this twice because of the funny separator
        self.main_seperator.set_visible(False)
        self.main_box.navigate(Handy.NavigationDirection.BACK)
        self.main_box.navigate(Handy.NavigationDirection.BACK)
        self.main_seperator.set_visible(True)


    def csd_update(self, *args, **kwargs):
        #print(kwargs)
        a = self.get_titlebar()



        # Check if main box is folded
        if self.main_box.props.folded:
            if not self.back_button:
                self.back_button = Gtk.Button.new_from_icon_name("go-previous-symbolic", 1)
                self.back_button.connect("clicked", self._on_back_button_clicked)
                self.header_right.pack_start(self.back_button)
                self.back_button.hide()
            #self.seperator.props.visible = False
            self.back_button.props.visible = True
        else:
            #self.seperator.props.visible = True
            if self.back_button:
                self.back_button.props.visible = False
        #print(a)


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

        self.listbox = Gtk.ListBox(can_default=True)
        self.listbox.get_style_context().add_class("tweak-categories")
        #self.listbox.connect("row-selected", self._on_select_row)
        #self.listbox.set_header_func(self._list_header_func, None)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER,
                          Gtk.PolicyType.AUTOMATIC)

        # Add content to listbox
        """ page1 = ListBoxRow("Tweaks", "system-run-symbolic", self, "Testing")
        self.listbox.add(page1)

        page2 = ListBoxRow("Settings", "preferences-system", self)
        self.listbox.add(page2)

        page3 = ListBoxRow("Backups", "drive-multidisk-symbolic", self)
        self.listbox.add(page3) """

        modules.load_modules_to_listbox(self.listbox, self)

        scroll.add(self.listbox)

        left_box.pack_start(self.searchbar, False, False, 0)
        left_box.pack_start(scroll, True, True, 0)

        self.hsize_group.add_widget(left_box)

        return left_box