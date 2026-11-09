# -*- coding: utf-8 -*-
"""Monta assets/voz.m4a a partir de plano_voz.json (gerado por cronograma.py).
Fontes: narracao original (roteiro inteiro, voz Emmett) + a frase das 24 horas, gerada depois que a ordem dos
passos mudou. Cada trecho e recortado do arquivo gerado e posto no instante do plano."""
import json, subprocess

plano = json.load(open("plano_voz.json", encoding="utf-8"))
DUR = max(p["fim"] for p in plano) + 2.1
fontes = sorted({p["fonte"] for p in plano})
PAD_A, PAD_D = 0.03, 0.05
partes, mix = [], []
for i, p in enumerate(plano):
    a2, b2 = max(0.0, p["a"] - PAD_A), p["b"] + PAD_D
    ms = int(round((p["ini"] - (p["a"] - a2)) * 1000))
    partes.append("[%d:a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st=%.3f:d=0.03,volume=%.1fdB,adelay=%d|%d[p%d]"
                  % (fontes.index(p["fonte"]), a2, b2, (b2 - a2) - 0.03, p["ganho_db"], max(ms, 0), max(ms, 0), i))
    mix.append("[p%d]" % i)
fc = ";".join(partes) + ";" + "".join(mix) + "amix=inputs=%d:normalize=0,apad=whole_dur=%.2f,atrim=0:%.2f,loudnorm=I=-16:TP=-1.5:LRA=7,alimiter=limit=0.89[out]" % (len(plano), DUR, DUR)
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
for f in fontes:
    cmd += ["-i", f]
cmd += ["-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "assets/voz.m4a"]
subprocess.run(cmd, check=True)
print("ok: assets/voz.m4a (%.2f s)" % DUR)
