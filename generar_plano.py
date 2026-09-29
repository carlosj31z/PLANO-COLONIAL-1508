#!/usr/bin/env python3
"""Plano referencial y ficha de inspección - Edificio A, Alto Lima Park Cercado.

Redibujo vectorial del plano anexo (V.02) sin medidas: los campos de cotas
quedan en blanco para llenarse durante la inspección.
Uso: python3 generar_plano.py  ->  PLANO_INSPECCION_DPTO_1508.pdf
"""
import math
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

OUT = "PLANO_INSPECCION_DPTO_1508.pdf"
W, H = landscape(A4)

INK = HexColor("#1f2933")
WALL = HexColor("#2b2f36")
MUTED = HexColor("#6b7280")
ACCENT = HexColor("#8a6d3b")
LINE = HexColor("#c9ced6")
F_DORM = HexColor("#efe4d2")
F_LIVING = HexColor("#f6efe3")
F_WET = HexColor("#dfe9ee")
F_SERV = HexColor("#e6e6e2")
F_BALC = HexColor("#d4d8dc")
FIX = HexColor("#ffffff")
FIXL = HexColor("#7a828c")

# --- transformación px (plano original) -> puntos PDF -----------------------
S = 0.262 * mm
OX, OY = 12 * mm, H - 33 * mm
PX0, PY0 = 110, 255


def X(px):
    return OX + (px - PX0) * S


def Y(py):
    return OY - (py - PY0) * S


T = 8  # espesor de muro (px)

c = canvas.Canvas(OUT, pagesize=(W, H))
c.setTitle("Plano referencial de inspección - Dpto. 1508, Edificio A")
c.setAuthor("Inspección")


def rect(x1, y1, x2, y2, fill, stroke=None, lw=0.4):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.rect(X(x1), Y(y2), (x2 - x1) * S, (y2 - y1) * S, fill=1, stroke=1 if stroke else 0)


def hwall(y, x1, x2):
    rect(x1 - T / 2, y - T / 2, x2 + T / 2, y + T / 2, WALL)


def vwall(x, y1, y2):
    rect(x - T / 2, y1 - T / 2, x + T / 2, y2 + T / 2, WALL)


def line(x1, y1, x2, y2, col=FIXL, lw=0.5, dash=None):
    c.setStrokeColor(col)
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    c.line(X(x1), Y(y1), X(x2), Y(y2))
    c.setDash()


def door(hx, hy, closed, opened, ln):
    """Puerta: bisagra, dirección cerrada, dirección abierta, largo (px)."""
    hxp, hyp = X(hx), Y(hy)
    r = ln * S
    a1 = math.degrees(math.atan2(-closed[1], closed[0]))
    a2 = math.degrees(math.atan2(-opened[1], opened[0]))
    ext = (a2 - a1 + 180) % 360 - 180
    c.setStrokeColor(FIXL)
    c.setLineWidth(0.45)
    c.setDash(1.2, 1.2)
    p = c.beginPath()
    p.arc(hxp - r, hyp - r, hxp + r, hyp + r, a1, ext)
    c.drawPath(p, stroke=1, fill=0)
    c.setDash()
    c.setStrokeColor(INK)
    c.setLineWidth(0.9)
    c.line(hxp, hyp, hxp + r * opened[0], hyp - r * opened[1])


def window_h(y, x1, x2):
    rect(x1, y - T / 2, x2, y + T / 2, white, INK, 0.5)
    line(x1, y, x2, y, INK, 0.4)


def window_v(x, y1, y2):
    rect(x - T / 2, y1, x + T / 2, y2, white, INK, 0.5)
    line(x, y1, x, y2, INK, 0.4)


def oval(cx, cy, rx, ry, fill=FIX):
    c.setFillColor(fill)
    c.setStrokeColor(FIXL)
    c.setLineWidth(0.45)
    c.ellipse(X(cx - rx), Y(cy + ry), X(cx + rx), Y(cy - ry), fill=1, stroke=1)


def box(x1, y1, x2, y2, fill=FIX, r=0):
    c.setFillColor(fill)
    c.setStrokeColor(FIXL)
    c.setLineWidth(0.45)
    if r:
        c.roundRect(X(x1), Y(y2), (x2 - x1) * S, (y2 - y1) * S, r * S, fill=1, stroke=1)
    else:
        c.rect(X(x1), Y(y2), (x2 - x1) * S, (y2 - y1) * S, fill=1, stroke=1)


def wc(cx, cy, facing):  # facing: 'u','d','l','r' (hacia donde mira)
    if facing in "ud":
        box(cx - 14, cy - 22 if facing == "u" else cy - 8, cx + 14, cy + 8 if facing == "u" else cy + 22, r=2)
        oval(cx, cy + (8 if facing == "u" else -8) * -1 if False else cy, 12, 16)
    else:
        oval(cx, cy, 16, 12)


def bed(x1, y1, x2, y2, head="u"):
    box(x1, y1, x2, y2, HexColor("#d9dde2"), r=3)
    if head == "u":
        pw = (x2 - x1) / 2 - 4
        box(x1 + 3, y1 + 3, x1 + 3 + pw, y1 + 22, white, r=3)
        box(x2 - 3 - pw, y1 + 3, x2 - 3, y1 + 22, white, r=3)
        line(x1, y1 + (y2 - y1) * 0.35, x2, y1 + (y2 - y1) * 0.35, FIXL, 0.4)
    else:
        ph = (y2 - y1) / 2 - 4
        box(x1 + 3, y1 + 3, x1 + 22, y1 + 3 + ph, white, r=3)
        box(x1 + 3, y2 - 3 - ph, x1 + 22, y2 - 3, white, r=3)
        line(x1 + (x2 - x1) * 0.35, y1, x1 + (x2 - x1) * 0.35, y2, FIXL, 0.4)


def label(px, py, num, name, size=5.6):
    cx, cy = X(px), Y(py)
    c.setFillColor(INK)
    c.circle(cx, cy + 3.4 * mm, 2.1 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(cx, cy + 3.4 * mm - 2.4, str(num))
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", size)
    for i, part in enumerate(name.split("\n")):
        c.drawCentredString(cx, cy - 0.2 * mm - i * (size + 1.2), part)


# =============================== PÁGINA 1 ===================================
# Cabecera
c.setFillColor(INK)
c.rect(0, H - 22 * mm, W, 22 * mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 15)
c.drawString(12 * mm, H - 11 * mm, "PLANO REFERENCIAL DE INSPECCIÓN")
c.setFont("Helvetica", 8.5)
c.drawString(12 * mm, H - 17 * mm,
             "Alto Lima Park Cercado  ·  Edificio A  ·  Departamento 1508  ·  Tipología 208 al 2008")
c.setFont("Helvetica-Bold", 8)
c.drawRightString(W - 12 * mm, H - 11 * mm, "LÁMINA 1 / 2")
c.setFont("Helvetica", 8)
c.drawRightString(W - 12 * mm, H - 17 * mm, "Distribución general")

# --- Pisos (zonas) ---
rect(205, 262, 385, 470, F_DORM)                # Dorm 2
rect(385, 262, 515, 470, F_DORM)                # Dorm 3
rect(118, 478, 315, 738, F_DORM)                # Dorm 1
rect(205, 470, 320, 540, F_LIVING)              # circulación
rect(320, 470, 515, 568, F_LIVING)              # pasillo
rect(515, 320, 703, 738, F_LIVING)              # sala / comedor
rect(517, 262, 700, 320, F_BALC)                # balcón
rect(318, 568, 412, 738, F_WET)                 # baño 1
rect(420, 568, 505, 738, F_WET)                 # baño 2
rect(703, 388, 820, 738, F_SERV)                # cocina + acceso
rect(820, 388, 950, 738, F_SERV)                # lav/depósito
rect(820, 640, 950, 738, F_WET)                 # baño 3
rect(118, 690, 315, 738, HexColor("#cfc6b6"))   # closet
rect(392, 680, 438, 738, white)                 # ducto / retranqueo

# grilla de piso muy tenue (sugerencia de acabado)
c.setStrokeColor(HexColor("#e2d6c2"))
c.setLineWidth(0.15)
for xx in range(210, 700, 22):
    c.line(X(xx), Y(738), X(xx), Y(262))

# --- Muros ---
hwall(262, 205, 515)
vwall(205, 262, 478)
vwall(385, 262, 470)
vwall(515, 262, 470)
hwall(470, 205, 325)
hwall(470, 445, 515)
hwall(262, 517, 700)
vwall(700, 262, 410)
line(525, 320, 692, 320, INK, 1.1)              # mampara balcón
line(525, 324, 692, 324, INK, 0.5)
vwall(703, 410, 660)
hwall(410, 700, 750)
vwall(750, 388, 410)
hwall(388, 750, 950)
vwall(950, 388, 738)
vwall(820, 460, 520)
vwall(820, 580, 738)
hwall(640, 820, 835)
hwall(640, 885, 950)
hwall(738, 118, 390)
hwall(738, 440, 755)
hwall(738, 815, 950)
vwall(390, 680, 738)
vwall(440, 680, 738)
hwall(680, 390, 440)
vwall(118, 478, 738)
hwall(478, 118, 205)
vwall(315, 540, 600)
vwall(315, 650, 738)
hwall(568, 318, 508)
vwall(415, 568, 738)
vwall(508, 568, 590)
vwall(508, 640, 738)
line(320, 690, 315, 690, INK)
hwall(690, 118, 315)                            # frente de closet

# --- Ventanas ---
window_h(262, 232, 360)
window_h(262, 412, 490)
window_v(205, 350, 440) if False else None
window_v(118, 520, 640)
window_h(388, 830, 940)
window_v(950, 420, 470)

# --- Puertas ---
door(378, 470, (0, 1), (0, -1), 53)
door(392, 470, (0, 1), (0, -1), 53)
door(315, 600, (0, 1), (-1, 0), 50)             # dorm1 -> baño 1 (bisagra al sur)
door(508, 590, (0, 1), (1, 0), 50)              # baño 2 -> comedor
door(820, 580, (0, -1), (1, 0), 56)             # cocina -> depósito
door(835, 640, (1, 0), (0, -1), 50)
c.setFillColor(F_LIVING)
c.rect(X(755), Y(738 + T / 2 + 1), 60 * S, T * S + 2, fill=1, stroke=0)
door(815, 738, (-1, 0), (0, -1), 60)            # ingreso principal
line(205, 470, 315, 470, LINE, 0.4, (1.2, 1.2))

# --- Mobiliario / sanitarios ---
bed(213, 272, 296, 385, "u")
bed(298, 272, 378, 385, "u")
bed(395, 272, 455, 385, "u")
box(213, 430, 300, 462, HexColor("#3a3f47"))
box(455, 430, 505, 462, HexColor("#3a3f47"))
bed(132, 520, 245, 652, "l")
box(122, 500, 140, 518, white, r=2)
box(122, 656, 140, 674, white, r=2)
# sala
box(548, 340, 695, 460, HexColor("#e7dfd2"), r=2)
box(575, 370, 625, 425, HexColor("#3a3f47"))
box(640, 350, 695, 390, HexColor("#cfc9be"), r=6)
box(640, 395, 695, 445, HexColor("#cfc9be"), r=6)
# comedor
box(548, 560, 630, 690, HexColor("#dcd3c3"), r=3)
for cy in (585, 625, 665):
    oval(540, cy, 9, 12)
    oval(638, cy, 9, 12)
# cocina
box(707, 420, 748, 655, HexColor("#b9bcc0"))
box(715, 430, 740, 455, white)                  # lavadero
for (a, b) in ((718, 510), (735, 510), (718, 528), (735, 528)):
    oval(a, b, 5, 5)
box(707, 590, 748, 655, HexColor("#8f959c"))    # refrigeradora
# lavandería
box(895, 395, 940, 440, white, r=2)
oval(917, 417, 14, 14)
box(830, 396, 880, 420, white)
# depósito
box(890, 500, 945, 632, HexColor("#dcdcd6"))
line(890, 500, 945, 632, FIXL, 0.35)
line(945, 500, 890, 632, FIXL, 0.35)
# baños
oval(350, 606, 14, 18); box(340, 585, 362, 600)
box(322, 700, 380, 733, white); line(322, 700, 380, 733, FIXL, 0.4)
box(330, 575, 372, 588)
oval(465, 606, 14, 18); box(455, 585, 477, 600)
box(425, 700, 500, 733, white); line(425, 700, 500, 733, FIXL, 0.4)
oval(858, 668, 14, 18); box(848, 647, 870, 662)
box(826, 700, 945, 733, white); line(826, 700, 945, 733, FIXL, 0.4)
# tocador
box(318, 542, 425, 566, HexColor("#3a3f47"))
# closet
for xx in (118, 187, 256):
    line(xx, 690, xx, 738, FIXL, 0.4)

# --- Etiquetas ---
label(295, 340, 2, "DORMITORIO 2") if False else None
label(295, 420, 2, "DORMITORIO 2")
label(450, 420, 3, "DORM. 3")
label(215, 682, 1, "DORMITORIO PRINCIPAL", 5)
label(614, 500, 6, "SALA")
label(590, 722, 7, "COMEDOR")
label(608, 290, 9, "BALCÓN")
label(365, 655, 4, "BAÑO 1", 4.8)
label(462, 655, 5, "BAÑO 2", 4.8)
label(785, 480, 8, "COCINA", 5.2)
label(880, 470, 10, "LAV.", 5.2)
label(866, 565, 11, "DEPÓSITO", 5.2)
label(905, 678, 12, "BAÑO 3", 5)
label(262, 505, 13, "", 4)
c.setFillColor(MUTED)
c.setFont("Helvetica", 5)
c.drawCentredString(X(216), Y(715), "CLOSET")
c.setFont("Helvetica-Bold", 5.5)
c.setFillColor(ACCENT)
c.drawString(X(760), Y(752), "INGRESO")
c.drawCentredString(X(370), Y(490), "CIRCULACIÓN")
line(820, 490, 950, 490, FIXL, 0.35, (1.5, 1.5))

# --- Panel lateral (leyenda) ---
lx = 236 * mm
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 8)
c.drawString(lx, H - 30 * mm, "AMBIENTES")
c.setStrokeColor(ACCENT)
c.setLineWidth(1)
c.line(lx, H - 31.5 * mm, W - 12 * mm, H - 31.5 * mm)
AMB = ["Dormitorio principal", "Dormitorio 2", "Dormitorio 3", "Baño 1 (principal)",
       "Baño 2 (común)", "Sala", "Comedor", "Cocina", "Balcón", "Lavandería",
       "Depósito", "Baño 3 (servicio)", "Circulación"]
yy = H - 37.5 * mm
for i, a in enumerate(AMB, 1):
    c.setFillColor(INK)
    c.circle(lx + 2 * mm, yy + 1 * mm, 1.7 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(lx + 2 * mm, yy + 1 * mm - 2, str(i))
    c.setFillColor(INK)
    c.setFont("Helvetica", 7.2)
    c.drawString(lx + 6 * mm, yy, a)
    yy -= 5.2 * mm

yy -= 2 * mm
c.setFont("Helvetica-Bold", 8)
c.drawString(lx, yy, "SIMBOLOGÍA")
c.setStrokeColor(ACCENT)
c.line(lx, yy - 1.5 * mm, W - 12 * mm, yy - 1.5 * mm)
yy -= 7 * mm
c.setFillColor(WALL)
c.rect(lx, yy, 8 * mm, 1.6 * mm, fill=1, stroke=0)
c.setFillColor(INK)
c.setFont("Helvetica", 7)
c.drawString(lx + 11 * mm, yy, "Muro / tabique")
yy -= 5 * mm
c.setFillColor(white)
c.setStrokeColor(INK)
c.setLineWidth(0.5)
c.rect(lx, yy, 8 * mm, 1.6 * mm, fill=1, stroke=1)
c.setFillColor(INK)
c.drawString(lx + 11 * mm, yy, "Ventana")
yy -= 5 * mm
c.setStrokeColor(FIXL)
c.setDash(1.2, 1.2)
c.arc(lx, yy - 3 * mm, lx + 7 * mm, yy + 4 * mm, 0, 90)
c.setDash()
c.setFillColor(INK)
c.drawString(lx + 11 * mm, yy, "Puerta y giro")

# Nota
ny = 46 * mm
c.setFillColor(HexColor("#f4efe6"))
c.setStrokeColor(ACCENT)
c.setLineWidth(0.6)
c.rect(lx, ny - 2 * mm, W - 12 * mm - lx, 26 * mm, fill=1, stroke=1)
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 6.6)
c.drawString(lx + 2 * mm, ny + 20 * mm, "NOTAS")
c.setFont("Helvetica", 6)
notas = ["1. Sin escala. Sin medidas: las cotas",
         "   se registran en la lámina 2.",
         "2. Redibujado a partir del Anexo de",
         "   Planos V.02 (referencial).",
         "3. Puertas y ventanas por confirmar",
         "   en campo."]
for i, t in enumerate(notas):
    c.drawString(lx + 2 * mm, ny + 16 * mm - i * 3 * mm, t)

# Norte
nx, ny2 = W - 22 * mm, 60 * mm

# Cuadro de datos (pie)
by = 8 * mm
bh = 30 * mm
c.setStrokeColor(INK)
c.setLineWidth(0.8)
c.rect(12 * mm, by, W - 24 * mm, bh, fill=0, stroke=1)
cols = [12, 92, 162, 232, 285]
for xx in cols[1:-1]:
    c.line(xx * mm, by, xx * mm, by + bh)
c.line(12 * mm, by + bh - 9 * mm, (W - 12 * mm), by + bh - 9 * mm)
hdr = ["PROYECTO", "UBICACIÓN", "DATOS DEL DEPARTAMENTO", "INSPECCIÓN"]
val = [
    ["Alto Lima Park Cercado", "Edificio A – Dpto. 1508", "Promotora: Imagina"],
    ["Av. Benavides / Jr. Treneman", "Cercado de Lima", "Etapas II, III, IV y V"],
    ["3 dormitorios · 2 baños + baño de servicio", "Cocina · Lavandería · Depósito · Balcón",
     "Área techada: 72.82 m² aprox. (según anexo)"],
    ["Fecha: ____ / ____ / ________", "Inspector: ______________________", "Firma: __________________"],
]
for k in range(4):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString((cols[k] + 3) * mm, by + bh - 6 * mm, hdr[k])
    c.setFillColor(INK)
    c.setFont("Helvetica", 7.2)
    for j, t in enumerate(val[k]):
        c.drawString((cols[k] + 3) * mm, by + bh - 14.5 * mm - j * 5.3 * mm, t)

c.showPage()

# =============================== PÁGINA 2 ===================================
c.setFillColor(INK)
c.rect(0, H - 22 * mm, W, 22 * mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 15)
c.drawString(12 * mm, H - 11 * mm, "FICHA DE MEDIDAS Y ESTADO POR AMBIENTE")
c.setFont("Helvetica", 8.5)
c.drawString(12 * mm, H - 17 * mm,
             "Edificio A  ·  Departamento 1508  ·  Completar durante la inspección (medidas en metros)")
c.setFont("Helvetica-Bold", 8)
c.drawRightString(W - 12 * mm, H - 11 * mm, "LÁMINA 2 / 2")

heads = ["N°", "AMBIENTE", "LARGO (m)", "ANCHO (m)", "ALTO (m)", "ÁREA (m²)",
         "PISO", "MUROS/TECHO", "PUERTA/VENT.", "INSTAL.", "OBSERVACIONES"]
widths = [8, 41, 19, 19, 17, 19, 15, 21, 21, 15, 62]
tx, ty = 12 * mm, H - 28 * mm
rh = 10.3 * mm
c.setFillColor(ACCENT)
c.rect(tx, ty - 8 * mm, sum(widths) * mm, 8 * mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 6.2)
xx = tx
for h_, w_ in zip(heads, widths):
    c.drawCentredString(xx + w_ * mm / 2, ty - 5 * mm, h_)
    xx += w_ * mm
y0 = ty - 8 * mm
for i in range(len(AMB) + 1):
    yb = y0 - (i + 1) * rh
    if i % 2 == 0:
        c.setFillColor(HexColor("#f7f4ee"))
        c.rect(tx, yb, sum(widths) * mm, rh, fill=1, stroke=0)
    if i < len(AMB):
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(tx + widths[0] * mm / 2, yb + rh / 2 - 2, str(i + 1))
        c.setFont("Helvetica", 7.4)
        c.drawString(tx + (widths[0] + 2) * mm, yb + rh / 2 - 2, AMB[i])
    else:
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7.4)
        c.drawString(tx + (widths[0] + 2) * mm, yb + rh / 2 - 2, "TOTAL / OBSERVACIÓN GENERAL")
# líneas
c.setStrokeColor(LINE)
c.setLineWidth(0.5)
tot_h = (len(AMB) + 1) * rh
for i in range(len(AMB) + 2):
    c.line(tx, y0 - i * rh, tx + sum(widths) * mm, y0 - i * rh)
xx = tx
for w_ in widths + [0]:
    c.line(xx, y0, xx, y0 - tot_h)
    xx += w_ * mm
# casillas B / R / M en columnas de estado
c.setFont("Helvetica", 5.4)
c.setFillColor(MUTED)
state_cols = [6, 7, 8, 9]
sx = tx + sum(widths[:6]) * mm
for i in range(len(AMB)):
    yb = y0 - (i + 1) * rh
    xcur = sx
    for k in range(6, 10):
        wcol = widths[k] * mm
        opts = ["B", "R", "M"]
        for j, o in enumerate(opts):
            cx_ = xcur + wcol * (j + 0.5) / 3
            c.setStrokeColor(LINE)
            c.circle(cx_, yb + rh / 2 + 0.5 * mm, 1.5 * mm, fill=0, stroke=1)
            c.drawCentredString(cx_, yb + 1.6 * mm, o)
        xcur += wcol

py_ = y0 - tot_h - 6 * mm
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 7)
c.drawString(tx, py_, "Estado:  B = Bueno   ·   R = Regular   ·   M = Malo (marcar con un círculo)")
c.setFont("Helvetica", 6.8)
c.setFillColor(MUTED)
c.drawString(tx, py_ - 4.5 * mm,
             "Área de cada ambiente = largo × ancho. Contrastar el total con el área techada del anexo (72.82 m² aprox.). "
             "Registrar fotografías con el número del ambiente.")
c.setStrokeColor(INK)
c.setLineWidth(0.6)
c.setFillColor(INK)
c.setFont("Helvetica", 7)
sy = 16 * mm
c.line(tx + 10 * mm, sy, tx + 80 * mm, sy)
c.drawCentredString(tx + 45 * mm, sy - 4 * mm, "Inspector")
c.line(tx + 110 * mm, sy, tx + 180 * mm, sy)
c.drawCentredString(tx + 145 * mm, sy - 4 * mm, "Conformidad / Fecha")
c.showPage()
c.save()
print("OK ->", OUT)
