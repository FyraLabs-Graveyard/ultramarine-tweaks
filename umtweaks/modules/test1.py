from . import Module

class TestModule(Module):
    """Test Module"""
    def __init__(self):
        super().__init__()
        # override the name
        self._name = "Test Module 1"

    def test_action(self):
        print("Test action")