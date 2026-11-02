"""Renderiza um vídeo a partir de uma pasta de projeto.

Estrutura da pasta:
  video.json      {"titulo": "...", "tema": "dracula", "voz": "...", "trilha": "synth", ...}
  roteiro.json    ["fala da cena 1", "fala da cena 2", ...]   (1 fala = 1 cena)
  cenas.py        def cenas(): return [[elementos da cena 1], [cena 2], ...]
  audio/          cena01.mp3 ... (gerado por narracao.py)

Uso:
  python render.py <pasta>                  -> <pasta>/saida/<nome>.mp4 + poster.jpg
  python render.py <pasta> --preview        -> último quadro de cada cena em saida/preview/
  python render.py <pasta> --cena 3         -> quadros da cena 3 a cada 1 s (conferir o timing)
  python render.py <pasta> --tema creme     -> força outro tema
Sem áudio ainda? O preview funciona: a duração é estimada pelo tamanho da fala.
"""
import argparse, importlib.util, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import motor  # noqa: E402


def carregar_cenas(pasta):
    spec = importlib.util.spec_from_file_location("cenas_projeto", os.path.join(pasta, "cenas.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, pasta)
    spec.loader.exec_module(mod)
    return mod.cenas()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--cena", type=int)
    ap.add_argument("--tema")
    ap.add_argument("--saida", help="nome do mp4 (sem extensão)")
    a = ap.parse_args()

    pasta = os.path.abspath(a.pasta)
    cfg_path = os.path.join(pasta, "video.json")
    cfg = json.load(open(cfg_path, encoding="utf-8")) if os.path.exists(cfg_path) else {}
    motor.usar_tema(a.tema or cfg.get("tema", "dracula"))  # antes de importar cenas.py!

    falas = json.load(open(os.path.join(pasta, "roteiro.json"), encoding="utf-8"))
    n = len(falas)
    lista = carregar_cenas(pasta)
    if len(lista) != n:
        raise SystemExit(f"roteiro tem {n} falas mas cenas.py tem {len(lista)} cenas — precisam ser iguais.")

    audios = [os.path.join(pasta, "audio", f"cena{i:02d}.mp3") for i in range(1, n + 1)]
    tem_audio = all(os.path.exists(p) for p in audios)
    if tem_audio:
        durs = [motor.duracao(p) + motor.PAD for p in audios]
    else:
        # estimativa: ~15 caracteres falados por segundo com rate +8%
        durs = [len(f) / 15 + motor.PAD for f in falas]
        print("aviso: sem áudio em audio/ — usando duração estimada (só serve para preview)")

    saida_dir = os.path.join(pasta, "saida")
    os.makedirs(saida_dir, exist_ok=True)

    if a.cena:
        i = a.cena
        d = os.path.join(saida_dir, f"cena{i:02d}")
        os.makedirs(d, exist_ok=True)
        t = 0.0
        while t < durs[i - 1]:
            motor.quadro(lista[i - 1], t, {}, i).save(os.path.join(d, f"t{t:05.1f}.png"))
            t += 1.0
        print(f"quadros da cena {i} ({durs[i-1]:.1f}s) em {d}")
        return

    if a.preview:
        d = os.path.join(saida_dir, "preview")
        os.makedirs(d, exist_ok=True)
        for i, (els, dur) in enumerate(zip(lista, durs), 1):
            motor.quadro(els, dur - 0.1, {}, i).save(os.path.join(d, f"cena{i:02d}.png"))
        print("preview pronto em", d)
        return

    if not tem_audio:
        raise SystemExit("falta a narração: rode narracao.py antes de renderizar o vídeo final.")

    # narração: cada fala + silêncio até completar a duração da cena
    narr = os.path.join(pasta, "audio", "narracao.wav")
    cmd = [motor.FFMPEG, "-y"]
    for p in audios:
        cmd += ["-i", p]
    filt = "".join(f"[{i}:a]apad=whole_dur={durs[i]:.3f}[a{i}];" for i in range(n))
    filt += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[out]"
    subprocess.run(cmd + ["-filter_complex", filt, "-map", "[out]", "-ar", "48000", narr], check=True,
                   capture_output=True)

    nome = a.saida or cfg.get("nome") or os.path.basename(pasta)
    mp4 = os.path.join(saida_dir, nome + ".mp4")
    W, H, FPS = motor.W, motor.H, motor.FPS
    enc = subprocess.Popen([motor.FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", narr, "-c:v", "libx264", "-preset", "medium",
                            "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                            "-movflags", "+faststart", mp4], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    cache, total = {}, 0
    for i, (els, dur) in enumerate(zip(lista, durs), 1):
        k = int(round(dur * FPS))
        for f in range(k):
            enc.stdin.write(motor.quadro(els, f / FPS, cache, i).tobytes())
        total += k
        print(f"cena {i}/{n} ok", flush=True)
    enc.stdin.close()
    enc.wait()

    # poster (capa) = fim da cena 1, que costuma ter o título e o "gancho"
    motor.quadro(lista[0], durs[0] - 0.1, {}, 1).convert("RGB").save(
        os.path.join(saida_dir, "poster.jpg"), quality=88)
    print(f"pronto: {mp4}  ({total / FPS:.1f}s)")


if __name__ == "__main__":
    main()
