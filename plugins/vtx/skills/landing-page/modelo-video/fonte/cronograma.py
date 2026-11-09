# -*- coding: utf-8 -*-
"""Cronograma unico do video: a partir da ORDEM e da duracao de cada trecho de voz calcula
(1) onde cada trecho entra no audio (plano_voz.json -> montar_voz.py e alinhar.py),
(2) todos os tempos de camera, etiquetas, tela, contador e CTA (assets/cues.js -> mundo.js e ui.html).
Ordem dos passos aprovada (2026-11-09): 1 = tres coisas; 2 = pagina do restaurante em ate 24 h;
3 = plaquinhas em 15 dias; 4 = treinamento. A voz comeca em 0,4 s (sem os 3 s de silencio).
Modelo para qualquer casa: a abertura NAO fala o nome (a unidade com o nome da casa foi retirada); o nome aparece so escrito (logo)."""
import json

T0 = 0.4
# (chave, texto, arquivo, inicio_no_arquivo, fim_no_arquivo)
O, N = "assets/voz-tts-original.mp3", "assets/voz-tts-24h.mp3"
SEG = [(0.000, 0.983), (1.209, 3.053), (3.398, 4.011), (4.317, 5.673), (5.988, 6.269), (6.608, 8.404), (8.655, 9.957),
       (10.150, 11.195), (11.490, 12.039), (12.286, 13.906), (14.151, 15.517), (15.734, 17.992), (18.235, 19.589),
       (19.873, 20.382), (20.624, 22.883), (23.219, 23.668), (23.907, 27.660), (27.887, 28.938), (29.185, 31.600)]
def o(i): return (O,) + SEG[i]
# (chave, texto, fonte, folga ANTES do trecho em s; None = folga natural da voz gerada)
U = [
    ("u2", "fechou com a VTX Tap.", o(1), None),
    ("u3", "E agora?", o(2), None),
    ("u4", "São quatro passos.", o(3), None),
    ("um", "Um:", o(4), 0.8),
    ("c1", "você manda três coisas.", o(9), 0.6),
    ("c2", "As imagens do cardápio,", o(10), 0.35),
    ("c3", "uma imagem para o banner e a sua logo.", o(11), 0.35),
    ("c4", "A gente cadastra tudo.", o(12), 0.35),
    ("dois", "Dois:", o(8), 0.9),
    ("h24", "Em até vinte e quatro horas depois de receber, a página do seu restaurante fica pronta.", (N, 0.0, 5.331), 0.6),
    ("p1", "É assim que ela vai ficar,", o(6), 0.35),
    ("p2", "com a sua cara.", o(7), 0.2),
    ("tres", "Três:", o(13), 0.9),
    ("d15", "em quinze dias, as plaquinhas chegam.", o(14), 0.6),
    ("quatro", "Quatro:", o(15), 0.9),
    ("trein", "quando chegarem, a gente marca o treinamento com a sua equipe e mostra todos os detalhes.", o(16), 0.6),
    ("f1", "Qualquer dúvida,", o(17), 1.1),
    ("f2", "é só me chamar no WhatsApp.", o(18), 0.3),
]
# ganho (dB) por arquivo, para casar o volume dos dois arquivos gerados
GANHO = {O: 0.0, N: 1.2}

plano, t, prev_fim_src = [], T0, None
for k, (chave, texto, (arq, a, b), folga) in enumerate(U):
    if k == 0:
        ini = T0
    elif folga is None:
        # folga natural entre dois trechos consecutivos do mesmo arquivo gerado
        ini = t + (a - prev_fim_src)
    else:
        ini = t + folga
    dur = b - a
    plano.append({"chave": chave, "texto": texto, "fonte": arq, "a": a, "b": b, "ini": round(ini, 3), "fim": round(ini + dur, 3), "ganho_db": GANHO[arq]})
    t, prev_fim_src = ini + dur, b
P = {p["chave"]: p for p in plano}
FIM_FALA = P["f2"]["fim"]
DUR = round(FIM_FALA + 2.1, 2)

def ini(k): return P[k]["ini"]
def fim(k): return P[k]["fim"]

# ---- tempos visuais (todos derivados do plano de voz) ----
sil_c3 = 9 / 14.0  # "uma imagem para o banner" = 9 de 14 silabas de c3
cue = {
    "dur": DUR, "fala_ini": T0,
    "fechou_ini": ini("u2") - 0.06, "fechou_fim": ini("u2") + 1.75,
    "lock_fim": ini("u4") - 0.15,
    "tiles": [ini("u4") + 0.2 + 0.22 * i for i in range(4)],
    # passo 1: tres coisas
    "p1_ini": ini("um"), "p1_fim": fim("c4") + 0.3,
    "dono_braco": [ini("um") - 0.1, ini("um") + 1.0], "celular_pop": [ini("um") + 0.3, ini("um") + 1.0],
    "cartao_ini": fim("c1") - 0.1, "dim_ini": fim("c1") - 0.15,
    "hl_cardapio": [ini("c2") + 0.0, fim("c2") + 0.05],
    "hl_banner": [ini("c3") + 0.0, ini("c3") + (fim("c3") - ini("c3")) * sil_c3 + 0.1],
    "hl_logo": [ini("c3") + (fim("c3") - ini("c3")) * sil_c3 + 0.15, fim("c3") + 0.05],
    "limpa_realces": ini("dois") - 0.1,
    # passo 2: pagina em ate 24 h
    "p2_ini": ini("dois"), "p2_fim": fim("p2") + 0.35,
    "cartao_fim": fim("p2") + 0.4, "dim_fim": fim("p2") + 0.6,
    # passo 3: 15 dias
    "p3_ini": ini("tres"), "p3_fim": fim("d15") + 0.8,
    "cena3_ini": fim("p2") + 0.4,
    "caminhao": [fim("p2") + 0.6, fim("d15") - 1.0],
    "caixa_pula": [fim("d15") - 0.75, fim("d15") + 0.05],
    "tampa": [fim("d15") - 0.05, fim("d15") + 0.4],
    "placa_sobe": [fim("d15") + 0.15, fim("d15") + 0.75],
    "contador": [ini("d15") + 0.3, fim("d15") + 0.1],
    # passo 4: treinamento
    "p4_ini": ini("quatro"), "p4_fim": fim("trein") + 0.9,
    "voo_salao": [ini("quatro") - 0.1, ini("trein") + 0.4],
    "celular_aproxima": [ini("trein") + 1.9, ini("trein") + 2.9],
    "aneis": [ini("trein") + 2.8, fim("trein") + 1.0],
    "braco_dono2": [ini("trein") + 1.4, ini("trein") + 2.2],
    "voo_volta": [fim("trein") + 0.85, ini("f1") + 1.3],
    "luzes": [fim("trein") + 0.9, fim("trein") + 3.0],
    # fecho
    "cta_ini": ini("f1") + 0.85, "trilha_fim": fim("trein") + 0.7,
}
json.dump(plano, open("plano_voz.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open("assets/cues.js", "w", encoding="utf-8").write(
    "/* gerado por cronograma.py - nao editar a mao */\nwindow.CUES = %s;\n" % json.dumps(cue, ensure_ascii=False, indent=1))
print("duracao do video: %.2f s | fala de %.2f a %.2f s" % (DUR, T0, FIM_FALA))
for p in plano:
    print("%-7s %6.2f-%6.2f  %s" % (p["chave"], p["ini"], p["fim"], p["texto"][:60]))
