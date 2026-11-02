# Elementos do motor (motor.py) e regras de layout

Tudo vem de `from motor import *`. O tempo `t` de cada elemento é em segundos **desde o início da
cena**. O elemento sobe 20–25 px e aparece em 0,4 s (ease-out cúbico) e depois fica na tela até o
fim da cena. Cada cena começa vazia.

## Tela

- 1080 x 1920. O centro horizontal é **x = 540**. Coordenadas são o **centro** do elemento.
- Faixas usadas nos vídeos:
  - **y 150–200**: selo pequeno (PASSO n, DICA)
  - **y 250–290**: título
  - **y 400–1550**: conteúdo principal
  - **y 1550–1700**: fechamento da cena (frase de efeito em caixa preenchida)
  - **abaixo de 1700**: evite. A legenda e os botões do TikTok/Reels/Shorts cobrem essa área.
- Margem lateral: nada a menos de 40 px da borda. Uma caixa de `w=900` em x=540 é o máximo
  confortável.
- Posições padrão de dois atores: `L = 250` (esquerda, cliente) e `R = 830` (direita, servidor).
  Uma linha entre eles vai de `(L + 165, y)` até `(R - 135, y)`.
- Três caixas lado a lado: x = 190, 540, 890 com `w=290`.
- Espaço entre linhas de caixas empilhadas: 130–160 px.

## Cores (mudam com o tema)

`BG INK WHITE SURFACE DARK TERM BLUE GREEN ORANGE PURPLE RED PINK GRAY`

Significados que ficaram consistentes e ajudam quem assiste:
- **GREEN**: seguro, certo, solução, servidor, "pronto"
- **RED**: perigo, problema, senha, erro, "nunca faça"
- **BLUE**: cliente, informação neutra, saída do comando
- **ORANGE**: atenção, destaque, etapa intermediária
- **PURPLE**: identidade, chaves, o "conceito novo" do vídeo
- **PINK**: dica extra
- **GRAY**: comentário, texto secundário
- **INK**: texto normal. Em `Box(filled=True)` com INK vira uma pílula neutra (frase-resumo).

Temas: `dracula` (padrão) e `creme`. Para criar um novo, adicione um dict em `TEMAS` no motor.py
com as mesmas chaves, incluindo `FILLED_TEXT` e `NEUTRAL_FILL`.

## Elementos

| Elemento | Assinatura | Para quê |
|---|---|---|
| `Title` | `Title(t, [("texto", COR), ...], y=250, size=92)` | Título com palavras coloridas. Tutorial usa `y=285, size=84` |
| `Text` | `Text(t, x, y, "texto", size=48, color=INK, kind="semi")` | Texto solto, aceita `\n`. kind: `semi`, `bold`, `mono` |
| `Box` | `Box(t, x, y, "texto", COR, size=50, w=None, h=None, filled=False, radius=22)` | Caixa contornada ou preenchida. Aceita `\n` |
| `Line` | `Line(t, (x1,y1), (x2,y2), color=INK, width=7, arrow=False, dashed=False, dur=0.6)` | Linha que se desenha. Seta, tracejada (conexão insegura/caminho) |
| `Packet` | `Packet(t, p1, p2, "texto", COR, dur=1.6, stay=False, size=40, mono=False)` | Pílula que viaja de p1 a p2 e some: dados na rede |
| `Terminal` | `Terminal(t, x, y, [("linha", COR), ...], w=940, size=38, typing=1.5)` | Terminal ilustrativo: tudo digitado em `typing` s |
| `Term` | `Term(t, y, [(tempo, tipo, "texto"), ...], w=960, size=32)` | Terminal de tutorial: cada linha no seu tempo, 24 letras/s. tipo: `$` comando, `>` continuação, `o` saída, `#` comentário |
| `Laptop` | `Laptop(t, x, y, "legenda", color=BLUE)` | Computador do usuário/cliente |
| `Server` | `Server(t, x, y, "legenda", color=GREEN)` | Servidor |
| `Logo` | `Logo(t, x, y, "SSH", size=230, color=PURPLE)` | Quadrado com palavra, cresce ao entrar |

Helpers:
- `selo(t, "DICA", PINK)`: pílula pequena no topo.
- `passo(n, [("primeiro ", INK), ("commit", ORANGE)], ORANGE)`: devolve [selo PASSO n, título]. Use com `+ [...]`.
- `lista_vertical(t0, [("1 · conexão", BLUE), ...], y0=420, passo_y=132, dt=1.2)`: caixas empilhadas que entram uma a uma.

## Tamanhos de texto que funcionam no celular

- Título: 84–110. Números de impacto ("1995", "< 1 segundo"): 110–200.
- Caixa principal: 44–56. Caixa secundária: 40–44. Nada abaixo de 34.
- Terminal de tutorial: size=32 (cabem ~44 caracteres). Passou disso? Quebre com `\` e uma linha `>`.
- Texto mono solto (comando citado): 38–42.

## Como criar um elemento novo

Herde de `El`, guarde `t` e os parâmetros e implemente `draw(self, d, now)`:
- `a = ease(self.prog(now))` dá o progresso da entrada (0→1).
- Desenhe com `d` (ImageDraw) multiplicando coordenadas por `S()` (supersampling 2x).
- Use `mix(cor, a)` para o fade.
- Se o elemento se mexe depois de entrar, sobrescreva `state()` para devolver `None` enquanto
  anima. Sem isso, o cache congela o quadro.
Coloque elementos reutilizáveis no motor.py da skill (beneficia vídeos futuros). Elementos únicos
ficam no cenas.py do projeto.

Ideias que ainda não existem e caberiam bem: `Cadeado` (HTTPS/TLS), `Nuvem` (internet, cloud),
`Container` (Docker), `Banco` (cilindro de banco de dados), `Celular`, `Destaque` (círculo pulsando
ao redor de algo), `Barra` (barra de progresso).
