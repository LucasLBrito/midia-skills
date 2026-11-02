"""Gera a narração: um MP3 por cena, com voz neural grátis da Microsoft (edge-tts).

Precisa de internet: o texto de cada fala é enviado ao serviço de voz da Microsoft.

Uso:
  python narracao.py <pasta>                     -> <pasta>/audio/cena01.mp3 ...
  python narracao.py <pasta> --so 3 5            -> refaz só as cenas 3 e 5
  python narracao.py <pasta> --mostrar           -> mostra o texto que a voz vai ler (sem gerar)
  python narracao.py <pasta> --tempos 4          -> mostra em que segundo cada palavra da cena 4 é dita
  python narracao.py <pasta> --voz pt-BR-FranciscaNeural --rate +0%
  python narracao.py --vozes                     -> lista as vozes pt-BR
  python narracao.py --texto "Olá, pessoal!" --saida C:/tmp/ola.mp3   -> fala avulsa, sem pasta

Lê:
  <pasta>/roteiro.json     lista de falas (1 por cena)
  <pasta>/video.json       opcional: {"voz": "...", "rate": "+8%"}
  pronuncia_base.json      (ao lado deste script) termos de dev em inglês -> grafia que soa certo
  <pasta>/pronuncia.json   opcional: termos do projeto (vence a base)
Grava também audio/cenaNN.json com o tempo de cada palavra (para sincronizar a animação).
"""
import argparse, asyncio, json, os, re, sys
import edge_tts

AQUI = os.path.dirname(os.path.abspath(__file__))
VOZ_PADRAO, RATE_PADRAO = "pt-BR-AntonioNeural", "+8%"


def carregar_mapa(pasta):
    mapa = {}
    for p in (os.path.join(AQUI, "pronuncia_base.json"), os.path.join(pasta, "pronuncia.json")):
        if os.path.exists(p):
            mapa.update(json.load(open(p, encoding="utf-8")))
    return mapa


def pronuncia(texto, mapa):
    """Troca termos em inglês (palavra inteira, sem diferenciar maiúsculas) pela grafia do mapa.
    Termos maiores primeiro, para 'Pull Request' vencer 'pull'."""
    for termo in sorted(mapa, key=len, reverse=True):
        texto = re.sub(rf"(?<![\w-]){re.escape(termo)}(?![\w-])", mapa[termo], texto, flags=re.IGNORECASE)
    return texto


async def gerar(texto, voz, rate, mp3, js):
    com = edge_tts.Communicate(texto, voz, rate=rate, boundary="WordBoundary")
    palavras = []
    with open(mp3, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                palavras.append({"t": round(ch["offset"] / 1e7, 2), "palavra": ch["text"]})
    json.dump(palavras, open(js, "w", encoding="utf-8"), ensure_ascii=False, indent=0)


async def listar_vozes():
    for v in await edge_tts.list_voices():
        if v["Locale"].startswith("pt-"):
            print(f'{v["ShortName"]:28} {v["Gender"]:7} {v["Locale"]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta", nargs="?")
    ap.add_argument("--so", type=int, nargs="+")
    ap.add_argument("--mostrar", action="store_true")
    ap.add_argument("--tempos", type=int)
    ap.add_argument("--voz")
    ap.add_argument("--rate")
    ap.add_argument("--vozes", action="store_true")
    ap.add_argument("--texto", help="fala avulsa (sem pasta): use com --saida")
    ap.add_argument("--saida", help="arquivo .mp3 da fala avulsa")
    ap.add_argument("--pronuncia", help="json extra de pronúncia para a fala avulsa")
    a = ap.parse_args()

    if a.vozes:
        asyncio.run(listar_vozes())
        return
    if a.texto:
        saida = os.path.abspath(a.saida or "fala.mp3")
        mapa = carregar_mapa(os.path.dirname(os.path.abspath(a.pronuncia)) if a.pronuncia else "")
        if a.pronuncia:
            mapa.update(json.load(open(a.pronuncia, encoding="utf-8")))
        os.makedirs(os.path.dirname(saida), exist_ok=True)
        asyncio.run(gerar(pronuncia(a.texto, mapa), a.voz or VOZ_PADRAO, a.rate or RATE_PADRAO,
                          saida, saida[:-4] + ".json"))
        print("ok", saida)
        return
    if not a.pasta:
        ap.error("informe a pasta do projeto")
    pasta = os.path.abspath(a.pasta)
    audio = os.path.join(pasta, "audio")

    if a.tempos:
        js = os.path.join(audio, f"cena{a.tempos:02d}.json")
        for p in json.load(open(js, encoding="utf-8")):
            print(f'{p["t"]:6.2f}s  {p["palavra"]}')
        return

    cfg_p = os.path.join(pasta, "video.json")
    cfg = json.load(open(cfg_p, encoding="utf-8")) if os.path.exists(cfg_p) else {}
    voz = a.voz or cfg.get("voz", VOZ_PADRAO)
    rate = a.rate or cfg.get("rate", RATE_PADRAO)
    mapa = carregar_mapa(pasta)
    falas = [pronuncia(t, mapa) for t in json.load(open(os.path.join(pasta, "roteiro.json"), encoding="utf-8"))]

    if a.mostrar:
        for i, f in enumerate(falas, 1):
            print(f"[{i}] {f}\n")
        return

    os.makedirs(audio, exist_ok=True)
    for i, texto in enumerate(falas, 1):
        if a.so and i not in a.so:
            continue
        mp3 = os.path.join(audio, f"cena{i:02d}.mp3")
        asyncio.run(gerar(texto, voz, rate, mp3, mp3[:-4] + ".json"))
        print("ok", mp3, flush=True)


if __name__ == "__main__":
    main()
