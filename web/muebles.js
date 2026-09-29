/* ------------------------------------------------------------ piezas que se abren */
let OPS_CUR = null;
function applyOp(op){ const o = op.obj, v = op.cur; if (op.prop === 'ry') o.rotation.y = v; else if (op.prop === 'rx') o.rotation.x = v; else if (op.prop === 'px') o.position.x = v; else if (op.prop === 'pz') o.position.z = v; }
function openable(parent, x, y, z, prop, closed, open){
  const g = new T3.Group(); g.position.set(x, y, z); parent.add(g);
  const op = { obj: g, prop, closed, open, cur: closed, state: false };
  applyOp(op); if (OPS_CUR) OPS_CUR.push(op); return g;
}
// cuerpo hueco con frente abierto (+z)
function carcass(p, m, w, h, d, x, y0, z, t = 0.018, inner){
  const mi = inner || m;
  bx(p, m, w, t, d, x, y0, z); bx(p, m, w, t, d, x, y0 + h - t, z);
  bx(p, m, t, h, d, x - w / 2 + t / 2, y0, z); bx(p, m, t, h, d, x + w / 2 - t / 2, y0, z);
  bx(p, mi, w - 2 * t, h - 2 * t, t, x, y0 + t, z - d / 2 + t / 2);
}
// puerta batiente: side -1 bisagra a la izquierda, +1 a la derecha
function hingeDoor(p, mat, w, h, x, y0, zf, side, handle = M.steel, t = 0.018, ang = 1.85){
  const pv = openable(p, x + side * w / 2, y0, zf, 'ry', 0, side * ang);
  bx(pv, mat, w - 0.004, h, t, -side * w / 2, 0, t / 2);
  if (handle) bx(pv, handle, 0.014, Math.min(0.2, h * 0.4), 0.02, -side * (w - 0.05), h * 0.5 - Math.min(0.1, h * 0.2), t + 0.01);
  return pv;
}
function drawer(p, m, w, h, d, x, y0, zf, handle = M.steel){
  const g = openable(p, 0, 0, 0, 'pz', 0, d * 0.7);
  bx(g, m, w - 0.004, h, 0.018, x, y0, zf + 0.009);
  const mi = matte('#ece8e0');
  bx(g, mi, w - 0.05, 0.012, d - 0.04, x, y0 + 0.02, zf - d / 2);
  bx(g, mi, 0.012, h * 0.6, d - 0.04, x - w / 2 + 0.03, y0 + 0.02, zf - d / 2);
  bx(g, mi, 0.012, h * 0.6, d - 0.04, x + w / 2 - 0.03, y0 + 0.02, zf - d / 2);
  bx(g, mi, w - 0.05, h * 0.6, 0.012, x, y0 + 0.02, zf - d + 0.03);
  if (handle) bx(g, handle, Math.min(0.16, w * 0.5), 0.012, 0.02, x, y0 + h * 0.6, zf + 0.028);
  return g;
}
function clothes(p, x0, x1, yRod, zc, R){
  const rod = cy(p, M.chrome, 0.012, 0.012, x1 - x0, (x0 + x1) / 2, yRod, zc); rod.rotation.z = Math.PI / 2; rod.position.y = yRod;
  const cols = ['#3f4a57', '#d8d2c6', '#8d3f35', '#6f7d6a', '#2f3336', '#c9a66b', '#9fb3c8', '#f2f0ea'];
  let x = x0 + 0.04;
  while (x < x1 - 0.04){ const th = 0.025 + R() * 0.03, hh = 0.55 + R() * 0.45; bx(p, fabric(cols[Math.floor(R() * cols.length)]), th, hh, 0.44, x, yRod - hh - 0.02, zc); x += th + 0.012 + R() * 0.02; }
}
function bottles(p, x0, x1, y, z, R, n = 5){
  const cols = ['#c7e2ef', '#f2c14e', '#e8e3d8', '#6f9a62', '#d97b66', '#ffffff'];
  for (let i = 0; i < n; i++){ const x = x0 + (i + 0.5) * (x1 - x0) / n; const h = 0.08 + R() * 0.12; cy(p, satin(cols[Math.floor(R() * cols.length)]), 0.022, 0.026, h, x, y, z + (R() - 0.5) * 0.05); }
}
function plates(p, x, y, z, n = 6, r = 0.12){ for (let i = 0; i < n; i++) cy(p, M.white, r, r * 0.8, 0.012, x, y + i * 0.014, z, 28); }
function flame(p, x, y, z){ const f = mesh(p, new T3.ConeGeometry(0.008, 0.028, 10), M.flame, x, y + 0.014, z); f.castShadow = false; return f; }
function instLeaves(p, n, R, place, greens = ['#4f7a45', '#5f8c4f', '#3f6a3b', '#6d9a57', '#7fa864'], size = 0.06){
  const geo = new T3.IcosahedronGeometry(size, 0);
  const im = new T3.InstancedMesh(geo, std('leafInst', { color: '#ffffff', roughness: 0.8, flatShading: true }), n);
  const m4 = new T3.Matrix4(), q = new T3.Quaternion(), e = new T3.Euler(), sc = new T3.Vector3(), pos = new T3.Vector3(), c = new T3.Color();
  for (let i = 0; i < n; i++){
    const [x, y, z, s] = place(i, R);
    e.set(R() * 3, R() * 3, R() * 3); q.setFromEuler(e); sc.set(s, s * (0.4 + R() * 0.5), s); pos.set(x, y, z);
    m4.compose(pos, q, sc); im.setMatrixAt(i, m4); im.setColorAt(i, c.set(greens[Math.floor(R() * greens.length)]));
  }
  im.castShadow = true; im.receiveShadow = true; p.add(im); return im;
}

/* ------------------------------------------------------------ texturas de detalle */
function screenTex(kind){
  return canvasTex('scr' + kind, 512, (g, s) => {
    if (kind === 'android'){
      g.fillStyle = '#0f1419'; g.fillRect(0, 0, s, s);
      g.fillStyle = '#9fb3c8'; g.font = '600 22px sans-serif'; g.fillText('08:45', 20, 34); g.fillText('Wi-Fi  87%', s - 140, 34);
      g.fillStyle = '#1d2733'; g.fillRect(20, 56, s - 40, 190);
      g.fillStyle = '#ffffff'; g.font = '700 96px sans-serif'; g.fillText('6.5', 40, 170); g.font = '500 28px sans-serif'; g.fillText('km/h', 200, 170);
      g.fillStyle = '#7fd1a8'; g.font = '600 24px sans-serif'; g.fillText('Inclinación 2 %', 40, 220);
      const tiles = [['Distancia', '1.24 km'], ['Tiempo', '11:32'], ['Calorías', '86 kcal']];
      tiles.forEach(([a, b], i) => { g.fillStyle = '#1d2733'; g.fillRect(20 + i * 160, 262, 148, 100); g.fillStyle = '#9fb3c8'; g.font = '500 20px sans-serif'; g.fillText(a, 32 + i * 160, 294); g.fillStyle = '#fff'; g.font = '700 30px sans-serif'; g.fillText(b, 32 + i * 160, 340); });
      const apps = ['#e53935', '#43a047', '#1e88e5', '#fb8c00', '#8e24aa', '#00acc1'];
      apps.forEach((c, i) => { g.fillStyle = c; g.beginPath(); if (g.roundRect) g.roundRect(28 + i * 78, 390, 60, 60, 14); else g.rect(28 + i * 78, 390, 60, 60); g.fill(); });
      g.strokeStyle = '#7fd1a8'; g.lineWidth = 4; g.beginPath(); g.moveTo(320, 220); for (let i = 0; i < 12; i++) g.lineTo(320 + i * 14, 150 + Math.sin(i) * 40); g.stroke();
    } else if (kind === 'pc'){
      g.fillStyle = '#1e1f24'; g.fillRect(0, 0, s, s); g.fillStyle = '#2b2d33'; g.fillRect(0, 0, 90, s);
      const cols = ['#c792ea', '#82aaff', '#c3e88d', '#f78c6c', '#89ddff', '#ffcb6b'];
      for (let i = 0; i < 26; i++){ g.fillStyle = cols[i % cols.length]; g.fillRect(110 + (i % 3) * 18, 20 + i * 18, 60 + (i * 53 % 260), 8); }
    } else {
      const gr = g.createLinearGradient(0, 0, 0, s); gr.addColorStop(0, '#f6b56a'); gr.addColorStop(0.45, '#e9866a'); gr.addColorStop(1, '#3d5a80');
      g.fillStyle = gr; g.fillRect(0, 0, s, s);
      g.fillStyle = '#fff3d6'; g.beginPath(); g.arc(s * 0.62, s * 0.42, 40, 0, 7); g.fill();
      const hill = (y, c, a) => { g.fillStyle = c; g.beginPath(); g.moveTo(0, s); for (let x = 0; x <= s; x += 16) g.lineTo(x, y + Math.sin(x / 70 + a) * 30 + Math.sin(x / 23) * 8); g.lineTo(s, s); g.fill(); };
      hill(s * 0.55, '#6b4f6f', 1); hill(s * 0.68, '#3e3a5a', 3); hill(s * 0.82, '#22243a', 5);
    }
  });
}
function screenMat(kind){ return std('scrM' + kind, { color: '#050607', emissive: '#ffffff', emissiveMap: screenTex(kind), emissiveIntensity: 0.75, roughness: 0.12 }); }
function artTex(seed){
  return canvasTex('art' + seed, 512, (g, s) => {
    const R = rng(seed); g.fillStyle = '#ece4d6'; g.fillRect(0, 0, s, s);
    const cols = ['#1f1f1f', '#b86f4c', '#d9b98c', '#6f7d6a', '#3f4a57'];
    g.fillStyle = cols[0]; g.beginPath(); g.arc(s * (0.3 + R() * 0.4), s * 0.62, s * 0.28, Math.PI, 0); g.fill();
    g.fillStyle = cols[1 + Math.floor(R() * 2)]; g.beginPath(); g.arc(s * (0.25 + R() * 0.5), s * 0.34, s * 0.12, 0, 7); g.fill();
    g.fillStyle = cols[3 + Math.floor(R() * 2)]; g.fillRect(s * 0.12, s * 0.78, s * 0.76, s * 0.05);
    g.strokeStyle = '#1f1f1f'; g.lineWidth = 3; g.beginPath(); g.arc(s * 0.7, s * 0.3, s * 0.18, 0.5, 2.6); g.stroke();
  });
}
function grassTex(){
  return canvasTex('grass', 256, (g, s) => {
    g.fillStyle = '#4c7a3a'; g.fillRect(0, 0, s, s); const R = rng(42);
    for (let i = 0; i < 2600; i++){ g.strokeStyle = ['#5f9a47', '#3f6a30', '#7ab35a', '#4d8a3a'][i % 4]; g.globalAlpha = 0.7; g.lineWidth = 1; const x = R() * s, y = R() * s; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (R() - 0.5) * 4, y - 3 - R() * 5); g.stroke(); }
    g.globalAlpha = 1;
  });
}
function netTex(){
  return canvasTex('net', 256, (g, s) => {
    g.clearRect(0, 0, s, s); g.strokeStyle = 'rgba(40,44,48,0.85)'; g.lineWidth = 2.2; const st = 32;
    for (let k = -s; k < 2 * s; k += st){ g.beginPath(); g.moveTo(k, 0); g.lineTo(k + s, s); g.stroke(); g.beginPath(); g.moveTo(k, s); g.lineTo(k + s, 0); g.stroke(); }
  });
}
function deckTex(c){
  return canvasTex('deck' + c, 1024, (g, s) => {
    const R = rng(hashStr(c)); const pw = s * 0.145 / 2.4, pl = s / 2;
    for (let row = 0; row * pw < s; row++){
      const off = (row * 0.41 % 1) * pl, y = row * pw;
      for (let x = -off; x < s; x += pl){
        g.fillStyle = shade(c, 0.9 + R() * 0.18); g.fillRect(x, y, pl, pw);
        g.strokeStyle = shade(c, 0.78); g.globalAlpha = 0.5; g.lineWidth = 1.2;
        for (let k = 1; k < 5; k++){ g.beginPath(); g.moveTo(x, y + k * pw / 5); g.lineTo(x + pl, y + k * pw / 5); g.stroke(); }
        g.globalAlpha = 1; g.fillStyle = shade(c, 0.45); g.fillRect(x, y, pl, 3); g.fillRect(x, y, 2, pw);
      }
    }
  });
}
function rugTex2(c, b){
  return canvasTex('rug2' + c + b, 512, (g, s) => {
    g.fillStyle = b; g.fillRect(0, 0, s, s); const m = 46;
    g.fillStyle = c; g.fillRect(m, m, s - 2 * m, s - 2 * m);
    g.fillStyle = shade(c, 0.62); for (let x = m; x < s - m; x += 8) for (let y = m; y < s - m; y += 8) if (((x + y) / 8) % 2 === 0) g.fillRect(x, y, 4, 4);
    noise(g, s, 5000, shade(b, 1.4), 0.25, 1.5, 33);
  });
}

/* ------------------------------------------------------------ catálogo de muebles */
const WOODS = ['#b08a60', '#8a6444', '#d1b28a', '#5e4636', '#e6ddcf'];
const FABRICS = ['#bdbcb8', '#8d9296', '#c8bfb1', '#6f7d6a', '#3f4a57', '#b9876a'];
const MELA = ['#f1efea', '#d9cbb5', '#a57f5a', '#6c6f72', '#e3e7e6'];
const VELVET = ['#1f8a70', '#e6dfd1', '#8a5a3c', '#1f3f8f', '#8d9296', '#b8455a'];
const TOWELS = ['#e8e2d6', '#9fb3a8', '#c9b89a', '#3f4a57', '#d9a6a0'];
const CAT = {
  cama_2p:    { n: 'Cama 2 plazas', g: 'Dormitorio', w: 1.55, d: 2.0, rw: [1.35, 2.0], colors: ['#7f8b77', '#c9c3b8', '#5d636b', '#b7866a', '#8fa0b3'] },
  cama_1p:    { n: 'Cama 1½ plaza', g: 'Dormitorio', w: 1.0, d: 1.95, rw: [0.9, 1.2], colors: ['#7f8b77', '#c9c3b8', '#5d636b', '#b7866a', '#8fa0b3'] },
  velador:    { n: 'Velador con cajón', g: 'Dormitorio', w: 0.45, d: 0.4, colors: WOODS },
  ropero:     { n: 'Ropero', g: 'Dormitorio', w: 1.4, d: 0.56, rw: [0.6, 2.4], colors: MELA },
  closet:     { n: 'Clóset de melamine', g: 'Dormitorio', w: 2.65, d: 0.6, rw: [1.0, 3.2], colors: MELA, c0: '#d9cbb5' },
  tv:         { n: 'Televisor', g: 'Sala y comedor', w: 1.9, d: 0.06, wall: true, sizes: [43, 55, 65, 75, 85], pulgadas: 55, alto: 1.2 },
  escritorio: { n: 'Escritorio con monitores', g: 'Trabajo y recreación', w: 1.4, d: 0.6, rw: [0.9, 1.8], colors: WOODS },
  silla_escritorio: { n: 'Silla ergonómica', g: 'Trabajo y recreación', w: 0.62, d: 0.62, colors: ['#2f3336', '#6f7d6a', '#b9876a', '#3f4a57'] },
  librero:    { n: 'Librero', g: 'Trabajo y recreación', w: 0.9, d: 0.35, rw: [0.6, 1.8], colors: WOODS },
  puff:       { n: 'Puf (bean bag)', g: 'Trabajo y recreación', w: 0.75, d: 0.75, colors: ['#c9774f', '#3f5a73', '#6f7d6a', '#d8d2c6', '#2f3336'] },
  sofa:       { n: 'Sofá 3 cuerpos', g: 'Sala y comedor', w: 2.0, d: 0.92, rw: [1.6, 2.4], colors: FABRICS },
  sillon:     { n: 'Sillón', g: 'Sala y comedor', w: 0.8, d: 0.82, colors: ['#c8a98a', '#8d9296', '#6f7d6a', '#3f4a57', '#e0d8cb'] },
  mesa_nido:  { n: 'Mesas de centro nido', g: 'Sala y comedor', w: 1.2, d: 0.9, colors: ['#6b4430', '#8a5a3c', '#b08a60', '#2f3336'] },
  mesa_centro:{ n: 'Mesa de centro', g: 'Sala y comedor', w: 0.9, d: 0.5, rw: [0.6, 1.3], colors: WOODS },
  mueble_tv:  { n: 'Mueble de TV flotante', g: 'Sala y comedor', w: 1.8, d: 0.38, rw: [1.0, 2.4], colors: ['#6b4430', '#b08a60', '#2f3336', '#f1efea'] },
  candelabros:{ n: 'Candelabros de mesa', g: 'Decoración', w: 0.22, d: 0.1, colors: ['#c9a44c', '#1f2224', '#d9d4ca'], elev: true },
  candelabro_pie:{ n: 'Candelabros de piso', g: 'Decoración', w: 0.4, d: 0.3, colors: ['#1f2224', '#c9a44c'] },
  split:      { n: 'Aire acondicionado split', g: 'Sala y comedor', w: 0.9, d: 0.22, wall: true },
  alfombra:   { n: 'Alfombra', g: 'Sala y comedor', w: 2.0, d: 1.6, rw: [0.8, 3.2], rd: [0.6, 3.2], low: true, colors: ['#e6dfd2', '#cfc6b6', '#8a94a0', '#7c6a5c', '#5c6b7a', '#8d8a83'] },
  mesa_comedor:{ n: 'Mesa de comedor (patas en X)', g: 'Sala y comedor', w: 0.9, d: 1.5, rd: [1.1, 2.2], colors: ['#b58c5e', '#8a6444', '#d1b28a', '#5e4636'] },
  silla:      { n: 'Silla de terciopelo', g: 'Sala y comedor', w: 0.5, d: 0.55, colors: VELVET },
  lampara_colgante:{ n: 'Lámpara colgante tipo jaula', g: 'Decoración', w: 0.26, d: 0.26, ceil: true, colors: ['#1f2224', '#c9a44c'] },
  lampara_tripode:{ n: 'Lámpara trípode', g: 'Decoración', w: 0.6, d: 0.6, colors: ['#b08a60', '#5e4636'] },
  lampara_pie:{ n: 'Lámpara de pie', g: 'Decoración', w: 0.4, d: 0.4, colors: ['#1f2224', '#b59b72', '#e6e2da'] },
  cuadro:     { n: 'Cuadro', g: 'Decoración', w: 0.9, d: 0.04, rw: [0.4, 1.6], wall: true },
  planta:     { n: 'Planta', g: 'Decoración', w: 0.45, d: 0.45, colors: ['#e7e2d8', '#b86f4c', '#2f3336', '#8aa0a8'] },
  jardin_vertical:{ n: 'Jardín vertical', g: 'Balcón', w: 0.55, d: 0.12, rw: [0.4, 1.6], wall: true },
  jardinera:  { n: 'Jardinera colgante', g: 'Balcón', w: 0.8, d: 0.2, rw: [0.4, 1.2], wall: true, colors: ['#2f3336', '#b86f4c', '#e6e2da'] },
  urinario_perro:{ n: 'Baño de césped para perro', g: 'Balcón', w: 0.7, d: 0.5, low: true },
  mesa_balcon:{ n: 'Mesa de balcón', g: 'Balcón', w: 0.6, d: 0.6, colors: ['#2f3336', '#e6e2da', '#6f7d6a'] },
  cocina_lineal:{ n: 'Muebles de cocina (bajos y altos)', g: 'Cocina y lavandería', w: 2.95, d: 0.6, rw: [1.8, 3.4], colors: MELA },
  cocina_4h:  { n: 'Cocina de pie 4 hornillas', g: 'Cocina y lavandería', w: 0.52, d: 0.6, colors: ['#f2f2f0', '#c9cdd1', '#2f3336'] },
  microondas: { n: 'Microondas', g: 'Cocina y lavandería', w: 0.48, d: 0.36, colors: ['#2f3336', '#c9cdd1', '#f2f2f0'], elev: true },
  refrigeradora:{ n: 'Refrigeradora', g: 'Cocina y lavandería', w: 0.7, d: 0.72, colors: ['#c9cdd1', '#f2f2f0', '#2f3336'] },
  lavadero:   { n: 'Lavadero de losa', g: 'Cocina y lavandería', w: 0.55, d: 0.5 },
  lavadora:   { n: 'Lavadora LG carga superior 20 kg', g: 'Cocina y lavandería', w: 0.68, d: 0.72, colors: ['#b9bcbf', '#f4f4f2', '#3a3d40'] },
  terma:      { n: 'Terma a gas', g: 'Cocina y lavandería', w: 0.45, d: 0.3, wall: true },
  caminadora: { n: 'Caminadora eléctrica con pantalla', g: 'Cocina y lavandería', w: 0.8, d: 1.8, colors: ['#2b2e33', '#c9cdd1'] },
  estante:    { n: 'Estantería metálica', g: 'Cocina y lavandería', w: 1.2, d: 0.4, rw: [0.6, 1.8] },
  inodoro:    { n: 'Inodoro', g: 'Baño', w: 0.4, d: 0.7 },
  lavatorio:  { n: 'Vanitorio', g: 'Baño', w: 0.5, d: 0.42, rw: [0.45, 0.9], colors: MELA },
  alfombra_bano:{ n: 'Alfombra de baño', g: 'Baño', w: 0.6, d: 0.4, low: true, colors: TOWELS },
  toallero:   { n: 'Toallero con toalla', g: 'Baño', w: 0.6, d: 0.1, wall: true, colors: TOWELS },
  portapapel: { n: 'Portapapel', g: 'Baño', w: 0.16, d: 0.12, wall: true },
  papelera:   { n: 'Papelera', g: 'Baño', w: 0.24, d: 0.24, colors: ['#e9ebec', '#c9cdd1', '#2f3336'] },
  repisa_bano:{ n: 'Repisa organizadora', g: 'Baño', w: 0.4, d: 0.16, wall: true, colors: WOODS },
};
function dims(it){ const C = CAT[it.tipo]; if (it.tipo === 'tv'){ const i = it.pulgadas || C.pulgadas; return [i * 0.02214 + 0.02, 0.06]; } return [it.w || C.w, it.d || C.d]; }

function build(it){
  const C = CAT[it.tipo]; const g = new T3.Group();
  const [w, d] = dims(it); const col = it.color || (C.c0 || (C.colors ? C.colors[0] : '#cccccc'));
  const R = rng(hashStr(it.id));
  const W = w / 2, D = d / 2;
  const ops = []; OPS_CUR = ops;
  switch (it.tipo){
    case 'cama_2p': case 'cama_1p': {
      const base = fabric('#d5d0c6'), head = fabric('#bdb4a6');
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(g, M.black, 0.022, 0.018, 0.08, sx * (W - 0.07), 0, sz * (D - 0.08));
      rb(g, base, w, 0.26, d, 0.025, 0, 0.08, 0);
      rb(g, fabric('#f4f3ef'), w - 0.04, 0.22, d - 0.08, 0.05, 0, 0.33, 0.02);
      rb(g, head, w + 0.06, 1.0, 0.09, 0.03, 0, 0.08, -D + 0.02);
      const duv = d * 0.64;
      rb(g, fabric(col), w + 0.03, 0.07, duv, 0.035, 0, 0.52, D - duv / 2 + 0.01);
      rb(g, fabric('#efebe4'), w + 0.03, 0.09, 0.2, 0.045, 0, 0.52, D - duv + 0.1);
      rb(g, fabric(shade(col, 0.75)), w + 0.05, 0.03, 0.42, 0.012, 0, 0.585, D - 0.32);
      const np = it.tipo === 'cama_2p' ? 2 : 1, pw = (w - 0.12) / np - 0.04;
      for (let i = 0; i < np; i++){ const x = -W + 0.06 + pw / 2 + i * (pw + 0.04) + 0.02; rb(g, fabric('#ffffff'), pw, 0.14, 0.38, 0.065, x, 0.53, -D + 0.3).rotation.x = -0.25; }
      rb(g, fabric(shade(col, 1.25)), Math.min(0.42, w * 0.35), 0.32, 0.12, 0.05, 0, 0.56, -D + 0.52).rotation.x = -0.35;
      break; }
    case 'velador': {
      const m = woodM(col);
      carcass(g, m, w, 0.5, d, 0, 0.04, 0);
      bx(g, m, w - 0.036, 0.015, d - 0.03, 0, 0.26, 0);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, M.black, 0.03, 0.04, 0.03, sx * (W - 0.04), 0, sz * (D - 0.04));
      drawer(g, woodM(shade(col, 0.92)), w - 0.04, 0.2, d - 0.06, 0, 0.3, D - 0.03);
      rb(g, matte('#3f4a57'), 0.2, 0.04, 0.15, 0.004, 0.02, 0.075, 0);
      cy(g, ceramicM('#d9d4ca'), 0.06, 0.07, 0.12, 0, 0.54, -0.04);
      cy(g, M.steel, 0.008, 0.008, 0.12, 0, 0.66, -0.04);
      mesh(g, cylG(0.1, 0.13, 0.15, 24, true), M.lamp, 0, 0.8, -0.04);
      break; }
    case 'ropero': {
      const hgt = 2.0, m = matte(col), m2 = satin(shade(col, 1.03)), inner = matte('#efece6');
      carcass(g, m, w, hgt - 0.08, d - 0.03, 0, 0.08, -0.015, 0.018, inner);
      bx(g, M.black, w - 0.04, 0.08, d - 0.08, 0, 0, -0.04);
      bx(g, inner, w - 0.04, 0.018, d - 0.06, 0, 1.72, -0.02);
      clothes(g, -W + 0.03, W - 0.03, 1.66, -0.02, R);
      for (let k = 0; k < Math.round(w / 0.3); k++) rb(g, fabric(['#d8d2c6', '#3f4a57', '#9fb3c8'][k % 3]), 0.26, 0.1, 0.35, 0.02, -W + 0.17 + k * 0.3, 1.74, -0.02);
      const n = Math.max(2, Math.round(w / 0.5)), fw = w / n;
      for (let i = 0; i < n; i++) hingeDoor(g, m2, fw, hgt - 0.12, -W + fw * (i + 0.5), 0.1, D - 0.02, i % 2 ? 1 : -1);
      break; }
    case 'closet': {
      const hgt = H - 0.02, m = matte(col), m2 = satin(shade(col, 1.03)), inner = matte('#efece6');
      carcass(g, m, w, hgt - 0.08, d - 0.06, 0, 0.08, -0.03, 0.018, inner);
      bx(g, M.black, w - 0.04, 0.08, d - 0.08, 0, 0, -0.04);
      bx(g, inner, w - 0.04, 0.018, d - 0.1, 0, 1.95, -0.03);
      clothes(g, -W + 0.03, W - 0.03, 1.86, -0.03, R);
      for (let k = 0; k < Math.round(w / 0.32); k++) rb(g, M.cardboard, 0.28, 0.2, 0.4, 0.01, -W + 0.18 + k * 0.32, 1.97, -0.03);
      for (let k = 0; k < Math.round(w / 0.3); k++){ const x = -W + 0.15 + k * 0.3; rb(g, matte(['#2f3336', '#8a5a3c', '#d8d2c6'][k % 3]), 0.1, 0.08, 0.26, 0.03, x - 0.055, 0.1, 0.02); rb(g, matte(['#2f3336', '#8a5a3c', '#d8d2c6'][k % 3]), 0.1, 0.08, 0.26, 0.03, x + 0.055, 0.1, 0.02); }
      const n = Math.max(2, Math.round(w / 0.66)), fw = w / n;
      for (let i = 0; i < n; i++){
        const x = -W + fw * (i + 0.5), zf = D - 0.012 - (i % 2) * 0.028;
        const dir = i < n - 1 ? 1 : -1;
        const pv = openable(g, 0, 0, 0, 'px', 0, dir * fw * 0.95);
        bx(pv, m2, fw + 0.02, hgt - 0.14, 0.02, x, 0.1, zf);
        bx(pv, M.aluDark, 0.018, 0.5, 0.012, x - dir * (fw / 2 - 0.05), 0.85, zf + 0.012);
      }
      bx(g, M.alu, w, 0.04, 0.08, 0, hgt - 0.05, D - 0.04);
      break; }
    case 'tv': {
      const inch = it.pulgadas || C.pulgadas, tw = inch * 0.02214, th = inch * 0.01245, ch = it.alto || C.alto;
      bx(g, M.black, Math.min(0.4, tw * 0.3), 0.25, 0.02, 0, ch - 0.12, -D + 0.01);
      bx(g, M.black, tw, th, 0.028, 0, ch - th / 2, -D + 0.034);
      bx(g, screenMat('tv'), tw - 0.012, th - 0.012, 0.002, 0, ch - th / 2 + 0.006, -D + 0.049);
      break; }
    case 'escritorio': {
      const m = woodM(col);
      rb(g, m, w, 0.035, d, 0.006, 0, 0.72, 0);
      for (const sx of [-1, 1]){ bx(g, M.black, 0.05, 0.72, d - 0.06, sx * (W - 0.05), 0, 0); }
      carcass(g, matte('#f1efea'), 0.42, 0.5, d - 0.08, W - 0.3, 0.2, -0.02);
      drawer(g, matte('#e9e6df'), 0.4, 0.22, d - 0.12, W - 0.3, 0.44, D - 0.06);
      drawer(g, matte('#e9e6df'), 0.4, 0.2, d - 0.12, W - 0.3, 0.21, D - 0.06);
      rb(g, satin('#1f2224'), 0.2, 0.42, 0.42, 0.01, -W + 0.2, 0, -0.02);
      bx(g, M.lamp, 0.01, 0.3, 0.3, -W + 0.305, 0.06, -0.02).castShadow = false;
      const mw = Math.min(0.62, (w - 0.2) / 2 - 0.02);
      for (const sx of w > 1.2 ? [-1, 1] : [0]){
        const x = sx * (mw / 2 + 0.02);
        bx(g, M.black, 0.2, 0.012, 0.16, x, 0.755, -D + 0.14); bx(g, M.black, 0.04, 0.2, 0.03, x, 0.765, -D + 0.12);
        const mon = bx(g, M.black, mw, 0.37, 0.025, x, 0.9, -D + 0.14); mon.rotation.y = -sx * 0.12;
        const sc = bx(g, screenMat('pc'), mw - 0.02, 0.35, 0.002, x, 0.91, -D + 0.154); sc.rotation.y = -sx * 0.12;
      }
      bx(g, matte('#2f3336'), 0.44, 0.02, 0.14, -0.05, 0.755, 0.08);
      rb(g, matte('#2f3336'), 0.06, 0.03, 0.1, 0.012, 0.28, 0.755, 0.08);
      cy(g, ceramicM('#e7e2d8'), 0.045, 0.04, 0.1, W - 0.12, 0.755, -D + 0.12);
      instLeaves(g, 10, R, () => [W - 0.12 + (R() - 0.5) * 0.08, 0.87 + R() * 0.1, -D + 0.12 + (R() - 0.5) * 0.08, 1], undefined, 0.035);
      break; }
    case 'silla_escritorio': {
      for (let k = 0; k < 5; k++){ const a = k / 5 * Math.PI * 2; const s = bx(g, M.black, 0.03, 0.03, 0.28, Math.sin(a) * 0.14, 0.05, Math.cos(a) * 0.14); s.rotation.y = a; mesh(g, new T3.SphereGeometry(0.025, 10, 8), M.black, Math.sin(a) * 0.28, 0.025, Math.cos(a) * 0.28); }
      cy(g, M.steel, 0.022, 0.022, 0.36, 0, 0.08, 0);
      rb(g, fabric(col), 0.5, 0.08, 0.48, 0.035, 0, 0.44, 0.02);
      rb(g, fabric(col), 0.46, 0.55, 0.06, 0.03, 0, 0.58, -0.24).rotation.x = 0.08;
      rb(g, fabric(col), 0.3, 0.14, 0.06, 0.03, 0, 1.17, -0.27).rotation.x = 0.1;
      bx(g, M.black, 0.05, 0.25, 0.03, 0, 0.44, -0.24);
      for (const sx of [-1, 1]){ bx(g, M.black, 0.03, 0.2, 0.03, sx * 0.26, 0.5, 0); rb(g, M.black, 0.06, 0.03, 0.24, 0.012, sx * 0.26, 0.7, 0.02); }
      break; }
    case 'puff': {
      const s = mesh(g, new T3.SphereGeometry(0.38, 28, 18), fabric(col), 0, 0.22, 0); s.scale.set(W / 0.38, 0.6, D / 0.38);
      const top = mesh(g, new T3.SphereGeometry(0.2, 20, 12), fabric(shade(col, 0.92)), 0.03, 0.4, -0.06); top.scale.set(1.2, 0.35, 1.1);
      break; }
    case 'sofa': {
      const f = fabric(col), f2 = fabric(shade(col, 0.95)), seam = fabric(shade(col, 0.8));
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, M.black, 0.09, 0.08, 0.09, sx * (W - 0.12), 0, sz * (D - 0.12));
      rb(g, f2, w - 0.02, 0.3, d - 0.05, 0.02, 0, 0.08, 0);
      for (const sx of [-1, 1]){ rb(g, f, 0.2, 0.44, d - 0.04, 0.03, sx * (W - 0.1), 0.08, 0.01); rb(g, f, 0.26, 0.12, d, 0.045, sx * (W - 0.125), 0.5, 0.02); }
      rb(g, f2, w - 0.42, 0.44, 0.18, 0.03, 0, 0.32, -D + 0.09);
      const cw = (w - 0.44) / 2;
      for (const sx of [-1, 1]){
        const x = sx * cw / 2;
        const seat = rb(g, f, cw - 0.012, 0.16, d - 0.24, 0.05, x, 0.38, 0.08);
        bx(seat, seam, 0.004, 0.002, d - 0.34, 0, 0.08, 0);
        const back = rb(g, f, cw - 0.014, 0.5, 0.2, 0.08, x, 0.5, -D + 0.22); back.rotation.x = -0.12;
        for (const lx of [-cw / 6, cw / 6]) bx(back, seam, 0.005, 0.4, 0.004, lx, -0.2, 0.1);
        for (const ly of [-0.08, 0.08]) bx(back, seam, cw - 0.06, 0.005, 0.004, 0, ly, 0.1);
      }
      break; }
    case 'sillon': {
      const f = fabric(col), f2 = fabric(shade(col, 0.93)), leg = woodM('#5e4636');
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(g, leg, 0.02, 0.014, 0.12, sx * (W - 0.08), 0, sz * (D - 0.08));
      rb(g, f2, w, 0.2, d, 0.03, 0, 0.12, 0);
      for (const sx of [-1, 1]) rb(g, f, 0.12, 0.38, d, 0.05, sx * (W - 0.06), 0.12, 0);
      rb(g, f, w - 0.02, 0.44, 0.2, 0.06, 0, 0.3, -D + 0.1);
      rb(g, f, w - 0.25, 0.14, d - 0.24, 0.055, 0, 0.32, 0.1);
      break; }
    case 'mesa_nido': {
      const wd = woodM(col);
      const table = (r, h, x, z) => {
        cy(g, wd, r, r, 0.025, x, h - 0.025, z, 40);
        const rim = mesh(g, new T3.TorusGeometry(r - 0.008, 0.012, 8, 48), wd, x, h + 0.002, z); rim.rotation.x = Math.PI / 2;
        for (let k = 0; k < 4; k++){ const a = k * Math.PI / 2 + 0.4; const leg = bx(g, M.black, 0.018, h - 0.03, 0.018, x + Math.cos(a) * r * 0.55, 0, z + Math.sin(a) * r * 0.55); leg.rotation.set(Math.sin(a) * 0.12, 0, -Math.cos(a) * 0.12); }
        const ring = mesh(g, new T3.TorusGeometry(r * 0.62, 0.01, 6, 36), M.black, x, 0.03, z); ring.rotation.x = Math.PI / 2;
      };
      table(0.4, 0.46, -0.18, -0.12); table(0.3, 0.38, 0.28, 0.2);
      mesh(g, new T3.IcosahedronGeometry(0.07, 0), ceramicM('#ecebe7'), -0.35, 0.53, -0.25).scale.y = 0.8;
      cy(g, ceramicM('#1f4d45'), 0.04, 0.035, 0.07, -0.1, 0.46, -0.38); cy(g, ceramicM('#1f4d45'), 0.07, 0.07, 0.008, -0.1, 0.46, -0.38);
      const mag = bx(g, std('mag', { map: artTex(7), roughness: 0.6 }), 0.36, 0.006, 0.26, -0.02, 0.46, 0.0); mag.rotation.y = 0.5;
      const mag2 = bx(g, std('mag2', { map: artTex(19), roughness: 0.6 }), 0.28, 0.006, 0.22, 0.34, 0.38, 0.28); mag2.rotation.y = -0.3;
      for (const [x, z, h] of [[0.2, 0.08, 0.22], [0.3, 0.12, 0.17]]){ cy(g, metal('#c9a44c', 0.3), 0.035, 0.04, 0.012, x, 0.38, z); cy(g, metal('#c9a44c', 0.3), 0.007, 0.01, h, x, 0.39, z); cy(g, metal('#c9a44c', 0.3), 0.016, 0.01, 0.02, x, 0.39 + h, z); cy(g, satin('#f08a24'), 0.01, 0.01, 0.16, x, 0.41 + h, z); flame(g, x, 0.57 + h, z); }
      for (let k = 0; k < 9; k++) mesh(g, new T3.SphereGeometry(0.025, 12, 8), ceramicM('#f7f5f0'), 0.36 + (k % 3) * 0.035, 0.41 + Math.floor(k / 3) * 0.03, 0.3 + ((k * 7) % 3) * 0.02);
      break; }
    case 'mesa_centro': {
      rb(g, woodM(col), w, 0.04, d, 0.01, 0, 0.36, 0);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, M.black, 0.022, 0.36, 0.022, sx * (W - 0.05), 0, sz * (D - 0.05));
      bx(g, woodM(shade(col, 0.9)), w - 0.1, 0.02, d - 0.1, 0, 0.1, 0);
      break; }
    case 'mueble_tv': {
      const m = woodM(col), y0 = 0.28, hh = 0.32;
      carcass(g, m, w, hh, d, 0, y0, 0, 0.02, matte('#2f3336'));
      const n = Math.max(2, Math.round(w / 0.6)), fw = (w - 0.04) / n;
      for (let i = 0; i < n; i++){ const pv = openable(g, -W + 0.02 + fw * (i + 0.5), y0 + 0.02, D, 'rx', 0, 1.3); bx(pv, woodM(shade(col, 0.94)), fw - 0.006, hh - 0.04, 0.016, 0, 0, 0.008); }
      bx(g, satin('#1f2224'), 0.3, 0.06, 0.2, -W + 0.3, y0 + 0.02, -0.02); bx(g, M.lamp, 0.012, 0.006, 0.006, -W + 0.2, y0 + 0.05, 0.08);
      bx(g, satin('#f2f2f0'), 0.26, 0.08, 0.2, W - 0.4, y0 + 0.02, -0.02);
      for (let k = 0; k < 5; k++) bx(g, matte(['#3f4a57', '#b9876a', '#d8c9a8', '#6f7d6a', '#2f3336'][k]), 0.03, 0.2, 0.2, W - 0.12 - k * 0.035, y0 + 0.02, 0);
      bx(g, M.lamp, w - 0.1, 0.006, 0.02, 0, y0 - 0.008, D - 0.05).castShadow = false;
      break; }
    case 'candelabros': case 'candelabro_pie': {
      const gm = metal(col, 0.3), floor = it.tipo === 'candelabro_pie';
      const set = floor ? [[-0.12, -0.02, 0.62], [0.02, 0.06, 0.85], [0.14, -0.04, 1.05]] : [[-0.06, 0, 0.22], [0.06, 0.01, 0.16]];
      for (const [x, z, h] of set){
        cy(g, gm, floor ? 0.08 : 0.035, floor ? 0.09 : 0.04, 0.012, x, 0, z, 24);
        cy(g, gm, floor ? 0.008 : 0.006, floor ? 0.01 : 0.009, h, x, 0.012, z);
        cy(g, gm, floor ? 0.05 : 0.016, floor ? 0.012 : 0.01, 0.02, x, 0.012 + h, z);
        const ch = floor ? 0.14 : 0.15, cr = floor ? 0.035 : 0.01;
        cy(g, satin(floor ? '#f4efe6' : '#f08a24'), cr, cr, ch, x, 0.032 + h, z);
        flame(g, x, 0.032 + h + ch, z);
      }
      break; }
    case 'split': {
      const y0 = 2.05, body = satin('#f7f7f5');
      rb(g, body, w, 0.3, d - 0.02, 0.04, 0, y0, 0.01);
      bx(g, M.black, w - 0.12, 0.03, 0.03, 0, y0 + 0.02, D - 0.06);
      const lv = bx(g, satin('#ebebe9'), w - 0.1, 0.05, 0.012, 0, y0 + 0.005, D - 0.02); lv.rotation.x = 0.4;
      bx(g, std('acDisp', { color: '#0b1f2a', emissive: '#4fd1ff', emissiveIntensity: 1.2 }), 0.07, 0.018, 0.004, W - 0.16, y0 + 0.16, D);
      cy(g, M.white, 0.012, 0.012, 0.25, -W + 0.1, y0 - 0.25, -D + 0.02);
      break; }
    case 'alfombra': {
      const m = it.borde ? std('rug2' + col + it.borde, { map: rugTex2(col, it.borde), roughness: 1 }) : std('rug' + col, { map: rugTex(col), roughness: 1 });
      rb(g, m, w, 0.012, d, 0.004, 0, 0.002, 0).castShadow = false;
      break; }
    case 'mesa_comedor': {
      const top = woodM(col), blk = std('blkMetal', { color: '#1b1c1e', roughness: 0.5, metalness: 0.6 });
      rb(g, top, w, 0.045, d, 0.008, 0, 0.725, 0);
      const span = w - 0.12, hh = 0.72, L = Math.hypot(span, hh), a = Math.atan2(hh, span);
      for (const sz of [-1, 1]){ for (const sgn of [-1, 1]){ const b = mesh(g, boxG(L, 0.05, 0.05), blk, 0, hh / 2, sz * (D - 0.15)); b.rotation.z = sgn * a; } bx(g, blk, span, 0.03, 0.05, 0, 0.695, sz * (D - 0.15)); }
      const st = cy(g, blk, 0.018, 0.018, d - 0.3, 0, 0.36, 0); st.rotation.x = Math.PI / 2; st.position.y = 0.36;
      if (it.servida){
        const pl = std('platoNegro', { color: '#1b1c1e', roughness: 0.25 });
        for (const sx of [-1, 1]) for (const sz of [-0.35, 0.35]){
          const x = sx * (W - 0.17), z = sz * (d / 1.5);
          bx(g, matte('#3a3c3f'), 0.3, 0.003, 0.4, x, 0.77, z);
          cy(g, pl, 0.13, 0.1, 0.015, x, 0.773, z, 32);
          const bw = mesh(g, new T3.SphereGeometry(0.065, 20, 10, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), pl, x, 0.855, z); bw.material.side = T3.DoubleSide;
          cy(g, M.glass, 0.035, 0.03, 0.14, x - sx * 0.12, 0.773, z - 0.14 * Math.sign(sz));
          bx(g, M.steel, 0.012, 0.004, 0.18, x + sx * 0.0 - 0.02, 0.774, z + 0.19 * 0);
        }
        const sb = mesh(g, new T3.SphereGeometry(0.14, 24, 12, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), ceramicM('#f5f4f0'), 0, 0.9, 0); sb.material = ceramicM('#f5f4f0');
        instLeaves(g, 22, R, () => [(R() - 0.5) * 0.16, 0.87 + R() * 0.04, (R() - 0.5) * 0.16, 1], ['#7fb35a', '#5f9a47', '#b8455a'], 0.03);
      }
      break; }
    case 'silla': {
      const f = fabric(col), blk = std('blkMetal', { color: '#1b1c1e', roughness: 0.5, metalness: 0.6 });
      for (const sx of [-1, 1]) for (const sz of [-1, 1]){ const l = cy(g, blk, 0.016, 0.009, 0.46, sx * 0.17, 0, sz * 0.17); l.rotation.set(sz * 0.1, 0, -sx * 0.1); }
      rb(g, f, 0.48, 0.09, 0.46, 0.035, 0, 0.44, 0.03);
      const shell = mesh(g, new T3.CylinderGeometry(0.27, 0.24, 0.46, 24, 1, true, Math.PI - 1.25, 2.5), std('fd' + col, { color: col, roughness: 0.9, side: T3.DoubleSide }), 0, 0.72, 0.02);
      shell.scale.set(1, 1, 0.9);
      break; }
    case 'lampara_colgante': {
      const bot = 1.72, blk = metal(col === '#c9a44c' ? '#c9a44c' : '#1f2224', 0.45);
      cy(g, blk, 0.035, 0.035, 0.02, 0, H - 0.02, 0);
      cy(g, M.black, 0.003, 0.003, H - bot - 0.25, 0, bot + 0.25, 0);
      mesh(g, new T3.ConeGeometry(0.05, 0.06, 20), blk, 0, bot + 0.22, 0);
      const cage = new T3.LineSegments(new T3.EdgesGeometry(new T3.CylinderGeometry(0.06, 0.11, 0.2, 6, 2)), new T3.LineBasicMaterial({ color: col === '#c9a44c' ? '#c9a44c' : '#1f2224' }));
      cage.position.set(0, bot + 0.1, 0); g.add(cage);
      mesh(g, new T3.SphereGeometry(0.045, 16, 12), M.bulb, 0, bot + 0.1, 0).castShadow = false;
      break; }
    case 'lampara_tripode': {
      const wd = woodM(col);
      for (let k = 0; k < 3; k++){ const a = k / 3 * Math.PI * 2; const l = cy(g, wd, 0.015, 0.02, 1.3, Math.cos(a) * 0.14, 0, Math.sin(a) * 0.14); l.rotation.set(Math.sin(a) * 0.2, 0, -Math.cos(a) * 0.2); }
      cy(g, M.black, 0.03, 0.03, 0.08, 0, 1.24, 0);
      const cage = new T3.LineSegments(new T3.EdgesGeometry(new T3.SphereGeometry(0.16, 8, 6)), new T3.LineBasicMaterial({ color: '#a0843f' }));
      cage.position.set(0, 1.45, 0); g.add(cage);
      mesh(g, new T3.SphereGeometry(0.05, 16, 12), M.bulb, 0, 1.45, 0).castShadow = false;
      break; }
    case 'lampara_pie': {
      const m = metal(col === '#e6e2da' ? '#d6d2ca' : col, 0.4);
      cy(g, m, 0.15, 0.16, 0.025, 0, 0, 0); cy(g, m, 0.012, 0.012, 1.4, 0, 0.025, 0);
      mesh(g, cylG(0.17, 0.21, 0.3, 28, true), M.lamp, 0, 1.52, 0);
      break; }
    case 'cuadro': {
      const hgt = w * 0.75, ch = it.alto || 1.5;
      bx(g, M.black, w, hgt, 0.03, 0, ch - hgt / 2, -D + 0.015);
      bx(g, std('art' + it.id, { map: artTex(hashStr(it.id)), roughness: 0.8 }), w - 0.06, hgt - 0.06, 0.004, 0, ch - hgt / 2 + 0.03, -D + 0.032);
      break; }
    case 'planta': {
      const pts = [[0.001, 0], [0.13, 0], [0.16, 0.05], [0.18, 0.3], [0.19, 0.34], [0.17, 0.34], [0.16, 0.31]].map(([x, y]) => new T3.Vector2(x, y));
      mesh(g, new T3.LatheGeometry(pts, 28), ceramicM(col), 0, 0, 0);
      cy(g, M.soil, 0.16, 0.16, 0.01, 0, 0.3, 0);
      instLeaves(g, 26, R, () => { const a = R() * 6.283, r = 0.03 + R() * 0.2; return [Math.cos(a) * r, 0.45 + R() * 0.75, Math.sin(a) * r, 1.4 + R()]; });
      for (let i = 0; i < 4; i++){ const st = cy(g, matte('#5b4a33'), 0.01, 0.014, 0.8, (R() - 0.5) * 0.08, 0.3, (R() - 0.5) * 0.08); st.rotation.z = (R() - 0.5) * 0.3; }
      break; }
    case 'jardin_vertical': {
      const y0 = 0.35, hh = 1.6;
      bx(g, matte('#2f3336'), w, hh, 0.03, 0, y0, -D + 0.015);
      for (let r = 0; r < 5; r++) bx(g, matte('#3a3d40'), w - 0.02, 0.07, 0.08, 0, y0 + 0.05 + r * 0.32, -D + 0.07);
      instLeaves(g, Math.round(w * 170), R, () => [(R() - 0.5) * (w - 0.04), y0 + 0.05 + R() * (hh - 0.1), -D + 0.05 + R() * 0.08, 0.8 + R() * 0.9], ['#4f7a45', '#5f8c4f', '#3f6a3b', '#6d9a57', '#8fb86a', '#2f5a2b'], 0.05);
      instLeaves(g, 14, R, () => [(R() - 0.5) * (w - 0.1), y0 + 0.1 + R() * (hh - 0.2), -D + 0.12, 0.5], ['#e7a1b0', '#f2d06b', '#ffffff'], 0.03);
      break; }
    case 'jardinera': {
      const y0 = 0.72;
      for (const sx of [-1, 1]) bx(g, M.black, 0.02, 0.28, 0.04, sx * (W - 0.1), y0 + 0.15, -D + 0.01);
      rb(g, satin(col), w, 0.18, d - 0.02, 0.01, 0, y0, 0.01);
      cy(g, M.soil, 0.001, 0.001, 0.001, 0, y0 + 0.17, 0);
      bx(g, M.soil, w - 0.03, 0.01, d - 0.05, 0, y0 + 0.16, 0.01);
      instLeaves(g, Math.round(w * 60), R, () => [(R() - 0.5) * (w - 0.05), y0 + 0.2 + R() * 0.2, (R() - 0.5) * 0.12, 0.8 + R() * 0.6]);
      instLeaves(g, Math.round(w * 14), R, () => [(R() - 0.5) * (w - 0.05), y0 + 0.3 + R() * 0.15, (R() - 0.5) * 0.12, 0.6], ['#d94f5c', '#f2d06b', '#b86fd9'], 0.03);
      break; }
    case 'urinario_perro': {
      rb(g, satin('#4f5358'), w, 0.05, d, 0.012, 0, 0, 0);
      bx(g, std('grassTop', { map: grassTex(), roughness: 1 }), w - 0.05, 0.012, d - 0.05, 0, 0.05, 0);
      const n = 260, geo = new T3.ConeGeometry(0.004, 0.04, 3);
      const im = new T3.InstancedMesh(geo, std('blade', { color: '#ffffff', roughness: 0.9 }), n); const m4 = new T3.Matrix4(), c = new T3.Color();
      for (let i = 0; i < n; i++){ m4.makeRotationZ((R() - 0.5) * 0.6); m4.setPosition((R() - 0.5) * (w - 0.06), 0.08, (R() - 0.5) * (d - 0.06)); im.setMatrixAt(i, m4); im.setColorAt(i, c.set(['#5f9a47', '#3f6a30', '#7ab35a'][i % 3])); }
      g.add(im);
      break; }
    case 'mesa_balcon': {
      cy(g, metal(col, 0.5), 0.3, 0.3, 0.025, 0, 0.72, 0); cy(g, metal(col, 0.5), 0.02, 0.02, 0.72, 0, 0, 0); cy(g, metal(col, 0.5), 0.2, 0.22, 0.02, 0, 0, 0);
      break; }
    case 'librero': {
      const m = woodM(col), hh = 1.9;
      for (const sx of [-1, 1]) bx(g, m, 0.02, hh, d, sx * (W - 0.01), 0, 0);
      for (let k = 0; k < 6; k++) bx(g, m, w - 0.04, 0.02, d, 0, k * (hh - 0.02) / 5, 0);
      bx(g, m, w, hh, 0.01, 0, 0, -D + 0.005);
      const bc = ['#3f4a57', '#b9876a', '#6f7d6a', '#d8c9a8', '#8d3f35', '#2f3336', '#c9a66b'];
      for (let k = 0; k < 5; k++){ let x = -W + 0.04; const y = k * (hh - 0.02) / 5 + 0.02; while (x < W - 0.12){ const bw = 0.02 + R() * 0.03, bh = 0.2 + R() * 0.12; if (R() < 0.85) bx(g, matte(bc[Math.floor(R() * bc.length)]), bw, bh, d * 0.75, x + bw / 2, y, 0); x += bw + 0.004; if (R() < 0.08) x += 0.12; } }
      break; }
    case 'cocina_lineal': {
      const mel = satin(col), carc = matte('#e9e8e4');
      const hx = Math.max(-W + 0.35, -0.47), hw = 0.56, sx = Math.min(W - 0.4, 0.59);
      const segs = [[-W, hx - hw / 2], [hx + hw / 2, W]];
      for (const [a, b] of segs){
        const sw = b - a; if (sw < 0.2) continue; const cx = (a + b) / 2;
        bx(g, M.black, sw, 0.1, d - 0.08, cx, 0, -0.04);
        carcass(g, carc, sw, 0.76, d - 0.03, cx, 0.1, -0.015);
        bx(g, carc, sw - 0.04, 0.015, d - 0.08, cx, 0.45, -0.03);
        const n = Math.max(1, Math.round(sw / 0.5)), fw = sw / n;
        for (let i = 0; i < n; i++){
          const x = a + fw * (i + 0.5);
          hingeDoor(g, mel, fw, 0.72, x, 0.12, D - 0.03, i % 2 ? 1 : -1);
          if (Math.abs(x - sx) > 0.3){ plates(g, x - 0.08, 0.47, -0.05, 5); cy(g, M.steel, 0.1, 0.1, 0.12, x + 0.1, 0.13, -0.05); }
        }
        rb(g, graniteMat, sw + 0.005, 0.035, d + 0.02, 0.004, cx, 0.86, 0.005);
      }
      // poza de acero inoxidable y grifería
      bx(g, M.steel, 0.52, 0.006, 0.44, sx, 0.895, 0.02);
      bx(g, metal('#8f959b', 0.35), 0.44, 0.004, 0.36, sx, 0.9, 0.02);
      cy(g, M.chrome, 0.016, 0.02, 0.22, sx, 0.895, -D + 0.07);
      const sp = mesh(g, new T3.TorusGeometry(0.08, 0.011, 8, 20, Math.PI), M.chrome, sx, 1.115, -D + 0.15); sp.rotation.y = Math.PI / 2;
      bx(g, M.chrome, 0.012, 0.012, 0.09, sx + 0.04, 1.02, -D + 0.07);
      // accesorios sobre el tablero
      const fx = hx + hw / 2 + 0.25;
      if (fx < sx - 0.35){ const fb = mesh(g, new T3.SphereGeometry(0.12, 20, 10, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), ceramicM('#f5f4f0'), fx, 1.02, -0.05); fb.material = ceramicM('#f5f4f0');
        for (const [c, dx, dz] of [['#f2c14e', -0.04, 0], ['#d94f3c', 0.04, 0.02], ['#e8912f', 0, -0.05], ['#7fb35a', 0.02, 0.05]]) mesh(g, new T3.SphereGeometry(0.04, 12, 10), satin(c), fx + dx, 0.95, -0.05 + dz); }
      const kx = -W + 0.18; if (kx < hx - hw / 2 - 0.1){ cy(g, satin('#2f3336'), 0.07, 0.08, 0.2, kx, 0.895, -0.1); bx(g, M.black, 0.03, 0.12, 0.02, kx + 0.09, 0.95, -0.1); }
      // muebles altos y campana
      carcass(g, carc, w, 0.7, 0.34, 0, 1.5, -D + 0.17);
      bx(g, carc, w - 0.04, 0.015, 0.3, 0, 1.84, -D + 0.17);
      const n = Math.max(2, Math.round(w / 0.5)), fw = w / n;
      for (let i = 0; i < n; i++){
        const x = -W + fw * (i + 0.5);
        const dr = hingeDoor(g, mel, fw, 0.68, x, 1.51, -D + 0.34, i % 2 ? 1 : -1, null);
        bx(dr, M.steel, 0.16, 0.012, 0.02, -(i % 2 ? 1 : -1) * fw / 2, 0.04, 0.03);
        for (let k = 0; k < 3; k++) cy(g, M.glass, 0.035, 0.03, 0.11, x - 0.1 + k * 0.1, 1.86, -D + 0.17);
        plates(g, x, 1.525, -D + 0.17, 4, 0.1);
      }
      bx(g, M.steel, 0.6, 0.1, 0.32, hx, 1.4, -D + 0.16);
      bx(g, M.lamp, w - 0.1, 0.01, 0.03, 0, 1.49, -D + 0.3).castShadow = false;
      break; }
    case 'cocina_4h': {
      const body = col === '#2f3336' ? satin(col) : ceramicM(col), dark = std('ovenIn', { color: '#1c1d1f', roughness: 0.6 });
      carcass(g, body, w, 0.84, d - 0.02, 0, 0.04, -0.01, 0.02, dark);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(g, M.black, 0.02, 0.02, 0.04, sx * (W - 0.05), 0, sz * (D - 0.06));
      bx(g, dark, w - 0.06, 0.012, d - 0.1, 0, 0.3, -0.02);
      for (let k = 0; k < 6; k++) bx(g, M.steel, 0.006, 0.006, d - 0.12, -W + 0.07 + k * (w - 0.14) / 5, 0.42, -0.02);
      bx(g, M.steel, w - 0.02, 0.012, d - 0.02, 0, 0.88, -0.01);
      for (const [dx, dz, r] of [[-0.12, -0.12, 0.045], [0.12, -0.12, 0.035], [-0.12, 0.12, 0.035], [0.12, 0.12, 0.05]]){ cy(g, metal('#3a3c3f', 0.4), r + 0.01, r + 0.015, 0.016, dx, 0.892, -0.01 + dz); cy(g, M.black, r, r, 0.012, dx, 0.908, -0.01 + dz); }
      for (const dz of [-0.2, -0.12, -0.04, 0.04, 0.12, 0.2]) bx(g, metal('#2a2b2d', 0.5), w - 0.04, 0.01, 0.01, 0, 0.93, -0.01 + dz);
      for (const dx of [-0.2, 0, 0.2]) bx(g, metal('#2a2b2d', 0.5), 0.01, 0.01, d - 0.08, dx, 0.93, -0.01);
      bx(g, body, w, 0.1, 0.02, 0, 0.77, D - 0.02);
      for (let k = 0; k < 5; k++){ const kn = cy(g, M.black, 0.018, 0.018, 0.025, -W + 0.07 + k * (w - 0.14) / 4, 0.8, D); kn.rotation.x = Math.PI / 2; kn.position.set(-W + 0.07 + k * (w - 0.14) / 4, 0.82, D); }
      const door = openable(g, 0, 0.1, D - 0.01, 'rx', 0, 1.45);
      bx(door, body, w - 0.02, 0.62, 0.025, 0, 0, 0.012);
      bx(door, std('ovenGlass', { color: '#101214', roughness: 0.05, metalness: 0.3 }), w - 0.14, 0.3, 0.004, 0, 0.18, 0.026);
      const hd = cy(door, M.steel, 0.012, 0.012, w - 0.1, 0, 0.56, 0.05); hd.rotation.z = Math.PI / 2; hd.position.set(0, 0.56, 0.05);
      drawer(g, body, w - 0.02, 0.05, d - 0.12, 0, 0.045, D - 0.01, M.steel);
      const lid = openable(g, 0, 0.94, -D + 0.02, 'rx', -1.45, 0);
      bx(lid, std('lidGlass', { color: '#20262b', roughness: 0.05, metalness: 0.2, transparent: true, opacity: 0.55 }), w - 0.02, 0.008, d - 0.04, 0, 0, (d - 0.04) / 2);
      ops[ops.length - 1].state = false;
      break; }
    case 'microondas': {
      const body = col === '#2f3336' ? satin(col) : metal(col, 0.35);
      carcass(g, body, w, 0.28, d, 0, 0, 0, 0.012, matte('#e8e6e1'));
      cy(g, M.glass, 0.12, 0.12, 0.006, -0.05, 0.015, 0, 28);
      bx(g, satin('#1f2224'), 0.12, 0.26, 0.02, W - 0.06, 0.01, D - 0.005);
      bx(g, std('mwDisp', { color: '#081018', emissive: '#6fe3a1', emissiveIntensity: 1 }), 0.07, 0.025, 0.003, W - 0.06, 0.22, D + 0.006);
      const dr = openable(g, -W, 0.01, D - 0.01, 'ry', 0, -1.6);
      bx(dr, satin('#1f2224'), w - 0.13, 0.26, 0.02, (w - 0.13) / 2, 0, 0.01);
      bx(dr, std('mwGlass', { color: '#0b0d0f', roughness: 0.05, metalness: 0.4 }), w - 0.2, 0.18, 0.004, (w - 0.13) / 2 - 0.01, 0.04, 0.021);
      break; }
    case 'refrigeradora': {
      const m = col === '#2f3336' ? satin(col) : metal(col, 0.35), inner = satin('#f4f5f5');
      carcass(g, m, w, 1.75, d - 0.06, 0, 0, -0.03, 0.03, inner);
      bx(g, inner, w - 0.06, 0.03, d - 0.1, 0, 1.18, -0.03);
      for (const y of [0.45, 0.8]) bx(g, M.glass, w - 0.07, 0.008, d - 0.12, 0, y, -0.03);
      bx(g, M.lamp, 0.1, 0.01, 0.04, 0, 1.15, -0.1).castShadow = false;
      bottles(g, -W + 0.1, W - 0.1, 0.81, -0.08, R, 5);
      rb(g, satin('#f2c14e'), 0.14, 0.1, 0.12, 0.02, -0.12, 0.46, -0.05); rb(g, satin('#d94f3c'), 0.18, 0.08, 0.14, 0.02, 0.12, 0.46, -0.08);
      for (let k = 0; k < 4; k++) mesh(g, new T3.SphereGeometry(0.035, 12, 10), satin(['#7fb35a', '#d94f3c', '#f2c14e', '#e8912f'][k]), -0.15 + k * 0.1, 0.07, 0.0);
      rb(g, satin('#e6f0f4'), 0.18, 0.08, 0.2, 0.02, -0.1, 1.22, -0.05); rb(g, satin('#e6f0f4'), 0.18, 0.08, 0.2, 0.02, 0.12, 1.22, -0.05);
      const doorF = (y0, h) => {
        const pv = hingeDoor(g, m, w, h, 0, y0, D - 0.03, 1, null, 0.04, 1.8);
        bx(pv, M.aluDark, 0.022, Math.min(0.5, h * 0.55), 0.035, -w + 0.06, h * 0.25, 0.06);
        bx(pv, inner, w - 0.1, 0.006, 0.08, -w / 2, h * 0.2, -0.04); bx(pv, inner, w - 0.1, 0.006, 0.08, -w / 2, h * 0.6, -0.04);
        bx(pv, M.glass, w - 0.1, 0.06, 0.006, -w / 2, h * 0.2, -0.08); bx(pv, M.glass, w - 0.1, 0.06, 0.006, -w / 2, h * 0.6, -0.08);
        return pv;
      };
      const fr = doorF(0.01, 1.16); const fz = doorF(1.19, 0.55);
      bottles(fr, -w + 0.1, -0.08, 0.235, -0.04, R, 4);
      void fz;
      break; }
    case 'lavadero': {
      const c = ceramicM('#f6f6f4');
      for (const sx of [-1, 1]) bx(g, c, 0.07, 0.6, d - 0.08, sx * (W - 0.05), 0, -0.02);
      rb(g, c, w, 0.3, d, 0.025, 0, 0.6, 0);
      bx(g, ceramicM('#d9dcde'), w - 0.1, 0.004, d * 0.46, 0, 0.9, D - d * 0.25 - 0.03);
      for (let k = 0; k < 6; k++) bx(g, c, w - 0.12, 0.012, 0.02, 0, 0.9, -D + 0.06 + k * 0.035);
      cy(g, M.chrome, 0.012, 0.012, 0.25, 0, 0.9, -D + 0.02);
      bx(g, M.chrome, 0.14, 0.018, 0.018, 0, 1.13, -D + 0.02); bx(g, M.chrome, 0.018, 0.018, 0.1, 0, 1.08, -D + 0.07);
      break; }
    case 'lavadora': {
      // carga superior: tapa de vidrio con bisagra atrás y tambor visible
      const m = col === '#3a3d40' ? satin(col) : (col === '#f4f4f2' ? ceramicM(col) : metal(col, 0.4)), hh = 0.9;
      rb(g, m, w, hh, d, 0.03, 0, 0, 0);
      bx(g, m, w, 0.012, d, 0, hh, 0); // se reemplaza visualmente por el marco
      const top = std('lgTop', { color: '#2b2e31', roughness: 0.3 });
      bx(g, top, w - 0.04, 0.006, d - 0.2, 0, hh + 0.012, 0.06);
      const drum = mesh(g, new T3.CylinderGeometry(0.25, 0.25, 0.5, 32, 1, true), std('drum', { color: '#c9cdd1', roughness: 0.3, metalness: 0.9, side: T3.DoubleSide }), 0, hh - 0.24, 0.06);
      cy(g, std('pulsator', { color: '#e9ecef', roughness: 0.4 }), 0.2, 0.22, 0.04, 0, hh - 0.5, 0.06);
      const ring = mesh(g, new T3.TorusGeometry(0.255, 0.018, 10, 40), std('lgRing', { color: '#1e2124', roughness: 0.3 }), 0, hh + 0.02, 0.06); ring.rotation.x = Math.PI / 2;
      void drum;
      rb(g, m, w, 0.16, 0.14, 0.03, 0, hh, -D + 0.07);
      bx(g, std('lgPanel', { color: '#15181b', roughness: 0.2 }), w - 0.1, 0.1, 0.004, 0, hh + 0.04, -D + 0.142);
      bx(g, std('lgDisp', { color: '#081018', emissive: '#ff5a5a', emissiveIntensity: 1.1 }), 0.08, 0.035, 0.003, 0.12, hh + 0.075, -D + 0.146);
      cy(g, M.chrome, 0.035, 0.035, 0.02, -0.12, hh + 0.09, -D + 0.14).rotation.x = Math.PI / 2;
      const lid = openable(g, 0, hh + 0.02, -D + 0.16, 'rx', 0, -1.3);
      rb(lid, std('lgLid', { color: '#1a2026', roughness: 0.05, metalness: 0.3, transparent: true, opacity: 0.6 }), w - 0.04, 0.015, d - 0.2, 0.01, 0, 0, (d - 0.2) / 2);
      bx(lid, std('lgLidF', { color: '#2b2e31', roughness: 0.3 }), 0.18, 0.02, 0.03, 0, 0.005, d - 0.2);
      break; }
    case 'terma': {
      rb(g, ceramicM('#f5f5f3'), w, 0.72, d, 0.05, 0, 1.3, 0);
      bx(g, M.black, 0.1, 0.04, 0.01, 0, 1.6, D);
      for (const sx of [-0.1, 0, 0.1]) cy(g, metal('#b87333', 0.35), 0.012, 0.012, 0.25, sx, 1.05, 0);
      break; }
    case 'caminadora': {
      const frame = satin(col), black = std('tmBlack', { color: '#161718', roughness: 0.85 });
      for (const sx of [-1, 1]) rb(g, frame, 0.09, 0.13, d - 0.1, 0.02, sx * (W - 0.05), 0.03, 0.04);
      bx(g, black, w - 0.2, 0.03, d - 0.4, 0, 0.12, 0.12);
      bx(g, satin('#3a3d40'), w - 0.2, 0.02, d - 0.4, 0, 0.1, 0.12);
      rb(g, frame, w - 0.02, 0.22, 0.34, 0.06, 0, 0.03, -D + 0.18);
      bx(g, std('tmAccent', { color: '#1b1c1e', emissive: '#2fd27a', emissiveIntensity: 0.6 }), w - 0.1, 0.012, 0.004, 0, 0.18, -D + 0.352);
      bx(g, frame, w - 0.18, 0.06, 0.08, 0, 0.05, D - 0.06);
      for (const sx of [-1, 1]){
        const up = bx(g, frame, 0.06, 1.2, 0.08, sx * (W - 0.06), 0.18, -D + 0.24); up.rotation.x = -0.18;
        bx(g, black, 0.04, 0.04, 0.42, sx * (W - 0.08), 1.02, -D + 0.5);
      }
      const bar = cy(g, black, 0.02, 0.02, w - 0.1, 0, 1.12, -D + 0.3); bar.rotation.z = Math.PI / 2; bar.position.y = 1.12;
      const con = new T3.Group(); con.position.set(0, 1.3, -D + 0.14); con.rotation.x = -0.45; g.add(con);
      rb(con, frame, 0.72, 0.46, 0.1, 0.03, 0, -0.23, 0);
      const sc = bx(con, screenMat('android'), 0.56, 0.34, 0.004, 0, -0.18, 0.051); sc.castShadow = false;
      for (const sx of [-1, 1]) bx(con, std('tmBtn', { color: '#1b1c1e', emissive: '#ff8a3d', emissiveIntensity: 0.5 }), 0.04, 0.12, 0.01, sx * 0.32, -0.08, 0.05);
      break; }
    case 'estante': {
      const m = metal('#8a8f94', 0.5);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, m, 0.03, 1.8, 0.03, sx * (W - 0.015), 0, sz * (D - 0.015));
      for (let k = 0; k < 5; k++) bx(g, m, w, 0.02, d, 0, 0.05 + k * 0.42, 0);
      for (let k = 0; k < 4; k++){ let x = -W + 0.05; while (x < W - 0.2){ const bw = 0.2 + R() * 0.2; if (R() < 0.75){ const bh = 0.15 + R() * 0.18; rb(g, M.cardboard, bw, bh, d * 0.8, 0.006, x + bw / 2, 0.07 + k * 0.42, 0); } x += bw + 0.03; } }
      break; }
    case 'inodoro': {
      const c = M.white;
      rb(g, c, 0.24, 0.36, 0.36, 0.06, 0, 0, 0.05);
      const bowl = mesh(g, new T3.SphereGeometry(0.2, 28, 16, 0, Math.PI * 2, 0, Math.PI / 2), c, 0, 0.42, 0.1); bowl.scale.set(0.95, -0.55, 1.25);
      const seat = mesh(g, new T3.TorusGeometry(0.155, 0.03, 10, 32), c, 0, 0.425, 0.1); seat.rotation.x = Math.PI / 2; seat.scale.set(1.18, 1.45, 0.4);
      const lid = openable(g, 0, 0.44, -D + 0.2, 'rx', -1.5, 0);
      const lm = mesh(lid, new T3.CylinderGeometry(0.19, 0.19, 0.02, 32), c, 0, 0.01, 0.22); lm.scale.set(0.95, 1, 1.2);
      rb(g, c, 0.39, 0.36, 0.17, 0.03, 0, 0.42, -D + 0.1);
      rb(g, c, 0.41, 0.035, 0.19, 0.012, 0, 0.78, -D + 0.1);
      cy(g, M.chrome, 0.022, 0.022, 0.012, 0, 0.815, -D + 0.1);
      break; }
    case 'lavatorio': {
      const open = !!it.abierto, m = satin(col);
      if (open){
        for (const sx of [-1, 1]) bx(g, m, 0.02, 0.7, d - 0.04, sx * (W - 0.01), 0.08, -0.02);
        bx(g, m, w, 0.02, d - 0.04, 0, 0.12, -0.02); bx(g, m, w, 0.02, d - 0.04, 0, 0.45, -0.02);
        rb(g, fabric('#d8d2c6'), w * 0.5, 0.06, d * 0.5, 0.02, -W * 0.3, 0.14, 0);
        bottles(g, 0, W - 0.04, 0.47, -0.02, R, 3);
      } else {
        carcass(g, m, w, 0.7, d - 0.04, 0, 0.08, -0.02, 0.016, matte('#efece6'));
        bottles(g, -W + 0.06, W - 0.06, 0.1, -0.05, R, 4);
        const n = w > 0.6 ? 2 : 1, fw = w / n;
        for (let i = 0; i < n; i++) hingeDoor(g, satin(shade(col, 1.03)), fw, 0.66, -W + fw * (i + 0.5), 0.1, D - 0.02, i % 2 ? 1 : -1);
      }
      rb(g, M.white, w + 0.01, 0.1, d, 0.02, 0, 0.78, 0);
      const bs = mesh(g, new T3.SphereGeometry(0.17, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), ceramicM('#e3e7ea'), 0, 0.885, 0.03); bs.scale.set(Math.min(1, (w - 0.1) / 0.36), -0.35, 0.8);
      cy(g, M.chrome, 0.018, 0.022, 0.14, 0, 0.88, -D + 0.06);
      bx(g, M.chrome, 0.02, 0.02, 0.1, 0, 1.0, -D + 0.1);
      cy(g, satin('#e8d9c4'), 0.03, 0.03, 0.14, W - 0.08, 0.88, -D + 0.08);
      bx(g, M.aluDark, w, 0.72, 0.012, 0, 1.12, -D + 0.006);
      bx(g, M.mirror, w - 0.03, 0.69, 0.006, 0, 1.135, -D + 0.015);
      break; }
    case 'alfombra_bano': {
      rb(g, fabric(col), w, 0.018, d, 0.008, 0, 0.002, 0).castShadow = false;
      for (let k = 0; k < 5; k++) bx(g, fabric(shade(col, 0.88)), w - 0.08, 0.002, 0.012, 0, 0.02, -D + 0.07 + k * (d - 0.14) / 4);
      break; }
    case 'toallero': {
      const y = 1.1;
      for (const sx of [-1, 1]) bx(g, M.chrome, 0.02, 0.04, 0.07, sx * (W - 0.03), y - 0.02, -D + 0.035);
      const rod = cy(g, M.chrome, 0.009, 0.009, w - 0.04, 0, y, -D + 0.07); rod.rotation.z = Math.PI / 2; rod.position.y = y;
      rb(g, fabric(col), w * 0.65, 0.5, 0.012, 0.004, 0, y - 0.48, -D + 0.085);
      rb(g, fabric(col), w * 0.65, 0.42, 0.012, 0.004, 0, y - 0.4, -D + 0.055);
      rb(g, fabric(col), w * 0.65, 0.03, 0.04, 0.012, 0, y - 0.005, -D + 0.07);
      break; }
    case 'portapapel': {
      const y = 0.72;
      bx(g, M.chrome, 0.06, 0.06, 0.012, 0, y - 0.03, -D + 0.006);
      const arm = cy(g, M.chrome, 0.006, 0.006, 0.14, 0, y, -D + 0.07); arm.rotation.z = Math.PI / 2; arm.position.set(0.02, y, -D + 0.06);
      const roll = cy(g, M.white, 0.055, 0.055, 0.1, 0, y, -D + 0.06, 24); roll.rotation.z = Math.PI / 2; roll.position.set(0.03, y, -D + 0.06);
      break; }
    case 'papelera': {
      const m = col === '#2f3336' ? satin(col) : metal(col, 0.3);
      cy(g, m, 0.11, 0.1, 0.28, 0, 0, 0, 24);
      const lid = openable(g, 0, 0.285, -0.11, 'rx', 0, -1.3);
      cy(lid, m, 0.112, 0.112, 0.012, 0, 0, 0.11, 24);
      bx(g, M.black, 0.06, 0.012, 0.04, 0, 0.01, 0.11);
      break; }
    case 'repisa_bano': {
      const m = woodM(col);
      for (let k = 0; k < 3; k++) bx(g, m, w, 0.018, d, 0, 1.25 + k * 0.22, 0);
      for (const sx of [-1, 1]) bx(g, M.chrome, 0.012, 0.46, 0.012, sx * (W - 0.02), 1.25, D - 0.01);
      bottles(g, -W + 0.04, W - 0.04, 1.268, 0, R, 4);
      for (let k = 0; k < 3; k++){ const t = cy(g, fabric(['#e8e2d6', '#9fb3a8', '#c9b89a'][k]), 0.04, 0.04, 0.12, -W + 0.08 + k * 0.12, 1.51, 0); t.rotation.z = Math.PI / 2; t.position.y = 1.53; }
      cy(g, M.glass, 0.04, 0.035, 0.1, 0.05, 1.708, 0);
      instLeaves(g, 8, R, () => [-0.1 + (R() - 0.5) * 0.06, 1.76 + R() * 0.06, (R() - 0.5) * 0.06, 1], undefined, 0.03);
      break; }
    default: bx(g, matte('#b0b0b0'), w, 0.6, d, 0, 0, 0);
  }
  OPS_CUR = null;
  g.userData.ops = ops;
  return g;
}
