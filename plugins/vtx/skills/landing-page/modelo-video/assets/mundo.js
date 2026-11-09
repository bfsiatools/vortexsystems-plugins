/* MUNDO 3D do video "proximos passos" (modelo para qualquer casa).
   Diorama baixo-poli feito so com formas simples. Tudo e funcao do tempo t (hf-seek).
   Logo do cliente e arte da plaquinha entram como TEXTURA SEM LUZ (MeshBasicMaterial): arte original, sem recolorir. */
(function () {
  var T = THREE, W = 1080, H = 1920;
  var renderer = new T.WebGLRenderer({ canvas: document.getElementById("mundo"), antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.setClearColor(0x000000, 0);
  var scene = new T.Scene();
  var camera = new T.PerspectiveCamera(46, W / H, 0.1, 400);

  scene.add(new T.HemisphereLight(0xfff4ec, 0xb5a2f2, 2.1));
  var sun = new T.DirectionalLight(0xffe6c0, 1.5);
  sun.position.set(-14, 26, 22);
  scene.add(sun);
  var rim = new T.DirectionalLight(0xa874ff, 0.6);
  rim.position.set(18, 10, -14);
  scene.add(rim);

  /* ---------- utilidades ---------- */
  function ease(x) { x = Math.max(0, Math.min(1, x)); return x * x * x * (x * (x * 6 - 15) + 10); }
  function clamp01(x) { return Math.max(0, Math.min(1, x)); }
  function seg(t, a, b) { return clamp01((t - a) / (b - a)); }
  function rnd(i) { var t = (i * 1831565813 + 0x6D2B79F5) | 0; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }
  function track(t, keys) {
    if (t <= keys[0][0]) return keys[0][1].slice();
    for (var i = 0; i < keys.length - 1; i++) {
      if (t < keys[i + 1][0]) {
        var k = ease((t - keys[i][0]) / (keys[i + 1][0] - keys[i][0])), a = keys[i][1], b = keys[i + 1][1], o = [];
        for (var j = 0; j < a.length; j++) o.push(a[j] + (b[j] - a[j]) * k);
        return o;
      }
    }
    return keys[keys.length - 1][1].slice();
  }
  function mat(c, o) { return new T.MeshStandardMaterial(Object.assign({ color: c, flatShading: true, roughness: 0.95, metalness: 0 }, o || {})); }
  function box(p, w, h, d, c, x, y, z, o) { var m = new T.Mesh(new T.BoxGeometry(w, h, d), mat(c, o)); m.position.set(x, y, z); p.add(m); return m; }
  function cyl(p, rt, rb, h, seg, c, x, y, z, o) { var m = new T.Mesh(new T.CylinderGeometry(rt, rb, h, seg), mat(c, o)); m.position.set(x, y, z); p.add(m); return m; }
  function sph(p, r, c, x, y, z, o, det) { var m = new T.Mesh(new T.IcosahedronGeometry(r, det === undefined ? 1 : det), mat(c, o)); m.position.set(x, y, z); p.add(m); return m; }
  function blob(p, x, z, r, op) { var m = new T.Mesh(new T.CircleGeometry(r, 20), new T.MeshBasicMaterial({ color: 0x07041a, transparent: true, opacity: op || 0.35, depthWrite: false })); m.rotation.x = -Math.PI / 2; m.position.set(x, 0.03, z); p.add(m); return m; }

  /* ---------- texturas (arte real, sem luz) ---------- */
  var loader = new T.TextureLoader(), pend = [];
  function tex(url) {
    return new Promise(function (ok) {
      loader.load(url, function (t) { t.colorSpace = T.SRGBColorSpace; t.anisotropy = 4; ok(t); }, undefined, function () { ok(null); });
    });
  }
  var logoMat = new T.MeshBasicMaterial({ color: 0xffffff }), plaqMat = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, alphaTest: 0.35, side: T.DoubleSide });
  pend.push(tex("assets/cliente/{{LOGO}}").then(function (t) { if (t) { logoMat.map = t; logoMat.needsUpdate = true; } }));
  pend.push(tex("assets/produto/plaquinha-nfc_frontal.png").then(function (t) { if (t) { plaqMat.map = t; plaqMat.needsUpdate = true; } }));

  /* ---------- pessoas (boneco de blocos, olha para +z) ---------- */
  function person(o) {
    var g = new T.Group(), u = g.userData;
    function limb(w, h, d, c, x, y) { var j = new T.Group(); j.position.set(x, y, 0); var m = new T.Mesh(new T.BoxGeometry(w, h, d), mat(c)); m.position.y = -h / 2; j.add(m); g.add(j); return j; }
    u.legL = limb(0.4, 1.05, 0.42, o.pants, -0.22, 1.05);
    u.legR = limb(0.4, 1.05, 0.42, o.pants, 0.22, 1.05);
    box(g, 1.05, 1.25, 0.62, o.shirt, 0, 1.68, 0);
    if (o.apron) box(g, 0.8, 0.9, 0.05, o.apron, 0, 1.5, 0.34);
    u.armL = limb(0.3, 1.05, 0.3, o.shirt, 0.72, 2.2);
    u.armR = limb(0.3, 1.05, 0.3, o.shirt, -0.72, 2.2);
    [u.armL, u.armR].forEach(function (a) { sph(a, 0.2, o.skin, 0, -1.08, 0, null, 0); });
    u.head = new T.Group(); u.head.position.set(0, 2.9, 0); g.add(u.head);
    sph(u.head, 0.68, o.skin, 0, 0, 0, null, 1);
    var hair = new T.Mesh(new T.SphereGeometry(0.72, 8, 5, 0, Math.PI * 2, 0, Math.PI * 0.52), mat(o.hair)); hair.position.set(0, 0.06, -0.04); u.head.add(hair);
    if (o.cap) { box(u.head, 1.1, 0.34, 1.1, o.cap, 0, 0.58, 0); box(u.head, 0.9, 0.08, 0.5, o.cap, 0, 0.48, 0.7); }
    [-0.24, 0.24].forEach(function (x) { box(u.head, 0.14, 0.2, 0.08, 0x140b33, x, 0.04, 0.62, { flatShading: true }); box(u.head, 0.2, 0.05, 0.06, 0x140b33, x, 0.26, 0.62); });
    u.mouth = box(u.head, 0.3, 0.07, 0.06, 0x5a1c1c, 0, -0.26, 0.64);
    blob(g, 0, 0, 1.1, 0.35);
    return g;
  }
  var SKIN1 = 0xc68642, SKIN2 = 0xe0ac69, SKIN3 = 0x8d5524;

  /* ---------- ceu: lua e estrelas (decoracao) ---------- */
  var moon = sph(scene, 3.2, 0xfff1d0, -34, 40, -80, { emissive: 0xffe9b8, emissiveIntensity: 0.9 }, 2);
  var stars = [];
  for (var s = 0; s < 70; s++) {
    var st = new T.Mesh(new T.OctahedronGeometry(0.22 + rnd(s + 9) * 0.25, 0), new T.MeshBasicMaterial({ color: 0xf1ecff, transparent: true }));
    st.position.set((rnd(s) - 0.5) * 150, 18 + rnd(s + 40) * 55, -45 - rnd(s + 80) * 60);
    st.userData.ph = rnd(s + 5) * 6; scene.add(st); stars.push(st);
  }

  /* ---------- rua e fachada da casa ---------- */
  var ground = box(scene, 220, 0.4, 220, 0x2b1c5e, 0, -0.2, 0);
  box(scene, 220, 0.12, 9, 0x1a1140, 0, 0.02, 16);                 // rua
  for (var d = -8; d < 12; d++) box(scene, 1.6, 0.05, 0.28, 0xf1ecff, d * 6 - 30, 0.09, 16);
  box(scene, 220, 0.2, 4.2, 0x4b3b88, 0, 0.1, 9.2);                // calcada
  var house = new T.Group(); scene.add(house);
  box(house, 15, 7.2, 9, 0xf3e8d8, 0, 3.6, 0);
  box(house, 16.4, 0.9, 10.4, 0x140b33, 0, 7.5, 0);
  box(house, 14, 0.5, 0.5, 0x3a2486, 0, 6.6, 4.7);
  var awn = box(house, 13.4, 0.35, 2.4, 0x3a2486, 0, 4.1, 5.5);
  var win = [];
  [-4.6, 4.6].forEach(function (x) {
    win.push(box(house, 4.4, 2.9, 0.15, 0xffd9a0, x, 2.1, 4.55, { emissive: 0xffb866, emissiveIntensity: 0.4 }));
    [-1.1, 0, 1.1].forEach(function (m) { box(house, 0.1, 2.9, 0.12, 0x140b33, x + m, 2.1, 4.66); });
    box(house, 4.4, 0.1, 0.12, 0x140b33, x, 2.1, 4.66);
  });
  box(house, 1.9, 3.2, 0.2, 0x140b33, 0, 1.7, 4.58);
  win.push(box(house, 1.3, 1.9, 0.12, 0xffd9a0, 0, 1.95, 4.7, { emissive: 0xffb866, emissiveIntensity: 0.4 }));
  box(house, 3.5, 3.5, 0.18, 0xffffff, 0, 5.4, 4.62);                // placa branca
  var sign = new T.Mesh(new T.PlaneGeometry(3.3, 3.3), logoMat); sign.position.set(0, 5.4, 4.73); house.add(sign);
  var lant = [];
  [-6, -3, 3, 6].forEach(function (x) { var l = sph(house, 0.42, 0xff9a3c, x, 3.4, 6.0, { emissive: 0xff8a2a, emissiveIntensity: 0.9 }, 1); lant.push(l); });
  blob(scene, 0, 5.5, 8, 0.25);
  [-12, 12, -20, 20].forEach(function (x, i) {
    cyl(scene, 0.18, 0.22, 1.6, 6, 0x4a2d1a, x, 0.8, 7.5 + (i % 2));
    sph(scene, 1.5, 0x2e8b6a, x, 3, 7.5 + (i % 2), null, 1);
    blob(scene, x, 7.5 + (i % 2), 1.6, 0.3);
  });
  [-8.5, 8.5].forEach(function (x) {                                   // postes
    cyl(scene, 0.12, 0.14, 5.4, 6, 0x140b33, x, 2.7, 11.6);
    sph(scene, 0.45, 0xfff1d0, x, 5.6, 11.6, { emissive: 0xffe3a8, emissiveIntensity: 1 }, 1);
  });

  /* ---------- dono na calcada, com o celular ---------- */
  var dono = person({ shirt: 0x7d27fc, pants: 0x140b33, skin: SKIN1, hair: 0x1a0f0a });
  dono.position.set(5.5, 0.12, 7.6); dono.rotation.y = 0.16; scene.add(dono);
  var phone = new T.Group(); phone.position.set(-0.72, 2.45, 0.95); phone.rotation.x = -0.25; dono.add(phone);
  box(phone, 0.62, 1.1, 0.09, 0x0c0820, 0, 0, 0);
  box(phone, 0.52, 0.98, 0.02, 0xe6dcff, 0, 0, 0.055, { emissive: 0xcdbdff, emissiveIntensity: 0.9 });

  /* ---------- caminhao de entrega e caixa ---------- */
  var truck = new T.Group(); scene.add(truck);
  box(truck, 4.2, 2.8, 2.6, 0xf1e6d6, -0.9, 2.1, 0);
  box(truck, 4.22, 0.5, 2.62, 0x7d27fc, -0.9, 1.2, 0);
  box(truck, 1.9, 2.1, 2.5, 0x5512c4, 2.1, 1.75, 0);
  box(truck, 0.12, 1.1, 2.0, 0xcdbdff, 3.08, 2.2, 0, { emissive: 0xcdbdff, emissiveIntensity: 0.5 });
  box(truck, 6.6, 0.4, 2.4, 0x140b33, 0.4, 0.55, 0);
  [-2, 0.2, 2.4].forEach(function (x) { [-1.3, 1.3].forEach(function (z) { var w = cyl(truck, 0.62, 0.62, 0.45, 9, 0x0c0820, x, 0.62, z); w.rotation.x = Math.PI / 2; }); });
  blob(truck, 0, 0, 3.6, 0.35);
  var crate = new T.Group(); scene.add(crate);
  box(crate, 1.7, 1.1, 1.3, 0xc89b5e, 0, 0.55, 0);
  var lid = new T.Group(); lid.position.set(0, 1.1, -0.65); crate.add(lid);
  var lidM = box(lid, 1.8, 0.14, 1.34, 0xa57a40, 0, 0.07, 0.65);
  blob(crate, 0, 0, 1.3, 0.35);

  function plaq(sc) {
    var g = new T.Group();
    var f = new T.Mesh(new T.PlaneGeometry(2.4, 1.6), plaqMat); f.position.z = 0.06; g.add(f);
    box(g, 2.22, 1.42, 0.1, 0x2b1c5e, 0, 0, 0);
    g.scale.setScalar(sc); return g;
  }
  var plaqOut = plaq(1.15); plaqOut.visible = false; scene.add(plaqOut);

  /* ---------- salao em corte (x = 40) ---------- */
  var IX = 40, room = new T.Group(); room.position.set(IX, 0, 0); scene.add(room);
  box(room, 17, 0.5, 12, 0xc9a374, 0, -0.1, 0);
  box(room, 17, 8.5, 0.5, 0xf3e8d8, 0, 4.2, -6);
  box(room, 0.5, 8.5, 12, 0xe9dcc8, -8.5, 4.2, 0);
  box(room, 0.5, 8.5, 12, 0xe9dcc8, 8.5, 4.2, 0);
  box(room, 17.6, 0.35, 0.7, 0x140b33, 0, 8.6, -6);
  box(room, 12, 1.7, 1.3, 0x3d2417, 0, 0.85, -5.0);                // balcao
  box(room, 12.2, 0.18, 1.5, 0x5b3a24, 0, 1.75, -5.0);
  [0xff8f5a, 0xe0405a, 0xffd36e, 0xff8f5a, 0xe0405a, 0xffd36e, 0xff8f5a, 0xe0405a].forEach(function (c, i) {
    var x = -4.6 + i * 1.3;
    cyl(room, 0.3, 0.3, 0.22, 8, 0xfbfbf7, x, 1.95, -5.0);
    box(room, 0.5, 0.12, 0.34, c, x, 2.12, -5.0);
  });
  box(room, 4.6, 0.28, 2.8, 0x5b3a24, 0, 2.7, 1.6);                // mesa
  [[-1.9, -1.0], [1.9, -1.0], [-1.9, 1.0], [1.9, 1.0]].forEach(function (p) { box(room, 0.28, 2.6, 0.28, 0x3d2417, p[0], 1.3, 1.6 + p[1]); });
  var plaqIn = plaq(0.82); plaqIn.position.set(0, 3.55, 1.2); plaqIn.rotation.x = -0.08; room.add(plaqIn);
  box(room, 0.5, 0.18, 0.5, 0x2b1c5e, 0, 2.95, 1.2);
  [-6.2, -3.4, 3.4, 6.2].forEach(function (x, i) {                 // luminarias
    box(room, 0.06, 2.4, 0.06, 0x140b33, x, 7.2, -2);
    sph(room, 0.55, 0xffe3a8, x, 5.9, -2, { emissive: 0xffc870, emissiveIntensity: 1 }, 1);
  });
  box(room, 2.2, 1.5, 0.1, 0xffffff, -5.8, 5.2, -5.7);
  var sign2 = new T.Mesh(new T.PlaneGeometry(2.0, 2.0), logoMat); sign2.position.set(0, 5.4, -5.62); room.add(sign2);
  var dono2 = person({ shirt: 0x7d27fc, pants: 0x140b33, skin: SKIN1, hair: 0x1a0f0a });
  dono2.position.set(-2.6, 0.16, 4.0); dono2.rotation.y = 0.45; room.add(dono2);
  var staff = [
    person({ shirt: 0xf4f2f9, pants: 0x140b33, skin: SKIN2, hair: 0x2a1a10, apron: 0x3a2486, cap: 0xf4f2f9 }),
    person({ shirt: 0xf4f2f9, pants: 0x140b33, skin: SKIN3, hair: 0x0c0820, apron: 0x3a2486 }),
    person({ shirt: 0x3a2486, pants: 0x140b33, skin: SKIN2, hair: 0x6b3a1a })
  ];
  [[2.7, 4.0, -0.45], [4.6, 2.2, -0.8], [-4.6, 2.0, 0.55]].forEach(function (p, i) { staff[i].position.set(p[0], 0.16, p[1]); staff[i].rotation.y = p[2]; room.add(staff[i]); });
  var phoneI = new T.Group(); room.add(phoneI);
  box(phoneI, 0.62, 1.1, 0.09, 0x0c0820, 0, 0, 0);
  box(phoneI, 0.52, 0.98, 0.02, 0xe6dcff, 0, 0, 0.055, { emissive: 0xcdbdff, emissiveIntensity: 0.9 });
  var rings = [];
  for (var r = 0; r < 3; r++) {
    var rg = new T.Mesh(new T.TorusGeometry(1, 0.045, 6, 40), new T.MeshBasicMaterial({ color: 0xa874ff, transparent: true, opacity: 0 }));
    rg.position.set(0, 3.55, 1.45); room.add(rg); rings.push(rg);
  }

    /* ---------- cena em funcao do tempo (todos os tempos vem de assets/cues.js, gerado por cronograma.py) ---------- */
  var C = window.CUES;
  var CAM = [
    [0.0,                    [12, 17, 42],           [0, 3.8, 2]],
    [2.4,                    [6, 9.5, 27],           [0, 4.6, 3]],
    [C.p1_ini - 0.2,         [3.5, 8, 23],           [0, 4.4, 3]],
    [C.p1_ini + 0.9,         [6.4, 3.4, 14.8],       [5.2, 2.9, 7.6]],
    [C.cartao_ini - 0.6,     [6.2, 3.3, 14.4],       [5.1, 2.9, 7.8]],
    [C.cartao_ini,           [4.7, 2.7, 11.4],       [4.78, 2.5, 8.5]],
    [C.cartao_fim - 0.05,    [4.7, 2.7, 11.2],       [4.78, 2.5, 8.5]],
    [C.cena3_ini,            [-2, 7.5, 44],          [-5, 2.6, 13]],
    [C.caixa_pula[0],        [-2, 7.5, 44],          [-6, 2.8, 12]],
    [C.voo_salao[0],         [-2, 7.2, 42],          [-6, 3.2, 12]],
    [C.voo_salao[0] + 0.5,   [18, 30, 42],           [30, 3, 4]],
    [C.voo_salao[1],         [IX, 7.6, 27],          [IX, 3.4, 0]],
    [C.celular_aproxima[0],  [IX, 7.2, 26],          [IX, 3.4, 0]],
    [C.celular_aproxima[1],  [IX + 0.2, 4.3, 10.4],  [IX, 3.5, 1.3]],
    [C.voo_volta[0],         [IX + 0.2, 4.2, 10.0],  [IX, 3.5, 1.3]],
    [C.voo_volta[0] + 0.6,   [22, 30, 40],           [20, 3, 6]],
    [C.voo_volta[1],         [3.5, 8, 23],           [0, 4.4, 3]],
    [C.dur,                  [2.5, 7, 20.5],         [0, 4.6, 3]]
  ];
  function lerpv(a, b, k) { return a + (b - a) * k; }
  function renderAt(t) {
    var cp = track(t, CAM.map(function (k) { return [k[0], k[1]]; })), cl = track(t, CAM.map(function (k) { return [k[0], k[2]]; }));
    camera.position.set(cp[0], cp[1], cp[2]); camera.lookAt(cl[0], cl[1], cl[2]);
    // luzes da casa acendem no final
    var on = 0.35 + 0.4 * ease(seg(t, C.luzes[0], C.luzes[1]));
    win.forEach(function (w) { w.material.emissiveIntensity = on; });
    lant.forEach(function (l, i) { l.material.emissiveIntensity = 0.7 + 0.25 * Math.sin(t * 2 + i); });
    stars.forEach(function (s) { s.material.opacity = 0.45 + 0.5 * Math.abs(Math.sin(t * 1.3 + s.userData.ph)); s.rotation.y = t * 0.4 + s.userData.ph; });
    // passo 1: o dono da calcada ergue o celular
    var up = ease(seg(t, C.dono_braco[0], C.dono_braco[1]));
    dono.userData.armR.rotation.x = -1.85 * up;
    dono.userData.armL.rotation.x = 0.06 * Math.sin(t * 2);
    dono.position.y = 0.12 + 0.05 * Math.abs(Math.sin(t * 2.6));
    dono.userData.head.rotation.y = 0.12 * Math.sin(t * 1.3);
    phone.visible = up > 0.35; phone.scale.setScalar(ease(seg(t, C.celular_pop[0], C.celular_pop[1])) + 0.001);
    // passo 3: caminhao chega, caixa pula, abre, plaquinha sobe
    var tx = track(t, [[C.caminhao[0], [-36]], [C.caminhao[1], [-4.5]]])[0];
    truck.position.set(tx, 0.12, 15.4);
    var wob = (t > C.caminhao[0] && t < C.caminhao[1]) ? 0.05 * Math.sin(t * 18) : 0; truck.position.y += Math.abs(wob);
    var jump = ease(seg(t, C.caixa_pula[0], C.caixa_pula[1]));
    crate.visible = t > C.caixa_pula[0] - 0.05;
    crate.position.set(-4.5 - 4.2 * jump + 0.001, 0.12 + 3.2 * Math.sin(Math.PI * jump) * 0.55, 15.4 - 5.2 * jump);
    crate.rotation.y = 0.5 * (1 - jump);
    lid.rotation.x = -2.0 * ease(seg(t, C.tampa[0], C.tampa[1]));
    var rise = ease(seg(t, C.placa_sobe[0], C.placa_sobe[1]));
    plaqOut.visible = t > C.placa_sobe[0] - 0.05 && t < C.placa_sobe[1] + 0.9;
    plaqOut.position.set(crate.position.x, crate.position.y + 0.6 + 2.4 * rise, crate.position.z);
    plaqOut.rotation.y = 0.9 * rise + 0.5 * Math.sin(t * 2);
    // passo 4: salao com a equipe, celular encosta na plaquinha, ondas NFC
    staff.concat([dono2]).forEach(function (p, i) {
      p.position.y = 0.16 + 0.03 * Math.abs(Math.sin(t * 2.2 + i));
      p.userData.head.rotation.y = 0.18 * Math.sin(t * 1.1 + i * 1.7);
      p.userData.head.rotation.x = 0.07 * Math.sin(t * 2.0 + i);
    });
    var hand = ease(seg(t, C.celular_aproxima[0] - 0.4, C.celular_aproxima[1] - 0.2));
    var px = lerpv(-3.8, 0.15, hand), py = lerpv(3.4, 3.05, hand), pz = lerpv(3.8, 2.0, hand);
    phoneI.position.set(px, py, pz); phoneI.rotation.set(-0.15, 0.1, 0); phoneI.scale.setScalar(0.72);
    phoneI.visible = t > C.voo_salao[1] - 0.4 && t < C.aneis[1] + 0.1;
    dono2.userData.armR.rotation.x = -1.7 * ease(seg(t, C.braco_dono2[0], C.braco_dono2[1]));
    rings.forEach(function (rg, i) {
      var ph = ((t - C.aneis[0] - i * 0.28) % 0.9 + 0.9) % 0.9 / 0.9, on2 = t > C.aneis[0] && t < C.aneis[1];
      var s2 = 0.35 + ph * 1.5; rg.scale.set(s2, s2, s2);
      rg.material.opacity = on2 ? 0.9 * (1 - ph) : 0;
    });
    renderer.render(scene, camera);
  }

  window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
  window.__hf.buildReady.mundo = Promise.all(pend).then(function () { renderAt(0); });
  window.addEventListener("hf-seek", function (e) { renderAt(e.detail.time); });
  renderAt(0);
})();
