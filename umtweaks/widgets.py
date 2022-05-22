import sys
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import Gtk, Gio, GLib, Handy



def titlebar(self):

        header = Handy.Leaflet()
        header.set_transition_type(Handy.LeafletTransitionType.SLIDE)
        header.connect("notify::visible-child", self._update_decorations)
        header.connect("notify::folded", self._update_decorations)

        left_header = Gtk.HeaderBar()
        left_header.props.show_close_button = True
        right_header = Gtk.HeaderBar()
        right_header.props.show_close_button = True
        right_header.props.hexpand = True

        self._left_header = left_header
        self._right_header = right_header

        left_header.get_style_context().add_class("titlebar")
        left_header.get_style_context().add_class("tweak-titlebar-left")
        right_header.get_style_context().add_class("titlebar")
        right_header.get_style_context().add_class("tweak-titlebar-right")

        self._group_titlebar_widget = None

        self.title = Gtk.Label(label="")
        self.title.get_style_context().add_class("title")
        right_header.set_custom_title(self.title)

        self.back_button = Gtk.Button.new_from_icon_name("go-previous-symbolic", 1)
        self.back_button.connect("clicked", self._on_back_clicked)
        header.bind_property("folded", self.back_button, "visible")
        right_header.pack_start(self.back_button)

        icon = Gtk.Image()
        icon.set_from_icon_name("edit-find-symbolic", Gtk.IconSize.MENU)
        self.button = Gtk.ToggleButton()
        self.button.add(icon)
        self.button.connect("toggled", self._on_find_toggled)
        self.button.props.valign = Gtk.Align.CENTER
        self.button.get_style_context().add_class("image-button")
        left_header.pack_start(self.button)

        lbl = Gtk.Label(label=_("Tweaks"))
        lbl.get_style_context().add_class("title")
        left_header.set_custom_title(lbl)

        self.builder = Gtk.Builder()
        assert(os.path.exists(gtweak.PKG_DATA_DIR))
        filename = os.path.join(gtweak.PKG_DATA_DIR, 'shell.ui')
        self.builder.add_from_file(filename)

        appmenu = self.builder.get_object('appmenu')
        icon = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="open-menu-symbolic"),
                                        Gtk.IconSize.BUTTON)
        self.menu_btn.set_image(icon)
        self.menu_btn.set_menu_model(appmenu)
        left_header.pack_end(self.menu_btn)

        header.add(left_header)
        header.child_set(left_header, name="sidebar")
        header.add(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        header.add(right_header)
        header.child_set(right_header, name="content")

        self.header_group = Handy.HeaderGroup()
        self.header_group.add_gtk_header_bar(left_header)
        self.header_group.add_gtk_header_bar(right_header)

        self.hsize_group.add_widget(left_header)

        return header