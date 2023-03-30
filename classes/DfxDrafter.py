from classes import AcmPanel
from classes import AcmPreset
import ezdxf as dxf
import math


class DfxDrafter:
    modelspace = None

    BLACK = {'color': 0}
    RED = {'color': 1}
    YELLOW = {'color': 2}
    GREEN = {'color': 3}
    CYAN = {'color': 4}
    BLUE = {'color': 5}
    PURPLE = {'color': 6}
    WHITE = {'color': 7}
    GRAY = {'color': 8}
    SILVER = {'color': 9}

    def __init__(self, panel: AcmPanel, output_path):
        output_file = "{}{}.dxf".format(output_path, panel.name)
        drawing = dxf.new(dxfversion='R2004')
        drawing.header['$MEASUREMENT'] = 1
        self.modelspace = drawing.modelspace()
        self.__panel_face(panel)
        self.__panel_corners(panel)
        self.__panel_folding_helper(panel)
        self.__panel_cutout(panel)
        self.__panel_drill(panel)
        self.__panel_name(panel)
        drawing.saveas(output_file)

    # add panel name
    def __panel_name(self, p: AcmPanel):
        self.modelspace.add_text(p.name + ' x ' + str(p.quantity), dxfattribs={'height': 2}).set_placement(((p.w / 2), (p.h / 2)), align=dxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # add drill holes
    def __panel_drill(self, p: AcmPanel):
        holes = []
        add_holes_lr = True
        add_holes_tb = True
        holeEdgeOff = p.preset.holeEdgeOff
        holeOff = p.preset.holeOff
        holeMaxOC = p.preset.holeMaxOC
        w = p.w
        h = p.h

        if p.is_corner and p.corner_type == 'h':
            add_holes_tb = False

            w1 = p.preset.cornerWidth - 0.25
            x1 = 0
            w2 = w - p.corner_width - 0.25
            x2 = p.corner_width + 0.25

            if w1 < 5.5:
                holes.append((x1 + w1 / 2, 0 - holeEdgeOff))
                holes.append((x1 + w1 / 2, h + holeEdgeOff))
            else:
                holes.append((x1 + holeOff, 0 - holeEdgeOff))
                holes.append((x1 + holeOff, h + holeEdgeOff))
                holes.append((x1 + w1 - holeOff, 0 - holeEdgeOff))
                holes.append((x1 + w1 - holeOff, h + holeEdgeOff))

                extra_holes_count = math.ceil((w1 - (2 * holeOff)) / holeMaxOC) - 1

                if extra_holes_count >= 1:
                    extra_holes_oc = (w1 - (2 * holeOff)) / (extra_holes_count + 1)
                    for i in range(1, extra_holes_count + 1):
                        holes.append((x1 + holeOff + (extra_holes_oc * i), 0 - holeEdgeOff))
                        holes.append((x1 + holeOff + (extra_holes_oc * i), h + holeEdgeOff))

            if w2 < 5.5:
                holes.append((x2 + w2 / 2, 0 - holeEdgeOff))
                holes.append((x2 + w2 / 2, h + holeEdgeOff))
            else:
                holes.append((x2 + holeOff, 0 - holeEdgeOff))
                holes.append((x2 + holeOff, h + holeEdgeOff))
                holes.append((x2 + w2 - holeOff, 0 - holeEdgeOff))
                holes.append((x2 + w2 - holeOff, h + holeEdgeOff))

                extra_holes_count = math.ceil((w2 - (2 * holeOff)) / holeMaxOC) - 1

                if extra_holes_count >= 1:
                    extra_holes_oc = (w2 - (2 * holeOff)) / (extra_holes_count + 1)
                    for i in range(1, extra_holes_count + 1):
                        holes.append((x2 + holeOff + (extra_holes_oc * i), 0 - holeEdgeOff))
                        holes.append((x2 + holeOff + (extra_holes_oc * i), h + holeEdgeOff))
        if p.is_corner and p.corner_type == 'v':
            add_holes_lr = False

            h1 = p.corner_width - 0.25
            y1 = 0
            h2 = h - p.corner_width - 0.25
            y2 = p.corner_width + 0.25

            if h1 < 5.5:
                holes.append((w + holeEdgeOff, y1 + h1 / 2))
                holes.append((0 - holeEdgeOff, y1 + h1 / 2))
            else:
                holes.append((w + holeEdgeOff, y1 + holeOff))
                holes.append((0 - holeEdgeOff, y1 + holeOff))
                holes.append((w + holeEdgeOff, y1 + h1 - holeOff))
                holes.append((0 - holeEdgeOff, y1 + h1 - holeOff))
                extra_holes_count = math.ceil((h1 - (2 * holeOff)) / holeMaxOC) - 1
                if extra_holes_count >= 1:
                    extra_holes_oc = (h1 - (2 * holeOff)) / (extra_holes_count + 1)
                    for i in range(1, extra_holes_count + 1):
                        holes.append((w + holeEdgeOff, y1 + holeOff + (extra_holes_oc * i)))
                        holes.append((0 - holeEdgeOff, y1 + holeOff + (extra_holes_oc * i)))

            if h2 < 5.5:
                holes.append((w + holeEdgeOff, y2 + h2 / 2))
                holes.append((0 - holeEdgeOff, y2 + h2 / 2))
            else:
                holes.append((w + holeEdgeOff, y2 + holeOff))
                holes.append((0 - holeEdgeOff, y2 + holeOff))
                holes.append((w + holeEdgeOff, y2 + h2 - holeOff))
                holes.append((0 - holeEdgeOff, y2 + h2 - holeOff))
                extra_holes_count = math.ceil((h2 - (2 * holeOff)) / holeMaxOC) - 1
                if extra_holes_count >= 1:
                    extra_holes_oc = (h2 - (2 * holeOff)) / (extra_holes_count + 1)
                    for i in range(1, extra_holes_count + 1):
                        holes.append((w + holeEdgeOff, y2 + holeOff + (extra_holes_oc * i)))
                        holes.append((0 - holeEdgeOff, y2 + holeOff + (extra_holes_oc * i)))

        # add left and right holes
        if add_holes_lr:
            if h < 5.5:
                holes.append((0 - holeEdgeOff, h / 2))
                holes.append((w + holeEdgeOff, h / 2))
            else:
                holes.append((0 - holeEdgeOff, holeOff))
                holes.append((w + holeEdgeOff, holeOff))
                holes.append((0 - holeEdgeOff, h - holeOff))
                holes.append((w + holeEdgeOff, h - holeOff))

                extra_holes_count = math.ceil((h - (2 * holeOff)) / holeMaxOC) - 1

                if extra_holes_count >= 1:
                    extra_holes_oc = (h - (2 * holeOff)) / (extra_holes_count + 1)
                    for i in range(1, extra_holes_count + 1):
                        holes.append((0 - holeEdgeOff, holeOff + (extra_holes_oc * i)))
                        holes.append((w + holeEdgeOff, holeOff + (extra_holes_oc * i)))

        # add top and bottom holes
        if add_holes_tb:
            if w < 5.5:
                holes.append((w / 2, 0 - holeEdgeOff))
                holes.append((w / 2, h + holeEdgeOff))
            else:
                holes.append((holeOff, 0 - holeEdgeOff))
                holes.append((holeOff, h + holeEdgeOff))
                holes.append((w - holeOff, 0 - holeEdgeOff))
                holes.append((w - holeOff, h + holeEdgeOff))

                extra_holes_count = math.ceil((w - (2 * holeOff)) / holeMaxOC) - 1

                if extra_holes_count >= 1:
                    extra_holes_oc = (w - (2 * holeOff)) / (extra_holes_count + 1)
                    for i in range(1, extra_holes_count + 1):
                        holes.append((holeOff + (extra_holes_oc * i), 0 - holeEdgeOff))
                        holes.append((holeOff + (extra_holes_oc * i), h + holeEdgeOff))

        # add bottom and top holes to DXF drawing
        for hole in holes:
            self.modelspace.add_circle((hole[0], hole[1]), p.preset.holeRad, dxfattribs=self.YELLOW)

    # add cutout outline
    def __panel_cutout(self, p: AcmPanel):
        l = 0 - p.preset.fWidth
        r = p.w + p.preset.fWidth
        t = p.h + p.preset.fWidth
        b = 0 - p.preset.fWidth
        off1 = 0.1768
        off2 = 0.0518
        h = p.h
        w = p.w
        z = p.z
        cutOff = p.preset.cutOff
        cCut = p.preset.cCut
        fWidth = p.preset.fWidth

        # cutout path for corner panel
        if p.is_corner and p.corner_type == 'h':
            self.modelspace.add_line((0 - cutOff, 0 - cCut), (0 - cutOff, h + cCut), dxfattribs=self.GREEN)  # left
            self.modelspace.add_line((w + cutOff, 0 - cCut), (w + cutOff, h + cCut), dxfattribs=self.GREEN)  # right

            self.modelspace.add_line((0 - cCut, h + cutOff), (z - fWidth + off2, h + cutOff), dxfattribs=self.GREEN)  # top
            self.modelspace.add_line((z - fWidth + off2, h + cutOff), (z, h + off1), dxfattribs=self.GREEN)  # top notch
            self.modelspace.add_line((z + fWidth - off2, h + cutOff), (z, h + off1), dxfattribs=self.GREEN)  # top notch
            self.modelspace.add_line((z + fWidth - off2, h + cutOff), (w + cCut, h + cutOff), dxfattribs=self.GREEN)  # top

            self.modelspace.add_line((0 - cCut, 0 - cutOff), (z - fWidth + off2, 0 - cutOff), dxfattribs=self.GREEN)  # btm
            self.modelspace.add_line((z - fWidth + off2, 0 - cutOff), (z, 0 - off1), dxfattribs=self.GREEN)  # btm notch
            self.modelspace.add_line((z + fWidth - off2, 0 - cutOff), (z, 0 - off1), dxfattribs=self.GREEN)  # btm notch
            self.modelspace.add_line((z + fWidth - off2, 0 - cutOff), (w + cCut, 0 - cutOff), dxfattribs=self.GREEN)  # btm
        elif p.is_corner and p.corner_type == 'v':
            self.modelspace.add_line((0 - cCut, h + cutOff), (w + cCut, h + cutOff), dxfattribs=self.GREEN)  # top
            self.modelspace.add_line((0 - cCut, 0 - cutOff), (w + cCut, 0 - cutOff), dxfattribs=self.GREEN)  # bottom

            self.modelspace.add_line((0 - cutOff, 0 - cCut), (0 - cutOff, z - fWidth + off2), dxfattribs=self.GREEN)  # left
            self.modelspace.add_line((0 - cutOff, z + fWidth - off2), (0 - off1, z), dxfattribs=self.GREEN)  # left notch
            self.modelspace.add_line((0 - cutOff, z - fWidth + off2), (0 - off1, z), dxfattribs=self.GREEN)  # left notch
            self.modelspace.add_line((0 - cutOff, z + fWidth - off2), (0 - cutOff, h + cCut), dxfattribs=self.GREEN)  # left

            self.modelspace.add_line((w + cutOff, 0 - cCut), (w + cutOff, z - fWidth + off2), dxfattribs=self.GREEN)  # rt
            self.modelspace.add_line((w + cutOff, z + fWidth - off2), (w + off1, z), dxfattribs=self.GREEN)  # rt notch
            self.modelspace.add_line((w + cutOff, z - fWidth + off2), (w + off1, z), dxfattribs=self.GREEN)  # rt notch
            self.modelspace.add_line((w + cutOff, z + fWidth - off2), (w + cutOff, h + cCut), dxfattribs=self.GREEN)  # rt
        # cutout path for rectangular panel
        else:
            self.modelspace.add_line((0 - cutOff, 0 - cCut), (0 - cutOff, h + cCut), dxfattribs=self.GREEN)  # left
            self.modelspace.add_line((w + cutOff, 0 - cCut), (w + cutOff, h + cCut), dxfattribs=self.GREEN)  # right
            self.modelspace.add_line((0 - cCut, h + cutOff), (w + cCut, h + cutOff), dxfattribs=self.GREEN)  # top
            self.modelspace.add_line((0 - cCut, 0 - cutOff), (w + cCut, 0 - cutOff), dxfattribs=self.GREEN)  # bottom

        self.modelspace.add_line((0 - cutOff, 0 - cCut), (0 - cCut, 0 - cCut), dxfattribs=self.GREEN)  # left bottom
        self.modelspace.add_line((0 - cutOff, h + cCut), (0 - cCut, h + cCut), dxfattribs=self.GREEN)  # left top
        self.modelspace.add_line((w + cutOff, 0 - cCut), (w + cCut, 0 - cCut), dxfattribs=self.GREEN)  # right bottom
        self.modelspace.add_line((w + cutOff, h + cCut), (w + cCut, h + cCut), dxfattribs=self.GREEN)  # right top
        self.modelspace.add_line((0 - cCut, h + cutOff), (0 - cCut, h + cCut), dxfattribs=self.GREEN)  # top left
        self.modelspace.add_line((w + cCut, h + cutOff), (w + cCut, h + cCut), dxfattribs=self.GREEN)  # top right
        self.modelspace.add_line((0 - cCut, 0 - cutOff), (0 - cCut, 0 - cCut), dxfattribs=self.GREEN)  # bottom left
        self.modelspace.add_line((w + cCut, 0 - cutOff), (w + cCut, 0 - cCut), dxfattribs=self.GREEN)  # bottom right

    # add extra lines that will be routed along fold line to help with folding
    def __panel_folding_helper(self, p: AcmPanel):
        # this only applies to 6mm ACM
        if p.preset.acm_type != AcmPreset.ACM_TYPE_6MM:
            return

        # Constant offset for these lines
        r_offset = 0.12

        self.modelspace.add_line((0 - p.preset.fWidth, 0 + r_offset), (0, 0 + r_offset), dxfattribs=self.CYAN)  # BL
        self.modelspace.add_line((p.w + p.preset.fWidth, 0 + r_offset), (p.w, 0 + r_offset), dxfattribs=self.CYAN)  # BR
        self.modelspace.add_line((0 - p.preset.fWidth, p.h - r_offset), (0, p.h - r_offset), dxfattribs=self.CYAN)  # TL
        self.modelspace.add_line((p.w + p.preset.fWidth, p.h - r_offset), (p.w, p.h - r_offset), dxfattribs=self.CYAN)  # TR

        self.modelspace.add_line((0 + r_offset, 0), (0 + r_offset, 0 - p.preset.fWidth), dxfattribs=self.CYAN)  # BL
        self.modelspace.add_line((p.w - r_offset, 0), (p.w - r_offset, 0 - p.preset.fWidth), dxfattribs=self.CYAN)  # BR
        self.modelspace.add_line((0 + r_offset, p.h), (0 + r_offset, p.h + p.preset.fWidth), dxfattribs=self.CYAN)  # TL
        self.modelspace.add_line((p.w - r_offset, p.h), (p.w - r_offset, p.h + p.preset.fWidth), dxfattribs=self.CYAN)  # TR

    # draw corner cutouts
    def __panel_corners(self, p: AcmPanel):
        self.modelspace.add_line((0 - p.preset.fWidth - p.preset.cOffset, 0 - p.preset.cOffset), (0 - p.preset.cOffset, 0 - p.preset.cOffset), dxfattribs=self.RED)  # BL
        self.modelspace.add_line((0 - p.preset.cOffset, 0 - p.preset.cOffset), (0 - p.preset.cOffset, 0 - p.preset.fWidth - p.preset.cOffset), dxfattribs=self.RED)  # BL
        self.modelspace.add_line((0 - p.preset.fWidth - p.preset.cOffset, p.h + p.preset.cOffset), (0 - p.preset.cOffset, p.h + p.preset.cOffset), dxfattribs=self.RED)  # TL
        self.modelspace.add_line((0 - p.preset.cOffset, p.h + p.preset.cOffset), (0 - p.preset.cOffset, p.h + p.preset.fWidth + p.preset.cOffset), dxfattribs=self.RED)  # TL
        self.modelspace.add_line((p.w + p.preset.fWidth + p.preset.cOffset, p.h + p.preset.cOffset), (p.w + p.preset.cOffset, p.h + p.preset.cOffset), dxfattribs=self.RED)  # TR
        self.modelspace.add_line((p.w + p.preset.cOffset, p.h + p.preset.cOffset), (p.w + p.preset.cOffset, p.h + p.preset.fWidth + p.preset.cOffset), dxfattribs=self.RED)  # TR
        self.modelspace.add_line((p.w + p.preset.fWidth + p.preset.cOffset, 0 - p.preset.cOffset), (p.w + p.preset.cOffset, 0 - p.preset.cOffset), dxfattribs=self.RED)  # BR
        self.modelspace.add_line((p.w + p.preset.cOffset, 0 - p.preset.cOffset), (p.w + p.preset.cOffset, 0 - p.preset.fWidth - p.preset.cOffset), dxfattribs=self.RED)  # BR

    # draw rectangular panel face
    def __panel_face(self, p: AcmPanel):
        self.modelspace.add_line((0, 0), (0, p.h), dxfattribs=self.WHITE)
        self.modelspace.add_line((0, p.h), (p.w, p.h), dxfattribs=self.WHITE)
        self.modelspace.add_line((p.w, p.h), (p.w, 0), dxfattribs=self.WHITE)
        self.modelspace.add_line((p.w, 0), (0, 0), dxfattribs=self.WHITE)

        # Add horizontal or vertical folding edge if it's a corner panel
        if p.is_corner:
            if p.corner_type == 'h':
                self.modelspace.add_line((p.z, 0), (p.z, p.h), dxfattribs=self.WHITE)
            else:
                self.modelspace.add_line((0, p.z), (p.w, p.z), dxfattribs=self.WHITE)
