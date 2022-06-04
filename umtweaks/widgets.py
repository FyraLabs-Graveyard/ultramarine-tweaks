from typing import Any, Callable
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import Gtk, Handy, GObject

# rom .window import MainWindow


def main_content():
    right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    right_box.set_size_request(540, -1)

    stack = Gtk.Stack()
    stack.get_style_context().add_class("main-container")

    right_box.pack_start(stack, True, True, 0)

    return right_box


class MainContent(Gtk.Box):
    def __init__(self, orientation: Gtk.Orientation = Gtk.Orientation.VERTICAL, spacing: int = 0):
        Gtk.Box.__init__(self, orientation=orientation, spacing=spacing)
        self.set_size_request(540, -1)
        self.stack = Gtk.Stack()
        self.stack.get_style_context().add_class("main-container")

        self.pack_start(self.stack, True, True, 0)


class TweaksListBox(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.set_selection_mode(Gtk.SelectionMode.NONE)


class TweaksBox(Gtk.Box):
    def __init__(self, orientation: Gtk.Orientation = Gtk.Orientation.HORIZONTAL, spacing: int = 0):
        Gtk.Box.__init__(self, orientation=orientation, spacing=spacing)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)


class TweaksListBoxRow(Gtk.ListBoxRow):
    def __init__(self):
        Gtk.ListBoxRow.__init__(self)
        self.set_size_request(540, -1)
        self.set_activatable(False)
        self.set_selectable(False)
        self.set_can_focus(False)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_margin_top(20)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        box.set_spacing(10)


class Page(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.set_name("UmTweaksPage")
        self.listbox = TweaksListBox()
        self.add(self.listbox)

    def add_row(self, widget: Gtk.Widget):
        self.listbox.add(widget)


class ListBoxRow(Gtk.ListBoxRow):
    def __init__(
        self,
        title: str,
        description: str,
        icon_name: str,
        window: Gtk.Window,
        page: Page,
    ):
        super().__init__()
        # Let's add a fancy box for padding
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_margin_left(10)
        hbox.set_margin_right(10)
        hbox.set_margin_top(10)
        hbox.set_margin_bottom(10)
        label = Gtk.Label(title)
        self.title = title
        if icon_name:
            icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.SMALL_TOOLBAR)
            # Spacing between icon and title
            icon.set_margin_right(10)
            hbox.pack_start(icon, False, False, 0)
        else:
            label.set_margin_left(25)

        hbox.add(label)

        self.add(hbox)
        self.set_activatable(False)
        # map on click
        self.connect("activate", self.select)
        self.connect("focus-in-event", self.select)

        # self.test_content = MainContent()
        self.window = window
        self.page = page

    def select(self, *args) -> None:
        # print(args)
        # print(kwargs)
        # print("select:", self.title)
        # self.window.main_box.navigate(Handy.NavigationDirection.FORWARD)
        # self.window.main_box.set_visible_child_name(self.title)
        # Get child of self.window.main_box.get_visible_child()
        # which should be a Gtk.Stack
        leaflet: Gtk.Container = self.window.main_box
        box: Gtk.Box = leaflet.get_children()[-1]
        stack: Gtk.Stack = box.get_children()[0]
        # Destroy all children of stack
        """ for child in stack.get_children():
            stack.remove(child)
        # Add new child to stack
        content = self.page
        stack.add(content) """

        stack.set_visible_child_name(self.title)

        stack.show_all()
        self.window.main_seperator.set_visible(False)
        leaflet.navigate(Handy.NavigationDirection.FORWARD)
        leaflet.navigate(Handy.NavigationDirection.FORWARD)
        self.window.main_seperator.set_visible(True)


class BooleanOption(TweaksListBoxRow):
    def __init__(
        self,
        title: str,
        description: str = '',
        bool_value: bool = False,
        set_action: Callable[[Gtk.Switch, GObject.GType], Any]|None = None,
    ):
        super().__init__()
        self.title = title
        self.description = description
        box = TweaksBox() # self.get_parent()
        # labelbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        title_label = Gtk.Label(title)
        box.add(title_label)
        if description:
            # Add description as tooltip
            title_label.set_tooltip_text(description)

        self.switch = Gtk.Switch()
        self.switch.set_active(bool_value)
        if set_action:
            self.switch.connect("notify::active", set_action)
        box.pack_end(self.switch, False, False, 0)

        self.add(box)

    def get_active(self) -> bool:
        return self.check_button.get_active()

    def set_value(self, value: bool) -> None:
        self.switch.set_active(value)


class ComboOption(TweaksListBoxRow):
    def __init__(
        self,
        title: str,
        description: str = '',
        options: list[str] = [],
        selected_index: int = 0,
        set_action: Callable[[Gtk.ComboBox, GObject.GType], Any]|None = None,
    ):
        super().__init__()

        box = TweaksBox()
        title_label = Gtk.Label(title)
        box.add(title_label)
        if description:
            # Add description as tooltip
            title_label.set_tooltip_text(description)

        combo = Gtk.ComboBox()
        model = Gtk.ListStore(str)
        for option in options:
            model.append([option])
        combo.set_model(model)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        combo.set_active(selected_index)
        if set_action:
            combo.connect("changed", set_action)
        box.pack_end(combo, False, False, 0)

        self.add(box)

    def get_active(self) -> int:
        return self.combo_box.get_active()


class TextOption(TweaksListBoxRow):
    def __init__(
        self,
        title: str,
        description: str = '',
        text: str = '',
        set_action: Callable[[Gtk.Entry, GObject.GType], Any]|None = None,
    ):
        super().__init__()
        self.text = text

        box = TweaksBox()
        title_label = Gtk.Label(title)
        box.add(title_label)
        if description:
            # Add description as tooltip
            title_label.set_tooltip_text(description)

        self.entry = Gtk.Entry()
        self.entry.set_text(self.text)
        if set_action:
            self.entry.connect("changed", set_action)
        box.pack_end(self.entry, False, False, 0)

        self.add(box)

    # on self.text change
    def get_text(self) -> str:
        return self.text

    def set_text(self, text: str) -> None:
        self.text = text
        self.entry.set_text(text)
