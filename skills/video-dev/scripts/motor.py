"""Motor de animação para vídeos explicativos verticais (9:16, 1080x1920, 30 fps).

Nasceu dos vídeos "O que é SSH" e "Boas práticas de Git" (explicativos curtos de tecnologia).
Cada cena é uma lista de elementos; cada elemento entra no tempo `t` (segundos desde
o início da cena) com uma animação curta (sobe + aparece).

Uso dentro de um arquivo cenas.py:

    from motor import *          # elementos, cores e helpers

    def cenas():
        return [
            [Title(0.1, [("o que é ", INK), ("SSH", GREEN), ("?", INK)]),
             Laptop(1.0, L, 900, "você"), Server(1.4, R, 900, "servidor")],
            ...
        ]

O tema (cores) é escolhido ANTES de importar cenas.py, por render.py, chamando usar_tema().
Por isso cenas.py deve importar as cores com `from motor import *` (nunca copiar valores).
"""
import math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, SS = 1080, 1920, 30, 2  # SS = supersampling (desenha em 2x e reduz: bordas suaves)
PAD = 0.7  # respiro no fim de cada cena (s), depois da fala
CPS = 24   # caracteres por segundo ao "digitar" comandos no Term
L, R = 250, 830  # posições x padrão de cliente (esquerda) e servidor (direita)

# ---------------------------------------------------------------- temas
TEMAS = {
    # Dracula (draculatheme.com): fundo escuro, cores neon. Visual dos vídeos finais.
    "dracula": dict(
        BG=(40, 42, 54), INK=(248, 248, 242), WHITE=(248, 248, 242), SURFACE=(52, 55, 70),
        DARK=(68, 71, 90), TERM=(30, 31, 41), BLUE=(139, 233, 253), GREEN=(80, 250, 123),
        ORANGE=(255, 184, 108), PURPLE=(189, 147, 249), RED=(255, 85, 85), PINK=(255, 121, 198),
        GRAY=(98, 114, 164),
        FILLED_TEXT=(40, 42, 54),   # texto sobre caixa colorida preenchida
        NEUTRAL_FILL=(68, 71, 90),  # caixa preenchida "neutra" (cor INK)
    ),
    # Creme: fundo papel, caixas brancas com contorno colorido. Visual da 1ª versão do SSH.
    "creme": dict(
        BG=(243, 238, 228), INK=(20, 20, 20), WHITE=(255, 255, 255), SURFACE=(255, 255, 255),
        DARK=(45, 45, 45), TERM=(30, 30, 30), BLUE=(59, 111, 224), GREEN=(18, 147, 107),
        ORANGE=(217, 138, 11), PURPLE=(139, 92, 230), RED=(217, 72, 59), PINK=(214, 51, 132),
        GRAY=(120, 116, 108),
        FILLED_TEXT=(255, 255, 255),
        NEUTRAL_FILL=(20, 20, 20),
    ),
}
TEMA = "dracula"


def usar_tema(nome):
    """Troca as cores globais do módulo. Chamar antes de importar cenas.py."""
    global TEMA
    if nome not in TEMAS:
        raise SystemExit(f"tema '{nome}' não existe. Opções: {', '.join(TEMAS)}")
    TEMA = nome
    globals().update(TEMAS[nome])


usar_tema(TEMA)

# ---------------------------------------------------------------- fontes
# Windows: Bahnschrift (títulos/caixas) e Consolas Bold (código). Outros sistemas: tenta
# DejaVu / Liberation; em último caso a fonte padrão do Pillow.
_fonts = {}
_SANS = ["C:/Windows/Fonts/bahnschrift.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "arialbd.ttf"]
_MONO = ["C:/Windows/Fonts/consolab.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
         "/System/Library/Fonts/Menlo.ttc", "courbd.ttf"]


def _abrir(lista, px):
    for p in lista:
        try:
            return ImageFont.truetype(p, px), p
        except OSError:
            continue
    return ImageFont.load_default(px), None


def font(size, kind="bold"):
    """kind: 'bold' (títulos, caixas), 'semi' (textos), 'mono' (código)."""
    key = (size, kind)
    if key not in _fonts:
        px = int(size * SS)
        if kind == "mono":
            f, _ = _abrir(_MONO, px)
        else:
            f, caminho = _abrir(_SANS, px)
            if caminho and "bahnschrift" in caminho:
                f.set_variation_by_name({"bold": "Bold SemiCondensed", "semi": "SemiBold SemiCondensed"}[kind])
        _fonts[key] = f
    return _fonts[key]


# ---------------------------------------------------------------- utilidades
def S(v):
    return int(round(v * SS))


def mix(c, a, base=None):
    """Cor c com opacidade a sobre base (padrão: fundo). Usado para o fade-in."""
    base = BG if base is None else base
    return tuple(int(base[i] + (c[i] - base[i]) * a) for i in range(3))


def clamp(x):
    return max(0.0, min(1.0, x))


def ease(x):
    return 1 - (1 - clamp(x)) ** 3


# ---------------------------------------------------------------- elementos
class El:
    """Base: aparece no tempo t e leva `anim` segundos animando."""
    anim = 0.4

    def __init__(self, t):
        self.t = t

    def prog(self, now):
        return clamp((now - self.t) / self.anim)

    def state(self, now):
        # "off"/"on" = parado (permite reaproveitar o quadro); None = animando
        p = self.prog(now)
        return "off" if p <= 0 else ("on" if p >= 1 else None)


class Title(El):
    """Título centralizado; partes = [(texto, cor), ...] para colorir palavras."""

    def __init__(self, t, parts, y=250, size=92):
        super().__init__(t)
        self.parts, self.y, self.size = parts, y, size

    def draw(self, d, now):
        a = ease(self.prog(now))
        f = font(self.size)
        widths = [d.textlength(txt, font=f) for txt, _ in self.parts]
        x = (S(W) - sum(widths)) / 2
        y = S(self.y + (1 - a) * 25)
        for (txt, col), w in zip(self.parts, widths):
            d.text((x, y), txt, font=f, fill=mix(col, a), anchor="lm")
            x += w


class Text(El):
    """Texto solto, centralizado em (x, y). Aceita '\\n'. kind: semi | bold | mono."""

    def __init__(self, t, x, y, text, size=48, color=None, kind="semi"):
        super().__init__(t)
        self.x, self.y, self.text, self.size, self.kind = x, y, text, size, kind
        self.color = INK if color is None else color

    def draw(self, d, now):
        a = ease(self.prog(now))
        d.multiline_text((S(self.x), S(self.y + (1 - a) * 20)), self.text, font=font(self.size, self.kind),
                         fill=mix(self.color, a), anchor="mm", align="center", spacing=S(10))


class Box(El):
    """Caixa arredondada com texto. Contornada (padrão) ou preenchida (filled=True).

    Com color=INK e filled=True vira uma "pílula neutra" (destaque de frase).
    w/h fixam o tamanho; sem eles a caixa se ajusta ao texto.
    """

    def __init__(self, t, x, y, text, color=None, size=50, w=None, h=None, filled=False, radius=22, pad=34):
        super().__init__(t)
        self.x, self.y, self.text, self.size = x, y, text, size
        self.color = BLUE if color is None else color
        self.w, self.h, self.filled, self.radius, self.pad = w, h, filled, radius, pad

    def draw(self, d, now):
        a = ease(self.prog(now))
        f = font(self.size)
        l, tp, r, b = d.multiline_textbbox((0, 0), self.text, font=f, spacing=S(8))
        w = S(self.w) if self.w else (r - l) + S(self.pad * 2)
        h = S(self.h) if self.h else (b - tp) + S(self.pad * 1.1)
        cx, cy = S(self.x), S(self.y + (1 - a) * 22)
        box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
        if self.filled:
            neutral = self.color == INK
            d.rounded_rectangle(box, S(self.radius), fill=mix(NEUTRAL_FILL if neutral else self.color, a))
            tc = WHITE if neutral else FILLED_TEXT
        else:
            d.rounded_rectangle(box, S(self.radius), fill=mix(SURFACE, a), outline=mix(self.color, a), width=S(6))
            tc = self.color
        d.multiline_text((cx, cy), self.text, font=f, fill=mix(tc, a), anchor="mm", align="center", spacing=S(8))


class Line(El):
    """Linha que se desenha de p1 até p2 em `dur` s. arrow=True põe ponta; dashed=True tracejada."""

    def __init__(self, t, p1, p2, color=None, width=7, arrow=False, dashed=False, dur=0.6):
        super().__init__(t)
        self.p1, self.p2, self.width = p1, p2, width
        self.color = INK if color is None else color
        self.arrow, self.dashed, self.anim = arrow, dashed, dur

    def draw(self, d, now):
        p = ease(self.prog(now))
        if p <= 0:
            return
        (x1, y1), (x2, y2) = self.p1, self.p2
        ex, ey = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
        col = self.color
        if self.dashed:
            n = 16
            for i in range(0, n, 2):
                s0, s1 = i / n, (i + 1) / n
                if s0 > p:
                    break
                s1 = min(s1, p)
                d.line([(S(x1 + (x2 - x1) * s0), S(y1 + (y2 - y1) * s0)),
                        (S(x1 + (x2 - x1) * s1), S(y1 + (y2 - y1) * s1))], fill=col, width=S(self.width))
        else:
            d.line([(S(x1), S(y1)), (S(ex), S(ey))], fill=col, width=S(self.width))
        if self.arrow and p > 0.98:
            ang = math.atan2(y2 - y1, x2 - x1)
            Lp = 30
            pts = [(x2, y2),
                   (x2 - Lp * math.cos(ang - 0.45), y2 - Lp * math.sin(ang - 0.45)),
                   (x2 - Lp * math.cos(ang + 0.45), y2 - Lp * math.sin(ang + 0.45))]
            d.polygon([(S(px), S(py)) for px, py in pts], fill=col)


class Packet(El):
    """Pílula que viaja de p1 a p2 entre t e t+dur e some (ou fica, com stay=True).
    Ótima para mostrar dados indo pela rede ("senha: 123456", "x8#Kq!9")."""

    def __init__(self, t, p1, p2, text, color=None, dur=1.6, stay=False, size=40, mono=False):
        super().__init__(t)
        self.p1, self.p2, self.text = p1, p2, text
        self.color = INK if color is None else color
        self.anim, self.stay, self.size, self.mono = dur, stay, size, mono

    def state(self, now):
        if now < self.t:
            return "off"
        if now > self.t + self.anim:
            return "on"
        return None

    def draw(self, d, now):
        if now < self.t or (now > self.t + self.anim and not self.stay):
            return
        q = clamp((now - self.t) / self.anim)
        q = q * q * (3 - 2 * q)
        x = self.p1[0] + (self.p2[0] - self.p1[0]) * q
        y = self.p1[1] + (self.p2[1] - self.p1[1]) * q
        f = font(self.size, "mono" if self.mono else "bold")
        l, tp, r, b = d.textbbox((0, 0), self.text, font=f)
        w, h = (r - l) + S(40), (b - tp) + S(28)
        neutral = self.color == INK
        d.rounded_rectangle((S(x) - w / 2, S(y) - h / 2, S(x) + w / 2, S(y) + h / 2), h / 2,
                            fill=NEUTRAL_FILL if neutral else self.color)
        d.text((S(x), S(y)), self.text, font=f, fill=WHITE if neutral else FILLED_TEXT, anchor="mm")


class Terminal(El):
    """Janela de terminal onde TODAS as linhas são digitadas ao longo de `typing` s.
    lines = [(texto, cor), ...]. Bom para 1–5 linhas ilustrativas (vídeo de conceito)."""

    def __init__(self, t, x, y, lines, w=940, size=38, typing=1.5):
        super().__init__(t)
        self.x, self.y, self.lines, self.w, self.size = x, y, lines, w, size
        self.typing = typing
        self.anim = 0.3 + typing

    def draw(self, d, now):
        a = ease((now - self.t) / 0.3)
        if a <= 0:
            return
        lh = self.size * 1.45
        h = 100 + lh * len(self.lines)
        cx, cy = self.x, self.y + (1 - a) * 22
        x0, y0 = cx - self.w / 2, cy - h / 2
        d.rounded_rectangle((S(x0), S(y0), S(x0 + self.w), S(y0 + h)), S(24), fill=mix(TERM, a),
                            outline=mix(DARK, a), width=S(3))
        for i, c in enumerate([RED, ORANGE, GREEN]):
            d.ellipse((S(x0 + 34 + i * 34 - 9), S(y0 + 23), S(x0 + 34 + i * 34 + 9), S(y0 + 41)),
                      fill=mix(c, a, TERM))
        total = sum(len(s) for s, _ in self.lines)
        shown = int(total * clamp((now - self.t - 0.3) / self.typing))
        f = font(self.size, "mono")
        for i, (txt, col) in enumerate(self.lines):
            part = txt[:max(0, shown)]
            shown -= len(txt)
            d.text((S(x0 + 40), S(y0 + 78 + i * lh)), part, font=f, fill=mix(col, a, TERM), anchor="lm")


class Term(El):
    """Terminal de tutorial: cada linha começa no SEU tempo e é digitada a CPS letras/s.

    linhas = [(tempo, tipo, texto)]  — tempo relativo ao início da cena
      "$" comando (com prompt verde)   ">" continuação de comando
      "o" saída do comando (azul)      "#" comentário (cinza)
    Use quando o vídeo ensina comandos que a pessoa vai digitar junto.
    Cabem ~44 caracteres por linha com size=32 e w=960.
    """

    def __init__(self, t, y, linhas, w=960, size=32, x=540):
        super().__init__(t)
        self.x, self.y, self.linhas, self.w, self.size = x, y, linhas, w, size
        fim = max(lt + (len(txt) / CPS if k in "$>" else 0) for lt, k, txt in linhas)
        self.anim = fim - t + 0.05

    def draw(self, d, now):
        a = ease((now - self.t) / 0.3)
        if a <= 0:
            return
        lh = self.size * 1.55
        h = 96 + lh * len(self.linhas)
        x0, y0 = self.x - self.w / 2, self.y - h / 2 + (1 - a) * 22
        d.rounded_rectangle((S(x0), S(y0), S(x0 + self.w), S(y0 + h)), S(24), fill=mix(TERM, a),
                            outline=mix(DARK, a), width=S(3))
        for i, c in enumerate([RED, ORANGE, GREEN]):
            cx = x0 + 34 + i * 34
            d.ellipse((S(cx - 9), S(y0 + 23), S(cx + 9), S(y0 + 41)), fill=mix(c, a, TERM))
        f = font(self.size, "mono")
        for i, (lt, k, txt) in enumerate(self.linhas):
            if now < lt:
                continue
            y = S(y0 + 80 + i * lh)
            x = S(x0 + 38)
            if k in "$>":
                part = txt[:int((now - lt) * CPS)]
                if k == "$":
                    d.text((x, y), "$ ", font=f, fill=mix(GREEN, a, TERM), anchor="lm")
                    x += d.textlength("$ ", font=f)
                else:
                    x += d.textlength("    ", font=f)
                d.text((x, y), part, font=f, fill=mix(INK if TEMA == "dracula" else WHITE, a, TERM), anchor="lm")
            else:
                col = GRAY if k == "#" else BLUE
                d.text((x, y), txt, font=f, fill=mix(col, a, TERM), anchor="lm")


class Laptop(El):
    """Ícone de notebook com legenda embaixo (cliente, você...)."""

    def __init__(self, t, x, y, label="cliente", color=None):
        super().__init__(t)
        self.x, self.y, self.label = x, y, label
        self.color = BLUE if color is None else color

    def draw(self, d, now):
        a = ease(self.prog(now))
        x, y = self.x, self.y + (1 - a) * 22
        d.rounded_rectangle((S(x - 120), S(y - 85), S(x + 120), S(y + 65)), S(18), fill=mix(SURFACE, a),
                            outline=mix(INK, a), width=S(8))
        d.rounded_rectangle((S(x - 90), S(y - 55), S(x + 90), S(y - 35)), S(8), fill=mix(self.color, a))
        d.rounded_rectangle((S(x - 90), S(y - 20), S(x + 40), S(y - 4)), S(8), fill=mix(GRAY, a))
        d.rounded_rectangle((S(x - 90), S(y + 10), S(x + 10), S(y + 26)), S(8), fill=mix(GRAY, a))
        d.rounded_rectangle((S(x - 155), S(y + 70), S(x + 155), S(y + 92)), S(10), fill=mix(INK, a))
        d.text((S(x), S(y + 140)), self.label, font=font(46), fill=mix(INK, a), anchor="mm")


class Server(El):
    """Ícone de servidor (3 gavetas com LED) com legenda embaixo."""

    def __init__(self, t, x, y, label="servidor", color=None):
        super().__init__(t)
        self.x, self.y, self.label = x, y, label
        self.color = GREEN if color is None else color

    def draw(self, d, now):
        a = ease(self.prog(now))
        x, y = self.x, self.y + (1 - a) * 22
        for i in range(3):
            yy = y - 85 + i * 58
            d.rounded_rectangle((S(x - 105), S(yy), S(x + 105), S(yy + 48)), S(12), fill=mix(DARK, a))
            d.ellipse((S(x + 62), S(yy + 16), S(x + 78), S(yy + 32)), fill=mix(self.color, a, DARK))
            d.rounded_rectangle((S(x - 80), S(yy + 19), S(x + 10), S(yy + 29)), S(5), fill=mix(GRAY, a, DARK))
        d.text((S(x), S(y + 140)), self.label, font=font(46), fill=mix(INK, a), anchor="mm")


class Logo(El):
    """Quadrado colorido com uma palavra (ex.: "SSH", "git") que cresce ao aparecer."""

    def __init__(self, t, x, y, text="SSH", size=230, color=None):
        super().__init__(t)
        self.x, self.y, self.text, self.size = x, y, text, size
        self.color = PURPLE if color is None else color

    def draw(self, d, now):
        a = ease(self.prog(now))
        s = self.size * (0.8 + 0.2 * a) / 2
        x, y = self.x, self.y
        d.rounded_rectangle((S(x - s), S(y - s), S(x + s), S(y + s)), S(s * 0.24), fill=mix(self.color, a))
        d.text((S(x), S(y)), self.text, font=font(int(self.size * 0.36)), fill=mix(BG, a, self.color),
               anchor="mm")


# ---------------------------------------------------------------- helpers de cena
def selo(t, texto, cor, y=175):
    """Pílula pequena no topo (ex.: "PASSO 3", "DICA", "DEPOIS DO MERGE")."""
    return Box(t, 540, y, texto, cor, filled=True, size=34, radius=30)


def passo(n, titulo, cor):
    """Cabeçalho padrão de tutorial: selo 'PASSO n' + título colorido."""
    return [selo(0.1, f"PASSO {n}", cor), Title(0.2, titulo, y=285, size=84)]


def lista_vertical(t0, itens, y0=420, passo_y=132, dt=1.2, w=860, size=42):
    """Caixas empilhadas que entram uma a uma. itens = [(texto, cor), ...]."""
    return [Box(t0 + i * dt, 540, y0 + i * passo_y, txt, cor, w=w, size=size) for i, (txt, cor) in enumerate(itens)]


# ---------------------------------------------------------------- render de quadro
def duracao(mp3):
    out = subprocess.run([FFMPEG, "-i", mp3], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def quadro(els, now, cache, idx):
    """Desenha a cena no instante `now`. Quadros parados são reaproveitados (cache)."""
    estados = [e.state(now) for e in els]
    key = None if None in estados else (idx, tuple(estados))
    if key and key in cache:
        return cache[key]
    img = Image.new("RGB", (S(W), S(H)), BG)
    d = ImageDraw.Draw(img)
    for e in els:
        if now >= e.t:
            e.draw(d, now)
    img = img.resize((W, H), Image.LANCZOS)
    if key:
        cache.clear()
        cache[key] = img
    return img
