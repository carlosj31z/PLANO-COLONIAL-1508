#!/usr/bin/env python3
"""Plano de distribución A3 con vista 3D - Alto Lima Park, Edificio A, Dpto. 1508.

Redibujo del plano anexo (V.02). Coordenadas en unidades de dibujo (px del
plano original), sin medidas reales.
Uso: python3 generar_plano.py  ->  PLANO_DPTO_1508_A3.pdf
"""
import heapq
import math
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas

OUT = "PLANO_DPTO_1508_A3.pdf"
PW, PH = landscape(A3)

INK = HexColor("#1f2933")
MUTED = HexColor("#6b7280")
ACCENT = HexColor("#8a6d3b")

T = 8        # espesor de muro
WALL_H = 46  # altura de corte de muros en la vista 3D
SLAB = 16    # espesor de losa

# --------------------------------------------------------------------------
# Geometría (x hacia la derecha, y hacia abajo en planta; +x = NORTE)
# --------------------------------------------------------------------------
boxes = []      # sólidos de la vista 3D
walls2d = []    # rectángulos de muro para la planta
wins2d = []     # ventanas / mamparas para la planta


def box(x1, y1, x2, y2, z0, z1, top, side=None, glass=False, kind="obj"):
    boxes.append(dict(x1=x1, y1=y1, x2=x2, y2=y2, z0=z0, z1=z1, top=HexColor(top),
                      side=HexColor(side or top), glass=glass, kind=kind))


WALL_TOP, WALL_SIDE = "#2d3138", "#f1eee9"


def wall(orient, pos, a, b, wins=()):
    """Muro con vanos: wins = [(a, b, tipo)] tipo 'v' ventana, 'p' baranda."""
    h = T / 2
    start = a - h
    pieces = []
    for (wa, wb, _t) in sorted(wins):
        pieces.append((start, wa))
        start = wb
    pieces.append((start, b + h))

    def rect(p1, p2):
        return (p1, pos - h, p2, pos + h) if orient == "h" else (pos - h, p1, pos + h, p2)

    for p1, p2 in pieces:
        if p2 - p1 > 0.5:
            r = rect(p1, p2)
            box(*r, 0, WALL_H, WALL_TOP, WALL_SIDE, kind="wall")
            walls2d.append(r)
    for (wa, wb, t) in wins:
        sill = 26 if t == "v" else 22
        box(*rect(wa, wb), 0, sill, WALL_TOP, WALL_SIDE, kind="wall")
        g = (wa, pos - 1.2, wb, pos + 1.2) if orient == "h" else (pos - 1.2, wa, pos + 1.2, wb)
        box(*g, sill, WALL_H if t == "v" else 44, "#a9cfe0", glass=True)
        wins2d.append((orient, pos, wa, wb))


# Muros
wall("h", 262, 205, 515, wins=[(232, 360, "v"), (412, 490, "v")])
wall("v", 205, 262, 474)
wall("v", 385, 262, 474)
wall("v", 515, 262, 474)
wall("h", 474, 118, 325)
wall("h", 474, 445, 515)
wall("h", 262, 519, 702, wins=[(519, 698, "p")])        # baranda del balcón
wall("v", 702, 262, 410)
wall("v", 702, 410, 660)
wall("h", 410, 702, 750)
wall("v", 750, 388, 410)
wall("h", 388, 750, 950, wins=[(830, 940, "v")])
wall("v", 950, 388, 738, wins=[(420, 470, "v")])
wall("v", 820, 388, 520)
wall("v", 820, 580, 738)
wall("h", 640, 820, 835)
wall("h", 640, 885, 950)
wall("h", 738, 118, 390)
wall("h", 738, 440, 755)
wall("h", 738, 815, 950)
wall("v", 390, 680, 738)
wall("v", 440, 680, 738)
wall("h", 680, 390, 440)
wall("v", 118, 474, 738, wins=[(520, 640, "v")])
wall("v", 315, 540, 600)
wall("v", 315, 650, 738)
wall("h", 568, 318, 508)
wall("v", 415, 568, 680)
wall("v", 508, 568, 590)
wall("v", 508, 640, 738)
# Mampara corrediza sala-balcón
box(519, 318.6, 698, 321.4, 0, WALL_H, "#a9cfe0", glass=True)
box(519, 317, 523, 323, 0, WALL_H, "#5b6169", kind="wall")
box(694, 317, 698, 323, 0, WALL_H, "#5b6169", kind="wall")
wins2d.append(("h", 320, 519, 698))

# Hojas de puerta (abiertas a 90°)
for r in [(375, 422, 379, 470), (392, 422, 396, 470), (266, 536, 311, 540),
          (319, 646, 362, 650), (463, 636, 504, 640), (824, 576, 870, 580),
          (881, 644, 885, 688), (811, 684, 815, 734)]:
    box(*r, 0, 44, "#cdb893", "#e4d3b7", kind="door")

# Dormitorio 2
for x1, x2 in ((213, 294), (300, 378)):
    box(x1, 266, x2, 272, 0, 44, "#6f757c", "#8b9197")
    box(x1, 272, x2, 385, 0, 20, "#e9ebee", "#c3c8ce")
    box(x1 + 4, 275, x2 - 4, 293, 20, 26, "#ffffff", "#e3e5e8")
    box(x1, 318, x2, 385, 20, 23, "#8b9a82", "#76856d")
box(213, 440, 300, 468, 0, 32, "#4a4f57", "#5f656d")
# Dormitorio 3
box(395, 266, 457, 272, 0, 44, "#6f757c", "#8b9197")
box(395, 272, 457, 385, 0, 20, "#e9ebee", "#c3c8ce")
box(399, 275, 453, 293, 20, 26, "#ffffff", "#e3e5e8")
box(395, 318, 457, 385, 20, 23, "#8b9a82", "#76856d")
box(462, 440, 509, 468, 0, 32, "#4a4f57", "#5f656d")
# Dormitorio principal
box(124, 515, 131, 657, 0, 46, "#6f757c", "#8b9197")
box(131, 515, 245, 657, 0, 21, "#e9ebee", "#c3c8ce")
box(134, 520, 156, 584, 21, 27, "#ffffff", "#e3e5e8")
box(134, 588, 156, 652, 21, 27, "#ffffff", "#e3e5e8")
box(195, 515, 245, 657, 21, 24, "#5d636b", "#4b5057")
box(123, 494, 141, 512, 0, 24, "#b89a6e", "#a0845b")
box(123, 660, 141, 678, 0, 24, "#b89a6e", "#a0845b")
box(122, 690, 312, 734, 0, WALL_H, "#9c8565", "#c9b594")      # clóset
# Circulación: escritorio
box(320, 544, 412, 564, 0, 30, "#4a4f57", "#5f656d")
# Sala
box(519, 352, 531, 438, 0, 22, "#4a4f57", "#5f656d")
box(520, 366, 524, 424, 22, 44, "#1f2328", "#30353b")
box(578, 375, 622, 425, 0, 14, "#3a3f47", "#4b5057")
box(648, 345, 696, 452, 0, 17, "#d7d1c6", "#c4bdb0")
box(686, 345, 696, 452, 17, 36, "#cfc8bb", "#bab2a3")
box(648, 345, 686, 355, 17, 28, "#cfc8bb", "#bab2a3")
box(648, 442, 686, 452, 17, 28, "#cfc8bb", "#bab2a3")
box(672, 270, 694, 292, 0, 16, "#9a8f80", "#877c6d")
box(675, 273, 691, 289, 16, 40, "#6f9a62", "#5c8551")
box(655, 488, 677, 510, 0, 14, "#9a8f80", "#877c6d")
box(658, 491, 674, 507, 14, 42, "#6f9a62", "#5c8551")
# Comedor
box(560, 580, 620, 690, 0, 32, "#c9b08a", "#b39a73")
for cy in (590, 627, 664):
    box(542, cy, 556, cy + 16, 0, 19, "#e3e0da", "#cfcbc3")
    box(539, cy, 543, cy + 16, 0, 38, "#e3e0da", "#cfcbc3")
    box(624, cy, 638, cy + 16, 0, 19, "#e3e0da", "#cfcbc3")
    box(637, cy, 641, cy + 16, 0, 38, "#e3e0da", "#cfcbc3")
# Cocina
box(706, 420, 748, 590, 0, 38, "#c9cdd1", "#eeeeec")
box(714, 432, 740, 456, 38, 39, "#9ea4aa")
box(712, 498, 742, 540, 38, 39, "#26292d")
box(706, 596, 748, 656, 0, WALL_H, "#b7bcc1", "#d4d8dc")
# Lavandería / depósito
box(894, 394, 944, 440, 0, 38, "#ffffff", "#e6e8ea")
box(828, 394, 878, 420, 0, 34, "#f4f4f2", "#dcdcd8")
box(890, 500, 944, 632, 0, WALL_H - 4, "#c8b999", "#e0d4bb")
# Baños
for (tx, vx) in ((372, 322), (440, 474)):
    box(tx, 572, tx + 22, 581, 0, 30, "#ffffff", "#e3e6e9")
    box(tx + 2, 581, tx + 20, 604, 0, 17, "#ffffff", "#e3e6e9")
    box(vx, 572, vx + 30, 596, 0, 30, "#ffffff", "#e3e6e9")
box(320, 694, 386, 734, 0, 2, "#eef2f4")
box(320, 692.5, 386, 694.5, 2, WALL_H, "#a9cfe0", glass=True)
box(444, 694, 504, 734, 0, 2, "#eef2f4")
box(444, 692.5, 504, 694.5, 2, WALL_H, "#a9cfe0", glass=True)
box(846, 725, 870, 734, 0, 30, "#ffffff", "#e3e6e9")
box(848, 702, 868, 725, 0, 17, "#ffffff", "#e3e6e9")
box(914, 704, 944, 734, 0, 30, "#ffffff", "#e3e6e9")
# Ducto
box(394, 684, 436, 734, 0, WALL_H, "#9aa0a6", "#c2c6cb", kind="wall")

# Pisos: (rect, tipo)
FLOORS = [
    ((118, 474, 315, 738), "wood"), ((205, 262, 385, 474), "wood"), ((385, 262, 515, 474), "wood"),
    ((315, 474, 515, 568), "wood"), ((508, 320, 702, 738), "wood"),
    ((315, 568, 415, 738), "wet"), ((415, 568, 508, 738), "wet"),
    ((702, 388, 820, 738), "tile"), ((820, 388, 950, 640), "tile"), ((820, 640, 950, 738), "wet"),
    ((515, 262, 702, 320), "balc"), ((390, 680, 440, 738), "duct"),
]
FLOOR_COL = {"wood": ("#dcc098", "#c9aa7c", 11), "wet": ("#e2e9ed", "#c8d2d8", 26),
             "tile": ("#ebe7df", "#d6d0c4", 28), "balc": ("#cfd3d6", "#b8bdc2", 22),
             "duct": ("#b5bac0", "#b5bac0", 0)}
FOOT = [(114, 470), (201, 470), (201, 258), (706, 258), (706, 406), (746, 406),
        (746, 384), (954, 384), (954, 742), (114, 742)]

# (n°, nombre, etiqueta 3D, etiqueta planta)
ROOMS = [
    (1, "Dormitorio principal", (190, 610), (190, 600)),
    (2, "Dormitorio 2", (295, 420), (295, 420)),
    (3, "Dormitorio 3", (450, 415), (450, 420)),
    (4, "Baño 1", (362, 640), (365, 640)),
    (5, "Baño 2", (470, 655), (462, 650)),
    (6, "Sala", (600, 470), (600, 470)),
    (7, "Comedor", (590, 715), (590, 715)),
    (8, "Cocina", (770, 520), (775, 520)),
    (9, "Balcón", (600, 292), (608, 292)),
    (10, "Lavandería", (870, 460), (870, 455)),
    (11, "Depósito", (860, 560), (860, 560)),
    (12, "Baño 3", (905, 675), (905, 690)),
]

# --------------------------------------------------------------------------
# Proyección axonométrica
# --------------------------------------------------------------------------
ANG = math.radians(24)
CA, SA = math.cos(ANG), math.sin(ANG)
K = 0.9


def raw(x, y, z):
    return (x * CA - y * SA, -((x * SA + y * CA) * K - z))


def depth(x, y):
    return x * SA + y * CA


pts = [raw(b[k1], b[k2], b[k3]) for b in boxes for k1 in ("x1", "x2")
       for k2 in ("y1", "y2") for k3 in ("z0", "z1")]
pts += [raw(x, y, -SLAB) for x, y in FOOT]
minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
AREA = (14 * mm, 30 * mm, 292 * mm, 262 * mm)   # x0, y0, x1, y1
SC = min((AREA[2] - AREA[0]) / (maxx - minx), (AREA[3] - AREA[1]) / (maxy - miny))
OX = AREA[0] + ((AREA[2] - AREA[0]) - (maxx - minx) * SC) / 2 - minx * SC
OY = AREA[1] + ((AREA[3] - AREA[1]) - (maxy - miny) * SC) / 2 - miny * SC


def P(x, y, z=0):
    u, v = raw(x, y, z)
    return OX + u * SC, OY + v * SC


c = canvas.Canvas(OUT, pagesize=(PW, PH))
c.setTitle("Plano de distribución - Dpto. 1508, Edificio A - Alto Lima Park")


def poly(points, fill=None, stroke=None, lw=0.3, alpha=None):
    p = c.beginPath()
    p.moveTo(*points[0])
    for q in points[1:]:
        p.lineTo(*q)
    p.close()
    c.saveState()
    if alpha is not None:
        c.setFillAlpha(alpha)
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.drawPath(p, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
    c.restoreState()


def shade(col, f):
    return Color(col.red * f, col.green * f, col.blue * f)


def inside(px, py, pg):
    ins = False
    for i in range(len(pg)):
        (x1, y1), (x2, y2) = pg[i], pg[i - 1]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
            ins = not ins
    return ins


# ---------- Losa ----------
SLAB_SIDE = HexColor("#8d949b")
edges = []
for i in range(len(FOOT)):
    (x1, y1), (x2, y2) = FOOT[i], FOOT[(i + 1) % len(FOOT)]
    nx, ny = y2 - y1, -(x2 - x1)
    ln = math.hypot(nx, ny)
    nx, ny = nx / ln, ny / ln
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if inside(mx + nx * 2, my + ny * 2, FOOT):
        nx, ny = -nx, -ny
    if nx * SA + ny * CA > 0:
        edges.append((depth(mx, my), (x1, y1, x2, y2), shade(SLAB_SIDE, 0.85 if abs(nx) > 0.5 else 1)))
for _, (x1, y1, x2, y2), col in sorted(edges):
    poly([P(x1, y1, 0), P(x2, y2, 0), P(x2, y2, -SLAB), P(x1, y1, -SLAB)], col, shade(col, 0.8))
poly([P(x, y, 0) for x, y in FOOT], HexColor("#e2ded6"), HexColor("#7d838a"), 0.4)

# ---------- Pisos ----------
for (x1, y1, x2, y2), kind in FLOORS:
    base, ln_col, step = FLOOR_COL[kind]
    quad = [P(x1, y1), P(x2, y1), P(x2, y2), P(x1, y2)]
    poly(quad, HexColor(base))
    if not step:
        continue
    c.saveState()
    p = c.beginPath()
    p.moveTo(*quad[0])
    for q in quad[1:]:
        p.lineTo(*q)
    p.close()
    c.clipPath(p, stroke=0, fill=0)
    c.setStrokeColor(HexColor(ln_col))
    c.setLineWidth(0.25)
    if kind == "wood":
        yy, row = y1, 0
        while yy < y2:
            c.line(*P(x1, yy), *P(x2, yy))
            xx = x1 + (row * 37) % 90
            while xx < x2:
                c.line(*P(xx, yy), *P(xx, min(yy + step, y2)))
                xx += 90
            yy += step
            row += 1
    else:
        xx = x1
        while xx < x2:
            c.line(*P(xx, y1), *P(xx, y2))
            xx += step
        yy = y1
        while yy < y2:
            c.line(*P(x1, yy), *P(x2, yy))
            yy += step
    c.restoreState()
# alfombra sala
poly([P(548, 340, .5), P(640, 340, .5), P(640, 462, .5), P(548, 462, .5)],
     HexColor("#efe9df"), HexColor("#d8cfc0"), 0.3)


def north_arrow(pt, R, cx, cy):
    """Flecha norte hacia +x, dibujada con la transformación pt(x, y)."""
    circ = [pt(cx + R * math.cos(t * math.pi / 24), cy + R * math.sin(t * math.pi / 24)) for t in range(48)]
    poly(circ, None, INK, 0.6)
    tip = pt(cx + R * 0.95, cy)
    mid = pt(cx - R * 0.15, cy)
    poly([tip, pt(cx - R * 0.45, cy - R * 0.36), mid], INK)
    poly([tip, mid, pt(cx - R * 0.45, cy + R * 0.36)], white, INK, 0.5)
    lab = pt(cx + R * 1.4, cy)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(lab[0], lab[1] - 4, "N")


# Norte sobre el terreno (vista 3D)
north_arrow(P, 36, 150, 360)

# ---------- Sólidos: orden de pintor ----------
for b in boxes:
    corners = [P(b[a], b[bb], b[z]) for a in ("x1", "x2") for bb in ("y1", "y2") for z in ("z0", "z1")]
    b["bb"] = (min(q[0] for q in corners), min(q[1] for q in corners),
               max(q[0] for q in corners), max(q[1] for q in corners))
    b["d"] = depth((b["x1"] + b["x2"]) / 2, (b["y1"] + b["y2"]) / 2)

E = 0.01


def first(a, b):
    """True si a va antes que b; False si después; None si no importa."""
    ab, bb_ = a["bb"], b["bb"]
    if ab[2] <= bb_[0] or bb_[2] <= ab[0] or ab[3] <= bb_[1] or bb_[3] <= ab[1]:
        return None
    ax = a["x2"] <= b["x1"] + E
    bx = b["x2"] <= a["x1"] + E
    ay = a["y2"] <= b["y1"] + E
    by = b["y2"] <= a["y1"] + E
    if (ax or ay) and not (bx or by):
        return True
    if (bx or by) and not (ax or ay):
        return False
    if ax or bx or ay or by:
        return a["d"] < b["d"]
    if a["z0"] != b["z0"]:
        return a["z0"] < b["z0"]
    if a["z1"] != b["z1"]:
        return a["z1"] < b["z1"]
    return None


n = len(boxes)
succ = [[] for _ in range(n)]
indeg = [0] * n
for i in range(n):
    for j in range(i + 1, n):
        r = first(boxes[i], boxes[j])
        if r is True:
            succ[i].append(j)
            indeg[j] += 1
        elif r is False:
            succ[j].append(i)
            indeg[i] += 1
heap = [(boxes[i]["d"], i) for i in range(n) if indeg[i] == 0]
heapq.heapify(heap)
order, done = [], [False] * n
while len(order) < n:
    if not heap:   # ciclo: se rompe por profundidad
        k = min((boxes[i]["d"], i) for i in range(n) if not done[i])[1]
        heap.append((boxes[k]["d"], k))
    _, i = heapq.heappop(heap)
    if done[i]:
        continue
    done[i] = True
    order.append(i)
    for j in succ[i]:
        indeg[j] -= 1
        if indeg[j] == 0 and not done[j]:
            heapq.heappush(heap, (boxes[j]["d"], j))

for i in order:
    b = boxes[i]
    x1, y1, x2, y2, z0, z1 = b["x1"], b["y1"], b["x2"], b["y2"], b["z0"], b["z1"]
    side = [P(x2, y1, z0), P(x2, y2, z0), P(x2, y2, z1), P(x2, y1, z1)]
    front = [P(x1, y2, z0), P(x2, y2, z0), P(x2, y2, z1), P(x1, y2, z1)]
    top = [P(x1, y1, z1), P(x2, y1, z1), P(x2, y2, z1), P(x1, y2, z1)]
    if b["glass"]:
        for f in (side, front, top):
            poly(f, b["top"], HexColor("#6f95a8"), 0.25, alpha=0.25)
        continue
    edge = shade(b["side"], 0.72) if b["kind"] != "wall" else HexColor("#8a8f96")
    poly(side, shade(b["side"], 0.82), edge, 0.25)
    poly(front, b["side"], edge, 0.25)
    poly(top, b["top"], shade(b["top"], 0.8) if b["kind"] == "wall" else edge, 0.25)

# hornillas
for (hx, hy) in ((720, 508), (734, 508), (720, 528), (734, 528)):
    ring = [P(hx + 4.5 * math.cos(t * math.pi / 8), hy + 4.5 * math.sin(t * math.pi / 8), 39.2) for t in range(16)]
    poly(ring, None, HexColor("#8a8f96"), 0.4)

# ---------- Etiquetas 3D ----------
for num, name, (lx, ly), _ in ROOMS:
    px, py = P(lx, ly, 0)
    w = c.stringWidth(name.upper(), "Helvetica-Bold", 7) + 7 * mm
    c.saveState()
    c.setFillColor(white)
    c.setFillAlpha(0.9)
    c.setStrokeColor(HexColor("#b9b2a5"))
    c.setLineWidth(0.4)
    c.roundRect(px - w / 2, py - 2.6 * mm, w, 5.2 * mm, 2.6 * mm, fill=1, stroke=1)
    c.restoreState()
    c.setFillColor(INK)
    c.circle(px - w / 2 + 2.6 * mm, py, 1.9 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(px - w / 2 + 2.6 * mm, py - 2.1, str(num))
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(px - w / 2 + 5.4 * mm, py - 2.4, name.upper())

# ---------- Marco ----------
c.setStrokeColor(INK)
c.setLineWidth(1.2)
c.rect(8 * mm, 8 * mm, PW - 16 * mm, PH - 16 * mm)
c.setLineWidth(0.5)
c.rect(10 * mm, 10 * mm, PW - 20 * mm, PH - 20 * mm)
RX = 300 * mm
c.setLineWidth(0.8)
c.line(RX, 10 * mm, RX, PH - 10 * mm)

c.setFillColor(INK)
c.setFont("Helvetica-Bold", 13)
c.drawString(16 * mm, PH - 19 * mm, "VISTA 3D — DISTRIBUCIÓN DEL DEPARTAMENTO")
c.setFont("Helvetica", 8.5)
c.setFillColor(MUTED)
c.drawString(16 * mm, PH - 24.5 * mm, "Vista axonométrica con corte horizontal de muros  ·  Sin escala")
c.setStrokeColor(ACCENT)
c.setLineWidth(1.2)
c.line(16 * mm, PH - 27 * mm, 120 * mm, PH - 27 * mm)

# --------------------------------------------------------------------------
# Columna derecha
# --------------------------------------------------------------------------
CX0, CX1 = RX + 5 * mm, PW - 15 * mm
CW = CX1 - CX0

c.setFillColor(INK)
c.rect(RX, PH - 36 * mm, PW - 10 * mm - RX, 26 * mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 17)
c.drawString(CX0, PH - 21 * mm, "ALTO LIMA PARK")
c.setFillColor(HexColor("#c9b27f"))
c.setFont("Helvetica", 9.5)
c.drawString(CX0, PH - 27.5 * mm, "C E R C A D O   D E   L I M A")
c.setFillColor(white)
c.setFont("Helvetica", 8)
c.drawString(CX0, PH - 32.5 * mm, "Edificio A  ·  Departamento 1508")


def section(y, title):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(CX0, y, title)
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.9)
    c.line(CX0, y - 2 * mm, CX1, y - 2 * mm)


# Planta 2D
section(PH - 44 * mm, "PLANTA DE DISTRIBUCIÓN")
s2 = CW / (954 - 114) * 0.98
ox2 = CX0 + (CW - (954 - 114) * s2) / 2 - 114 * s2
oy2 = PH - 50 * mm + 258 * s2


def Q(x, y):
    return ox2 + x * s2, oy2 - y * s2


def qrect(x1, y1, x2, y2, stroke=0):
    c.rect(Q(x1, y2)[0], Q(x1, y2)[1], (x2 - x1) * s2, (y2 - y1) * s2, fill=1, stroke=stroke)


for (x1, y1, x2, y2), kind in FLOORS:
    c.setFillColor(HexColor(FLOOR_COL[kind][0]))
    qrect(x1, y1, x2, y2)
c.setFillColor(HexColor("#2b2f36"))
for r in walls2d:
    qrect(*r)
c.setFillColor(HexColor("#9aa0a6"))
qrect(394, 684, 436, 734)
c.setStrokeColor(INK)
c.setLineWidth(0.35)
for (o, pos, a, b) in wins2d:
    c.setFillColor(white)
    if o == "h":
        qrect(a, pos - 4, b, pos + 4, 1)
        c.line(*Q(a, pos), *Q(b, pos))
    else:
        qrect(pos - 4, a, pos + 4, b, 1)
        c.line(*Q(pos, a), *Q(pos, b))
# giros de puerta
c.setStrokeColor(MUTED)
c.setLineWidth(0.3)
c.setDash(1, 1)
for (hx, hy, a0, ext, r) in [(378, 474, 90, 90, 50), (392, 474, 90, -90, 50), (315, 540, 180, 90, 48),
                             (315, 650, 0, -90, 46), (508, 640, 180, -90, 45), (820, 580, 0, -90, 50),
                             (885, 640, 270, -90, 46), (815, 738, 90, 90, 56)]:
    cx_, cy_ = Q(hx, hy)
    rr = r * s2
    p = c.beginPath()
    p.arc(cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr, a0, ext)
    c.drawPath(p, stroke=1, fill=0)
c.setDash()
for num, name, _, (lx, ly) in ROOMS:
    px, py = Q(lx, ly)
    c.setFillColor(INK)
    c.circle(px, py, 1.7 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 5.6)
    c.drawCentredString(px, py - 2, str(num))
ix, iy = Q(785, 738)
c.setFillColor(ACCENT)
c.setFont("Helvetica-Bold", 5.5)
c.drawCentredString(ix, iy - 3.4 * mm, "INGRESO")

# Norte de la planta
plan_bottom = Q(0, 742)[1]
north_arrow(lambda x, y: (x, y), 6.5 * mm, CX1 - 12 * mm, plan_bottom - 11 * mm)

# Leyenda
ly0 = plan_bottom - 26 * mm
section(ly0, "AMBIENTES")
yy = ly0 - 7.5 * mm
colw = CW / 2
for k, (num, name, _, _) in enumerate(ROOMS):
    col, row = divmod(k, 6)
    x = CX0 + col * colw
    y = yy - row * 5.4 * mm
    c.setFillColor(INK)
    c.circle(x + 2 * mm, y + 1 * mm, 1.8 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(x + 2 * mm, y + 1 * mm - 2.1, str(num))
    c.setFillColor(INK)
    c.setFont("Helvetica", 7.8)
    c.drawString(x + 6 * mm, y, name)

# Datos
dy0 = yy - 6 * 5.4 * mm - 4 * mm
section(dy0, "DATOS DEL DEPARTAMENTO")
datos = [("Tipología", "Dptos. 208 al 2008 (Edificio A)"),
         ("Dormitorios", "3"),
         ("Baños", "2 + baño de servicio"),
         ("Servicios", "Cocina · Lavandería · Depósito"),
         ("Exterior", "Balcón"),
         ("Área techada", "72.82 m² aprox.")]
yy = dy0 - 7.5 * mm
for k, v in datos:
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.6)
    c.drawString(CX0, yy, k)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(CX0 + 26 * mm, yy, v)
    yy -= 5 * mm

# Rótulo
by0, bh = 10 * mm, 34 * mm
RW = PW - 10 * mm
c.setStrokeColor(INK)
c.setLineWidth(0.8)
c.line(RX, by0 + bh, RW, by0 + bh)
c.line(RX, by0 + bh - 13 * mm, RW, by0 + bh - 13 * mm)
c.line(RX, by0 + 9 * mm, RW, by0 + 9 * mm)
m1, m2 = RX + (RW - RX) / 3, RX + 2 * (RW - RX) / 3
c.line(m1, by0, m1, by0 + 9 * mm)
c.line(m2, by0, m2, by0 + 9 * mm)
for (y, lab, val) in ((by0 + bh - 4.5 * mm, "PROYECTO", "Alto Lima Park – Cercado de Lima"),
                      (by0 + bh - 17.5 * mm, "PLANO", "Distribución – Planta y vista 3D")):
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.2)
    c.drawString(CX0, y, lab)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(CX0, y - 5 * mm, val)
for (x, lab, val) in ((RX, "LÁMINA", "A-01"), (m1, "ESCALA", "S/E"), (m2, "FECHA", "09 / 2026")):
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6)
    c.drawString(x + 3 * mm, by0 + 5.6 * mm, lab)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 3 * mm, by0 + 1.8 * mm, val)

# Simbología
sy0 = yy - 4 * mm
section(sy0, "SIMBOLOGÍA")
yy = sy0 - 8 * mm
c.setFillColor(HexColor("#2b2f36"))
c.rect(CX0, yy, 9 * mm, 1.8 * mm, fill=1, stroke=0)
c.setFillColor(white)
c.setStrokeColor(INK)
c.setLineWidth(0.4)
c.rect(CX0 + colw, yy, 9 * mm, 1.8 * mm, fill=1, stroke=1)
c.line(CX0 + colw, yy + 0.9 * mm, CX0 + colw + 9 * mm, yy + 0.9 * mm)
c.setFillColor(INK)
c.setFont("Helvetica", 7.6)
c.drawString(CX0 + 12 * mm, yy, "Muro / tabique")
c.drawString(CX0 + colw + 12 * mm, yy, "Ventana / mampara")
yy -= 7 * mm
c.setStrokeColor(MUTED)
c.setDash(1, 1)
p = c.beginPath()
p.arc(CX0 - 6 * mm, yy - 6 * mm, CX0 + 6 * mm, yy + 6 * mm, 0, 90)
c.drawPath(p, stroke=1, fill=0)
c.setDash()
c.setStrokeColor(INK)
c.line(CX0, yy, CX0, yy + 6 * mm)
c.drawString(CX0 + 12 * mm, yy, "Puerta y sentido de giro")

c.setFillColor(MUTED)
c.setFont("Helvetica-Oblique", 6.3)
c.drawString(16 * mm, 13 * mm, "Plano referencial. Distribución basada en el anexo de planos del proyecto (V.02).")

c.showPage()
c.save()
print("OK ->", OUT)
