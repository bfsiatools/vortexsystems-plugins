# -*- coding: utf-8 -*-
"""Gera compositions/legendas.html (uma palavra por legenda, estilo da referencia) a partir de palavras.json.
Palavras curtas se juntam a seguinte (max. 2 por legenda). Tempos PROVISORIOS (ver alinhar.py)."""
import json, re

pal = json.load(open("palavras.json", encoding="utf-8"))
FUNC = {"a", "e", "o", "é", "de", "do", "da", "em", "as", "os", "no", "na", "me", "com", "que", "vai", "ela", "sua", "uma", "para"}
CHAVE = {"fechou", "vtx", "tap", "quatro", "um", "dois", "três", "página", "cardápio", "banner", "logo", "quinze",
         "plaquinhas", "treinamento", "whatsapp", "dúvida", "restaurante", "horas", "pronta"}

def limpo(w):
    return re.sub(r"[.,:]", "", w)

grupos, buf = [], []
for p in pal:
    buf.append(p)
    w = p["w"]
    fim_frase = w[-1] in ".,:?"
    curta = re.sub(r"[^\wáéíóúâêôãõç]", "", w.lower()) in FUNC
    if fim_frase or not curta or len(buf) >= 2:
        grupos.append(buf)
        buf = []
if buf:
    grupos.append(buf)

itens = []
for i, g in enumerate(grupos):
    ini, fim = g[0]["ini"], g[-1]["fim"]
    prox = grupos[i + 1][0]["ini"] if i + 1 < len(grupos) else fim + 0.5
    fim = min(max(fim + 0.10, ini + 0.35), prox - 0.02) if prox > ini + 0.4 else fim
    fim = max(fim, ini + 0.2)
    html = []
    for p in g:
        k = re.sub(r"[^\wáéíóúâêôãõç]", "", p["w"].lower())
        txt = limpo(p["w"])
        html.append('<b class="k">%s</b>' % txt if k in CHAVE else txt)
    itens.append((ini, fim, " ".join(html)))

linhas, tw = [], []
for n, (ini, fim, h) in enumerate(itens, 1):
    dur = round(fim - ini, 3)
    linhas.append('    <div id="l-g%d" class="grp clip" data-start="%.3f" data-duration="%.3f" data-track-index="1"><span>%s</span></div>' % (n, ini, dur, h))
    tw.append('      ["#l-g%d", %.3f, %.3f]' % (n, ini, dur))

saida = """<template>
  <style>
    @font-face { font-family: "Schibsted Grotesk"; src: url("assets/fonts/SchibstedGrotesk-Variable.ttf") format("truetype"); font-weight: 400 900; font-style: normal; }
    #root { position: absolute; inset: 0; }
    /* Legenda de UMA palavra (gramatica do estilo "desmontando o mundo", nas cores e fonte da VTX):
       branco com contorno noite, sem placa; palavra-chave em ouro. Base da zona de legenda em y ~1600. */
    .grp { position: absolute; left: 0; width: 1080px; top: 1530px; height: 160px; display: flex; align-items: center; justify-content: center; padding: 0 60px; text-align: center; opacity: 0; }
    .grp > span {
      display: inline-block; font-family: "Schibsted Grotesk", system-ui, sans-serif; font-weight: 900; font-size: 112px; line-height: 1.05;
      color: #ffffff; letter-spacing: -0.015em; -webkit-text-stroke: 14px #140b33; paint-order: stroke fill; text-stroke: 14px #140b33;
    }
    .grp .k { color: #ffc61a; font-weight: 900; }
  </style>

  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
%s
  </div>

  <script>
    const tl = gsap.timeline({ paused: true });
    const grupos = [
%s
    ];
    grupos.forEach(([id, ini, dur]) => {
      const fim = ini + dur;
      tl.fromTo(id, { opacity: 0, scale: 0.86, transformOrigin: "50%% 60%%" }, { opacity: 1, scale: 1, duration: 0.1, ease: "power2.out" }, ini);
      tl.to(id, { opacity: 0, duration: 0.05, ease: "power1.in" }, fim - 0.05);
    });
    window.__timelines["legendas"] = tl;
  </script>
</template>
""" % ("\n".join(linhas), ",\n".join(tw))

open("compositions/legendas.html", "w", encoding="utf-8").write(saida)
print(len(itens), "legendas")
for ini, fim, h in itens:
    print("%6.2f-%6.2f %s" % (ini, fim, re.sub(r"<[^>]+>", "", h)))

