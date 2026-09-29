#!/usr/bin/env python3
"""Plano de distribución A3 con vista 3D - Alto Lima Park, Edificio A, Dpto. 1508.

Usa la geometría de modelo.py (redibujo del Anexo de Planos V.02).
Unidades de dibujo: centímetros. Sin escala impresa (el anexo no trae cotas).
Uso: python3 generar_plano.py  ->  PLANO_DPTO_1508_A3.pdf
"""
import heapq
import math
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas

import modelo

OUT = "PLANO_DPTO_1508_A3.pdf"
PW, PH = landscape(A3)
M = modelo.build()

INK = HexColor("#1f2933")
MUTED = HexColor("#6b7280")
ACCENT = HexColor("#8a6d3b")

CUT = 95     # altura de corte horizontal de la vista 3D (cm)
SLAB = 22    # espesor de losa (cm)


def cm(v):
    return v * 100


# --------------------------------------------------------------------------
# Sólidos de la vista 3D (x hacia la derecha = NORTE, y hacia abajo)
# --------------------------------------------------------------------------
boxes = []


def box(x1, y1, x2, y2, z0, z1, top, side=None, glass=False, kind="obj"):
    z1 = min(z1, CUT)
    if z1 <= z0:
        return
    boxes.append(dict(x1=x1, y1=y1, x2=x2, y2=y2, z0=z0, z1=z1, top=HexColor(top),
                      side=HexColor(side or top), glass=glass, kind=kind))


GLASS = "#a9cfe0"
WALL_TOP, WALL_SIDE = "#2d3138", "#f1eee9"

for w in M["muros"]:
    x1, y1, x2, y2 = map(cm, w["r"])
    box(x1, y1, x2, y2, cm(w["z"][0]), cm(w["z"][1]), WALL_TOP, WALL_SIDE, kind="wall")

for v in M["ventanas"]:
    x1, y1, x2, y2 = map(cm, v["r"])
    z0, z1 = cm(v["z"][0]), cm(v["z"][1])
    if v["o"] == "h":
        c_ = (y1 + y2) / 2
        g = (x1, c_ - 1, x2, c_ + 1)
    else:
        c_ = (x1 + x2) / 2
        g = (c_ - 1, y1, c_ + 1, y2)
    if v["tipo"] == "baranda":
        box(x1, y1, x2, y2, 0, 15, WALL_TOP, WALL_SIDE, kind="wall")
        box(*g, 15, 100, GLASS, glass=True)
    else:
        box(*g, z0, z1, GLASS, glass=True)
    if v["tipo"] == "mampara":
        for xx in (x1, (x1 + x2) / 2 - 2, x2 - 4):
            box(xx, g[1] - 1, xx + 4, g[3] + 1, 0, z1, "#5b6169", kind="wall")

for d in M["puertas"]:
    hx, hy = cm(d["hinge"][0]), cm(d["hinge"][1])
    ox, oy = d["abierta"]
    L = cm(d["ancho"]) - 4
    ex, ey = hx + ox * L, hy + oy * L
    # desplaza la hoja 2 cm fuera del eje del muro y le da 4 cm de espesor
    cx, cy = d["cerrada"]
    hx, hy, ex, ey = hx + cx * 3, hy + cy * 3, ex + cx * 3, ey + cy * 3
    x1, x2 = sorted((hx - 2 if ox == 0 else hx, ex + 2 if ox == 0 else ex))
    y1, y2 = sorted((hy - 2 if oy == 0 else hy, ey + 2 if oy == 0 else ey))
    col = ("#b58f63", "#8a6a45") if d["tipo"] == "principal" else ("#e9e4da", "#d4cdbf")
    box(x1, y1, x2, y2, 0, 205, col[1], col[0], kind="door")

for r in M["ductos"]:
    box(*map(cm, r), 0, 240, "#9aa0a6", "#c2c6cb", kind="wall")

for s in M["duchas"]:
    x1, y1, x2, y2 = map(cm, s["r"])
    box(x1, y1, x2, y2, 0, 3, "#f4f6f7", "#dde3e7")
    o, at = s["vidrio"]
    at = cm(at)
    if o == "h":
        box(x1, at - 1, x2, at + 1, 3, 200, GLASS, glass=True)
    else:
        box(at - 1, y1, at + 1, y2, 3, 200, GLASS, glass=True)


# ---------------------------------------------------------------- muebles
def fparts(t, w, d, it):
    """Piezas (x1, y1, x2, y2, z0, z1, top, side) en cm, locales, frente hacia +y."""
    W, D = w / 2, d / 2
    P = []
    if t in ("cama_1p", "cama_2p"):
        P += [(-W, -D, W, -D + 6, 0, 100, "#6f757c", "#8b9197"),
              (-W, -D + 6, W, D, 0, 45, "#e9ebee", "#c3c8ce")]
        if t == "cama_1p":
            P.append((-W + 8, -D + 12, W - 8, -D + 45, 45, 56, "#ffffff", "#e3e5e8"))
            P.append((-W, -D + 60, W, D, 45, 51, "#8b9a82", "#76856d"))
        else:
            P.append((-W + 8, -D + 12, -3, -D + 48, 45, 57, "#ffffff", "#e3e5e8"))
            P.append((3, -D + 12, W - 8, -D + 48, 45, 57, "#ffffff", "#e3e5e8"))
            P.append((-W, -D + 62, W, D, 45, 51, "#5d636b", "#4b5057"))
    elif t == "velador":
        P.append((-W, -D, W, D, 0, 55, "#b89a6e", "#a0845b"))
    elif t in ("ropero", "closet", "estante"):
        col = {"ropero": ("#e8e2d6", "#d4ccbd"), "closet": ("#c9b594", "#b39d78"),
               "estante": ("#c8b999", "#b0a07e")}[t]
        P.append((-W, -D, W, D, 0, 240, *col))
    elif t in ("sofa", "sillon"):
        P += [(-W, -D, W, D, 0, 42, "#d7d1c6", "#c4bdb0"),
              (-W, -D, W, -D + 20, 42, 82, "#cfc8bb", "#bab2a3"),
              (-W, -D + 20, -W + 16, D, 42, 62, "#cfc8bb", "#bab2a3"),
              (W - 16, -D + 20, W, D, 42, 62, "#cfc8bb", "#bab2a3")]
    elif t == "mesa_centro":
        P.append((-W, -D, W, D, 0, 40, "#3a3f47", "#4b5057"))
    elif t == "alfombra":
        P.append((-W, -D, W, D, 0, 1, "#efe9df", "#d8cfc0"))
    elif t == "lampara_pie":
        P += [(-15, -15, 15, 15, 0, 3, "#2b2d30", "#2b2d30"), (-2, -2, 2, 2, 3, 150, "#2b2d30", "#2b2d30")]
    elif t == "planta":
        P += [(-14, -14, 14, 14, 0, 35, "#9a8f80", "#877c6d"), (-12, -12, 12, 12, 35, 110, "#6f9a62", "#5c8551")]
    elif t == "mesa_comedor":
        for sx in (-1, 1):
            for sy in (-1, 1):
                P.append((sx * W - (4 if sx > 0 else -4) - 2, sy * D - (4 if sy > 0 else -4) - 2,
                          sx * W - (4 if sx > 0 else -4) + 2, sy * D - (4 if sy > 0 else -4) + 2, 0, 72,
                          "#8a7050", "#8a7050"))
        P.append((-W, -D, W, D, 72, 76, "#c9b08a", "#b39a73"))
    elif t == "silla":
        P += [(-W, -D, W, D, 0, 46, "#e3e0da", "#cfcbc3"), (-W, -D, W, -D + 5, 46, 90, "#e3e0da", "#cfcbc3")]
    elif t == "cocina_lineal":
        P += [(-W, -D, W, D, 0, 86, "#f2f2f0", "#e2e2de"), (-W, -D, W, D, 86, 90, "#77797c", "#5d5f62"),
              (-W, -D, W, -D + 35, 150, 220, "#f2f2f0", "#e2e2de")]
    elif t == "refrigeradora":
        P.append((-W, -D, W, D, 0, 175, "#b7bcc1", "#d4d8dc"))
    elif t in ("lavadero", "lavadora"):
        P.append((-W, -D, W, D, 0, 88, "#ffffff", "#e6e8ea"))
    elif t == "terma":
        P.append((-W, -D, W, D, 130, 205, "#ffffff", "#e6e8ea"))
    elif t == "inodoro":
        P += [(-19, -D, 19, -D + 18, 0, 78, "#ffffff", "#e3e6e9"), (-17, -D + 18, 17, D, 0, 42, "#ffffff", "#e3e6e9")]
    elif t == "lavatorio":
        P.append((-W, -D, W, D, 0, 85, "#ffffff", "#e3e6e9"))
    else:
        P.append((-W, -D, W, D, 0, 75, "#b89a6e", "#a0845b"))
    return P


DEF = {"cama_1p": (95, 195), "cama_2p": (155, 200), "velador": (45, 40), "ropero": (140, 56),
       "closet": (260, 60), "sofa": (190, 88), "sillon": (78, 80), "mesa_centro": (90, 50),
       "alfombra": (210, 210), "planta": (40, 40), "mesa_comedor": (90, 140), "silla": (45, 50),
       "cocina_lineal": (295, 60), "refrigeradora": (70, 70), "lavadero": (55, 50), "lavadora": (60, 62),
       "terma": (45, 30), "estante": (120, 40), "inodoro": (38, 70), "lavatorio": (48, 42)}

for it in M["muebles"]:
    t = it["tipo"]
    w0, d0 = DEF.get(t, (60, 60))
    w = cm(it["w"]) if "w" in it else w0
    cx, cy = cm(it["x"]), cm(it["y"])
    a = math.radians(it["rot"])
    ca, sa = round(math.cos(a)), round(math.sin(a))
    for (lx1, ly1, lx2, ly2, z0, z1, top, side) in fparts(t, w, d0, it):
        pts = [(lx * ca + ly * sa, -lx * sa + ly * ca) for lx, ly in ((lx1, ly1), (lx2, ly2))]
        box(cx + min(p[0] for p in pts), cy + min(p[1] for p in pts),
            cx + max(p[0] for p in pts), cy + max(p[1] for p in pts), z0, z1, top, side)

FLOOR_COL = {"laminado": ("#dcc098", "#c9aa7c", 15), "ceramico_bano": ("#e2e9ed", "#c8d2d8", 30),
             "ceramico": ("#ebe7df", "#d6d0c4", 45), "ceramico_ext": ("#cfd3d6", "#b8bdc2", 40)}
FLOORS = [([cm(v) for v in r], a["piso"]) for a in M["ambientes"] for r in a["rects"]]
FOOT = [(cm(x), cm(y)) for x, y in M["contorno"]]
ROOMS = [(i + 1, a["nombre"], (cm(a["etiqueta"][0]), cm(a["etiqueta"][1]))) for i, a in enumerate(M["ambientes"])]

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
AREA = (14 * mm, 22 * mm, 292 * mm, 262 * mm)
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
    c.saveState()
    p = c.beginPath()
    p.moveTo(*quad[0])
    for q in quad[1:]:
        p.lineTo(*q)
    p.close()
    c.clipPath(p, stroke=0, fill=0)
    c.setStrokeColor(HexColor(ln_col))
    c.setLineWidth(0.25)
    if kind == "laminado":
        yy, row = y1, 0
        while yy < y2:
            c.line(*P(x1, yy), *P(x2, yy))
            xx = x1 + (row * 47) % 120
            while xx < x2:
                c.line(*P(xx, yy), *P(xx, min(yy + step, y2)))
                xx += 120
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


# Norte sobre el terreno (vista 3D), en el hueco junto al dormitorio 2
north_arrow(P, 48, 30, 110)

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
            poly(f, b["top"], HexColor("#6f95a8"), 0.25, alpha=0.14)
        continue
    edge = shade(b["side"], 0.72) if b["kind"] != "wall" else HexColor("#8a8f96")
    poly(side, shade(b["side"], 0.82), edge, 0.25)
    poly(front, b["side"], edge, 0.25)
    poly(top, b["top"], shade(b["top"], 0.8) if b["kind"] == "wall" else edge, 0.25)

# ---------- Etiquetas 3D ----------
for num, name, (lx, ly) in ROOMS:
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
c.drawString(16 * mm, PH - 24.5 * mm, "Vista axonométrica con corte horizontal a 0.95 m  ·  Sin escala")
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
fx = [p[0] for p in FOOT]
fy = [p[1] for p in FOOT]
PX0, PX1, PY0 = min(fx), max(fx), min(fy)
s2 = CW / (PX1 - PX0) * 0.98
ox2 = CX0 + (CW - (PX1 - PX0) * s2) / 2 - PX0 * s2
oy2 = PH - 50 * mm + PY0 * s2


def Q(x, y):
    return ox2 + x * s2, oy2 - y * s2


def qrect(x1, y1, x2, y2, stroke=0):
    c.rect(Q(x1, y2)[0], Q(x1, y2)[1], (x2 - x1) * s2, (y2 - y1) * s2, fill=1, stroke=stroke)


for (x1, y1, x2, y2), kind in FLOORS:
    c.setFillColor(HexColor(FLOOR_COL[kind][0]))
    qrect(x1, y1, x2, y2)
c.setFillColor(HexColor("#2b2f36"))
for w in M["muros"]:
    if w["z"][0] == 0 and w["z"][1] >= 2.0:
        qrect(*map(cm, w["r"]))
c.setFillColor(HexColor("#9aa0a6"))
for r in M["ductos"]:
    qrect(*map(cm, r))
c.setStrokeColor(INK)
c.setLineWidth(0.35)
for v in M["ventanas"]:
    x1, y1, x2, y2 = map(cm, v["r"])
    c.setFillColor(white)
    qrect(x1, y1, x2, y2, 1)
    if v["o"] == "h":
        c.line(*Q(x1, (y1 + y2) / 2), *Q(x2, (y1 + y2) / 2))
    else:
        c.line(*Q((x1 + x2) / 2, y1), *Q((x1 + x2) / 2, y2))
# duchas
c.setLineWidth(0.3)
for s in M["duchas"]:
    x1, y1, x2, y2 = map(cm, s["r"])
    c.setFillColor(HexColor("#f4f6f7"))
    qrect(x1, y1, x2, y2, 1)
    c.line(*Q(x1, y1), *Q(x2, y2))
    c.line(*Q(x1, y2), *Q(x2, y1))
# puertas: hoja y giro
for d in M["puertas"]:
    hx, hy = cm(d["hinge"][0]), cm(d["hinge"][1])
    L = cm(d["ancho"])
    cx_, cy_ = d["cerrada"]
    ox, oy = d["abierta"]
    a1 = math.degrees(math.atan2(-cy_, cx_))
    a2 = math.degrees(math.atan2(-oy, ox))
    ext = (a2 - a1 + 180) % 360 - 180
    qx, qy = Q(hx, hy)
    rr = L * s2
    c.setStrokeColor(MUTED)
    c.setLineWidth(0.3)
    c.setDash(1, 1)
    p = c.beginPath()
    p.arc(qx - rr, qy - rr, qx + rr, qy + rr, a1, ext)
    c.drawPath(p, stroke=1, fill=0)
    c.setDash()
    c.setStrokeColor(INK)
    c.setLineWidth(0.7)
    c.line(qx, qy, *Q(hx + ox * L, hy + oy * L))
for num, name, (lx, ly) in ROOMS:
    px, py = Q(lx, ly)
    c.setFillColor(INK)
    c.circle(px, py, 1.7 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 5.6)
    c.drawCentredString(px, py - 2, str(num))
ing = next(d for d in M["puertas"] if d["tipo"] == "principal")
ix, iy = Q(cm(ing["r"][0] + ing["r"][2]) / 2, cm(ing["r"][3]))
c.setFillColor(ACCENT)
c.setFont("Helvetica-Bold", 5.5)
c.drawCentredString(ix, iy - 3.4 * mm, "INGRESO")

plan_bottom = Q(0, max(fy))[1]
north_arrow(lambda x, y: (x, y), 6.5 * mm, CX1 - 12 * mm, plan_bottom - 11 * mm)

# Leyenda
ly0 = plan_bottom - 26 * mm
section(ly0, "AMBIENTES")
yy = ly0 - 7.5 * mm
colw = CW / 2
half = (len(ROOMS) + 1) // 2
for k, (num, name, _) in enumerate(ROOMS):
    col, row = divmod(k, half)
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
dy0 = yy - half * 5.4 * mm - 4 * mm
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
c.setFillColor(HexColor("#f4f6f7"))
c.setStrokeColor(INK)
c.rect(CX0 + colw, yy - 0.5 * mm, 9 * mm, 4 * mm, fill=1, stroke=1)
c.line(CX0 + colw, yy - 0.5 * mm, CX0 + colw + 9 * mm, yy + 3.5 * mm)
c.line(CX0 + colw, yy + 3.5 * mm, CX0 + colw + 9 * mm, yy - 0.5 * mm)
c.setFillColor(INK)
c.drawString(CX0 + colw + 12 * mm, yy, "Ducha")

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

c.setFillColor(MUTED)
c.setFont("Helvetica-Oblique", 6.3)
c.drawString(16 * mm, 13 * mm, "Plano referencial. Distribución basada en el anexo de planos del proyecto (V.02).")

c.showPage()
c.save()
print("OK ->", OUT)
