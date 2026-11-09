# -*- coding: utf-8 -*-
"""Confere a landing page gerada, sem servidor e sem enviar nada.

Uso:
    py -I -X utf8 verificar.py PASTA_DO_CLIENTE_OU_index.html [--chrome CAMINHO] [--sem-fotos]

Checagens (erro = para; aviso = olhar com atencao):
  erro   placeholder sobrando, assets que nao existem, link do WhatsApp mal formado ou com numeros diferentes,
         falta de noindex, falta do cartao do vendedor, menos de 4 passos
  aviso  valores em reais, promessas de resultado, imagem sem alt
Se achar o Chrome/Edge, tira fotos em 1440 e 390 px (pasta verificacao/ ao lado da saida) para olhar a olho.
Overflow horizontal e cliques bloqueados: use verificar-navegador.cjs (precisa de Playwright).
"""
import glob, html, os, re, shutil, subprocess, sys, urllib.parse

erros, avisos = [], []


def achar_chrome(pedido):
    # chrome-headless-shell (do HyperFrames) respeita o tamanho exato da janela; o Chrome comum do Windows nunca fica abaixo de ~500 px
    cands = [pedido, os.environ.get("CHROME")]
    cands += glob.glob(os.path.expanduser(r"~/.cache/hyperframes/chrome/chrome-headless-shell/*/*/chrome-headless-shell*"))
    cands += [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    cands += [shutil.which(n) for n in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge")]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return None


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.exit(__doc__)
    alvo = os.path.abspath(args[0])
    idx = alvo if alvo.lower().endswith(".html") else os.path.join(alvo, "index.html")
    if not os.path.isfile(idx):
        sys.exit("ERRO: nao achei " + idx)
    base = os.path.dirname(idx)
    txt = open(idx, encoding="utf-8").read()
    corpo = re.sub(r"<(script|style)\b.*?</\1>", "", txt, flags=re.S | re.I)
    visivel = html.unescape(re.sub(r"<[^>]+>", " ", corpo))

    if "{{" in txt or "}}" in txt:
        erros.append("sobrou placeholder {{...}} no HTML")
    if not re.search(r'<meta name="robots" content="[^"]*noindex', txt):
        erros.append("falta <meta name=\"robots\" content=\"noindex\"> (a pagina fica publica por endereco)")
    if not re.search(r"<title>[^<]{3,}</title>", txt):
        erros.append("titulo vazio")
    for ref in sorted(set(re.findall(r'(?:src|poster|href)=["\'](assets/[^"\']+)', txt))):
        if not os.path.isfile(os.path.join(base, *ref.split("/"))):
            erros.append("asset ausente: " + ref)
    sem_alt = re.findall(r"<img\b(?![^>]*\balt=)[^>]*>", txt)
    if sem_alt:
        avisos.append("%d imagem(ns) sem atributo alt" % len(sem_alt))

    links = re.findall(r'href="(https://wa\.me/[^"]+)"', txt)
    numeros = set()
    if len(links) < 3:
        erros.append("esperava >= 3 links de WhatsApp (material, treinamento, contato); achei %d" % len(links))
    for l in links:
        u = urllib.parse.urlparse(html.unescape(l))
        num = u.path.strip("/")
        numeros.add(num)
        if not re.fullmatch(r"55\d{10,11}", num):
            erros.append("numero de WhatsApp fora do padrao 55+DDD+numero: " + num)
        if not urllib.parse.parse_qs(u.query).get("text", [""])[0].strip():
            erros.append("link de WhatsApp sem mensagem pronta: " + l[:60])
    if len(numeros) > 1:
        erros.append("links de WhatsApp com numeros diferentes: " + ", ".join(sorted(numeros)))

    if not re.search(r'<img src="assets/cliente/vendedor-[^"]+" alt="[^"]+"', txt):
        erros.append("cartao do vendedor sem foto ou sem alt")
    if len(re.findall(r'<li class="passo\b', txt)) != 4:
        erros.append("a linha do tempo precisa ter 4 passos")
    if not re.search(r"<h1>[^<]*Bem-vind[oa]s?,", txt):
        avisos.append("o h1 nao comeca com 'Bem-vindo(a)(s),'; confira a saudacao")

    for padrao, rotulo in ((r"R\$\s?\d", "valor em reais"), (r"\b\d+\s?%", "percentual"), (r"\bgarant", "promessa de garantia"),
                           (r"vende mais|aumenta(r)? (as )?vendas|fatur", "promessa de resultado")):
        m = re.search(padrao, visivel, flags=re.I)
        if m:
            avisos.append("texto com %s: %r (a pagina nao pode afirmar isso)" % (rotulo, visivel[max(0, m.start() - 20):m.end() + 20].strip()))

    chrome = None if "--sem-fotos" in args else achar_chrome(args[args.index("--chrome") + 1] if "--chrome" in args else None)
    fotos = []
    if chrome:
        pasta = os.path.join(os.path.dirname(base), "verificacao", os.path.basename(base))
        os.makedirs(pasta, exist_ok=True)
        url = "file:///" + idx.replace("\\", "/")
        for nome, larg, alt in (("desktop-1440", 1440, 3600), ("celular-390", 390, 6400)):
            png = os.path.join(pasta, nome + ".png")
            subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=9000", "--force-prefers-reduced-motion",
                            "--window-size=%d,%d" % (larg, alt), "--screenshot=" + png, url],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            if os.path.isfile(png):
                fotos.append(png)
        if "headless-shell" not in os.path.basename(chrome).lower():
            avisos.append("o Chrome comum limita a janela a ~500 px: a foto de 390 px sai cortada. Para conferir 390/320 use verificar-navegador.cjs")
    else:
        avisos.append("Chrome/Edge nao encontrado: sem fotos de conferencia (use --chrome CAMINHO)")

    print("Arquivo:", idx)
    for e in erros:
        print("ERRO:", e)
    for a in avisos:
        print("AVISO:", a)
    for f in fotos:
        print("FOTO:", f)
    print("RESULTADO:", "FALHOU" if erros else "OK (%d aviso(s))" % len(avisos))
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()


