"""Confere se o computador tem tudo para fazer os vídeos. Com --instalar, instala o que faltar.

Uso:  python checar.py            python checar.py --instalar
"""
import importlib, os, subprocess, sys

PACOTES = {"edge_tts": "edge-tts", "PIL": "pillow", "imageio_ffmpeg": "imageio-ffmpeg", "numpy": "numpy"}
FONTES = ["C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/consolab.ttf"]

faltando = []
for mod, pip in PACOTES.items():
    try:
        importlib.import_module(mod)
        print(f"ok      {pip}")
    except ImportError:
        print(f"FALTA   {pip}")
        faltando.append(pip)

if faltando and "--instalar" in sys.argv:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", *faltando], check=True)
    print("instalado:", " ".join(faltando))
    faltando = []

try:
    import imageio_ffmpeg
    print("ok      ffmpeg ->", imageio_ffmpeg.get_ffmpeg_exe())
except Exception:
    print("FALTA   ffmpeg (vem com imageio-ffmpeg)")

for f in FONTES:
    print(("ok      " if os.path.exists(f) else "aviso   sem ") + os.path.basename(f) +
          ("" if os.path.exists(f) else " (vai usar fonte alternativa; o visual muda)"))

if faltando:
    print("\nRode:  python -m pip install " + " ".join(faltando) + "   (ou: python checar.py --instalar)")
    sys.exit(1)
print("\ntudo pronto (a voz precisa de internet na hora de gerar a narração)")
