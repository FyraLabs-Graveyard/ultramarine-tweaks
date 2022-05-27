from . import Module
from umtweaks.widgets import BooleanOption, Page, TweaksListBoxRow, ComboOption, TextOption


class PowerManagmentModule(Module):
    """Power Managment Module"""
    def __init__(self):
        super().__init__()
        self._name = "Power Managment"
        self._description = "Option for the power management"
        self._icon = "battery-full-symbolic"

        combobox = ComboOption(
            title="Power Profile",
            description="Select a power profile",
            options=["Normal Mode", "Energy Saver", "Ultra Power Mode"]
        )

        self.page.add_row(combobox)

        self.StandbyTime = TextOption(
            title="Standby Time in minutes",
            description="Set the standby time",
            text="30"
        )

        self.page.add_row(self.StandbyTime)

    def test_action(self):
        print("Power Module")
        