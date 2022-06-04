import subprocess as sp

from . import Module
from umtweaks.widgets import BooleanOption
from gi.repository import Gtk, GObject


class ServiceModule(Module):
    """Manage systemd modules"""

    def __init__(self):
        super().__init__()
        self.name = "Service Management"
        self.description = "Disable services from weak dependencies"
        self.icon = "system-run-symbolic"

        # we have to init self.page here, or else it will results in
        # startup:
        # Gtk-CRITICAL gtk_container_add_with_properties: assertion '_gtk_widget_get_parent (widget) == NULL' failed
        # clicking on the corresponding item on the page on the left
        # Gtk-WARNING Child name 'Module Name' not found in GtkStack
        # self.page = Page()
        self.list()

    def enable(self, service: str) -> bool:
        sp.run(f"systemctl enable {service}".split())
        return self.is_enabled(service) == "enabled"

    def disable(self, service: str) -> bool:
        sp.run(f"systemctl disable {service}".split())
        return self.is_enabled(service) == "disabled"

    def toggle(self, widget: Gtk.Switch, _: GObject.GType):
        tweakbox = widget.get_parent()
        assert tweakbox
        boolopt = tweakbox.get_parent()
        assert isinstance(boolopt, BooleanOption)
        service = boolopt.title.split()[0]
        if (state := self.is_enabled(service)) not in ['enabled', 'disabled']:
            return widget.set_sensitive(False)
        if state == 'enabled'  and     widget.get_active(): return
        if state == 'disabled' and not widget.get_active(): return
        if self.is_active(service) ==  widget.get_active():  return
        succ = self.enable(service) if widget.get_active() else self.disable(service)
        if not succ: widget.set_active(self.is_enabled(service) == "enabled")

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
        if out not in ["enabled", "disabled", "static", "linked", "generated", "enabled-runtime", "indirect"]:
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
        for i, (ser, info) in enumerate(self.list_blame()):
            # this looks weird becauase same line + clear
            print(end=f"\x1b[2Kservices: {i+1} {ser}\r")
            enabled = info["enabled"]
            opt = BooleanOption(
                ser + ' ' + info['time'],
                info["desc"],
                enabled == "enabled",
                self.toggle
            )
            if enabled not in ['enabled', 'disabled']:
                opt.set_sensitive(False)
                opt.set_value(self.is_active(ser))
                opt.switch.set_tooltip_text(f"This service is {enabled}.")
            self.page.add_row(opt)
        print("\nservices: Done!")

    def list_blame(self):
        out = sp.getoutput("systemd-analyze blame --no-pager")
        for line in out.splitlines():
            time, ser = line.split()
            yield ser, {
                "time": time,
                "desc": [
                    l.split("=")[1]
                    for l in sp.getoutput(f"systemctl show {ser}").splitlines()
                    if l.startswith("Description=")
                ][0],
                "enabled": self.is_enabled(ser),
            }
