from datetime import datetime
import pwd
from umtweaks.widgets import BooleanOption, Page, TweaksListBoxRow, ComboOption
from . import Module
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gi
gi.require_version("Gtk", "3.0")
#gi.require_version("GtkSource", "3.0")
from gi.repository import Gtk, Gio

try:
    # WTF I hate DBus
    bus = dbus.SystemBus(mainloop=DBusGMainLoop())
    snapper = dbus.Interface(bus.get_object('org.opensuse.Snapper',
                                        '/org/opensuse/Snapper'),
                         dbus_interface='org.opensuse.Snapper')
except dbus.DBusException:
    snapper = None
    print("Unable to connect to snapper")

class SnapperSnapshot(object):
    def __init__(self, id, date, user, description):
        # DBus types to python types
        self.id = int(id)
        # get date from epoch
        if date == -1:
            self.date = "Now"
        else:
            self.date = datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d %H:%M:%S")
        # get username from UID
        self.user = pwd.getpwuid(int(user)).pw_name
        self.description = str(description)

class SnapperConfig(object):
    def __init__(self, name, root):
        self.name = name
        self.root = root

    def list_configs():
        configs = []
        configs_dbus = snapper.ListConfigs()
        for config in configs_dbus:
            configs.append(SnapperConfig(config[0], config[1]))
        return configs

    def get_config(name):
        config_dbus = snapper.GetConfig(name)
        return SnapperConfig(config_dbus[0], config_dbus[1])

    def into_dbus(self):
        return snapper.GetConfig(self.name)

    def list_snapshots(self):
        snapshots = []
        snapshots_dbus = snapper.ListSnapshots(self.name)
        for snapshot in snapshots_dbus:
            snapshots.append(SnapperSnapshot(id=snapshot[0], date=snapshot[3], user=snapshot[4], description=snapshot[5]))
        return snapshots



""" config = SnapperConfig.get_config("root")

snapshots = config.list_snapshots()

for snapshot in snapshots:
    print(snapshot.__dict__)
 """

class SnapperBackupsModule(Module):
    """Test Module"""
    def __init__(self):
        super().__init__()
        self.name = "Snapshots"
        self.description = "This is a test module"
        self.icon = "drive-multidisk-symbolic"

        
        # if snapper is not None
        if snapper is not None:
        #if snapper_enabled:
            self.page = Page()
            self.configs = SnapperConfig.list_configs()
            config_names = [str(config.name) for config in self.configs]
            #print(f"Configs: {config_names}")

            self.selected_config: SnapperConfig = SnapperConfig.get_config(config_names[0])

            #print(self.selected_config.__dict__)

            self.config_option = ComboOption(
                "Config",
                "Select a config",
                config_names,
                0,
            )
            self.page.add_row(self.config_option)

            self.treeview = Gtk.TreeView()
            self.treeview_model = Gtk.ListStore(int, str, str, str)
            self.treeview.set_model(self.treeview_model)

            # Add some columns
            id_column = Gtk.TreeViewColumn("ID")
            id_cell = Gtk.CellRendererText()
            id_column.pack_start(id_cell, True)
            id_column.add_attribute(id_cell, "text", 0)
            id_column.set_fixed_width(50)
            id_column.set_resizable(False)
            self.treeview.append_column(id_column)

            date_column = Gtk.TreeViewColumn("Date")
            date_cell = Gtk.CellRendererText()
            date_column.pack_start(date_cell, True)
            date_column.add_attribute(date_cell, "text", 1)
            date_column.set_fixed_width(200)
            date_column.set_resizable(True)
            self.treeview.append_column(date_column)

            user_column = Gtk.TreeViewColumn("User")
            user_cell = Gtk.CellRendererText()
            user_column.pack_start(user_cell, True)
            user_column.add_attribute(user_cell, "text", 2)
            user_column.set_fixed_width(100)
            user_column.set_resizable(True)
            self.treeview.append_column(user_column)

            description_column = Gtk.TreeViewColumn("Description")
            description_cell = Gtk.CellRendererText()
            description_column.pack_start(description_cell, True)
            description_column.add_attribute(description_cell, "text", 3)
            description_column.set_fixed_width(400)
            description_column.set_resizable(True)
            # align text to the right
            #description_column.set_alignment(1.0)
            self.treeview.append_column(description_column)


            # Load the config
            # get the selected config from ComboOption
            self.snapshots = self.selected_config.list_snapshots()
            for snapshot in self.snapshots:
                self.treeview_model.append([snapshot.id, snapshot.date, snapshot.user, snapshot.description])


            self.page.add_row(self.treeview)

        else:
            self.page = Page()
            no_snapper_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            icon = Gtk.Image.new_from_icon_name("dialog-error-symbolic", size=Gtk.IconSize.DIALOG)
            no_snapper_box.add(icon)
            label = Gtk.Label("Snapper is not yet set up for this system. Would you like to set up Snapper?")
            no_snapper_box.add(label)
            # Custom icon size
            button = Gtk.Button("Set up Snapper")
            no_snapper_box.add(button)
            button.connect("clicked", self.set_up_snapper)
            self.page.add_row(no_snapper_box)




    def test_action(self, *args, **kwargs):
        print("Test action")
    def set_up_snapper(self, *args, **kwargs):
        print("Set up snapper")