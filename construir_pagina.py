#!/usr/bin/env python3
"""Genera la página del modelo 3D.

- recorrido_3d.html: contenido del artifact (sin <html>/<head>/<body>).
- public/index.html: documento completo listo para Vercel (o cualquier hosting estático).
"""
import json
import os
import shutil

import modelo

data = modelo.build()
tpl = open("web/plantilla.html", encoding="utf-8").read()
muebles = open("web/muebles.js", encoding="utf-8").read()
js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
page = tpl.replace("/*__MUEBLES__*/", muebles).replace("__PLANTA_JSON__", js)
open("recorrido_3d.html", "w", encoding="utf-8").write(page)

doc = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Modelo 3D editable del Departamento 1508, Alto Lima Park (Edificio A).">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}*{box-sizing:border-box}body{margin:0;font:14px system-ui,sans-serif;background:#e9ecea}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
""" + page + "\n</body>\n</html>\n"
os.makedirs("public", exist_ok=True)
open("public/index.html", "w", encoding="utf-8").write(doc)
if os.path.exists("PLANO_DPTO_1508_A3.pdf"):
    shutil.copy("PLANO_DPTO_1508_A3.pdf", "public/PLANO_DPTO_1508_A3.pdf")
print("OK -> recorrido_3d.html y public/index.html (%d KB)" % (len(doc.encode()) // 1024))
