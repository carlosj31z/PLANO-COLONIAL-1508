# Departamento 1508 · Alto Lima Park

Modelo 3D editable y plano A3 del Dpto. 1508 (Edificio A, tipología 208 al 2008).

- `public/index.html`: la página 3D (vista aérea, planta y recorrido). Es lo que se publica en Vercel.
- `public/PLANO_DPTO_1508_A3.pdf`: plano A3 con planta y vista 3D.

## Desplegar en Vercel

La página es estática: no necesita instalación ni compilación.

1. En Vercel, **Add New → Project** e importa este repositorio (rama `claude/magical-allen-c3xw1n` o la que uses).
2. Deja los valores que toma de `vercel.json`: sin *build command* y con *output directory* `public`.
3. Pulsa **Deploy**. La página queda en `https://<tu-proyecto>.vercel.app` y el plano en `/PLANO_DPTO_1508_A3.pdf`.

También funciona con la CLI: `npx vercel --prod` desde la raíz del repositorio.

## Regenerar

```bash
pip install reportlab
python3 modelo.py            # geometría -> planta.json
python3 generar_plano.py     # plano A3 en PDF
python3 construir_pagina.py  # página 3D -> recorrido_3d.html y public/
```

La geometría y los muebles por defecto están en `modelo.py`; el catálogo de muebles en `web/muebles.js` y la interfaz en `web/plantilla.html`. Las medidas son aproximadas: el anexo no trae cotas y la escala se dedujo del área techada (72.82 m²).
