from umtweaks.widgets import BooleanOption, Page, TweaksListBoxRow, ComboOption
from . import Module
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "3.0")


# WTF I hate DBus
bus = dbus.SystemBus(mainloop=DBusGMainLoop())
snapper = dbus.Interface(bus.get_object('org.opensuse.Snapper',
                                        '/org/opensuse/Snapper'),
                         dbus_interface='org.opensuse.Snapper')



class SnapperBackupsModule(Module):
    """Test Module"""
    def __init__(self):
        super().__init__()
        self.name = "Snapshots"
        self.description = "This is a test module"
        self.icon = "drive-multidisk-symbolic"
        self.actions = [
            {
                "name": "Test Action",
                "description": "This is a test action",
                "icon": "dialog-information",
                "callback": self.test_action
            }
        ]
        self.page = Page()
        boxrow = BooleanOption("Backup Test", description="Test Description", bool_value=True, set_action=self.test_action)
        configs = snapper.ListConfigs()

        self.page.add_row(boxrow)


    def test_action(self, *args, **kwargs):
        print("Test action")