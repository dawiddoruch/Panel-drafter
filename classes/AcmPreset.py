ACM_TYPE_4MM = 0x0001
ACM_TYPE_6MM = 0x0002


class AcmPreset:
    pDimCorr = 0  # this is how much larger panel will be after folding
    holeRad = 0  # radius of hole marks
    fWidth = 0  # width of the folded edge
    holeOff = 0  # hole offset from mitered panel corner
    holeMaxOC = 0  # max distance between holes
    holeEdgeOff = 0  # hole offset from folded edge
    cCut = 0  # actual corner cutout is offset by that value
    cOffset = 0  # corner groove/cutout offset
    cutExt = 0  # panel cutout path extension
    cutOff = 0  # cutout offset : half the size of cutting tool
    acm_type = ACM_TYPE_4MM

    def __init__(self, acm_type=ACM_TYPE_4MM):
        self.change_preset(acm_type)

    def change_preset(self, acm_type=ACM_TYPE_4MM):
        if acm_type == ACM_TYPE_4MM:
            self.pDimCorr = 0.06
            self.holeRad = 0.32
            self.fWidth = 1.02
            self.holeOff = 2.25
            self.holeMaxOC = 16
            self.holeEdgeOff = 0.6
            self.cCut = 0.11
            self.cOffset = 0.07
            self.cutExt = 0.2
        elif acm_type == ACM_TYPE_6MM:
            self.pDimCorr = 0.06
            self.holeRad = 0.32
            self.fWidth = 1.095
            self.holeOff = 2.35
            self.holeMaxOC = 16
            self.holeEdgeOff = 0.705
            self.cCut = 0.11
            self.cOffset = 0.07
            self.cutExt = 0.2
        self.cutOff = self.fWidth + (1 / 4 / 2)
        self.acm_type = acm_type

    def select_preset(self):
        print("Available presets:")
        print("1. Alpolic 4mm")
        print("2. Alpolic 6mm")
        print("E. Exit")
        selection = input("Select preset... ")

        if selection == '1':
            self.change_preset(ACM_TYPE_4MM)
        elif selection == '2':
            self.change_preset(ACM_TYPE_6MM)
        elif selection.lower() == "e":
            print("Good bye!s")
            exit()
        else:
            print("\nIncorrect selection. Try again.\n\n")
            self.select_preset()
