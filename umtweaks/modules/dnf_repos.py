import os
from umtweaks.widgets import BooleanOption, Page, TweaksListBoxRow, ComboOption
from . import Module

import gi
from gi.repository import Gtk, Gio

class YumRepo():
    def __init__(self, name, enabled, baseurl):
        self.name = name
        self.enabled = enabled
        self.baseurl = baseurl

    def from_file(file):
        with open(file, "r") as f:
            # TODO: Finish this
            lines = f.readlines()
            name = lines[0].strip()
            enabled = lines[1].strip()
            baseurl = lines[2].strip()
            return YumRepo(name, enabled, baseurl)


class ReposModule(Module):
    """Test Module"""
    def __init__(self):
        super().__init__()
        self.name = "Repositories"
        self.description = "This is a test module"
        self.icon = "system-software-install-symbolic"
        self.page = Page()
        treeview = Gtk.TreeView()

        # Create the model
        model = Gtk.ListStore(str, str, str, str)
        treeview.set_model(model)

        # Create the TreeViewColumns to display the data
        tvcolumn = Gtk.TreeViewColumn("Name")
        tvcolumn2 = Gtk.TreeViewColumn("Enabled")
        tvcolumn3 = Gtk.TreeViewColumn("Base URL")
        tvcolumn4 = Gtk.TreeViewColumn("ID")
        treeview.append_column(tvcolumn)
        treeview.append_column(tvcolumn2)
        treeview.append_column(tvcolumn3)
        treeview.append_column(tvcolumn4)

        self.page.add_row(treeview)
