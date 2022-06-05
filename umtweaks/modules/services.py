import subprocess as sp
from threading import Thread

from . import Module
from umtweaks.widgets import BooleanOption, TextOption, TweaksBox
from gi.repository import Gtk, GObject


class ServiceModule(Module):
    """Manage systemd modules"""
    rows: list[BooleanOption] = []

    def __init__(self):
        super().__init__()
        self.name = "Service Management"
        self.description = "Disable services from weak dependencies"
        self.icon = "system-run-symbolic"

        search = TextOption("Search", set_action=self.search)
        box = search.get_children()[0]
        assert isinstance(box, TweaksBox)
        searchLbl = box.get_children()[0]
        assert isinstance(searchLbl, Gtk.Label)
        self.searchLbl = searchLbl
        self.page.add_row(search)
        Thread(target=self.list).start()

    def enable(self, service: str) -> bool:
        sp.run(f"systemctl enable {service}".split())
        return self.is_enabled(service) == "enabled"

    def disable(self, service: str) -> bool:
        sp.run(f"systemctl disable {service}".split())
        return self.is_enabled(service) == "disabled"

    def toggle(self, widget: Gtk.Switch, _: GObject.GType|None):
        tweakbox = widget.get_parent()
        assert tweakbox
        boolopt = tweakbox.get_parent()
        assert isinstance(boolopt, BooleanOption)
        service = boolopt.title.split()[0]
        if (state := self.is_enabled(service)) not in ["enabled", "disabled"]:
            return widget.set_sensitive(False)
        if state == "enabled"  and     widget.get_active(): return
        if state == "disabled" and not widget.get_active(): return
        if self.is_active(service)  == widget.get_active(): return
        if not self.enable(service) if widget.get_active() else self.disable(service):
            widget.set_active(self.is_enabled(service) == "enabled")

    def is_enabled(self, service: str):
        cmd = f"systemctl is-enabled {service}"
        # vmware.service:
        # vmware.service is not a native service, redirecting to systemd-sysv-install.
        # Executing: /usr/lib/systemd/systemd-sysv-install is-enabled vmware
        # enabled
        out = sp.getoutput(cmd).splitlines()[-1]
        # static: plymouth-start.service
        # linked: dracut-initqueue.service
        # generated: dev-zram0.swap
        # enabled-runtime: systemd-remount-fs.service
        # indirect: sssd-kcm.service
        if out not in [
            "enabled",
            "disabled",
            "static",
            "linked",
            "generated",
            "enabled-runtime",
            "indirect",
        ]:
            raise Exception(f"Ran '{cmd}' and got:\n" + out)
        return out

    def is_active(self, service: str) -> bool:
        cmd = f"systemctl is-active {service}"
        out = sp.getoutput(cmd)
        if out not in ["inactive", "active", "failed"]:
            raise Exception(f"Ran '{cmd}' and got:\n" + out)
        return out == "active"

    def list(self):
        print("services: Gathering info from systemd")
        print("services: This may take a while.")
        i = 0
        for i, (ser, time, desc, enabled) in enumerate(self.list_blame()):
            # this looks weird becauase same line + clear
            print(end=f"\x1b[2Kservices: {i+1} {ser}\r")
            opt = BooleanOption(
                ser + " " + time, desc, enabled == "enabled", self.toggle
            )
            if enabled not in ["enabled", "disabled"]:
                opt.set_sensitive(False)
                opt.set_value(self.is_active(ser))
                opt.switch.set_tooltip_text(f"This service is {enabled}.")
            self.rows.append(opt)
            self.page.add_row(opt)
            self.searchLbl.set_text(f"Search ({len(self.rows)})")
        print("\nservices: Done!")

    def list_blame(self):
        out = sp.getoutput("systemd-analyze blame --no-pager")
        for line in out.splitlines():
            time, ser = line.split()
            desc = [
                l.split("=")[1]
                for l in sp.getoutput(f"systemctl show {ser}").splitlines()
                if l.startswith("Description=")
            ][0]
            yield ser, time, desc, self.is_enabled(ser)

    def search(self, widget: Gtk.Entry):
        query = widget.get_text()
        if not query:
            self.searchLbl.set_text(f"Search ({len(self.rows)})")
            return [opt.show() for opt in self.rows]
        i = 0
        for opt in self.rows:
            if query in opt.title:
                i += 1
                opt.show()
            else:
                opt.hide()
        self.searchLbl.set_text(f"Search ({i})")
