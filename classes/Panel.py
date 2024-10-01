from classes.PanelPreset import PanelPreset
from classes.DxfDrafter import DxfDrafter


class Panel:
    preset = None
    name = ''
    quantity = 0
    priority = 1

    tab_t = 0.0
    tab_r = 0.0
    tab_b = 0.0
    tab_l = 0.0

    angle = 90

    width = 0.0
    height = 0.0

    w = 0.0
    h = 0.0
    z = 0.0

    def __init__(self, panel_preset: PanelPreset):
        self.preset = panel_preset

    def draft(self, output_path):
        # skip this panel if quantity is 0
        if self.quantity == 0:
            return False

        if self.tab_t != 0:
            self.tab_t -= self.preset.pDimCorr
        if self.tab_r != 0:
            self.tab_r -= self.preset.pDimCorr
        if self.tab_b != 0:
            self.tab_b -= self.preset.pDimCorr
        if self.tab_l != 0:
            self.tab_l -= self.preset.pDimCorr

        self.w = self.width - self.preset.pDimCorr
        self.h = self.height - self.preset.pDimCorr

        DxfDrafter(self, output_path)
