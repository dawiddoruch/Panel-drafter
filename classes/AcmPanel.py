from classes.AcmPreset import AcmPreset
from classes.DfxDrafter import DfxDrafter


class AcmPanel:
    preset = None
    name = ''
    width = 0
    height = 0
    is_corner = False
    corner_width = 0
    corner_type = 'h'
    quantity = 1

    w = 0
    h = 0
    z = 0

    def __init__(self, acm_preset: AcmPreset):
        self.preset = acm_preset

    def draft(self, output_path):
        # skip this panel if quantity is 0
        if self.quantity == 0:
            return False

        # add extension dimension to either height or width
        if self.is_corner and self.corner_type == 'h':
            self.width += self.corner_width
        if self.is_corner and self.corner_type == 'v':
            self.height += self.corner_width

        self.w = self.width - self.preset.pDimCorr
        self.h = self.height - self.preset.pDimCorr
        self.z = self.corner_width - (self.preset.pDimCorr / 2)

        drafter = DfxDrafter(self, output_path)
