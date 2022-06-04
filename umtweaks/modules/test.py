from umtweaks.widgets import BooleanOption, Page, ComboOption, TextOption
from . import Module

from gi.repository import Gtk

class Test1Module(Module):
    """Test Module"""
    def __init__(self):
        super().__init__()
        self.name = "Test Module 0"
        self.description = "This is a test module"
        self.icon = "dialog-information"
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

        combobox = ComboOption(
            title="List",
            description="List of Snapshots",
            options=["test", "test2"],
            selected_index=0,
            set_action=self.combobox_changed
            )

        self.page.add_row(combobox)

        text = TextOption(
            title="Text",
            description="Text",
            text="test",
            )

        self.page.add_row(text)

    def test_action(self, widget: Gtk.Switch, _: bool):
        # if widget is a ComboBox
        print(widget)
        print("Test action")

    def combobox_changed(self, widget: Gtk.ComboBox):
        # Get the index of the selected item
        print(widget.get_active())
