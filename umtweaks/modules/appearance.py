import os
from umtweaks.widgets import BooleanOption, Page, TweaksListBoxRow, ComboOption
from . import Module

import gi
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
                "callback": self.test_action
            }
        ]
        self.page = Page()
        boxrow = BooleanOption("Test", description="Test Description", bool_value=True, set_action=self.test_action)

        self.page.add_row(boxrow)
        self.themes = self.get_gtk_themes()


        combobox = ComboOption(
            title="GTK Theme",
            description="Select a GTK theme",
            options=self.themes,
            selected_index=self.get_gtk_theme_index(),
            set_action=self.set_gtk_theme
            )

        self.page.add_row(combobox)

    def test_action(self, widget):
        # if widget is a ComboBox
        print("Test action")

    def set_gtk_theme(self, widget: Gtk.ComboBox):
        # Get the index of the selected item
        #print(widget.get_active())
        index = widget.get_active()

        # Get the theme name
        theme = self.themes[index]
        #print(theme)

        # Set the theme in Gsettings
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        settings.set_string("gtk-theme", theme)


    def get_gtk_theme_index(self) -> int:
        """Get the current GTK theme"""
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        theme = settings.get_string("gtk-theme")
        #print(theme)

        # Get the index of the selected item
        index = self.themes.index(theme)
        #print(index)
        return index

    def get_gtk_themes(self) -> list:
        """Get all themes"""
        # list folders in /usr/share/themes

        system_themes = []
        for folder in os.listdir("/usr/share/themes"):
            if os.path.isdir("/usr/share/themes/" + folder):
                system_themes.append(folder)

        user_themes = []
        # if ~/.themes exists
        if os.path.isdir(os.path.expanduser("~/.themes")):
            for folder in os.listdir(os.path.expanduser("~/.themes")):
                if os.path.isdir(os.path.expanduser("~/.themes/") + folder):
                    user_themes.append(folder)

        # merge both lists, remove duplicates
        themes = list(set(system_themes + user_themes))

        #print(themes)
        return themes