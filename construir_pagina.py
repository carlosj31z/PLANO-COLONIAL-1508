#!/usr/bin/env python3
"""Genera recorrido_3d.html a partir de web/plantilla.html y la geometría de modelo.py."""
import json
import modelo

data = modelo.build()
tpl = open("web/plantilla.html", encoding="utf-8").read()
js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = tpl.replace("__PLANTA_JSON__", js)
open("recorrido_3d.html", "w", encoding="utf-8").write(out)
print("OK -> recorrido_3d.html (%d KB)" % (len(out.encode()) // 1024))
