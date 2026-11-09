# -*- coding: utf-8 -*-
"""Gera o video "proximos passos" (vertical 1080x1920, ~41 s, voz e legendas prontas) de UM cliente.

Uso:
    py -I -X utf8 gerar_video.py CLIENTE.json [--equipe equipe.json] [--sem-render] [--manter] [--poster-em 1.3]

O video e o mesmo para todas as casas (a voz nao fala o nome da casa). Muda so:
  - a logo da casa (cliente.json -> logo_cliente: png, webp ou jpg; SVG nao serve no 3D),
  - o print da pagina da casa no VTX Tap (cliente.json -> tela_previa; vertical, ~734x1280),
  - o WhatsApp de quem fechou o contrato (cliente.json -> vendedor, igual a landing).
Se o print NAO for o padrao (734x1280, com banner, logo e card "Cardapio" nas mesmas posicoes do print padrão aprovado),
descreva onde ficam as tres marcacoes em cliente.json -> video_realces (coordenadas no cartao de 640 px de largura;
o print e escalado para 640 px de largura: x e y = posicao no print x 640 / largura do print):
  "video_realces": {"banner": [esq, topo, larg, alt], "logo": [esq, topo, larg, alt], "cardapio": [esq, topo, larg, alt] ou null}
null esconde a marcacao daquele item (ex.: o cardapio nao aparece no print).
Saida, na pasta do cliente.json: proximos-passos.mp4 e poster.jpg. O cliente.json recebe "video" e "poster".

Precisa de Node.js (npx), ffmpeg e internet na primeira vez (baixa o HyperFrames 0.8.209).
Render leva uns 2 a 3 minutos. Nao sobe servidor e nao publica nada.
"""
import json, os, re, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gerar  # reaproveita vendedor, WhatsApp e validacoes da landing

MODELO_VIDEO = os.path.normpath(os.path.join(AQUI, "..", "modelo-video"))
HYPERFRAMES = "hyperframes@0.8.209"
ARQUIVOS_COM_MARCADOR = ["index.html", os.path.join("assets", "mundo.js"), os.path.join("compositions", "ui.html")]
RASTER = {".png", ".webp", ".jpg", ".jpeg"}
PROPORCAO_TELA = 734 / 1280.0


LARGURA_CARTAO, ALTURA_CARTAO_MAX = 640, 959
REALCES_PADRAO = {"banner": [0, 0, 640, 275], "logo": [14, 196, 164, 164], "cardapio": [26, 702, 589, 251]}


def estilos_realces(realces):
    """Posicoes (CSS) do realce, da etiqueta e do check de cada item. Padrao = o layout aprovado."""
    out = {}
    for chave, nome in (("cardapio", "CARD"), ("banner", "BAN"), ("logo", "LOGO")):
        r = realces.get(chave, REALCES_PADRAO[chave])
        if r is None:
            for pre in ("H", "L", "C"):
                out["ST_%s_%s" % (pre, nome)] = "display: none;"
            continue
        if not (isinstance(r, list) and len(r) == 4 and all(isinstance(v, (int, float)) for v in r)):
            erro("video_realces.%s precisa ser [esquerda, topo, largura, altura] ou null" % chave)
        l, t, w, h = [int(round(v)) for v in r]
        out["ST_H_" + nome] = "left: %dpx; top: %dpx; width: %dpx; height: %dpx;" % (l, t, w, h)
        if chave == "cardapio":
            lab, chk = (l + 14, t - 34), (l + w - 63, t - 34)
        elif chave == "banner":
            lab, chk = (l + 22, t + 22), (l + w - 92, t + 22)
        else:
            lab, chk = (l + w + 18, t + h // 2 - 8), (l + w - 46, t - 8)
        out["ST_L_" + nome] = "left: %dpx; top: %dpx;" % lab
        out["ST_C_" + nome] = "left: %dpx; top: %dpx;" % chk
    return out


def dimensoes_webp(caminho):
    with open(caminho, "rb") as f:
        b = f.read(40)
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP" and b[12:16] == b"VP8X":
        return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    return None


def dimensoes(caminho):
    d = gerar.dimensoes(caminho)
    return d or dimensoes_webp(caminho)


def erro(msg):
    sys.exit("ERRO: " + msg)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.exit(__doc__)

    def opcao(nome, padrao):
        return args[args.index(nome) + 1] if nome in args else padrao

    sem_render, manter = "--sem-render" in args, "--manter" in args
    poster_em = float(opcao("--poster-em", "1.3"))
    caminho_equipe = os.path.abspath(opcao("--equipe", os.path.join("landing-pages", "equipe", "equipe.json")))
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--equipe", "--poster-em"))]
    if len(pos) != 1:
        sys.exit(__doc__)
    cj = os.path.abspath(pos[0])
    pasta = os.path.dirname(cj)
    bruto = json.load(open(cj, encoding="utf-8-sig"))
    cli = {**gerar.PADRAO, **bruto}

    for k in ("slug", "casa", "logo_cliente", "vendedor", "tela_previa"):
        if not cli.get(k):
            erro("para o video o cliente.json precisa de %r%s" % (k, " (o print da pagina da casa)" if k == "tela_previa" else ""))
    if not os.path.isdir(MODELO_VIDEO):
        erro("modelo do video nao encontrado: " + MODELO_VIDEO)

    logo = gerar.achar_arquivo(cli["logo_cliente"], pasta)
    tela = gerar.achar_arquivo(cli["tela_previa"], pasta)
    ext_logo, ext_tela = os.path.splitext(logo)[1].lower(), os.path.splitext(tela)[1].lower()
    if ext_logo not in RASTER:
        erro("no video a logo precisa ser png, webp ou jpg (veio %s). SVG nao carrega no cenario 3D." % (ext_logo or "sem extensao"))
    if ext_tela not in RASTER:
        erro("o print da pagina precisa ser png, webp ou jpg (veio %s)." % (ext_tela or "sem extensao"))

    realces = bruto.get("video_realces") or {}
    d = dimensoes(tela)
    altura_img = 1117                                   # 640 x 1280 / 734 (print padrao)
    if d:
        w, h = d
        padrao = abs(w / float(h) - PROPORCAO_TELA) <= 0.04 and w >= 600
        if not padrao and not realces:
            erro("o print da pagina (%dx%d) nao e o padrao (vertical, ~734x1280, com banner, logo e card Cardapio). "
                 "Mande um print nesse formato ou descreva as marcacoes em cliente.json -> video_realces (veja --help)." % (w, h))
        if w < 400:
            print("AVISO: o print da pagina e estreito (%d px); no video vai ficar borrado." % w)
        altura_img = int(round(LARGURA_CARTAO * h / float(w)))
    else:
        print("AVISO: nao consegui medir o print da pagina; confira se e vertical, ~734x1280.")
    dl = dimensoes(logo)
    if dl and min(dl) < 400:
        print("AVISO: a logo e pequena (%dx%d px); no video vai ficar borrada." % dl)

    vend, _ = gerar.carregar_vendedor(cli, caminho_equipe)
    wa_exib = vend.get("whatsapp_exibicao", "").strip() or gerar.formatar_whatsapp(gerar.normalizar_whatsapp(vend["whatsapp"]))

    trabalho = os.path.join(pasta, "video-trabalho")
    if os.path.isdir(trabalho):
        shutil.rmtree(trabalho)
    shutil.copytree(MODELO_VIDEO, trabalho, ignore=shutil.ignore_patterns("fonte"))
    os.makedirs(os.path.join(trabalho, "assets", "cliente"), exist_ok=True)
    nome_logo, nome_tela = "logo" + ext_logo, "tela" + ext_tela
    shutil.copy(logo, os.path.join(trabalho, "assets", "cliente", nome_logo))
    shutil.copy(tela, os.path.join(trabalho, "assets", "cliente", nome_tela))
    valores = {"CARD_H": str(min(ALTURA_CARTAO_MAX, altura_img)), "IMG_H": str(altura_img), **estilos_realces(realces),
               "LOGO": nome_logo, "TELA": nome_tela, "WA_EXIB": gerar.esc(wa_exib), "CASA": gerar.esc(cli["casa"])}
    for rel in ARQUIVOS_COM_MARCADOR:
        p = os.path.join(trabalho, rel)
        txt = open(p, encoding="utf-8").read()
        for k, v in valores.items():
            txt = txt.replace("{{%s}}" % k, v)
        sobra = sorted(set(re.findall(r"\{\{(\w+)\}\}", txt)))
        if sobra:
            erro("marcadores sem valor em %s: %s" % (rel, ", ".join(sobra)))
        open(p, "w", encoding="utf-8").write(txt)
    print("Video preparado em %s (numero no fecho: %s)" % (trabalho, wa_exib))
    if sem_render:
        print("--sem-render: parei antes do render.")
        return

    npx = shutil.which("npx")
    ffmpeg = shutil.which("ffmpeg")
    if not npx:
        erro("Node.js (npx) nao encontrado. Instale o Node.js e tente de novo.")
    if not ffmpeg:
        erro("ffmpeg nao encontrado. Instale o ffmpeg (no Windows: winget install Gyan.FFmpeg) e tente de novo.")
    saida = os.path.join(pasta, "proximos-passos.mp4")
    print("Renderizando (2 a 3 minutos)...")
    r = subprocess.run([npx, "--yes", HYPERFRAMES, "render", ".", "-o", saida, "--quiet"], cwd=trabalho, timeout=1500)
    if r.returncode != 0 or not os.path.isfile(saida):
        erro("o render falhou (codigo %s). Rode de novo com --manter e veja %s." % (r.returncode, trabalho))
    poster = os.path.join(pasta, "poster.jpg")
    subprocess.run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-ss", str(poster_em), "-i", saida, "-frames:v", "1", "-q:v", "3", poster], check=True)

    bruto["video"], bruto["poster"] = "proximos-passos.mp4", "poster.jpg"
    with open(cj, "w", encoding="utf-8", newline="\n") as f:
        json.dump(bruto, f, ensure_ascii=False, indent=2)
        f.write("\n")
    if not manter:
        shutil.rmtree(trabalho, ignore_errors=True)
    mb = os.path.getsize(saida) / 1048576.0
    print("OK: %s (%.1f MB) e %s. cliente.json atualizado (video, poster)." % (saida, mb, poster))


if __name__ == "__main__":
    main()
