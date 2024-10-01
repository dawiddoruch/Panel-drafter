from classes import Panel
from classes import PanelPreset
from classes.DxfColors import DxfColors as dxfc
import ezdxf as dxf
from math import ceil
import math


class DxfDrafter:
    modelspace = None
    holes = []
    preset = None

    HOLES_LEFT = "hl"
    HOLES_RIGHT = "hr"
    HOLES_TOP = "ht"
    HOLES_BOTTOM = "hb"

    dxfa = {'MILL-E': {'layer': 'MILL-E', 'color': dxfc.BLUE},
            'MILL-VGR': {'layer': 'MILL-VGR', 'color': dxfc.RED},
            'MILL-VGR-ALT': {'layer': 'MILL-VGR-ALT', 'color': dxfc.BURGUNDY},
            'HOLE': {'layer': 'HOLE', 'color': dxfc.YELLOW},
            'BLINDHOLE': {'layer': 'BLINDHOLE', 'color': dxfc.ORANGE},
            'MILL-I': {'layer': 'MILL-I', 'color': dxfc.CYAN},
            'MILL-C': {'layer': 'MILL-C', 'color': dxfc.PURPLE},
            'GRAVE': {'layer': 'GRAVE', 'color': dxfc.SEA},
            'POCKET': {'layer': 'POCKET', 'color': dxfc.GREEN},
            'INFOPIECE': {'layer': 'INFOPIECE', 'color': dxfc.WHITE, 'height': 2},
            'INFOPROJECT': {'layer': 'INFOPROJECT', 'color': dxfc.PINK},
            'HELPER': {'layer': 'HELPER', 'color': dxfc.CYAN},
            'CORNER': {'layer': 'CORNER', 'color': dxfc.RED}}

    dxfattributes = dxfa['MILL-E']

    def __init__(self, panel: Panel, output_path):
        output_file = "{}{} x {}.dxf".format(output_path, panel.name, panel.quantity)
        drawing = dxf.new(dxfversion='R2004')
        drawing.header['$MEASUREMENT'] = 1

        for key in self.dxfa:
            drawing.layers.add(name=self.dxfa[key]['layer'], color=self.dxfa[key]['color'])

        self.holes = []
        self.preset = panel.preset
        self.modelspace = drawing.modelspace()

        # draw panel based on what type it is
        if panel.preset.panel_type == panel.preset.TYPE_4MM_ARROWHEAD_LEAN:
            self.__panel_face_lean(panel)
            self.__panel_name(panel)
            self.__panel_cutout_lean(panel)
        elif panel.preset.panel_type == panel.preset.TYPE_FIBERCEMENT:
            self.__panel_face_fc(panel)
            self.__panel_name(panel)
        else:
            self.__panel_face(panel)
            self.__panel_corners(panel)
            # self.__panel_folding_helper(panel)
            self.__panel_cutout(panel)
            self.__panel_drill(panel)
            self.__panel_name(panel)

        drawing.saveas(output_file)

    # Panel cutout for fibercement
    def __panel_face_fc(self, p: Panel):
        self.__set_dxfattributes('MILL-E')
        w = p.w
        h = p.h
        self.__add_line((0, 0), (w, 0))
        self.__add_line((w, 0), (w, h))
        self.__add_line((w, h), (0, h))
        self.__add_line((0, h), (0, 0))

    # Panel cutout for Arrowhead LEAN
    def __panel_cutout_lean(self, p: Panel):
        tt, tr, tb, tl = p.tab_t, p.tab_r, p.tab_b, p.tab_l
        case = (tt != 0, tr != 0, tb != 0, tl != 0)

        self.__set_dxfattributes('MILL-E')
        if (0, 0, 0, 0) == case:
            # print("NO TABS")
            pass

        elif (1, 0, 0, 0) == case:
            # print("TOP")
            pass

        elif (0, 0, 1, 0) == case:
            # print("BOTTOM")
            pass

        elif (0, 1, 0, 0) == case:
            # print("RIGHT")
            pass

        elif (0, 0, 0, 1) == case:
            # print("LEFT")
            pass

        elif (1, 0, 1, 0) == case:
            # print("TOP BOTTOM")
            pass

        elif (0, 1, 0, 1) == case:
            # print("RIGHT LEFT")
            pass

    # Set dxf attributes that will be used for all operations that are to follow
    def __set_dxfattributes(self, operation):
        self.dxfattributes = self.dxfa[operation]
        # print(self.dxfattributes)

    # add panel name
    def __panel_name(self, p: Panel):
        self.__set_dxfattributes('INFOPIECE')
        panel_name = "{}/{}/{}".format(p.name, p.quantity, p.priority)
        self.modelspace.add_text(panel_name, dxfattribs=self.dxfattributes).set_placement(((p.w / 2), (p.h / 2)),
                                                                                          align=dxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # add drill holes
    def __panel_drill(self, p: Panel):
        self.__set_dxfattributes('HOLE')
        for hole in self.holes:
            self.modelspace.add_circle((hole[0], hole[1]), p.preset.holeRad, dxfattribs=self.dxfattributes)

    # add cutout outline
    def __panel_cutout(self, p: Panel):
        w = p.w
        h = p.h
        co = p.preset.cutOff  # 1.145
        cc = p.preset.cCut  # 0.11
        fw = p.preset.fWidth  # 1.02
        tip = p.preset.cutOff - 0.9682  # 0.1768
        top = fw - 0.0518

        tt, tr, tb, tl = p.tab_t, p.tab_r, p.tab_b, p.tab_l
        case = (tt != 0, tr != 0, tb != 0, tl != 0)

        self.__set_dxfattributes('MILL-E')
        if (0, 0, 0, 0) == case:
            # print("NO TABS")
            self.__add_line((-co, -cc), (-co, h + cc), self.HOLES_LEFT)  # Left
            self.__add_line((-cc, h + co), (w + cc, h + co), self.HOLES_TOP)  # Top
            self.__add_line((w + co, h + cc), (w + co, -cc), self.HOLES_RIGHT)  # Right
            self.__add_line((-cc, -co), (w + cc, -co), self.HOLES_BOTTOM)  # Bottom

        elif (1, 0, 0, 0) == case:
            # print("TOP")
            self.__add_line((-cc, h + tt + co), (w + cc, h + tt + co), self.HOLES_TOP)  # Top
            self.__add_line((-cc, -co), (w + cc, -co), self.HOLES_BOTTOM)  # Bottom
            # LEFT
            self.__add_line((-co, -cc), (-co, h - top), self.HOLES_LEFT)
            self.__add_line((-tip, h), (-co, h - top))
            self.__add_line((-tip, h), (-co, h + top))
            self.__add_line((-co, h + tt + cc), (-co, h + top), self.HOLES_LEFT)
            # RIGHT
            self.__add_line((w + co, -cc), (w + co, h - top), self.HOLES_RIGHT)
            self.__add_line((w + tip, h), (w + co, h - top))
            self.__add_line((w + tip, h), (w + co, h + top))
            self.__add_line((w + co, h + tt + cc), (w + co, h + top), self.HOLES_RIGHT)

        elif (0, 0, 1, 0) == case:
            # print("BOTTOM")
            self.__add_line((-cc, h + co), (w + cc, h + co), self.HOLES_TOP)  # Top
            self.__add_line((-cc, -co - tb), (w + cc, -co - tb), self.HOLES_BOTTOM)  # Bottom
            # LEFT
            self.__add_line((-co, h + cc), (-co, top), self.HOLES_LEFT)
            self.__add_line((-co, top), (-tip, 0))
            self.__add_line((-tip, 0), (-co, -top))
            self.__add_line((-co, -top), (-co, -tb - cc), self.HOLES_LEFT)
            # RIGHT
            self.__add_line((w + co, h + cc), (w + co, top), self.HOLES_RIGHT)
            self.__add_line((w + co, top), (w + tip, 0))
            self.__add_line((w + tip, 0), (w + co, -top))
            self.__add_line((w + co, -top), (w + co, -tb - cc), self.HOLES_RIGHT)

        elif (0, 1, 0, 0) == case:
            # print("RIGHT")
            self.__add_line((-co, -cc), (-co, h + cc), self.HOLES_LEFT)  # Left
            self.__add_line((w + co + tr, -cc), (w + co + tr, h + cc), self.HOLES_RIGHT)  # Right
            # TOP
            self.__add_line((-cc, h + co), (w - top, h + co), self.HOLES_TOP)
            self.__add_line((w - top, h + co), (w, h + tip))
            self.__add_line((w, h + tip), (w + top, h + co))
            self.__add_line((w + top, h + co), (w + cc + tr, h + co), self.HOLES_TOP)
            # BOTTOM
            self.__add_line((-cc, -co), (w - top, -co), self.HOLES_BOTTOM)
            self.__add_line((w - top, -co), (w, -tip))
            self.__add_line((w, -tip), (w + top, -co))
            self.__add_line((w + top, -co), (w + cc + tr, -co), self.HOLES_BOTTOM)

        elif (0, 0, 0, 1) == case:
            # print("LEFT")
            self.__add_line((-tl - co, -cc), (-tl - co, h + cc), self.HOLES_LEFT)  # Left
            self.__add_line((w + co, -cc), (w + co, h + cc), self.HOLES_RIGHT)  # Right
            # TOP
            self.__add_line((-tl - cc, h + co), (-top, h + co), self.HOLES_TOP)
            self.__add_line((-top, h + co), (0, h + tip))
            self.__add_line((0, h + tip), (top, h + co))
            self.__add_line((top, h + co), (w + cc, h + co), self.HOLES_TOP)
            # BOTTOM
            self.__add_line((-tl - cc, -co), (-top, -co), self.HOLES_BOTTOM)
            self.__add_line((-top, -co), (0, -tip))
            self.__add_line((0, -tip), (top, -co))
            self.__add_line((top, -co), (w + cc, -co), self.HOLES_BOTTOM)

        elif (1, 0, 1, 0) == case:
            # print("TOP BOTTOM")
            self.__add_line((-cc, h + tt + co), (w + cc, h + tt + co), self.HOLES_TOP)  # Top
            self.__add_line((-cc, -co - tb), (w + cc, -co - tb), self.HOLES_BOTTOM)  # Bottom
            # LEFT
            self.__add_line((-co, -tb - cc), (-co, -top), self.HOLES_LEFT)
            self.__add_line((-co, -top), (-tip, 0))
            self.__add_line((-tip, 0), (-co, top))
            self.__add_line((-co, top), (-co, h - top), self.HOLES_LEFT)
            self.__add_line((-co, h - top), (-tip, h))
            self.__add_line((-tip, h), (-co, h + top))
            self.__add_line((-co, h + top), (-co, h + tt + cc), self.HOLES_LEFT)
            # RIGHT
            self.__add_line((w + co, -tb - cc), (w + co, -top), self.HOLES_RIGHT)
            self.__add_line((w + co, -top), (w + tip, 0), )
            self.__add_line((w + tip, 0), (w + co, top), )
            self.__add_line((w + co, top), (w + co, h - top), self.HOLES_RIGHT)
            self.__add_line((w + co, h - top), (w + tip, h))
            self.__add_line((w + tip, h), (w + co, h + top))
            self.__add_line((w + co, h + top), (w + co, h + tt + cc), self.HOLES_RIGHT)

        elif (0, 1, 0, 1) == case:
            # print("RIGHT LEFT")
            self.__add_line((-tl - co, -cc), (-tl - co, h + cc), self.HOLES_LEFT)  # Left
            self.__add_line((w + co + tr, -cc), (w + co + tr, h + cc), self.HOLES_RIGHT)  # Right
            # TOP
            self.__add_line((-tl - cc, h + co), (-top, h + co), self.HOLES_TOP)
            self.__add_line((-top, h + co), (0, h + tip))
            self.__add_line((0, h + tip), (top, h + co))
            self.__add_line((top, h + co), (w - top, h + co), self.HOLES_TOP)
            self.__add_line((w - top, h + co), (w, h + tip))
            self.__add_line((w, h + tip), (w + top, h + co))
            self.__add_line((w + top, h + co), (w + tr + cc, h + co), self.HOLES_TOP)
            # BOTTOM
            self.__add_line((-tl - cc, -co), (-top, -co), self.HOLES_BOTTOM)
            self.__add_line((-top, -co), (0, -tip), )
            self.__add_line((0, -tip), (top, -co), )
            self.__add_line((top, -co), (w - top, -co), self.HOLES_BOTTOM)
            self.__add_line((w - top, -co), (w, -tip))
            self.__add_line((w, -tip), (w + top, -co))
            self.__add_line((w + top, -co), (w + tr + cc, -co), self.HOLES_BOTTOM)

        elif (1, 1, 0, 0) == case:
            print("TOP RIGHT")

        elif (0, 1, 1, 0) == case:
            print("RIGHT BOTTOM")

        elif (0, 0, 1, 1) == case:
            print("BOTTOM LEFT")

        elif (1, 0, 0, 1) == case:
            print("LEFT TOP")

        elif (1, 1, 1, 0) == case:
            print("TOP RIGHT BOTTOM")

        elif (1, 1, 0, 1) == case:
            print("TOP RIGHT LEFT")

        elif (1, 0, 1, 1) == case:
            print("TOP BOTTOM LEFT")

        elif (0, 1, 1, 1) == case:
            print("RIGHT BOTTOM LEFT")

        elif (1, 1, 1, 1) == case:
            print("TOP RIGHT BOTTOM LEFT")

    # add extra lines that will be routed along fold line to help with folding
    def __panel_folding_helper(self, p: Panel):
        # this only applies to 6mm ACM
        if p.preset.acm_type != PanelPreset.TYPE_6MM:
            return

        # Constant offset for these lines
        r_offset = 0.12

        self.__set_dxfattributes('HELPER')
        self.__add_line((0 - p.preset.fWidth, 0 + r_offset), (0, 0 + r_offset))  # BL
        self.__add_line((p.w + p.preset.fWidth, 0 + r_offset), (p.w, 0 + r_offset))  # BR
        self.__add_line((0 - p.preset.fWidth, p.h - r_offset), (0, p.h - r_offset))  # TL
        self.__add_line((p.w + p.preset.fWidth, p.h - r_offset), (p.w, p.h - r_offset))  # TR

        self.__add_line((0 + r_offset, 0), (0 + r_offset, 0 - p.preset.fWidth))  # BL
        self.__add_line((p.w - r_offset, 0), (p.w - r_offset, 0 - p.preset.fWidth))  # BR
        self.__add_line((0 + r_offset, p.h), (0 + r_offset, p.h + p.preset.fWidth))  # TL
        self.__add_line((p.w - r_offset, p.h), (p.w - r_offset, p.h + p.preset.fWidth))  # TR

    # draw corner cutouts
    def __panel_corners(self, p: Panel):
        co = p.preset.cOffset
        cc = p.preset.cCut

        tr1 = tr2 = tl1 = tl2 = bl1 = bl2 = br1 = br2 = p.preset.cutOff - cc
        if p.tab_t != 0 and p.tab_r != 0:
            tr1 = p.tab_r
            tr2 = p.tab_t
        if p.tab_t != 0 and p.tab_l != 0:
            tl1 = p.tab_l
            tl2 = p.tab_t
        if p.tab_b != 0 and p.tab_l != 0:
            bl1 = p.tab_l
            bl2 = p.tab_b
        if p.tab_b != 0 and p.tab_r != 0:
            br1 = p.tab_r
            br2 = p.tab_b

        tr3 = tl3 = bl3 = br3 = 0
        if p.tab_t == 0 and p.tab_r != 0:
            tr3 = p.tab_r
        if p.tab_t == 0 and p.tab_l != 0:
            tl3 = p.tab_l
        if p.tab_b == 0 and p.tab_l != 0:
            bl3 = p.tab_l
        if p.tab_b == 0 and p.tab_r != 0:
            br3 = p.tab_r

        tr4 = tl4 = bl4 = br4 = 0
        if p.tab_t != 0 and p.tab_r == 0:
            tr4 = p.tab_t
        if p.tab_t != 0 and p.tab_l == 0:
            tl4 = p.tab_t
        if p.tab_b != 0 and p.tab_l == 0:
            bl4 = p.tab_b
        if p.tab_b != 0 and p.tab_r == 0:
            br4 = p.tab_b

        # TR
        self.__set_dxfattributes('CORNER')
        self.__add_line((p.w + co + tr3, p.h + co + tr4), (p.w + tr3 + tr1, p.h + co + tr4))  # H
        self.__add_line((p.w + co + tr3, p.h + co + tr4), (p.w + co + tr3, p.h + tr2 + tr4))  # V
        self.__set_dxfattributes('MILL-E')
        self.__add_line((p.w + tr3 + cc, p.h + tr4 + cc), (p.w + tr3 + tr1 + cc, p.h + tr4 + cc))
        self.__add_line((p.w + tr3 + cc, p.h + tr4 + cc), (p.w + tr3 + cc, p.h + tr2 + tr4 + cc))
        # TL
        self.__set_dxfattributes('CORNER')
        self.__add_line((-co - tl3, p.h + co + tl4), (- tl1 - tl3, p.h + co + tl4))  # H
        self.__add_line((-co - tl3, p.h + co + tl4), (-co - tl3, p.h + tl2 + tl4))  # V
        self.__set_dxfattributes('MILL-E')
        self.__add_line((-tl3 - cc, p.h + tl4 + cc), (-tl1 - tl3 - cc, p.h + tl4 + cc))
        self.__add_line((-tl3 - cc, p.h + tl4 + cc), (-tl3 - cc, p.h + tl2 + tl4 + cc))
        # BL
        self.__set_dxfattributes('CORNER')
        self.__add_line((-co - bl3, -co - bl4), (-bl1 - bl3, -co - bl4))  # H
        self.__add_line((-co - bl3, -co - bl4), (-co - bl3, -bl2 - bl4))  # V
        self.__set_dxfattributes('MILL-E')
        self.__add_line((-bl3 - cc, - bl4 - cc), (-bl1 - bl3 - cc, -bl4 - cc))
        self.__add_line((-bl3 - cc, - bl4 - cc), (-bl3 - cc, -bl2 - bl4 - cc))
        # BR
        self.__set_dxfattributes('CORNER')
        self.__add_line((p.w + co + br3, -co - br4), (p.w + br3 + br1, -co - br4))  # H
        self.__add_line((p.w + co + br3, -co - br4), (p.w + br3 + co, -br2 - br4))  # V
        self.__set_dxfattributes('MILL-E')
        self.__add_line((p.w + br3 + cc, -br4 - cc), (p.w + br3 + br1 + cc, - br4 - cc))
        self.__add_line((p.w + br3 + cc, -br4 - cc), (p.w + br3 + cc, -br2 - br4 - cc))

    def __set_conditional_dxfattributes(self, test_var, true_val, true_res, false_res):
        if test_var == true_val:
            self.__set_dxfattributes(true_res)
        else:
            self.__set_dxfattributes(false_res)

    # draw rectangular panel face
    def __panel_face_lean(self, p: Panel):
        ex = 0.51
        bx = 0.43
        tl = p.tab_l
        tr = p.tab_r
        tt = p.tab_t
        tb = p.tab_b
        bl = 0 if tl == 0 else ex
        br = 0 if tr == 0 else ex
        bt = 0 if tt == 0 else ex
        bb = 0 if tb == 0 else ex

        deg_gamma = 90 - (0.5 * p.angle)
        rad_gamma = math.radians(deg_gamma)
        tan_gamma = round(math.tan(rad_gamma), 6)

        x1 = round(ex * tan_gamma, 4)
        x2 = round((ex + bx) * tan_gamma, 4)

        self.__set_conditional_dxfattributes(tb, 0, 'MILL-VGR', 'MILL-C')
        self.__add_line((-ex - tl + bb, 0), (p.w + ex + tr - bb, 0))  # bottom

        self.__set_conditional_dxfattributes(tt, 0, 'MILL-VGR', 'MILL-C')
        self.__add_line((-ex - tl + bt, p.h), (p.w + ex + tr - bt, p.h))  # top

        self.__set_conditional_dxfattributes(tr, 0, 'MILL-VGR', 'MILL-C')
        self.__add_line((p.w, -ex - tb + br), (p.w, p.h + ex + tt - br))  # right

        self.__set_conditional_dxfattributes(tl, 0, 'MILL-VGR', 'MILL-C')
        self.__add_line((0, -ex - tb + bl), (0, p.h + ex + tt - bl))  # left

        if [tt, tr, tb, tl] == [0, 0, 0, 0]:
            self.__set_dxfattributes('MILL-VGR-ALT')
            self.__add_multi_line([
                (-ex, 0),
                (-ex, p.h),
                (0, p.h + ex),
                (p.w, p.h + ex),
                (p.w + ex, p.h),
                (p.w + ex, 0),
                (p.w, -ex),
                (0, -ex),
                (-ex, 0)
            ])

        if tr == 0 and tl == 0:
            self.__set_dxfattributes('MILL-E')
            # Bottom cutout
            self.__add_line((0, -tb), (0, -tb - ex))
            self.__add_line((0, -tb - ex), (bx, -tb - ex - bx))
            self.__add_line((bx, -tb - ex - bx), (p.w - bx, -tb - ex - bx))
            self.__add_line((p.w - bx, -tb - ex - bx), (p.w, -tb - ex))
            self.__add_line((p.w, -tb - ex), (p.w, -tb))
            # Top cutout
            self.__add_line((0, p.h + tt), (0, p.h + tt + ex))
            self.__add_line((0, p.h + tt + ex), (bx, p.h + tt + ex + bx))
            self.__add_line((bx, p.h + tt + ex + bx), (p.w - bx, p.h + tt + ex + bx))
            self.__add_line((p.w - bx, p.h + tt + ex + bx), (p.w, p.h + tt + ex))
            self.__add_line((p.w, p.h + tt + ex), (p.w, p.h + tt))

        if tb == 0 and tt == 0:
            self.__set_dxfattributes('MILL-E')
            # Right cutout
            self.__add_line((p.w + tr, 0), (p.w + tr + ex, 0))
            self.__add_line((p.w + tr + ex, 0), (p.w + tr + ex + bx, bx))
            self.__add_line((p.w + tr + ex + bx, bx), (p.w + tr + ex + bx, p.h - bx))
            self.__add_line((p.w + tr + ex + bx, p.h - bx), (p.w + tr + ex, p.h))
            self.__add_line((p.w + tr + ex, p.h), (p.w + tr, p.h))
            # Left cutout
            self.__add_line((-tl, 0), (-tl - ex, 0))
            self.__add_line((-tl - ex, 0), (-tl - ex - bx, bx))
            self.__add_line((-tl - ex - bx, bx), (-tl - ex - bx, p.h - bx))
            self.__add_line((-tl - ex - bx, p.h - bx), (-tl - ex, p.h))
            self.__add_line((-tl - ex, p.h), (-tl, p.h))

        # top tab
        if tt != 0:
            self.__set_dxfattributes('MILL-VGR')
            self.__add_line((-ex, p.h + tt), (p.w + ex, p.h + tt))
            self.__set_dxfattributes('MILL-VGR-ALT')
            self.__add_multi_line([
                (-ex, 0),
                (-ex, p.h + tt),
                (0, p.h + tt + ex),
                (p.w, p.h + tt + ex),
                (p.w + ex, p.h + tt),
                (p.w + ex, 0),
                (p.w, -ex),
                (0, -ex),
                (p.w, -ex)])
            # left side
            self.__set_dxfattributes('MILL-E')
            self.__add_multi_line([
                (0, 0),
                (-ex, 0),
                (-ex - bx, bx),
                (-ex - bx, p.h - x2),
                (0, p.h),
                (-ex - bx, p.h + x2),
                (-ex - bx, p.h + tt - bx),
                (-ex, p.h + tt),
                (0, p.h + tt)])
            # right side
            self.__add_multi_line([
                (p.w, 0),
                (p.w + ex, 0),
                (p.w + ex + bx, bx),
                (p.w + ex + bx, p.h - x2),
                (p.w, p.h),
                (p.w + ex + bx, p.h + x2),
                (p.w + ex + bx, p.h + tt - bx),
                (p.w + ex, p.h + tt),
                (p.w, p.h + tt)])

        # bottom tab
        if tb != 0:
            self.__set_dxfattributes('MILL-VGR')
            self.__add_line((-ex, -tb), (p.w + ex, -tb))
            self.__set_dxfattributes('MILL-VGR-ALT')
            self.__add_multi_line([
                (-ex, p.h),
                (0, p.h + ex),
                (p.w, p.h + ex),
                (p.w + ex, p.h),
                (p.w + ex, -tb),
                (p.w, -tb - ex),
                (0, -tb - ex),
                (-ex, -tb),
                (-ex, p.h)])
            # left side
            self.__set_dxfattributes('MILL-E')
            self.__add_multi_line([
                (0, p.h),
                (-ex, p.h),
                (-ex - bx, p.h - bx),
                (-ex - bx, x2),
                (0, 0),
                (-ex - bx, -x2),
                (-ex - bx, -tb + bx),
                (-ex, -tb),
                (0, -tb)])
            # right side
            self.__add_multi_line([
                (p.w, p.h),
                (p.w + ex, p.h),
                (p.w + ex + bx, p.h - bx),
                (p.w + ex + bx, x2),
                (p.w, 0),
                (p.w + ex + bx, -x2),
                (p.w + ex + bx, -tb + bx),
                (p.w + ex, -tb),
                (p.w, -tb)])

        # right tab
        if tr != 0:
            self.__set_dxfattributes('MILL-VGR')
            self.__add_line((p.w + tr, -ex), (p.w + tr, p.h + ex))
            self.__set_dxfattributes('MILL-VGR-ALT')
            self.__add_multi_line([
                (-ex, 0),
                (-ex, p.h),
                (0, p.h + ex),
                (p.w + tr, p.h + ex),
                (p.w + tr + ex, p.h),
                (p.w + tr + ex, 0),
                (p.w + tr, -ex),
                (0, -ex),
                (-ex, 0)])
            # top side
            self.__set_dxfattributes('MILL-E')
            self.__add_multi_line([
                (0, p.h),
                (0, p.h + ex),
                (bx, p.h + ex + bx),
                (p.w - x2, p.h + ex + bx),
                (p.w, p.h),
                (p.w + x2, p.h + bx + ex),
                (p.w + tr - bx, p.h + bx + ex),
                (p.w + tr, p.h + ex),
                (p.w + tr, p.h)
            ])
            # bottom side
            self.__add_multi_line([
                (0, 0),
                (0, -ex),
                (bx, -ex - bx),
                (p.w - x2, - ex - bx),
                (p.w, 0),
                (p.w + x2, - bx - ex),
                (p.w + tr - bx, - bx - ex),
                (p.w + tr, -ex),
                (p.w + tr, 0)
            ])

        # left tab
        if tl != 0:
            self.__set_dxfattributes('MILL-VGR')
            self.__add_line((-tl, -ex), (-tl, p.h + ex))
            self.__set_dxfattributes('MILL-VGR-ALT')
            self.__add_multi_line([
                (-tl - ex, 0),
                (-tl - ex, p.h),
                (-tl, p.h + ex),
                (p.w, p.h + ex),
                (p.w + ex, p.h),
                (p.w + ex, 0),
                (p.w, -ex),
                (-tl, -ex),
                (-tl - ex, 0)])
            # top side
            self.__set_dxfattributes('MILL-E')
            self.__add_multi_line([
                (p.w, p.h),
                (p.w, p.h + ex),
                (p.w - bx, p.h + ex + bx),
                (x2, p.h + ex + bx),
                (0, p.h),
                (-x2, p.h + ex + bx),
                (-tl + bx, p.h + ex + bx),
                (-tl, p.h + ex),
                (-tl, p.h)])
            # bottom side
            self.__add_multi_line([
                (p.w, 0),
                (p.w, -ex),
                (p.w - bx, -ex - bx),
                (x2, -ex - bx),
                (0, 0),
                (-x2, -ex - bx),
                (-tl + bx, -ex - bx),
                (-tl, -ex),
                (-tl, 0)])

    # draw rectangular panel face
    def __panel_face(self, p: Panel):
        self.__set_dxfattributes('MILL-VGR')
        self.__add_line((0, 0), (p.w, 0))
        self.__add_line((p.w, 0), (p.w, p.h))
        self.__add_line((p.w, p.h), (0, p.h))
        self.__add_line((0, p.h), (0, 0))

        if p.tab_t != 0:
            self.__add_line((0, p.h), (0, p.h + p.tab_t))
            self.__add_line((0, p.h + p.tab_t), (p.w, p.h + p.tab_t))
            self.__add_line((p.w, p.h + p.tab_t), (p.w, p.h))

        if p.tab_b != 0:
            self.__add_line((0, 0), (0, -p.tab_b))
            self.__add_line((0, -p.tab_b), (p.w, -p.tab_b))
            self.__add_line((p.w, -p.tab_b), (p.w, 0))

        if p.tab_r != 0:
            self.__add_line((p.w, 0), (p.w + p.tab_r, 0))
            self.__add_line((p.w + p.tab_r, 0), (p.w + p.tab_r, p.h))
            self.__add_line((p.w + p.tab_r, p.h), (p.w, p.h))

        if p.tab_l != 0:
            self.__add_line((0, 0), (-p.tab_l, 0))
            self.__add_line((-p.tab_l, 0), (-p.tab_l, p.h))
            self.__add_line((-p.tab_l, p.h), (0, p.h))

    def __add_multi_line(self, points):
        total_points = len(points)
        if total_points > 2:
            for x in range(1, total_points):
                self.__add_line(points[x - 1], points[x])

    def __add_line(self, start, end, append_holes=None):

        self.modelspace.add_line(start, end, dxfattribs=self.dxfattributes)

        if append_holes is not None:
            length = start_x = start_y = 0
            if append_holes == self.HOLES_TOP:
                length = abs(end[0] - start[0])
                start_x = min(start[0], end[0])
                start_y = start[1]
            elif append_holes == self.HOLES_BOTTOM:
                length = abs(end[0] - start[0])
                start_x = min(start[0], end[0])
                start_y = start[1]
            elif append_holes == self.HOLES_LEFT:
                length = abs(end[1] - start[1])
                start_y = min(start[1], end[1])
                start_x = start[0]
            elif append_holes == self.HOLES_RIGHT:
                length = abs(end[1] - start[1])
                start_y = min(start[1], end[1])
                start_x = start[0]
            self.__add_holes(length, start_x, start_y, append_holes)

    def __add_holes(self, length, start_x, start_y, append_holes):
        hole_edge_off = self.preset.cutOff - self.preset.holeEdgeOff
        hole_off = self.preset.holeOff
        hole_max_oc = self.preset.holeMaxOC
        usable_length = length - (hole_off * 2)
        holes_count = 0

        holes_spacing = 0
        if 2.75 < length < 6.5:
            holes_count = 1
            hole_off = length / 2
        elif length >= 6.5:
            holes_count = ceil(usable_length / hole_max_oc) + 1
            if holes_count < 2:
                holes_count = 2
            holes_spacing = usable_length / (holes_count - 1)

        if append_holes == self.HOLES_RIGHT and False:
            print("Length: {}".format(length))
            print("Start X: {}".format(start_x))
            print("Start Y: {}".format(start_y))
            print("Usable length: {}".format(usable_length))
            print("Spacing: {}".format(holes_spacing))
            print("Holes count: {}".format(holes_count))
            print("")

        for i in range(0, holes_count):
            hole_x = 0
            hole_y = 0
            if append_holes in (self.HOLES_TOP, self.HOLES_BOTTOM):
                hole_y = start_y
                hole_x = hole_off + start_x + (i * holes_spacing)
                if append_holes == self.HOLES_TOP:
                    hole_y -= hole_edge_off
                else:
                    hole_y += hole_edge_off
            elif append_holes in (self.HOLES_LEFT, self.HOLES_RIGHT):
                hole_y = hole_off + start_y + (i * holes_spacing)
                hole_x = start_x
                if append_holes == self.HOLES_LEFT:
                    hole_x += hole_edge_off
                else:
                    hole_x -= hole_edge_off
            self.holes.append((hole_x, hole_y))
