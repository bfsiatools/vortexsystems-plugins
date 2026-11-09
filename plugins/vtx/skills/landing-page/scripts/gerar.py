# -*- coding: utf-8 -*-
"""Gera a landing page de boas-vindas + proximos passos de UM cliente fechado.

Uso:
    py -I -X utf8 gerar.py CLIENTE.json [--equipe equipe.json] [--saida PASTA] [--unico]

  CLIENTE.json  dados do cliente (ver ../referencia/estrutura.md). Os arquivos citados nele (logo, video...)
                ficam na mesma pasta do CLIENTE.json.
  --equipe      cadastro de quem fecha contratos (nome, foto, WhatsApp). Padrao: ./landing-pages/equipe/equipe.json
  --saida       pasta onde sai <slug>/index.html. Padrao: ./landing-pages/saida
  --unico       gera tambem <slug>-unico.html: UM arquivo com fontes, logos, fotos e video embutidos.

So usa a biblioteca padrao do Python (Pillow, se existir, so serve para medir imagens).
Todo valor vindo do cliente e escapado para HTML. Nada aqui envia mensagem nem publica nada.
"""
import base64, datetime, html, json, os, re, shutil, sys, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.normpath(os.path.join(AQUI, "..", "modelo"))
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
ARTIGOS = {"o": "do", "a": "da", "os": "dos", "as": "das"}   # artigo -> preposicao "de" + artigo
ROTULO = {"feito": "Feito", "agora": "Agora", "depois": "Depois"}
OBRIGATORIOS = ["slug", "casa", "casa_curta", "cidade", "logo_cliente", "vendedor"]
PADRAO = {
    "donos": [], "contato": "", "genero_donos": "m", "saudacao": "", "artigo": "o", "elogio": "",
    "tela_previa": "", "tela_legenda": "Prévia da página da casa.", "video": "", "poster": "", "video_legenda": "Os quatro passos, em vídeo.",
    "data_inicio": "", "prazo_dias": 15, "estado_passos": ["agora", "depois", "depois", "depois"],
    # dados da empresa (rodape e cartao do time); mude so se a marca for outra
    "site_rodape": "tap.vortexsystems.tech", "insta": "@vtxtap", "email_time": "contato@vortexsystems.tech",
}
EXT_IMG = {".png", ".webp", ".jpg", ".jpeg", ".svg"}
MIME = {".ttf": "font/ttf", ".svg": "image/svg+xml", ".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".mp4": "video/mp4"}
avisos = []


def esc(v):
    return html.escape(str(v), quote=True)


def sair(msg):
    sys.exit("ERRO: " + msg)


def data_extenso(d):
    return "%d de %s de %d" % (d.day, MESES[d.month - 1], d.year)


def lista_nomes(nomes):
    nomes = [n.strip() for n in nomes if n.strip()]
    if len(nomes) <= 1:
        return "".join(nomes)
    return ", ".join(nomes[:-1]) + " e " + nomes[-1]


def saudacao(qtd, genero, override):
    if override.strip():
        return override.strip()
    fem = genero == "f"
    base = "Bem-vind" + ("a" if fem else "o")
    return base + ("s" if qtd > 1 else "")


def normalizar_whatsapp(bruto):
    d = re.sub(r"\D", "", str(bruto))
    if len(d) in (10, 11):
        d = "55" + d
    if not (len(d) in (12, 13) and d.startswith("55")):
        sair("WhatsApp invalido: %r. Use DDD + numero (ex.: 11 90000-0000) ou o numero completo com 55." % bruto)
    return d


def formatar_whatsapp(d):
    local = d[2:]
    ddd, resto = local[:2], local[2:]
    corte = len(resto) - 4
    return "(%s) %s-%s" % (ddd, resto[:corte], resto[corte:])


def dimensoes(caminho):
    """(largura, altura) ou None. Pillow se houver; senao so PNG/JPEG simples."""
    try:
        from PIL import Image
        with Image.open(caminho) as im:
            return im.size
    except Exception:
        pass
    with open(caminho, "rb") as f:
        b = f.read(65536)
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")
    return None


def checar_imagem(caminho, rotulo, minimo):
    ext = os.path.splitext(caminho)[1].lower()
    if ext not in EXT_IMG:
        sair("%s precisa ser png, webp, jpg ou svg (veio %s)" % (rotulo, ext or "sem extensao"))
    if ext != ".svg":
        dim = dimensoes(caminho)
        if dim and min(dim) < minimo:
            avisos.append("%s e pequena (%dx%d px); abaixo de %d px fica borrada. Peca uma versao maior." % (rotulo, dim[0], dim[1], minimo))
    if os.path.getsize(caminho) > 8 * 1024 * 1024:
        avisos.append("%s tem mais de 8 MB; vale reduzir." % rotulo)


def achar_arquivo(nome, *pastas):
    if os.path.basename(nome) != nome and not os.path.isabs(nome):
        # permite subpasta relativa (ex.: fotos/ana.jpg) mas nunca sair da pasta
        partes = os.path.normpath(nome).split(os.sep)
        if ".." in partes:
            sair("caminho de arquivo invalido: " + nome)
    for p in pastas:
        c = nome if os.path.isabs(nome) else os.path.join(p, nome)
        if os.path.isfile(c):
            return os.path.abspath(c)
    sair("arquivo nao encontrado: %s (procurei em: %s)" % (nome, "; ".join(pastas)))


def arquivo_unico(txt, base):
    def troca(m):
        rel = m.group(2)
        ext = os.path.splitext(rel)[1].lower()
        with open(os.path.join(base, *rel.split("/")), "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return "%s%s;base64,%s%s" % (m.group(1), "data:" + MIME[ext], b64, m.group(3))
    return re.sub(r'((?:src|poster)=["\']|url\(["\']?)(assets/[^"\')]+)(["\')])', troca, txt)


def carregar_vendedor(cli, caminho_equipe):
    v = cli["vendedor"]
    pastas = [os.path.dirname(os.path.abspath(caminho_equipe))] if caminho_equipe else []
    if isinstance(v, str):
        if not caminho_equipe or not os.path.isfile(caminho_equipe):
            sair("vendedor %r pede o cadastro da equipe, mas %s nao existe. Crie-o ou passe o vendedor inline." % (v, caminho_equipe))
        eq = json.load(open(caminho_equipe, encoding="utf-8-sig")).get("pessoas", {})
        if v not in eq:
            sair("vendedor %r nao esta no cadastro. Cadastrados: %s" % (v, ", ".join(sorted(eq)) or "(ninguem)"))
        v = eq[v]
    for k in ("nome", "whatsapp", "foto"):
        if not str(v.get(k, "")).strip():
            sair("vendedor sem %r. Todo vendedor precisa de nome, foto e WhatsApp." % k)
    return v, pastas


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.exit(__doc__)
    unico = "--unico" in args
    def opcao(nome, padrao):
        return os.path.abspath(args[args.index(nome) + 1]) if nome in args else padrao
    caminho_equipe = opcao("--equipe", os.path.abspath(os.path.join("landing-pages", "equipe", "equipe.json")))
    raiz_saida = os.path.realpath(opcao("--saida", os.path.abspath(os.path.join("landing-pages", "saida"))))
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--equipe", "--saida"))]
    if len(pos) != 1:
        sys.exit(__doc__)
    cj = os.path.abspath(pos[0])
    pasta_cli = os.path.dirname(cj)
    cli = {**PADRAO, **json.load(open(cj, encoding="utf-8-sig"))}

    faltam = [k for k in OBRIGATORIOS if not cli.get(k)]
    if faltam:
        sair("faltam campos no cliente.json: " + ", ".join(faltam))
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", cli["slug"]):
        sair("slug so aceita letras minusculas sem acento, numeros e hifens entre palavras (ex.: casa-do-joao)")
    if len(cli["estado_passos"]) != 4 or any(s not in ROTULO for s in cli["estado_passos"]):
        sair("estado_passos precisa ter 4 itens entre: feito, agora, depois")
    if cli["genero_donos"] not in ("m", "f"):
        sair("genero_donos precisa ser 'm' ou 'f'")
    if cli["artigo"] not in ARTIGOS:
        sair("artigo precisa ser um destes: o, a, os, as (ex.: 'o Bar do Exemplo', 'a Casa Exemplo')")
    art = cli["artigo"]
    do_ = ARTIGOS[art]

    donos = cli["donos"] or ([cli["contato"]] if cli["contato"].strip() else [])
    nome_exib = lista_nomes(donos) or cli["casa_curta"]
    sauda = saudacao(max(len(donos), 1), cli["genero_donos"], cli["saudacao"])

    vend, pastas_vend = carregar_vendedor(cli, caminho_equipe)
    wa_num = normalizar_whatsapp(vend["whatsapp"])
    wa_exib = vend.get("whatsapp_exibicao", "").strip() or formatar_whatsapp(wa_num)
    primeiro = vend["nome"].strip().split()[0]
    wa = "https://wa.me/%s?text=" % wa_num
    msg = lambda t: wa + urllib.parse.quote(t)

    hoje = datetime.date.today()
    inicio = datetime.date.fromisoformat(cli["data_inicio"]) if cli["data_inicio"] else hoje
    prev = inicio + datetime.timedelta(days=int(cli["prazo_dias"]))

    # ---- arquivos ----
    f_logo = achar_arquivo(cli["logo_cliente"], pasta_cli)
    checar_imagem(f_logo, "A logo do cliente", 400)
    f_foto = achar_arquivo(vend["foto"], pasta_cli, *pastas_vend)
    checar_imagem(f_foto, "A foto de %s" % vend["nome"], 240)
    extras = {}
    for chave in ("tela_previa", "video", "poster"):
        if cli[chave]:
            extras[chave] = achar_arquivo(cli[chave], pasta_cli)
    if cli["tela_previa"]:
        checar_imagem(extras["tela_previa"], "A previa de tela", 500)

    foto_nome = "vendedor-" + os.path.basename(f_foto)
    logo_nome = os.path.basename(f_logo)

    # ---- blocos opcionais ----
    elogio = "<p>%s</p>" % esc(cli["elogio"]) if cli["elogio"].strip() else ""
    previa = video = ""
    if cli["tela_previa"]:
        previa = ('<div class="previa"><div class="tela"><img src="assets/cliente/%s" alt="Prévia da página da casa" /></div></div>'
                  '<p class="legenda">%s</p>') % (esc(os.path.basename(cli["tela_previa"])), esc(cli["tela_legenda"]))
    if cli["video"]:
        poster = ' poster="assets/cliente/%s"' % esc(os.path.basename(cli["poster"])) if cli["poster"] else ""
        video = ('<div class="video"><video controls playsinline preload="metadata"%s>'
                 '<source src="assets/cliente/%s" type="video/mp4" /></video></div>'
                 '<p class="legenda">%s</p>') % (poster, esc(os.path.basename(cli["video"])), esc(cli["video_legenda"]))
    bloco = ""
    if previa or video:
        cols = "".join("<div>%s</div>" % b for b in (previa, video) if b)
        bloco = '<section class="secao"><div class="wrap reveal"><h2>Como vai ficar</h2><div class="duas">%s</div></div></section>' % cols

    vals = {
        "saudacao": esc(sauda), "art_o": esc(art), "Art_O": esc(art.capitalize()), "art_do": esc(do_), "casa": esc(cli["casa"]), "casa_curta": esc(cli["casa_curta"]), "cidade": esc(cli["cidade"]),
        "contato": esc(nome_exib), "nome_h1": esc(nome_exib), "logo_cliente": esc(logo_nome),
        "prazo": esc(cli["prazo_dias"]), "previsao": esc(data_extenso(prev)), "data_inicio": esc(data_extenso(inicio)),
        "vendedor_nome": esc(vend["nome"].strip()), "vendedor_foto": esc(foto_nome),
        "vendedor_funcao": esc(vend.get("funcao", "").strip() or "Seu contato direto, do início ao fim."),
        "wa_exib": esc(wa_exib), "site_rodape": esc(cli["site_rodape"]), "insta": esc(cli["insta"]), "email_time": esc(cli["email_time"]),
        "wa_geral": esc(msg("Oi, %s! Aqui é %s %s." % (primeiro, do_, cli["casa_curta"]))),
        "wa_material": esc(msg("Oi, %s! Aqui é %s %s. Estou enviando o material: cardápio, banner e logo." % (primeiro, do_, cli["casa_curta"]))),
        "wa_treino": esc(msg("Oi, %s! Aqui é %s %s. Quero combinar o dia do treinamento da equipe." % (primeiro, do_, cli["casa_curta"]))),
        "BLOCO_ELOGIO": elogio, "BLOCO_PREVIA_VIDEO": bloco,
    }
    for i, est in enumerate(cli["estado_passos"], 1):
        vals["classe%d" % i] = est
        vals["rotulo%d" % i] = ROTULO[est]

    txt = open(os.path.join(MODELO, "index.html"), encoding="utf-8").read()
    for k, v in vals.items():
        txt = txt.replace("{{%s}}" % k, v)
    sobra = sorted(set(p.split("}}")[0] for p in txt.split("{{")[1:]))
    if sobra:
        sair("placeholders sem valor no modelo: " + ", ".join(sobra))

    saida = os.path.realpath(os.path.join(raiz_saida, cli["slug"]))
    if os.path.dirname(saida) != raiz_saida:
        sair("a pasta de saida precisa ficar dentro de " + raiz_saida)
    if os.path.isdir(saida):
        shutil.rmtree(saida)
    shutil.copytree(os.path.join(MODELO, "assets"), os.path.join(saida, "assets"))
    os.makedirs(os.path.join(saida, "assets", "cliente"))
    shutil.copy(f_logo, os.path.join(saida, "assets", "cliente", logo_nome))
    shutil.copy(f_foto, os.path.join(saida, "assets", "cliente", foto_nome))
    for f in extras.values():
        shutil.copy(f, os.path.join(saida, "assets", "cliente", os.path.basename(f)))
    open(os.path.join(saida, "index.html"), "w", encoding="utf-8").write(txt)

    print("OK: " + os.path.join(saida, "index.html"))
    if unico:
        alvo = os.path.join(raiz_saida, cli["slug"] + "-unico.html")
        open(alvo, "w", encoding="utf-8").write(arquivo_unico(txt, saida))
        print("OK (arquivo unico, tudo embutido): %s (%.1f MB)" % (alvo, os.path.getsize(alvo) / 1048576))
    print("Titulo da abertura: %s, %s." % (sauda, nome_exib))
    print("Contato: %s | %s | %s" % (vend["nome"].strip(), wa_exib, "wa.me/" + wa_num))
    print("Previsao das plaquinhas: %s (contada de %s)" % (data_extenso(prev), data_extenso(inicio)))
    for a in avisos:
        print("AVISO: " + a)


if __name__ == "__main__":
    main()




