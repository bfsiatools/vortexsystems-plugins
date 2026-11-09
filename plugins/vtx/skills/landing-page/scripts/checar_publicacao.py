# -*- coding: utf-8 -*-
"""Antes de tornar a skill publica: procura dados pessoais, de cliente ou segredos dentro da pasta da skill.

Uso:  py -I -X utf8 checar_publicacao.py [PASTA_DA_SKILL]      (padrao: a pasta acima de scripts/)
Sai com codigo 1 se achar algo que NAO pode ir para um repositorio publico.

Procura: telefones, e-mails que nao sejam os da empresa, caminhos de usuario do computador, chaves/tokens,
fotos de pessoas e videos (jpg/jpeg/mp4/mov), cadastro real da equipe e arquivos de cliente.
Os nomes proibidos (cliente, pessoas) ficam em .nomes-privados.txt (um por linha) NA RAIZ DO PROJETO, fora da skill,
para que a propria lista nao vire vazamento. Use --nomes CAMINHO para apontar outro arquivo.
"""
import os, re, sys

PERMITIDOS_EMAIL = {"contato@vortexsystems.tech"}            # contato institucional da empresa (ja e publico)
PERMITIDOS_ARQUIVOS_BINARIOS = {".ttf", ".svg", ".webp", ".png"}  # fontes, marca e o logo ficticio do exemplo
EXT_BLOQUEADAS = {".jpg", ".jpeg", ".mp4", ".mov", ".heic", ".gif", ".pdf", ".tar", ".gz", ".zip"}
PADROES = [
    (r"\(?\b\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b", "telefone"),
    (r"\b55\d{10,11}\b", "telefone com 55"),
    (r"[A-Za-z]:[\\/]Users[\\/][^\\/\s\"']+", "caminho de usuario do computador"),
    (r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,}\.)", "chave ou token"),
]
IGNORAR_DIRS = {".git", "node_modules", "__pycache__"}


def main():
    args = sys.argv[1:]
    raiz = os.path.abspath(args[0]) if args and not args[0].startswith("--") else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    nomes_arq = args[args.index("--nomes") + 1] if "--nomes" in args else None
    if not nomes_arq:
        p = raiz
        for _ in range(6):                               # sobe procurando .nomes-privados.txt
            c = os.path.join(p, ".nomes-privados.txt")
            if os.path.isfile(c):
                nomes_arq = c
                break
            p = os.path.dirname(p)
    nomes = []
    if nomes_arq and os.path.isfile(nomes_arq):
        nomes = [n.strip() for n in open(nomes_arq, encoding="utf-8-sig") if n.strip() and not n.startswith("#")]
    achados = []
    for d, ds, fs in os.walk(raiz):
        ds[:] = [x for x in ds if x not in IGNORAR_DIRS]
        for f in fs:
            c = os.path.join(d, f)
            rel = os.path.relpath(c, raiz)
            ext = os.path.splitext(f)[1].lower()
            if ext in EXT_BLOQUEADAS:
                achados.append((rel, "arquivo %s nao vai para repositorio publico (foto, video ou pacote)" % ext))
                continue
            if f.lower() in ("equipe.json", "cliente.json") and "exemplo" not in rel.lower():
                achados.append((rel, "cadastro real de equipe/cliente"))
            if ext in PERMITIDOS_ARQUIVOS_BINARIOS and ext not in (".svg",):
                continue
            try:
                t = open(c, encoding="utf-8").read()
            except Exception:
                continue
            if f == os.path.basename(__file__):
                continue
            for pad, rot in PADROES:
                for m in re.finditer(pad, t):
                    trecho = m.group(0)
                    if rot == "telefone" and re.fullmatch(r"\d{4}[-\s]?\d{4}", trecho):
                        continue
                    if re.sub(r"\D", "", trecho) in ("11900000000", "5511900000000", "900000000"):   # numero ficticio do exemplo, em qualquer arquivo
                        continue
                    achados.append((rel, "%s: %s" % (rot, trecho)))
            for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", t):
                if e.lower() not in PERMITIDOS_EMAIL and not e.lower().endswith("@exemplo.com"):
                    achados.append((rel, "e-mail: " + e))
            for n in nomes:
                if re.search(r"\b%s\b" % re.escape(n), t, flags=re.I):
                    achados.append((rel, "nome privado: " + n))
    if achados:
        for rel, o in sorted(set(achados)):
            print("BLOQUEIA:", rel, "->", o)
        print("RESULTADO: NAO PUBLICAR (%d achado(s))" % len(set(achados)))
        sys.exit(1)
    print("RESULTADO: limpo. Pasta verificada:", raiz, "| lista de nomes:", nomes_arq or "(nenhuma; crie .nomes-privados.txt)")


if __name__ == "__main__":
    main()


