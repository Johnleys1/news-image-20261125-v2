#!/usr/bin/env python3
"""Render THE WORLD - Wednesday 25 November 2026 (1024x1024 PNG).
Pure stdlib: a tiny raster canvas, a 5x7 bitmap font drawn from scratch,
vector scenes, a world map band, and a zlib PNG writer.
"""
import math
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font: 5x7
# Each glyph: 7 rows of 5 cells, '#' = ink.
FONT = {
'A': ("  #  ", " # # ", "#   #", "#   #", "#####", "#   #", "#   #"),
'B': ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
'C': (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
'D': ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
'E': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
'F': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
'G': (" ####", "#    ", "#    ", "# ###", "#   #", "#   #", " ### "),
'H': ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
'I': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"),
'J': ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
'K': ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
'L': ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
'M': ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
'N': ("#   #", "##  #", "##  #", "# # #", "#  ##", "#  ##", "#   #"),
'O': (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
'P': ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
'Q': (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
'R': ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
'S': (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
'T': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
'U': ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
'V': ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
'W': ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
'X': ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
'Y': ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
'Z': ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
'a': ("     ", "     ", " ### ", "    #", " ####", "#   #", " ####"),
'b': ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "),
'c': ("     ", "     ", " ####", "#    ", "#    ", "#    ", " ####"),
'd': ("    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"),
'e': ("     ", "     ", " ### ", "#   #", "#####", "#    ", " ### "),
'f': ("  ## ", " #  #", " #   ", "#### ", " #   ", " #   ", " #   "),
'g': ("     ", "     ", " ####", "#   #", "#   #", " ####", "    #"),
'h': ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"),
'i': ("  #  ", "     ", " ##  ", "  #  ", "  #  ", "  #  ", " ### "),
'j': ("   # ", "     ", "  ## ", "   # ", "   # ", "   # ", "   # "),
'k': ("#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "),
'l': (" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
'm': ("     ", "     ", "## # ", "# # #", "# # #", "# # #", "# # #"),
'n': ("     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"),
'o': ("     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "),
'p': ("     ", "     ", "#### ", "#   #", "#   #", "#### ", "#    "),
'q': ("     ", "     ", " ####", "#   #", "#   #", " ####", "    #"),
'r': ("     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "),
's': ("     ", "     ", " ####", "#    ", " ### ", "    #", "#### "),
't': (" #   ", " #   ", "#### ", " #   ", " #   ", " #   ", "  ## "),
'u': ("     ", "     ", "#   #", "#   #", "#   #", "#  ##", " ## #"),
'v': ("     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "),
'w': ("     ", "     ", "#   #", "# # #", "# # #", "# # #", " # # "),
'x': ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
'y': ("     ", "     ", "#   #", "#   #", " ####", "    #", " ### "),
'z': ("     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"),
'0': (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
'1': ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
'2': (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
'3': ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
'4': ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
'5': ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
'6': (" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "),
'7': ("#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "),
'8': (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
'9': (" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "),
' ': ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
'.': ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
',': ("     ", "     ", "     ", "     ", " ##  ", " ##  ", " #   "),
':': ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
';': ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", " #   "),
'!': ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
'?': (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
"'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
'"': (" # # ", " # # ", " # # ", "     ", "     ", "     ", "     "),
'-': ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
'\u2013': ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
'\u2014': ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
'(': ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
')': (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
'/': ("    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "),
'%': ("##  #", "## # ", "   # ", "  #  ", " #   ", "# ## ", "#  ##"),
'$': ("  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "),
'+': ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
'&': (" ##  ", "#  # ", "# #  ", " #   ", "# # #", "#  # ", " ## #"),
'@': (" ### ", "#   #", "# ###", "# # #", "# ###", "#    ", " ### "),
'#': (" # # ", " # # ", "#####", " # # ", "#####", " # # ", " # # "),
'*': ("     ", "#   #", " # # ", "  #  ", " # # ", "#   #", "     "),
'=': ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
'<': ("   # ", "  #  ", " #   ", "#    ", " #   ", "  #  ", "   # "),
'>': (" #   ", "  #  ", "   # ", "    #", "   # ", "  #  ", " #   "),
'_': ("     ", "     ", "     ", "     ", "     ", "     ", "#####"),
'\u2022': ("     ", "     ", " ##  ", " ##  ", " ##  ", "     ", "     "),
'x': ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
}

# ---------------------------------------------------------------- palette
BONE = (250, 247, 238)
INK = (22, 22, 26)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
NAVY = (16, 32, 64)
TEAL = (14, 90, 96)
GREEN = (46, 125, 50)
LGREEN = (118, 185, 0)
GOLD = (176, 141, 40)
GREY = (110, 110, 108)
LGREY = (210, 208, 198)
SKY = (186, 214, 232)
SEA = (52, 110, 158)
SAND = (232, 222, 196)
WHITE = (255, 255, 255)
ORANGE = (214, 106, 32)

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w=W, h=H, bg=BONE):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c, lw=1):
        for t in range(lw):
            self.fill_rect(x + t, y + t, w - 2 * t, 1, c)
            self.fill_rect(x + t, y + h - 1 - t, w - 2 * t, 1, c)
            self.fill_rect(x + t, y + t, 1, h - 2 * t, c)
            self.fill_rect(x + w - 1 - t, y + t, 1, h - 2 * t, c)

    def hline(self, x, y, w, c):
        self.fill_rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.fill_rect(x, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c, th=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for a in range(th):
                for b in range(th):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d <= r * r:
                        self.set(xx, yy, c)
                else:
                    if abs(d - r * r) <= r:
                        self.set(xx, yy, c)

    def poly(self, pts, c):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    if y1 != y0:
                        xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                    self.set(x, y, c)

    def vgrad(self, x, y, w, h, c1, c2):
        for yy in range(h):
            t = yy / max(1, h - 1)
            c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
            self.fill_rect(x, y + yy, w, 1, c)

    def speckle(self, x, y, w, h, density, dark, light, seed=7):
        s = seed
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                s = (s * 1103515245 + 12345) & 0x7FFFFFFF
                if s % 1000 < density * 10:
                    self.set(xx, yy, dark if (s >> 8) % 2 else light)

    # -- text -------------------------------------------------------------
    def text(self, s, x, y, scale=1, color=INK):
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                ch2 = ch.upper()
                g = FONT.get(ch2, FONT[' '])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '#':
                        self.fill_rect(cx + col * scale, y + r * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx - x

    def text_w(self, s, scale=1):
        return len(s) * 6 * scale - scale

    def wrap(self, s, x, y, w, scale=1, color=INK, leading=None):
        if leading is None:
            leading = 9 * scale
        words = s.split(' ')
        lines, cur = [], ''
        for wd in words:
            t = (cur + ' ' + wd).strip()
            if self.text_w(t, scale) <= w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        yy = y
        for ln in lines:
            self.text(ln, x, yy, scale, color)
            yy += leading
        return yy - y

    def centre(self, s, x, y, w, scale=1, color=INK):
        tw = self.text_w(s, scale)
        self.text(s, x + max(0, (w - tw) // 2), y, scale, color)


# ---------------------------------------------------------------- PNG out
def write_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(typ, data):
        c = struct.pack('>I', len(data)) + typ + data
        c += struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)
        return c

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
           + chunk(b'IDAT', comp) + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- scenes
def draw_chip_scene(cv, x, y, w, h):
    """NVIDIA hero: night fab skyline, rising chart, green chip."""
    cv.vgrad(x, y, w, h, (10, 24, 52), (16, 84, 92))
    # stars / circuit dots
    s = 11
    for yy in range(y + 6, y + h - 60, 14):
        for xx in range(x + 8, x + w - 8, 18):
            s = (s * 1103515245 + 12345) & 0x7FFFFFFF
            if s % 5 == 0:
                cv.set(xx, yy, (120, 180, 200))
    # skyline silhouette
    base = y + h - 58
    bx = x + 10
    while bx < x + w - 40:
        bw = 26 + (bx * 7) % 30
        bh = 30 + (bx * 13) % 50
        cv.fill_rect(bx, base - bh, bw, bh, (8, 18, 38))
        for wy in range(4):
            for wx in range(3):
                if (bx + wy * 3 + wx) % 2 == 0:
                    cv.fill_rect(bx + 4 + wx * 8, base - bh + 6 + wy * 12, 4, 6, (240, 200, 90))
        bx += bw + 6
    # rising chart line
    pts = [(x + 20, y + h - 30), (x + 150, y + h - 60), (x + 300, y + h - 50),
           (x + 470, y + h - 90), (x + 640, y + h - 75), (x + 820, y + h - 120),
           (x + w - 30, y + h - 140)]
    for a, b in zip(pts, pts[1:]):
        cv.line(a[0], a[1], b[0], b[1], LGREEN, 4)
    cv.poly([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 22, pts[-1][1] + 4),
             (pts[-1][0] - 8, pts[-1][1] + 16)], LGREEN)
    # chip
    cx, cy, cw, ch = x + w - 250, y + 20, 210, 130
    cv.fill_rect(cx - 6, cy - 6, cw + 12, ch + 12, (6, 14, 30))
    cv.fill_rect(cx, cy, cw, ch, (24, 64, 32))
    cv.rect(cx, cy, cw, ch, LGREEN, 3)
    for px in range(cx + 12, cx + cw - 8, 16):
        cv.fill_rect(px, cy - 12, 5, 12, LGREEN)
        cv.fill_rect(px, cy + ch, 5, 12, LGREEN)
    for py in range(cy + 12, cy + ch - 8, 16):
        cv.fill_rect(cx - 12, py, 12, 5, LGREEN)
        cv.fill_rect(cx + cw, py, 12, 5, LGREEN)
    cv.fill_rect(cx + 30, cy + 30, cw - 60, ch - 60, (10, 40, 20))
    cv.rect(cx + 30, cy + 30, cw - 60, ch - 60, LGREEN, 2)
    cv.text("NVDA", cx + 62, cy + 52, 3, LGREEN)
    cv.text("+31.5%", cx + 42, cy + 96, 2, WHITE)
    cv.speckle(x, y, w, h, 5, (200, 220, 230), (30, 60, 90), seed=21)


def draw_missile_scene(cv, x, y, w, h):
    """Poland hero: dusk sky, three missiles, NATO jet, radar, flag."""
    cv.vgrad(x, y, w, h, (64, 42, 60), (214, 130, 62))
    # sun
    cv.circle(x + w - 70, y + 34, 26, (244, 196, 90))
    cv.circle(x + w - 70, y + 34, 20, (250, 220, 130))
    # radar arcs
    for r in (18, 30, 42):
        cv.circle(x + 46, y + h - 44, r, (240, 240, 230), fill=False)
    cv.line(x + 46, y + h - 44, x + 80, y + h - 78, (240, 240, 230), 2)
    # missiles: body + flame + trail (kept inside the scene box)
    for mx, my, ang in ((x + 90, y + 4, 1), (x + 210, y + 8, 1), (x + 330, y + 2, 1)):
        cv.line(mx, my + 34, mx - 22, my + 62, (255, 255, 255), 3)
        cv.poly([(mx, my), (mx - 10, my + 26), (mx + 10, my + 26)], (240, 240, 240))
        cv.poly([(mx - 10, my + 26), (mx + 10, my + 26), (mx, my + 40)], RED)
        cv.poly([(mx - 22, my + 62), (mx - 15, my + 62), (mx - 18, my + 76)], ORANGE)
        cv.poly([(mx - 18, my + 76), (mx - 12, my + 76), (mx - 15, my + 88)], GOLD)
    # NATO jet silhouette
    jx, jy = x + w - 190, y + h - 68
    cv.poly([(jx, jy), (jx + 60, jy - 12), (jx + 96, jy - 2), (jx + 60, jy + 6),
             (jx + 20, jy + 10), (jx - 6, jy + 4)], (30, 30, 40))
    cv.poly([(jx + 30, jy - 8), (jx + 44, jy - 22), (jx + 52, jy - 6)], (30, 30, 40))
    # Polish skyline + flag
    base = y + h - 14
    cv.fill_rect(x, base, w, 14, (40, 40, 48))
    for bx in range(x + 14, x + w - 60, 54):
        bh = 22 + (bx * 11) % 26
        cv.fill_rect(bx, base - bh, 34, bh, (52, 52, 60))
    fx, fy = x + w - 66, y + h - 58
    cv.fill_rect(fx, fy, 44, 12, WHITE)
    cv.fill_rect(fx, fy + 12, 44, 12, RED)
    cv.vline(fx - 2, fy - 8, 34, INK)
    cv.speckle(x, y, w, h, 5, (255, 230, 200), (90, 60, 70), seed=33)


def draw_tanker_scene(cv, x, y, w, h):
    """Hormuz hero: sea, three tankers, mines, blast rings."""
    cv.vgrad(x, y, w, h, (120, 170, 205), (18, 58, 96))
    # sun glare
    cv.circle(x + 70, y + 30, 22, (250, 226, 150))
    # waves
    for wy in range(y + h - 70, y + h - 6, 12):
        for wx in range(x, x + w, 26):
            cv.line(wx, wy, wx + 14, wy + 4, (150, 195, 225), 2)
    # tankers (hulls and funnels kept inside the scene box)
    for tx, ty, tw in ((x + 24, y + h - 44, 150), (x + 200, y + h - 36, 130),
                       (x + 350, y + h - 48, 110)):
        cv.fill_rect(tx, ty, tw, 22, (40, 40, 46))
        cv.fill_rect(tx + 8, ty - 18, 22, 18, (200, 200, 205))
        cv.fill_rect(tx + tw - 40, ty - 12, 26, 12, (200, 200, 205))
        cv.fill_rect(tx, ty + 22, tw, 5, RED)
        cv.line(tx + tw + 6, ty + 12, tx + tw + 34, ty + 12, (220, 220, 220), 2)
    # mines: spiked circles
    for mx, my in ((x + 150, y + 40), (x + 300, y + 60), (x + 430, y + 34)):
        cv.circle(mx, my, 12, (30, 30, 36))
        for a in range(8):
            ang = a * math.pi / 4
            cv.line(mx, my, int(mx + 18 * math.cos(ang)), int(my + 18 * math.sin(ang)), (30, 30, 36), 2)
        cv.circle(mx, my, 4, RED)
    # blast rings
    for bx, by, br in ((x + 150, y + 40, 26), (x + 300, y + 60, 28), (x + 430, y + 34, 24)):
        cv.circle(bx, by, br, (255, 240, 180), fill=False)
        cv.circle(bx, by, br + 6, (255, 200, 120), fill=False)
    cv.speckle(x, y, w, h, 5, (200, 225, 240), (20, 50, 90), seed=47)


# ---------------------------------------------------------------- grid scenes
def _scene_band(cv, x, y, w, h, c1, c2):
    cv.vgrad(x, y, w, h, c1, c2)


def scene_tariff(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (70, 90, 130), (30, 44, 70))
    for i, col in enumerate((RED, GOLD, TEAL, (200, 200, 200))):
        cv.fill_rect(x + 12 + i * 34, y + h - 26, 28, 20, col)
        cv.rect(x + 12 + i * 34, y + h - 26, 28, 20, INK, 1)
    cv.text("%", x + w - 46, y + 4, 3, WHITE)


def scene_anthropic(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (40, 40, 52), (90, 30, 34))
    pts = [(x + 10, y + 10), (x + 60, y + 14), (x + 110, y + 26), (x + 160, y + 34)]
    for a, b in zip(pts, pts[1:]):
        cv.line(a[0], a[1], b[0], b[1], RED, 3)
    cv.text("$83", x + 10, y + h - 22, 2, WHITE)


def scene_huawei(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (30, 70, 60), (14, 40, 34))
    cv.fill_rect(x + 70, y + 4, 60, h - 8, (20, 20, 24))
    cv.rect(x + 70, y + 4, 60, h - 8, LGREY, 2)
    cv.fill_rect(x + 78, y + 10, 44, h - 22, (60, 140, 160))
    cv.circle(x + 100, y + h // 2, 9, GOLD)
    cv.fill_rect(x + 96, y + h // 2 - 2, 8, 4, INK)


def scene_gaza(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (150, 120, 90), (90, 70, 50))
    for i, bh in enumerate((26, 34, 22, 30)):
        cv.fill_rect(x + 12 + i * 30, y + h - 8 - bh, 24, bh, (50, 44, 40))
    cv.circle(x + w - 40, y + 14, 12, (250, 220, 150))
    cv.poly([(x + 30, y + 6), (x + 44, y + 22), (x + 16, y + 22)], (220, 220, 220))


def scene_climate(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (90, 140, 160), (30, 60, 80))
    cv.circle(x + w // 2, y + h // 2, 16, (60, 140, 90))
    cv.fill_rect(x + w // 2 - 16, y + h // 2 - 4, 32, 8, (40, 100, 160))
    cv.line(x + w // 2 - 10, y + h // 2 - 14, x + w // 2 + 4, y + h // 2 + 2, (20, 40, 60), 2)
    cv.line(x + w // 2 + 4, y + h // 2 + 2, x + w // 2 - 2, y + h // 2 + 14, (20, 40, 60), 2)


def scene_gta(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (200, 90, 120), (90, 30, 70))
    cv.fill_rect(x + 60, y + 10, 84, 24, (30, 30, 40))
    cv.rect(x + 60, y + 10, 84, 24, WHITE, 2)
    cv.circle(x + 76, y + 22, 4, WHITE)
    cv.circle(x + 128, y + 22, 4, WHITE)
    cv.text("VI", x + w - 52, y + 4, 3, WHITE)


def scene_india(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (220, 160, 80), (140, 90, 40))
    cv.fill_rect(x + 60, y + h - 18, 84, 12, (90, 50, 30))
    cv.fill_rect(x + 72, y + h - 30, 60, 12, (110, 60, 34))
    cv.circle(x + 102, y + h - 30, 12, (130, 70, 40))
    cv.fill_rect(x + 100, y + h - 44, 4, 6, GOLD)


def scene_nepal(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (140, 170, 210), (60, 90, 130))
    cv.poly([(x + 10, y + h - 6), (x + 60, y + 8), (x + 110, y + h - 6)], (230, 235, 240))
    cv.poly([(x + 70, y + h - 6), (x + 130, y + 2), (x + 190, y + h - 6)], (200, 210, 220))
    cv.poly([(x + 52, y + 16), (x + 68, y + 16), (x + 60, y + 8)], WHITE)
    cv.text("5.6", x + w - 44, y + 4, 2, INK)


def scene_iraq(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (180, 150, 110), (90, 70, 40))
    cv.line(x + 90, y + h - 6, x + 110, y + 6, INK, 3)
    cv.line(x + 110, y + 6, x + 130, y + h - 6, INK, 3)
    cv.line(x + 96, y + h - 6, x + 124, y + h - 6, INK, 3)
    cv.circle(x + 150, y + 16, 8, (30, 30, 34))
    cv.circle(x + 150, y + 16, 12, (30, 30, 34), fill=False)


def scene_iran(cv, x, y, w, h):
    _scene_band(cv, x, y, w, h, (120, 60, 90), (60, 25, 45))
    cv.fill_rect(x + 90, y + h - 8, 24, 8, (200, 200, 200))
    cv.line(x + 102, y + h - 8, x + 102, y + 12, (220, 220, 220), 3)
    cv.circle(x + 102, y + 10, 7, (220, 220, 220))
    cv.text("74", x + w - 46, y + 4, 3, WHITE)


GRID_SCENES = [scene_tariff, scene_anthropic, scene_huawei, scene_gaza,
               scene_climate, scene_gta, scene_india, scene_nepal,
               scene_iraq, scene_iran]


# ---------------------------------------------------------------- world map
NA = [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
      (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-97, 16),
      (-105, 20), (-115, 30), (-125, 40), (-125, 49), (-140, 60),
      (-155, 58), (-165, 60)]
SA = [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
      (-50, -30), (-60, -40), (-70, -50), (-73, -40), (-72, -20), (-78, -5)]
EU = [(-10, 36), (-10, 44), (0, 48), (5, 58), (10, 57), (20, 55), (28, 60),
      (30, 70), (40, 68), (45, 60), (40, 50), (30, 45), (20, 40), (10, 38),
      (0, 36), (-5, 38)]
AF = [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
      (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30),
      (20, -35), (15, -30), (12, -18), (8, -5), (8, 4), (-8, 4), (-13, 8)]
AS = [(40, 70), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
      (160, 70), (170, 66), (162, 60), (158, 52), (150, 45), (140, 40),
      (135, 35), (127, 35), (120, 30), (110, 20), (105, 10), (100, 8),
      (95, 15), (90, 22), (80, 15), (75, 8), (70, 20), (60, 25), (55, 28),
      (50, 30), (45, 30), (42, 40), (40, 50), (40, 60)]
AU = [(113, -22), (114, -30), (115, -35), (125, -33), (130, -32), (135, -35),
      (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (145, -15),
      (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)]
CONTINENTS = [NA, SA, EU, AF, AS, AU]


def draw_map(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (196, 216, 228))
    cv.vgrad(x, y, w, h, (200, 220, 232), (178, 202, 220))
    # graticule
    for gx in range(x + 60, x + w, 60):
        cv.vline(gx, y, h, (170, 195, 212))
    for gy in range(y + 18, y + h, 18):
        cv.hline(x, gy, w, (170, 195, 212))
    # ocean wave texture
    for wy in range(y + 10, y + h - 6, 16):
        for wx in range(x + 12, x + w - 12, 34):
            cv.line(wx, wy, wx + 12, wy + 3, (150, 185, 208), 1)

    def proj(lon, lat):
        px = x + (lon + 170) / 360.0 * w
        py = y + (75 - lat) / 130.0 * h
        return (int(px), int(py))

    for cont in CONTINENTS:
        cv.poly([proj(lo, la) for lo, la in cont], SAND)
        pts = [proj(lo, la) for lo, la in cont]
        for a, b in zip(pts, pts[1:] + pts[:1]):
            cv.line(a[0], a[1], b[0], b[1], (150, 138, 108), 1)
    # markers
    for lon, lat, label, big in (
            (-122, 37, "NVIDIA +31.5%", True),
            (19, 52, "POLAND", True),
            (56, 26, "HORMUZ", True),
            (34, 31, "", False),
            (78, 21, "", False),
            (-1, 52, "", False),
            (84, 28, "", False)):
        mx, my = proj(lon, lat)
        cv.circle(mx, my, 7 if big else 4, RED)
        cv.circle(mx, my, 3 if big else 2, WHITE)
        if label:
            lx = mx + 10
            if lx + len(label) * 6 > x + w - 4:
                lx = mx - 10 - len(label) * 6
            cv.text(label, lx, my - 4, 1, RED)
    cv.text("WORLD MAP - WHERE THE NEWS HAPPENED", x + 8, y + 4, 1, BLUE)

# ---------------------------------------------------------------- layout
GRID = [
    ("TRUMP'S NEW TARIFF WAVE",
     "New import tariffs after excess-capacity probe \u2022 25 Nov"),
    ("ANTHROPIC BELOW IPO PRICE",
     "Shares under $83 IPO price; ~$200B at risk \u2022 25 Nov"),
    ("HUAWEI GUILTY OF THEFT",
     "Guilty of stealing trade secrets; racketeering cleared \u2022 25 Nov"),
    ("GAZA CRISIS DEEPENS",
     "UN warns of deepening crisis; strike kills Hamas official \u2022 25 Nov"),
    ("CLIMATE TALKS COLLAPSE",
     "COP31 global climate talks end with no deal \u2022 25 Nov"),
    ("GTA 6: BIGGEST LAUNCH",
     "Out worldwide 19 Nov on PS5 and Xbox \u2022 19 Nov"),
    ("BJP AND SAD REUNITE",
     "Punjab 2027 pact after six years apart \u2022 25 Nov"),
    ("NEPAL PM IN INDIA",
     "First state visit to India; 5.6 quake in Koshi \u2022 25 Nov"),
    ("BAGHDAD TAKES KURD OIL",
     "Federal control of Kurd fields ordered; Kurds refuse \u2022 25 Nov"),
    ("SINGER FLOGGED 74 TIMES",
     "74 lashes for performing without hijab \u2022 25 Nov"),
]

RAIL = [
    "Giuliani gets Medal of Freedom \u2014 25 Nov",
    "Two held over break-in at William's home \u2014 25 Nov",
    "Denmark court upholds 'ghetto' evictions \u2014 25 Nov",
    "Israeli soldier suicides at 16-year high \u2014 25 Nov",
    "Saudi coalition condemns Riyadh attack \u2014 25 Nov",
    "Zimbabwean jailed over Ukraine war bid \u2014 25 Nov",
    "US consumer confidence data moves markets \u2014 25 Nov",
    "Sensex drops 1,484; Nifty under 25,400 \u2014 25 Nov",
    "England beat Australia in 2nd T20I \u2014 25 Nov",
    "Sooryavanshi: fastest List A double ton \u2014 25 Nov",
    "New Zealand hold India to draw, 1st Test \u2014 25 Nov",
    "Priyansh Arya 181, 2nd-highest T20 score \u2014 25 Nov",
    "Vera Rubin telescope's first images amaze \u2014 25 Nov",
    "Didymos/Dimorphos asteroid eclipse \u2014 25 Nov",
    "'Impossible' star system 28 ly away \u2014 25 Nov",
    "Great Barrier Reef: 12 corals revived \u2014 25 Nov",
    "Day to end violence against women \u2014 25 Nov",
    "12,000 evacuated from UK concert \u2014 25 Nov",
    "Modi-Merz talk India-Germany partnership \u2014 25 Nov",
    "India space economy heads to $40-45B \u2014 25 Nov",
    "US-Qatar discuss strategic cooperation \u2014 25 Nov",
]


def build():
    cv = Canvas()
    # paper grain over the whole sheet for visual richness
    cv.speckle(0, 0, W, H, 7, (238, 234, 222), (255, 252, 244), seed=5)

    # ---- masthead
    cv.text("THE WORLD", 16, 8, 5, INK)
    cv.text("Wednesday 25 November 2026", 660, 14, 2, INK)
    cv.text("34 stories, 9 regions", 16, 48, 2, RED)
    cv.text("Checked 25 November 2026", 700, 50, 1, BLUE)
    cv.fill_rect(0, 62, W, 3, RED)

    # ---- stat strip
    cv.centre("NVIDIA +31.5%   |   +$952B IN A DAY   |   3 MISSILES OVER POLAND   |   3 TANKERS MINED IN HORMUZ",
              0, 70, W, 1, INK)

    # ---- world map band
    draw_map(cv, 8, 84, W - 16, 112)
    cv.rect(8, 84, W - 16, 112, INK, 1)

    # ---- hero 1: NVIDIA
    hy = 196
    cv.fill_rect(8, hy, W - 16, 32, NAVY)
    cv.text("HUANG IS BACK AT NVIDIA", 20, hy + 6, 3, WHITE)
    cv.text("23 Nov", W - 110, hy + 10, 2, LGREEN)
    draw_chip_scene(cv, 8, hy + 32, W - 16, 160)
    cv.fill_rect(8, hy + 192, W - 16, 48, INK)
    cv.text("+$952B in a day, best since 2003", 20, hy + 200, 2, LGREEN)
    cv.text("Nasdaq +6.51%  S&P +4.73%  Dow +1,448", 20, hy + 220, 1, WHITE)

    # ---- heroes 2 & 3
    wy = 436
    for hx, title, date, scene in (
            (8, "MISSILES OVER POLAND", "25 Nov", draw_missile_scene),
            (516, "TANKERS MINED IN HORMUZ", "25 Nov", draw_tanker_scene)):
        cv.fill_rect(hx, wy, 500, 30, NAVY)
        cv.text(title, hx + 12, wy + 5, 2, WHITE)
        cv.text(date, hx + 500 - 84, wy + 9, 1, LGREEN)
        scene(cv, hx, wy + 30, 500, 96)
        cv.fill_rect(hx, wy + 126, 500, 34, INK)
        if "POLAND" in title:
            cv.text("NATO jets scrambled; Putin vows reply", hx + 12, wy + 136, 1, WHITE)
        else:
            cv.text("Iran's Guards: mines hit 3 tankers", hx + 12, wy + 136, 1, WHITE)

    # ---- grid 10
    gy = 596
    for i, (title, detail) in enumerate(GRID):
        col, row = i % 5, i // 5
        gx = 8 + col * 204
        gyy = gy + row * 120
        cv.rect(gx, gyy, 200, 116, INK, 1)
        GRID_SCENES[i](cv, gx + 1, gyy + 1, 198, 44)
        cv.text(str(i + 4), gx + 8, gyy + 52, 1, RED)
        used = cv.wrap(title, gx + 8, gyy + 52, 184, 2, INK, leading=15)
        cv.wrap(detail, gx + 8, gyy + 52 + used + 2, 184, 1, GREY, leading=9)

    # ---- rail 21
    ry = 836
    cv.fill_rect(0, ry - 4, W, 2, RED)
    for i, line in enumerate(RAIL):
        col, row = i % 3, i // 3
        rx = 8 + col * 341
        ryy = ry + row * 27
        cv.text("%d." % (i + 14), rx, ryy + 4, 1, RED)
        cv.text(line, rx + 26, ryy + 4, 1, INK)
        if row < 6:
            cv.hline(rx, ryy + 24, 325, LGREY)
    return cv


def main():
    import hashlib
    import os
    cv = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    n = write_png(cv, out)
    md5 = hashlib.md5(open(out, "rb").read()).hexdigest()
    print("entry.png %dx%d %d bytes md5 %s" % (W, H, n, md5))
    print("stories: 34 (3 heroes + 10 grid + 21 rail), drawn scenes: 13")


if __name__ == "__main__":
    main()
