"""Põe a trilha de fundo por baixo da narração, com ducking (a música abaixa quando a voz fala).

Uso:
  python mixar.py <video.mp4> <estilo|arquivo.wav|arquivo.mp3> [saida.mp4] [--trilha 0.32] [--voz 0.667]

  <estilo> = lofi | ambiente | piano | synth -> a trilha é composta na hora com a duração exata do vídeo.
  Saída padrão: <video>_trilha.mp4. O vídeo não é recodificado (só o áudio).

Níveis que ficaram bons nos vídeos de SSH e Git: trilha 0.32, voz 0.667.
Música alta demais? baixe --trilha (0.2–0.25). Voz baixa? suba --voz até 1.0.
"""
import argparse, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import imageio_ffmpeg  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()


def duracao(p):
    out = subprocess.run([FF, "-i", p], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("trilha")
    ap.add_argument("saida", nargs="?")
    ap.add_argument("--trilha", dest="vt", type=float, default=0.32)
    ap.add_argument("--voz", dest="vv", type=float, default=0.667)
    a = ap.parse_args()

    video = os.path.abspath(a.video)
    saida = a.saida or video[:-4] + "_trilha.mp4"
    musica = a.trilha
    if not os.path.exists(musica):
        import trilhas
        if musica not in trilhas.ESTILOS:
            raise SystemExit(f"'{musica}' não é arquivo nem estilo ({', '.join(trilhas.ESTILOS)})")
        trilhas.OUT = os.path.join(os.path.dirname(video), "trilha")
        seg = duracao(video) + 1
        print(f"compondo trilha '{musica}' com {seg:.0f}s...", flush=True)
        musica = trilhas.salvar(trilhas.ESTILOS[musica](seg), musica + "_full", fade=3.0)

    # voz -> divide em 2: uma vai pra mixagem, outra comanda o compressor da música (sidechain)
    filt = (f"[0:a]volume={a.vv},asplit=2[voz][sc];"
            f"[1:a]volume={a.vt},aresample=48000[mus];"
            f"[mus][sc]sidechaincompress=threshold=0.04:ratio=4:attack=30:release=450[duck];"
            f"[voz][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", video, "-i", musica, "-filter_complex", filt,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", saida], check=True)
    print("pronto:", saida)


if __name__ == "__main__":
    main()
