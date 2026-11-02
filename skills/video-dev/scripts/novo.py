"""Cria a pasta de um vídeo novo com os arquivos-base.

Uso:  python novo.py <pasta> --tipo conceito|tutorial [--titulo "O que é Docker"] [--tema dracula|creme]

Gera video.json, roteiro.json (rascunho com marcadores) e cenas.py (esqueleto com uma cena
de abertura pronta e as demais como lista vazia para preencher).
"""
import argparse, json, os

ESQ_CONCEITO = '''"""Cenas do vídeo: {titulo}. 1 lista de elementos por fala do roteiro.json."""
from motor import *


def cenas():
    c = []
    # 1 · abertura (gancho + "o problema / a solução / como funciona")
    c.append([
        Title(0.1, [("{titulo}", INK)]),
        Laptop(1.5, L, 900, "você"),
        Server(2.0, R, 900, "servidor"),
        Line(2.6, (L + 165, 900), (R - 135, 900), dashed=True, dur=0.8),
        Box(5.0, 540, 1380, "o problema", RED, size=46),
        Box(5.8, 540, 1520, "a solução", GREEN, size=46),
        Box(6.6, 540, 1660, "como funciona", BLUE, size=46),
    ])
    # demais cenas: preencha seguindo o roteiro (use os tempos de narracao.py --tempos N)
{resto}    return c
'''

ESQ_TUTORIAL = '''"""Cenas do tutorial: {titulo}. 1 lista de elementos por fala do roteiro.json."""
from motor import *


def cenas():
    c = []
    # 1 · abertura: tema + como acompanhar
    c.append([
        Title(0.1, [("{titulo}", INK)], y=260, size=96),
        Text(0.8, 540, 390, "passo a passo", 52, INK),
        Box(4.0, 540, 1080, "1 · pause o vídeo", BLUE, w=620, size=52),
        Line(4.6, (540, 1135), (540, 1205), arrow=True, dur=0.3),
        Box(5.2, 540, 1270, "2 · digite no terminal", GREEN, w=620, size=52),
        Line(5.8, (540, 1325), (540, 1395), arrow=True, dur=0.3),
        Box(6.4, 540, 1460, "3 · continue", PURPLE, w=620, size=52),
    ])
    # demais cenas: passo(n, titulo, cor) + Term(...) + caixa de dica/alerta
{resto}    return c
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--tipo", choices=["conceito", "tutorial"], required=True)
    ap.add_argument("--titulo", default="Título do vídeo")
    ap.add_argument("--tema", default="dracula")
    ap.add_argument("--cenas", type=int, default=12)
    a = ap.parse_args()

    os.makedirs(a.pasta, exist_ok=True)
    nome = os.path.basename(os.path.abspath(a.pasta))
    cfg = {"titulo": a.titulo, "nome": nome, "tema": a.tema, "tipo": a.tipo,
           "voz": "pt-BR-AntonioNeural", "rate": "+8%", "trilha": "synth"}
    json.dump(cfg, open(os.path.join(a.pasta, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    rot = os.path.join(a.pasta, "roteiro.json")
    if not os.path.exists(rot):
        falas = [f"FALA {i}: escreva aqui o texto falado da cena {i}." for i in range(1, a.cenas + 1)]
        json.dump(falas, open(rot, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    cen = os.path.join(a.pasta, "cenas.py")
    if not os.path.exists(cen):
        resto = "".join(f"    c.append([])  # {i}\n" for i in range(2, a.cenas + 1))
        esq = ESQ_CONCEITO if a.tipo == "conceito" else ESQ_TUTORIAL
        open(cen, "w", encoding="utf-8").write(esq.format(titulo=a.titulo, resto=resto))
    print("criado:", os.path.abspath(a.pasta))


if __name__ == "__main__":
    main()
