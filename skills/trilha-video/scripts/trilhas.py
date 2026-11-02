"""Trilhas de fundo calmas, sintetizadas do zero (sem direitos autorais, sem internet).

Uso:
  python trilhas.py preview [pasta]          -> 30 s de cada estilo: <pasta>/opcao_<estilo>.mp3
  python trilhas.py lofi 220 [pasta]         -> trilha 'lofi' com 220 s em <pasta>/lofi_full.wav
Estilos: lofi, ambiente, piano, synth.  Pasta padrão: ./trilhas
"""
import os, subprocess, sys
import numpy as np
import imageio_ffmpeg

SR = 44100
OUT = os.path.abspath("trilhas")
rng = np.random.default_rng(7)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(dur):
    return np.arange(int(dur * SR)) / SR


def add(buf, sig, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    n = min(len(sig), len(buf) - i)
    buf[i:i + n] += sig[:n]


def lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def reverb(x, secs=2.5, mix=0.3, tone=5000):
    ir = rng.standard_normal(int(secs * SR)) * np.exp(-t_(secs) / (secs / 5))
    ir = lowpass(ir, tone)
    ir /= np.abs(ir).sum() ** 0.5 * 4
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    wet = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
    wet *= np.abs(x).max() / (np.abs(wet).max() + 1e-9)
    return x * (1 - mix) + wet * mix


# ---------------------------------------------------------------- instrumentos
def rhodes(m, dur):
    t = t_(dur + 1.2)
    f = hz(m)
    env = np.exp(-t * 1.6) * np.minimum(1, t / 0.01)
    bell = np.exp(-t * 9)
    trem = 1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)
    s = np.sin(2 * np.pi * f * t) + 0.35 * bell * np.sin(2 * np.pi * f * 2 * t) + 0.15 * bell * np.sin(
        2 * np.pi * f * 3.98 * t)
    rel = np.clip((dur + 1.2 - t) / 1.2, 0, 1)
    return s * env * trem * rel


def piano(m, dur, vel=1.0):
    t = t_(dur + 2.0)
    f = hz(m)
    s = np.zeros_like(t)
    for n in range(1, 8):
        fn = f * n * (1 + 0.0004 * n * n)
        s += np.sin(2 * np.pi * fn * t) / n ** 1.4 * np.exp(-t * (0.9 + 0.7 * n))
    s *= np.minimum(1, t / 0.004)
    return s * vel


def pad(m, dur, atk=2.0, rel=3.0):
    t = t_(dur + rel)
    s = np.zeros_like(t)
    for d in (-0.07, 0.0, 0.06):
        f = hz(m + d)
        for n in range(1, 6):
            s += np.sin(2 * np.pi * f * n * t + rng.uniform(0, 6.28)) / n ** 1.6
    env = np.minimum(1, t / atk) * np.clip((dur + rel - t) / rel, 0, 1)
    return s * env / 3


def pluck(m, dur=0.4):
    t = t_(dur + 0.6)
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 20)
    return s * np.exp(-t * 7) * np.minimum(1, t / 0.003)


def bass(m, dur):
    t = t_(dur + 0.3)
    s = np.sin(2 * np.pi * hz(m) * t) + 0.2 * np.sin(2 * np.pi * hz(m) * 2 * t)
    return s * np.minimum(1, t / 0.02) * np.clip((dur + 0.3 - t) / 0.3, 0, 1) * np.exp(-t * 0.5)


def kick():
    t = t_(0.45)
    f = 45 + 80 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare():
    t = t_(0.3)
    n = highpass(rng.standard_normal(len(t)), 1500) * np.exp(-t * 22)
    return 0.6 * n + 0.3 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)


def hat():
    t = t_(0.08)
    return highpass(rng.standard_normal(len(t)), 7000) * np.exp(-t * 60)


# ---------------------------------------------------------------- estilos
def lofi(sec):
    """Lo-fi calmo: piano elétrico, baixo e bateria bem suave, chiado de vinil. 72 BPM."""
    beat = 60 / 72
    chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]  # Fmaj7 Em7 Dm7 Cmaj7
    roots = [41, 40, 38, 36]
    mel, dr = np.zeros(int(sec * SR)), np.zeros(int(sec * SR))
    bar, k = 4 * beat, 0
    while k * bar < sec:
        i = k % 4
        for j, m in enumerate(chords[i]):
            add(mel, rhodes(m, bar * 0.95) * 0.22, k * bar + j * 0.018)
        add(mel, bass(roots[i], bar * 0.9) * 0.35, k * bar)
        for b in range(4):
            at = k * bar + b * beat
            if b in (0, 2):
                add(dr, kick() * 0.5, at)
            if b in (1, 3):
                add(dr, snare() * 0.18, at)
            add(dr, hat() * 0.07, at)
            add(dr, hat() * 0.05, at + beat * 0.6)  # swing
        k += 1
    vinyl = lowpass(rng.standard_normal(len(mel)), 3000) * 0.012
    vinyl[rng.random(len(mel)) < 0.0004] += 0.15
    return lowpass(reverb(mel, 2.0, 0.25) + dr, 4500) + vinyl


def ambiente(sec):
    """Ambiente/foco: camadas longas que evoluem devagar e sinos esparsos. Sem bateria."""
    chords = [[50, 57, 62, 66, 69], [47, 54, 59, 62, 66], [43, 50, 55, 59, 62], [45, 52, 57, 61, 64]]
    x = np.zeros(int(sec * SR))
    dur, k = 8.0, 0
    while k * dur < sec:
        for m in chords[k % 4]:
            add(x, pad(m, dur, atk=2.5, rel=3.5) * 0.12, k * dur)
        k += 1
    x = lowpass(x, 1800)
    bells = np.zeros_like(x)
    escala = [74, 76, 78, 81, 83, 86]
    t = 1.5
    while t < sec:
        add(bells, piano(rng.choice(escala), 1.0) * 0.12, t)
        t += rng.uniform(1.8, 4.0)
    return reverb(x + bells, 4.0, 0.45, 3500)


def piano_suave(sec):
    """Piano suave: arpejos lentos sobre uma camada leve. 66 BPM."""
    beat = 60 / 66
    chords = [[45, 52, 57, 60, 64], [41, 48, 53, 57, 60], [36, 43, 48, 52, 55], [43, 50, 55, 59, 62]]  # Am F C G
    pat = [0, 1, 2, 3, 4, 3, 2, 1]
    x, p = np.zeros(int(sec * SR)), np.zeros(int(sec * SR))
    bar, k = 4 * beat, 0
    while k * bar < sec:
        ch = chords[k % 4]
        for j, idx in enumerate(pat):
            vel = 0.9 if j == 0 else 0.55 + 0.1 * rng.random()
            add(x, piano(ch[idx] + 12, beat / 2, vel) * 0.25, k * bar + j * beat / 2 + rng.uniform(0, 0.012))
        add(x, piano(ch[0], bar, 0.8) * 0.25, k * bar)
        for m in ch[2:]:
            add(p, pad(m, bar, atk=1.5, rel=2.0) * 0.05, k * bar)
        k += 1
    return reverb(x + lowpass(p, 1200), 3.0, 0.35, 4000)


def synth(sec):
    """Synth tech minimalista: arpejo de pluck em 16 avos, sub-baixo pulsando. 92 BPM."""
    beat = 60 / 92
    chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [55, 59, 62, 67]]  # Am F C G
    roots = [33, 29, 36, 31]
    x, lo, dr = (np.zeros(int(sec * SR)) for _ in range(3))
    bar, k = 4 * beat, 0
    order = [0, 2, 1, 3, 2, 0, 3, 1]
    while k * bar < sec:
        ch = chords[k % 4]
        for s in range(16):
            m = ch[order[s % 8]] + (12 if s % 8 == 7 else 0)
            add(x, pluck(m, 0.25) * (0.16 if s % 4 == 0 else 0.1), k * bar + s * beat / 4)
        for b in range(4):
            add(lo, bass(roots[k % 4] + 12, beat * 0.8) * 0.28, k * bar + b * beat)
            add(dr, hat() * 0.04, k * bar + b * beat + beat / 2)
        add(dr, kick() * 0.25, k * bar)
        add(dr, kick() * 0.2, k * bar + 2 * beat)
        k += 1
    sweep = 0.5 + 0.5 * np.sin(2 * np.pi * t_(sec)[:len(x)] / 32 - 1.5)
    x = lowpass(x, 2500) * (0.55 + 0.45 * sweep)
    return reverb(x, 2.2, 0.3) + lowpass(lo, 300) + dr


ESTILOS = {"lofi": lofi, "ambiente": ambiente, "piano": piano_suave, "synth": synth}


def salvar(x, nome, fade=2.0):
    x = x.copy()
    n = int(fade * SR)
    x[:n] *= np.linspace(0, 1, n)
    x[-n:] *= np.linspace(1, 0, n)
    x = x / (np.abs(x).max() + 1e-9) * 0.89
    os.makedirs(OUT, exist_ok=True)
    wav = os.path.join(OUT, nome + ".wav")
    pcm = (x * 32767).astype(np.int16)
    import wave
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return wav


def main():
    global OUT
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    extra = sys.argv[2:] if sys.argv[1] == "preview" else sys.argv[3:]
    if extra:
        OUT = os.path.abspath(extra[0])
    if sys.argv[1] == "preview":
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        for nome, fn in ESTILOS.items():
            wav = salvar(fn(30), nome + "_preview")
            subprocess.run([ff, "-y", "-loglevel", "error", "-i", wav, "-b:a", "160k",
                            os.path.join(OUT, f"opcao_{nome}.mp3")], check=True)
            print("ok", nome)
    else:
        nome, sec = sys.argv[1], float(sys.argv[2])
        print(salvar(ESTILOS[nome](sec), nome + "_full", fade=3.0))


if __name__ == "__main__":
    main()
