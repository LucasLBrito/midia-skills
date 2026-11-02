"""Atalho para os scripts do plugin watch-video, que muda de pasta entre sessões.

Uso:
  python wv.py watch_video <args...>    -> scripts/watch_video.py (vídeo: quadros + transcrição)
  python wv.py transcribe <args...>     -> scripts/transcribe.py  (só áudio)
  python wv.py --onde                   -> mostra onde o plugin está
  python wv.py --checar                 -> confere dependências (ffmpeg, faster-whisper, av...)

Também põe o FFmpeg instalado pelo winget no PATH, caso o terminal ainda não o enxergue.
"""
import glob, os, shutil, subprocess, sys

HOME = os.path.expanduser("~")


def achar_plugin():
    cands = []
    raiz = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if raiz:
        cands.append(os.path.join(raiz, "scripts", "watch_video.py"))
    cands.append(os.path.join(HOME, ".claude", "skills", "watch-video", "scripts", "watch_video.py"))
    cands += glob.glob(os.path.join(HOME, "AppData", "Local", "Claude-Data", "*", "rpm", "**",
                                    "scripts", "watch_video.py"), recursive=True)
    cands += glob.glob(os.path.join(HOME, ".claude", "plugins", "**", "scripts", "watch_video.py"), recursive=True)
    achados = [c for c in cands if os.path.exists(c)]
    if not achados:
        raise SystemExit("plugin watch-video não encontrado. Instale o plugin watch-video (Plugins no app) ou clone-o em ~/.claude/skills/watch-video.")
    # mais recente primeiro (atualização do plugin cria pasta nova)
    achados.sort(key=os.path.getmtime, reverse=True)
    return os.path.dirname(achados[0])


def arrumar_path():
    # terminais abertos antes da instalação não enxergam o PATH novo
    if not shutil.which("ffprobe"):
        for b in glob.glob(os.path.join(HOME, "AppData", "Local", "Microsoft", "WinGet", "Packages",
                                        "Gyan.FFmpeg*", "*", "bin")):
            os.environ["PATH"] = b + os.pathsep + os.environ["PATH"]
            break
    tess = r"C:\Program Files\Tesseract-OCR"
    if not shutil.which("tesseract") and os.path.exists(os.path.join(tess, "tesseract.exe")):
        os.environ["PATH"] += os.pathsep + tess
    # idiomas do OCR (eng, por) ficam em ~/tessdata: Program Files exige admin
    td = os.path.join(HOME, "tessdata")
    if not os.environ.get("TESSDATA_PREFIX") and os.path.isdir(td):
        os.environ["TESSDATA_PREFIX"] = td


def checar():
    arrumar_path()
    ok = True
    for exe in ("ffmpeg", "ffprobe"):
        p = shutil.which(exe)
        print(("ok      " if p else "FALTA   ") + exe + ("" if p else "  -> winget install Gyan.FFmpeg"))
        ok &= bool(p)
    for mod, pip in (("faster_whisper", "faster-whisper"), ("yt_dlp", "yt-dlp"), ("imagehash", "imagehash")):
        try:
            __import__(mod)
            print("ok      " + pip)
        except ImportError:
            print(f"FALTA   {pip}  -> python -m pip install {pip}")
            ok = False
    try:
        import av
        maior = int(av.__version__.split(".")[0])
        if maior >= 16:
            print(f"ERRO    av {av.__version__}: incompatível com faster-whisper -> python -m pip install \"av<16\"")
            ok = False
        else:
            print(f"ok      av {av.__version__}")
    except ImportError:
        pass
    print("ok      tesseract (OCR, opcional)" if shutil.which("tesseract") else
          "aviso   sem tesseract: --ocr não funciona (opcional: winget install UB-Mannheim.TesseractOCR)")
    print("plugin:", achar_plugin())
    sys.exit(0 if ok else 1)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == "--onde":
        print(achar_plugin())
        return
    if sys.argv[1] == "--checar":
        checar()
    arrumar_path()
    alvo = os.path.join(achar_plugin(), sys.argv[1].removesuffix(".py") + ".py")
    if not os.path.exists(alvo):
        raise SystemExit(f"script não existe no plugin: {alvo}")
    sys.exit(subprocess.call([sys.executable, alvo, *sys.argv[2:]]))


if __name__ == "__main__":
    main()
