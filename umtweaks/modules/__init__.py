from ..widgets import ListBoxRow

from gi.repository import Gio, Gtk

import os

class Module:
    """Template for an Ultramarine Tweaks Module"""
    def __init__(self):
        self.name: str = "Module"
        self.description: str = None
        self.icon: str = None
        self.restart_required: bool = False
        self.actions: list = []
        # Polkit permissions required to use this module
        self.require_permissions: list = []

    def generate_row(self) -> ListBoxRow:
        return ListBoxRow(
            text=self.name,
            description=self.description,
            icon=self.icon
        )

    def load(self):
        """Load the module"""
        pass

def find_modules() -> list:
    """Find modules in the system"""
    # List all python files in __file__
    files = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py")]
    print(files)
    pass


def load_modules_to_listbox(listbox: Gtk.ListBox):
    """Load modules to a listbox"""
    pass # TODO: Implement this