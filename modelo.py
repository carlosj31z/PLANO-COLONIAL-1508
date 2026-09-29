#!/usr/bin/env python3
"""Modelo geométrico del Dpto. 1508 (Edificio A, Alto Lima Park).

Las coordenadas se tomaron del Anexo de Planos V.02 escaneado (px de la
imagen a 300 dpi) y se convierten a metros con una escala deducida del área
techada (72.82 m² aprox.). Son aproximadas: el anexo no trae cotas.

Ejes en planta: x hacia la derecha (NORTE), y hacia abajo (ESTE);
el balcón queda al OESTE (y mínimo).
Uso: python3 modelo.py  ->  planta.json
"""
import json

S = 0.0113          # m por px del escaneo
OX, OY = 50, 62     # esquina de referencia (px)
H = 2.40            # altura de piso a techo
DOOR_H = 2.10


def m(v):
    return round(v * S, 3)


def X(px):
    return round((px - OX) * S, 3)


def Y(py):
    return round((py - OY) * S, 3)


# ---------------------------------------------------------------- muros (px)
# (orientación, eje, desde, hasta, espesor, vanos[(desde, hasta, tipo)])
WALLS = [
    ("h", 69, 157, 555, 14, [(232, 320, "ventana"), (400, 482, "ventana")]),
    ("h", 69, 555, 799, 10, [(555, 793, "baranda")]),
    ("v", 163, 62, 347, 13, []),
    ("h", 347, 50, 312, 13, []),
    ("v", 388, 62, 353, 12, []),
    ("h", 347, 462, 549, 10, []),
    ("v", 549, 62, 347, 12, []),
    ("h", 133, 555, 787, 8, [(555, 787, "mampara")]),
    ("v", 793, 62, 562, 13, []),
    ("h", 225, 793, 1100, 13, [(850, 935, "ventana_cocina"), (1010, 1090, "ventana_cocina")]),
    ("v", 1100, 225, 614, 13, [(410, 490, "ventana_alta")]),
    ("h", 614, 1100, 1156, 8, []),
    ("v", 1156, 614, 662, 8, []),
    ("h", 662, 931, 1156, 10, []),
    ("h", 664, 50, 859, 14, []),
    ("v", 57, 347, 664, 14, [(400, 560, "ventana")]),
    ("v", 938, 312, 662, 13, []),
    ("h", 562, 793, 866, 12, []),
    ("h", 356, 1006, 1100, 8, []),
    ("h", 536, 1004, 1100, 9, []),
    ("v", 307, 419, 526, 13, []),
    ("v", 306, 581, 664, 10, []),
    ("h", 459, 312, 482, 9, []),
    ("v", 430, 459, 584, 8, []),
    ("v", 549, 459, 664, 12, []),
]

# Ventanas: (antepecho, dintel)
WIN = {
    "ventana": (0.95, DOOR_H),
    "ventana_cocina": (1.05, DOOR_H),
    "ventana_alta": (1.60, DOOR_H),
    "mampara": (0.0, DOOR_H),
    "baranda": (0.0, 1.0),
}

# Puertas: (orientación, eje, desde, hasta, espesor, bisagra 'a'|'b', lado ±1, tipo, nombre)
DOORS = [
    ("v", 307, 354, 419, 13, "a", -1, "interior", "Dormitorio principal"),
    ("v", 307, 526, 581, 13, "b", +1, "interior", "Baño 1"),
    ("h", 459, 482, 543, 9, "b", +1, "interior", "Baño 2"),
    ("h", 347, 312, 382, 12, "b", -1, "interior", "Dormitorio 2"),
    ("h", 347, 394, 462, 10, "a", -1, "interior", "Dormitorio 3"),
    ("h", 562, 866, 932, 12, "b", -1, "interior", "Cocina"),
    ("h", 664, 859, 932, 14, "b", -1, "principal", "Ingreso"),
    ("h", 356, 944, 1006, 8, "a", +1, "interior", "Depósito"),
    ("h", 536, 944, 1004, 9, "a", -1, "interior", "Baño 3"),
]

# Ambientes: id, nombre, rects(px), piso, pared, etiqueta(px)
ROOMS = [
    ("dorm1", "Dormitorio principal", [(57, 347, 307, 664)], "laminado", "papel", (185, 470)),
    ("dorm2", "Dormitorio 2", [(163, 69, 388, 347)], "laminado", "papel", (275, 260)),
    ("dorm3", "Dormitorio 3", [(388, 69, 549, 347)], "laminado", "papel", (470, 250)),
    ("sala", "Sala – comedor", [(549, 133, 793, 664), (307, 347, 549, 459), (793, 562, 938, 664)],
     "laminado", "papel", (660, 420)),
    ("balcon", "Balcón", [(549, 69, 793, 133)], "ceramico_ext", "exterior", (671, 101)),
    ("bano1", "Baño 1", [(307, 459, 430, 664)], "ceramico_bano", "pintura", (355, 530)),
    ("bano2", "Baño 2", [(430, 459, 549, 664)], "ceramico_bano", "pintura", (500, 520)),
    ("cocina", "Cocina", [(793, 225, 938, 562)], "ceramico", "pintura", (895, 400)),
    ("lav", "Lavandería", [(938, 225, 1100, 356)], "ceramico", "pintura", (990, 280)),
    ("deposito", "Depósito", [(938, 356, 1100, 536)], "ceramico", "pintura", (1010, 450)),
    ("bano3", "Baño 3", [(938, 536, 1156, 662)], "ceramico_bano", "pintura", (975, 580)),
]

SHOWERS = [  # zona de ducha (px), lado del vidrio, mezcladora (x, y, normal)
    ((312, 584, 392, 657), ("h", 584), (392, 624, -1, 0)),
    ((470, 584, 543, 657), ("h", 584), (470, 624, 1, 0)),
    ((1034, 618, 1152, 658), ("v", 1034), (1152, 638, -1, 0)),
]
DUCTS = [(392, 584, 470, 657)]
# zócalos cerámicos: (x1, y1, x2, y2, z0, z1) en px / m
SPLASH = [
    (799.5, 232, 801, 490, 0.90, 1.50),     # cocina, entre mueble alto y bajo
    (1092, 236, 1093.5, 290, 0.85, 1.45),   # sobre lavadero
]

# Muebles por defecto: tipo, x, y (px, centro), rotación (°), extras
FURN = [
    # Dormitorio principal
    ("cama_2p", 153, 475, 90, {}), ("velador", 83, 392, 90, {}), ("velador", 83, 558, 90, {}),
    ("closet", 183, 630, 180, {"w": 2.65}), ("tv", 298.5, 472, -90, {"pulgadas": 55, "alto": 1.15}),
    ("alfombra", 205, 475, 90, {"w": 2.1, "d": 1.5, "color": "#d6cfc2"}),
    # Dormitorio 2
    ("cama_1p", 210, 162, 0, {}), ("cama_1p", 341, 162, 0, {}), ("velador", 275, 94, 0, {}),
    ("ropero", 236, 314, 180, {"w": 1.45}), ("cuadro", 381, 175, -90, {"w": 0.7, "alto": 1.45}),
    # Dormitorio 3: trabajo y recreación
    ("escritorio", 470, 103, 0, {"w": 1.4, "d": 0.6}), ("silla_escritorio", 470, 160, 180, {}),
    ("librero", 409.5, 235, 90, {}), ("tv", 505, 340, 180, {"pulgadas": 43, "alto": 1.1}),
    ("puff", 468, 282, 20, {"color": "#c9774f"}), ("puff", 522, 250, -30, {"color": "#3f5a73"}),
    ("alfombra", 495, 262, 0, {"w": 1.2, "d": 1.0, "color": "#5c6b7a"}), ("planta", 527, 180, 0, {}),
    # Sala
    ("sofa", 744, 248, -90, {"w": 2.0}), ("split", 777, 248, -90, {}),
    ("tv", 557, 240, 90, {"pulgadas": 85, "alto": 1.3}), ("mueble_tv", 572, 240, 90, {"w": 1.8}),
    ("candelabros", 572, 168, 90, {"z": 0.6}), ("mesa_nido", 652, 240, 90, {}),
    ("alfombra", 650, 245, 90, {"w": 2.2, "d": 1.6, "color": "#cfc6b6"}),
    ("candelabro_pie", 569, 331, 0, {}), ("lampara_tripode", 770, 362, 0, {}), ("planta", 612, 152, 0, {}),
    ("cuadro", 505, 353, 0, {"w": 0.8, "alto": 1.5}),
    # Comedor
    ("alfombra", 651, 529, 0, {"w": 1.9, "d": 2.3, "color": "#8d8a83", "borde": "#1f1f1f"}),
    ("mesa_comedor", 651, 529, 0, {"servida": True}),
    ("silla", 590, 500, 90, {"color": "#1f8a70"}), ("silla", 590, 558, 90, {"color": "#e6dfd1"}),
    ("silla", 712, 500, -90, {"color": "#8a5a3c"}), ("silla", 712, 558, -90, {"color": "#1f3f8f"}),
    ("lampara_colgante", 651, 505, 0, {}), ("lampara_colgante", 651, 553, 0, {}),
    ("cuadro", 556.5, 560, 90, {"w": 1.0, "alto": 1.55}),
    # Balcón
    ("urinario_perro", 600, 102, 0, {}), ("jardin_vertical", 556, 101, 90, {}),
    ("jardin_vertical", 785.5, 101, -90, {}), ("jardinera", 700, 83, 0, {}), ("jardinera", 765, 83, 0, {"w": 0.4}),
    # Cocina
    ("cocina_lineal", 826, 361, 90, {"w": 2.95}), ("cocina_4h", 826, 402, 90, {}),
    ("microondas", 815.5, 460, 90, {"z": 0.9}), ("refrigeradora", 831, 522, 90, {}),
    # Lavandería y depósito
    ("lavadero", 1073, 263, -90, {}), ("lavadora", 1008, 319, 180, {}), ("terma", 1081, 318, -90, {}),
    ("caminadora", 1057.5, 446, 0, {}),
    # Baños
    ("inodoro", 395, 491, -90, {}), ("lavatorio", 408, 556, -90, {}),
    ("alfombra_bano", 350, 560, 0, {}), ("toallero", 314.5, 480, 90, {}), ("portapapel", 370, 464.5, 0, {}),
    ("papelera", 330, 476, 0, {}), ("repisa_bano", 425, 491, -90, {}),
    ("lavatorio", 452, 486, 90, {"abierto": True}), ("inodoro", 465, 550, 90, {}),
    ("alfombra_bano", 505, 542, 90, {"color": "#9fb3a8"}), ("toallero", 542, 565, -90, {"color": "#9fb3a8"}),
    ("portapapel", 435, 525, 90, {}), ("papelera", 525, 570, 0, {}),
    ("inodoro", 985, 626, 180, {}), ("alfombra_bano", 1060, 598, 0, {"color": "#c9b89a"}),
    ("toallero", 1060, 541.5, 0, {"color": "#c9b89a"}), ("portapapel", 945.5, 615, 90, {}),
    ("papelera", 962, 570, 0, {}),
]

FOOTPRINT = [(50, 341), (157, 341), (157, 62), (799, 62), (799, 219), (1106, 219),
             (1106, 608), (1160, 608), (1160, 668), (50, 668)]


def build():
    solids, windows, doors = [], [], []
    for o, pos, a, b, t, ops in WALLS:
        h = t / 2
        rect = (lambda p1, p2: (p1, pos - h, p2, pos + h)) if o == "h" else \
               (lambda p1, p2: (pos - h, p1, pos + h, p2))
        start = a - h
        for (wa, wb, k) in sorted(ops):
            if wa - start > 0.5:
                solids.append(dict(r=rect(start, wa), z=[0, H], ext=t >= 13))
            sill, head = WIN[k]
            r = rect(wa, wb)
            if sill > 0:
                solids.append(dict(r=r, z=[0, sill], ext=t >= 13))
            if k != "baranda":
                solids.append(dict(r=r, z=[head, H], ext=t >= 13))
            windows.append(dict(r=r, o=o, tipo=k, z=[sill, head]))
            start = wb
        if b + h - start > 0.5:
            solids.append(dict(r=rect(start, b + h), z=[0, H], ext=t >= 13))
    for o, pos, a, b, t, hinge, side, kind, name in DOORS:
        h = t / 2
        r = (a, pos - h, b, pos + h) if o == "h" else (pos - h, a, pos + h, b)
        solids.append(dict(r=r, z=[DOOR_H, H], ext=False))
        hp = a if hinge == "a" else b
        hx, hy = (hp, pos) if o == "h" else (pos, hp)
        cd = (1 if hinge == "a" else -1)
        closed = (cd, 0) if o == "h" else (0, cd)
        opened = (0, side) if o == "h" else (side, 0)
        doors.append(dict(r=r, o=o, hinge=[X(hx), Y(hy)], cerrada=list(closed), abierta=list(opened),
                          ancho=m(b - a), esp=m(t), tipo=kind, nombre=name))

    def R(r):
        return [X(r[0]), Y(r[1]), X(r[2]), Y(r[3])]

    data = dict(
        nota="Geometría aproximada a partir del Anexo de Planos V.02 (sin cotas). Escala deducida del área techada.",
        H=H, puerta_h=DOOR_H,
        norte=[1, 0],
        muros=[dict(r=R(s["r"]), z=s["z"], ext=s["ext"]) for s in solids],
        ventanas=[dict(r=R(w["r"]), o=w["o"], tipo=w["tipo"], z=list(w["z"])) for w in windows],
        puertas=[dict(d, r=R(d["r"])) for d in doors],
        ambientes=[dict(id=i, nombre=n, rects=[R(r) for r in rs], piso=p, pared=w, etiqueta=[X(l[0]), Y(l[1])])
                   for i, n, rs, p, w, l in ROOMS],
        duchas=[dict(r=R(r), vidrio=[o, X(v) if o == "v" else Y(v)], mezcladora=[X(mx), Y(my), nx, ny])
                for r, (o, v), (mx, my, nx, ny) in SHOWERS],
        ductos=[R(r) for r in DUCTS],
        zocalos=[dict(r=R(r[:4]), z=[r[4], r[5]]) for r in SPLASH],
        contorno=[[X(x), Y(y)] for x, y in FOOTPRINT],
        muebles=[dict(tipo=t, x=X(x), y=Y(y), rot=rot, **ex) for t, x, y, rot, ex in FURN],
    )
    return data


if __name__ == "__main__":
    d = build()
    with open("planta.json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    xs = [p[0] for p in d["contorno"]]
    ys = [p[1] for p in d["contorno"]]
    print("OK planta.json  ancho %.2f m  fondo %.2f m  muros %d  puertas %d" %
          (max(xs) - min(xs), max(ys) - min(ys), len(d["muros"]), len(d["puertas"])))
