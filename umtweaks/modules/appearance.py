import os
from typing import Any
from umtweaks.widgets import BooleanOption, ComboOption
from . import Module

from gi.repository import Gtk, Gio


class AppearanceModule(Module):
    """Test Module"""

    def __init__(self):
        super().__init__()
        self.name = "Appearance"
        self.description = "This is a test module"
        self.icon = "applications-graphics-symbolic"
        self.actions = [
            {
                "name": "Test Action",
                "description": "This is a test action",
                "icon": "dialog-information",
                "callback": self.test_action,
            }
        ]
        boxrow = BooleanOption(
            "Test",
            description="Test Description",
            bool_value=True,
            set_action=self.test_action,
        )

        self.page.add_row(boxrow)
        self.themes = self.get_gtk_themes()

        gtk_theme = ComboOption(
            title="GTK Theme",
            description="Select a GTK theme",
            options=self.themes,
            selected_index=self.get_gtk_theme_index(),
            set_action=self.set_gtk_theme,
        )

        self.page.add_row(gtk_theme)

        self.icon_themes = self.get_icon_themes()

        icon_theme = ComboOption(
            title="Icon Theme",
            description="Select a icon theme",
            options=self.icon_themes,
            selected_index=self.get_icon_theme_index(),
            set_action=self.set_icon_theme,
        )

        self.page.add_row(icon_theme)

        color_scheme_options = [
            "Default",
            "Prefer Dark",
            "Prefer Light",
        ]

        color_scheme = ComboOption(
            title="GNOME Color Scheme",
            description="Color schemes for GNOME apps",
            options=color_scheme_options,
            selected_index=self.get_color_scheme(),
            set_action=self.set_color_scheme,
        )

        self.page.add_row(color_scheme)

        self.screenshare_modes = [
            "mirror-primary",
            "extend"
        ]

        self.page.add_row(ComboOption(
            title="RDP Screenshare Mode",
            description="Whether the RDP backend mirrors the primary screen, or whether a virtual monitor is created",
            options=self.screenshare_modes,
            selected_index=self.get_screenshare_mode(),
            set_action=self.set_screenshare_mode
        ))

    def test_action(self, widget: Gtk.Widget, *args: Any):
        # if widget is a ComboBox
        print("Test action")

    def set_gtk_theme(self, widget: Gtk.ComboBox):
        # Get the index of the selected item
        # print(widget.get_active())
        index = widget.get_active()

        # Get the theme name
        theme = self.themes[index]
        # print(theme)

        # Set the theme in Gsettings
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        settings.set_string("gtk-theme", theme)

    def get_gtk_theme_index(self) -> int:
        """Get the current GTK theme"""
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        theme: str = settings.get_string("gtk-theme")
        # print(theme)

        # Get the index of the selected item
        index = self.themes.index(theme)
        # print(index)
        return index

    def get_gtk_themes(self) -> list[str]:
        """Get all themes"""
        # list folders in /usr/share/themes

        system_themes: list[str] = []
        for folder in os.listdir("/usr/share/themes"):
            if os.path.isdir("/usr/share/themes/" + folder):
                system_themes.append(folder)

        user_themes: list[str] = []
        # if ~/.themes exists
        if os.path.isdir(os.path.expanduser("~/.themes")):
            for folder in os.listdir(os.path.expanduser("~/.themes")):
                if os.path.isdir(os.path.expanduser("~/.themes/") + folder):
                    user_themes.append(folder)

        # merge both lists, remove duplicates
        themes = list(set(system_themes + user_themes))

        # print(themes)
        return themes

    def get_color_scheme(self) -> int:
        """Get the current color scheme"""
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        scheme: str = settings.get_string("color-scheme")
        # Scheme is an enum of "default", "prefer-dark", "prefer-light"
        match scheme:
            case "default":
                return 0
            case "prefer-dark":
                return 1
            case "prefer-light":
                return 2
            case _:
                raise Exception()

    def set_color_scheme(self, widget: Gtk.ComboBox):
        # Get the index of the selected item
        # print(widget.get_active())
        index = widget.get_active()

        # Get the scheme name
        scheme = ["default", "prefer-dark", "prefer-light"][index]
        # print(scheme)

        # Set the scheme in Gsettings
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        settings.set_string("color-scheme", scheme)

    def get_icon_themes(self):
        """Get all icon themes"""
        # list folders in /usr/share/icons
        system_themes: list[str] = []
        for folder in os.listdir("/usr/share/icons"):
            if os.path.isdir("/usr/share/icons/" + folder):
                system_themes.append(folder)

        user_themes: list[str] = []
        # if ~/.icons exists
        if os.path.isdir(os.path.expanduser("~/.icons")):
            for folder in os.listdir(os.path.expanduser("~/.icons")):
                if os.path.isdir(os.path.expanduser("~/.icons/") + folder):
                    user_themes.append(folder)

        # merge both lists, remove duplicates
        themes = list(set(system_themes + user_themes))

        # print(themes)
        return themes

    def get_icon_theme_index(self) -> int:
        """Get the current icon theme"""
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        theme: str = settings.get_string("icon-theme")
        # print(theme)

        # Get the index of the selected item
        try:
            index = self.icon_themes.index(theme)
        except ValueError:
            index = 0
        #print(index)
        return index

    def set_icon_theme(self, widget: Gtk.ComboBox):
        # Get the index of the selected item
        # print(widget.get_active())
        index = widget.get_active()

        # Get the theme name
        theme = self.icon_themes[index]
        # print(theme)

        # Set the theme in Gsettings
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        settings.set_string("icon-theme", theme)

    def get_screenshare_mode(self) -> int:
        """Get the current screenshare mode"""
        settings = Gio.Settings.new("org.gnome.desktop.remote-desktop.rdp")
        mode: str = settings.get_string("screen-share-mode")
        return self.screenshare_modes.index(mode)

    def set_screenshare_mode(self, widget: Gtk.ComboBox):
        index = widget.get_active()
        mode = self.screenshare_modes[index]
        settings = Gio.Settings.new("org.gnome.desktop.remote-desktop.rdp")
        settings.set_string("screen-share-mode", mode)
