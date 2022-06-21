from . import Module


class KernelTweaker(Module):
    """KernelTweaker"""

    def __init__(self):
        super().__init__()
        # override the name
        self._name = "Kernel Tweaker"
        self._description = "Options for the kernel"
        self._icon = "system-run-symbolic"

    def test_action(self):
        print("Test action")

    def list_modules(self):
        pass
