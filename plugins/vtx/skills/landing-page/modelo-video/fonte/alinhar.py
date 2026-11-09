# -*- coding: utf-8 -*-
"""Tempo das palavras da narracao. Sem reconhecimento de fala (faster-whisper bloqueado por politica
de Controle de Aplicativo do Windows): o texto e o do roteiro (a narracao foi gerada a partir dele) e o
tempo de cada palavra e estimado por silabas dentro do trecho de fala de cada frase."""
import json, re, sys

# trechos de fala NA LINHA DO TEMPO DO VIDEO (plano_voz.json, gerado por cronograma.py); 1 trecho por unidade do roteiro.
# A voz foi gerada a partir do roteiro, entao o texto e exato; o tempo de cada palavra dentro do trecho e estimado por silabas.
_plano = json.load(open("plano_voz.json", encoding="utf-8"))
FALA = [[p["ini"], p["fim"]] for p in _plano]
FRASES = [(p["texto"], [i]) for i, p in enumerate(_plano)]
SIL_FIXO = {"vtx": 3, "tap": 1, "whatsapp": 3, "sushi": 2, "seu": 1, "só": 1, "é": 1, "e": 1}

def silabas(p):
    k = re.sub(r"[^a-záéíóúâêôãõç]", "", p.lower())
    if k in SIL_FIXO:
        return SIL_FIXO[k]
    grupos = re.findall(r"[aeiouáéíóúâêôãõ]+", k)
    n = 0
    for g in grupos:
        # ditongos comuns contam como uma silaba; hiatos simples como duas
        n += 2 if re.search(r"[aáeéoó][aáeéoó]|[íú][aeiou]|[aeo]í|[aeo]ú", g) and len(g) == 2 and g not in ("ou", "ei", "ai", "au", "eu", "ão", "õe", "ae") else 1
    return max(1, n)

def alinhar():
    palavras = []
    for texto, idx in FRASES:
        trechos = [FALA[i] for i in idx]
        ws = texto.split()
        sil = [silabas(w) for w in ws]
        total = float(sum(sil))
        dur_total = sum(b - a for a, b in trechos)
        # posicao acumulada no eixo "so fala" -> tempo real
        def real(x):
            for a, b in trechos:
                d = b - a
                if x <= d + 1e-9:
                    return a + x
                x -= d
            return trechos[-1][1]
        acc = 0.0
        for w, s in zip(ws, sil):
            ini = real(acc / total * dur_total)
            acc += s
            fim = real(acc / total * dur_total)
            palavras.append({"w": w, "ini": round(ini, 3), "fim": round(fim, 3)})
    return palavras

if __name__ == "__main__":
    pal = alinhar()
    with open("palavras.json", "w", encoding="utf-8") as f:
        json.dump(pal, f, ensure_ascii=False, indent=1)
    for p in pal:
        print("%6.2f-%6.2f  %s" % (p["ini"], p["fim"], p["w"]))


