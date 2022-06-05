import functools
from typing import Callable, Any, TypeAlias

from umtweaks.widgets import ListBoxRow, Page

from gi.repository import Gtk

import os

ActionT: TypeAlias = list[dict[str, str | Callable[[Gtk.Widget], None]]]
ReqPermT: TypeAlias = list[Any]  #! not sure


class Module:
    """Template for an Ultramarine Tweaks Module"""

    _name: str = "Module"
    _description: str = "This is a module"
    _icon: str = ""
    _restart_required: bool = False
    _actions: ActionT = []
    # Polkit perms requied to use this module
    _require_permissions: ReqPermT = []
    _page: Page = Page()

    def __init__(self) -> None:
        # somehow page dw
        self.page = Page()

    def generate_row(self, window: Gtk.Window) -> ListBoxRow:
        return ListBoxRow(
            title=self.name,
            description=self.description,
            icon_name=self.icon,
            window=window,
            page=self.page,
        )

    def load(self):
        """Load the module"""
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value: str):
        self._icon = value

    @property
    def restart_required(self):
        return self._restart_required

    @restart_required.setter
    def restart_required(self, value: bool):
        self._restart_required = value

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, value: ActionT):
        self._actions = value

    @property
    def require_permissions(self):
        return self._require_permissions

    @require_permissions.setter
    def require_permissions(self, value: ReqPermT):
        self._require_permissions = value

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value: Page):
        self._page = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


@functools.cache
def find_modules() -> list[Module]:
    """Find modules in the system"""
    # List all python files in __file__
    files = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py")]
    # print(files)

    # Import the file and find a class that inherits from Module
    modules: list[Module] = []
    for file in files:
        if file == "__init__.py":
            continue
        # print(file)
        module = __import__(
            f"umtweaks.modules.{file[:-3]}", fromlist=["umtweaks.modules"]
        )
        for name, obj in list(module.__dict__.items()):
            # print(name, obj)]
            # if from __init__.py, skip
            if name == "__file__":
                continue

            if isinstance(obj, type) and issubclass(obj, Module):
                # print(name)
                # get file where object is from
                a = obj.__module__
                if a == "umtweaks.modules":
                    continue
                # Holy shit i love this hack
                modules.append(obj())

    # sort the modules by name
    modules.sort(key=lambda x: x.name)
    return modules


def load_modules_to_listbox(listbox: Gtk.ListBox, window: Gtk.Window):
    """Load modules to a listbox"""
    modules = find_modules()
    for module in modules:
        # print all of the modules properties
        # print(module.name)
        listbox.add(module.generate_row(window))


def load_modules_to_pages(stack: Gtk.Stack):
    """Load modules to a pages"""
    modules = find_modules()
    for module in modules:
        # print(f"module: {module.name}")
        stack.add_named(module.page, module.name)
