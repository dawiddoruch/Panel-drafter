class PanelPreset:
    TYPE_4MM = 0x0001
    TYPE_6MM = 0x0002
    TYPE_4MM_NO_OFFSET = 0x0003
    TYPE_6MM_NO_OFFSET = 0x0004
    TYPE_4MM_ARROWHEAD_LEAN = 0x0005
    TYPE_FIBERCEMENT = 0x0006

    pDimCorr = 0  # this is how smaller panel will be drawn to compensate for size increase after folding
    holeRad = 0  # radius of hole marks
    fWidth = 0  # width of the folded edge
    holeOff = 0  # hole offset from mitered panel corner
    holeMaxOC = 0  # max distance between holes
    holeEdgeOff = 0  # hole offset from folded edge
    cCut = 0  # actual corner cutout is offset by that value
    cOffset = 0  # corner groove/cutout offset
    cOffsetWidth = 0  # length of the red offset cut
    cutExt = 0  # panel cutout path extension
    cutOff = 0  # cutout offset : half the size of cutting tool
    panel_type = TYPE_4MM

    def __init__(self, panel_type=TYPE_4MM):
        self.change_preset(panel_type)

    def change_preset(self, panel_type=TYPE_4MM):
        if panel_type == self.TYPE_4MM:
            self.pDimCorr = 0.06
            self.holeRad = 0.1
            self.fWidth = 1.02
            self.holeOff = 2.25
            self.holeMaxOC = 16
            self.holeEdgeOff = 0.6
            self.cCut = 0.11
            self.cOffset = 0.07
            self.cOffsetWidth = self.fWidth
            self.cutExt = 0.2
            self.cutOff = self.fWidth + 0.125
        elif panel_type == self.TYPE_4MM_NO_OFFSET:
            self.pDimCorr = 0.06
            self.holeRad = 0.1
            self.fWidth = 1.02
            self.holeOff = 2.25
            self.holeMaxOC = 16
            self.holeEdgeOff = 0.6
            self.cCut = 0
            self.cOffset = 0.04
            self.cOffsetWidth = self.fWidth - self.cOffset
            self.cutExt = 0.2
            self.cutOff = self.fWidth
        elif panel_type == self.TYPE_6MM:
            self.pDimCorr = 0.06
            self.holeRad = 0.1
            self.fWidth = 1.095
            self.holeOff = 2.35
            self.holeMaxOC = 16
            self.holeEdgeOff = 0.705
            self.cCut = 0.11
            self.cOffset = 0.07
            self.cOffsetWidth = self.fWidth
            self.cutExt = 0.2
            self.cutOff = self.fWidth + 0.125
        elif panel_type == self.TYPE_6MM_NO_OFFSET:
            self.pDimCorr = 0.06
            self.holeRad = 0.1
            self.fWidth = 1.095
            self.holeOff = 2.35
            self.holeMaxOC = 16
            self.holeEdgeOff = 0.705
            self.cCut = 0
            self.cOffset = 0.07
            self.cOffsetWidth = self.fWidth - self.cOffset
            self.cutExt = 0.2
            self.cutOff = self.fWidth
        elif panel_type == self.TYPE_4MM_ARROWHEAD_LEAN:
            pass
        elif panel_type == self.TYPE_FIBERCEMENT:
            self.pDimCorr = 0

        self.panel_type = panel_type

    def select_preset(self, debug_default_preset=-1):
        print("Available presets:")
        print("1. ACM 4mm no offset (XCAM)")
        print("2. ACM 6mm no offset (XCAM)")
        print("3. ACM 4mm Arrowhead Lean")
        print("4. Fibercement")
        # print("5. ACM 4mm 1/8 offset")
        # print("6. ACM 6mm 1/8 offset")
        print("E. Exit")

        selection = str(debug_default_preset)
        if debug_default_preset == -1:
            selection = input("Select preset... ")

        if selection == '1':
            self.change_preset(self.TYPE_4MM_NO_OFFSET)
        elif selection == '2':
            self.change_preset(self.TYPE_6MM_NO_OFFSET)
        elif selection == '3':
            self.change_preset(self.TYPE_4MM_ARROWHEAD_LEAN)
        elif selection == '4':
            self.change_preset(self.TYPE_FIBERCEMENT)
        # elif selection == '5':
        #    self.change_preset(self.TYPE_4MM)
        # elif selection == '6':
        #     self.change_preset(self.TYPE_6MM)
        elif selection.lower() == "e":
            print("Good bye!")
            exit()
        else:
            print("\nIncorrect selection. Try again.\n\n")
            self.select_preset()
