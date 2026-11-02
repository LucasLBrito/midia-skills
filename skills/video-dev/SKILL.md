---
name: video-dev
description: Cria vídeos explicativos verticais (9:16, Shorts/Reels/TikTok) sobre temas de programação e tecnologia, com diagramas animados, narração em português e trilha de fundo, tudo gerado com Python e sem programas de edição. É o ponto de partida: faz as perguntas certas, prepara o computador, monta a pasta do vídeo e chama as skills video-conceito, video-tutorial-terminal, narracao-voz e trilha-video. Use sempre que o usuário pedir "fazer um vídeo", "vídeo explicativo", "vídeo curto", "vídeo pro TikTok/Reels/Shorts", "explicar X em vídeo", "tutorial em vídeo", ou quiser continuar, alterar ou refazer os vídeos de SSH e Git, mesmo que ele não diga a palavra "skill".
---

# Vídeos dev (hub)

> **Caminhos:** `${CLAUDE_PLUGIN_ROOT}` é a raiz deste plugin. Se a variável não estiver definida,
> a raiz fica duas pastas acima do "Base directory" desta skill (`<raiz>/skills/<skill>`). Se as
> skills foram copiadas soltas para `~/.claude/skills`, use `~/.claude/skills` no lugar de
> `${CLAUDE_PLUGIN_ROOT}/skills`.

Esta skill guarda o que foi aprendido fazendo os vídeos **"O que é SSH"** e **"Boas práticas de
Git e GitHub"**.
O resultado é um MP4 vertical 1080x1920 a 30 fps, com animações desenhadas quadro a quadro em
Python (Pillow), voz neural grátis (edge-tts) e música composta por código (numpy). Não usa
After Effects, CapCut nem nenhum programa pago.

Responda em português do Brasil, simples, resultado primeiro.

## Mapa das skills

| Skill | Quando usar |
|---|---|
| **video-dev** (esta) | Sempre primeiro: perguntas, preparação, pasta, render final, entrega |
| **video-conceito** | Explicar *como algo funciona* (SSH, DNS, HTTPS, Docker, JWT...): diagramas, pacotes viajando |
| **video-tutorial-terminal** | Ensinar *comandos para digitar junto* (Git, Docker CLI, npm, Linux...): terminal com digitação |
| **narracao-voz** | Escrever/ajustar o roteiro falado, voz, pronúncia de termos em inglês, tempos das palavras |
| **trilha-video** | Música de fundo e mixagem com a voz (ducking) |

Leia a skill do tipo escolhido assim que souber o tipo. Narração e trilha você pode ler quando
chegar nessas etapas.

## Caminhos

```
SK = ${CLAUDE_PLUGIN_ROOT}/skills   (raiz do plugin; veja "Caminhos" abaixo)
SK/video-dev/scripts/            motor.py, render.py, novo.py, checar.py
SK/video-dev/exemplos/ssh/       projeto completo do vídeo de SSH (conceito)
SK/video-dev/exemplos/git/       projeto completo do vídeo de Git (tutorial)
SK/narracao-voz/scripts/         narracao.py, pronuncia_base.json
SK/trilha-video/scripts/         trilhas.py, mixar.py
SK/video-dev/references/         elementos.md (API e layout), licoes.md (erros já cometidos)
```

## Passo 1 — Perguntar (antes de qualquer arquivo)

Faça as perguntas com a ferramenta AskUserQuestion, numa única rodada de até 4 perguntas, com a
opção recomendada primeiro. Pule o que o usuário já respondeu no pedido. Se ele disser "decide você",
use os padrões (em negrito).

**Rodada 1 (sempre):**
1. **Tipo de vídeo**: **conceito** (como funciona, com diagramas) · tutorial de terminal (comandos
   passo a passo) · misto (conceito e depois os comandos: use a skill de conceito e pegue o `Term`
   emprestado da de tutorial).
2. **Visual**: **Dracula** (escuro, cores neon, igual aos vídeos finais) · creme (fundo papel,
   caixas brancas, estilo papel).
3. **Duração**: **curto, até 60 s** (5–6 cenas, bom para Shorts) · médio, 1:30–2 min (8–10 cenas)
   · completo, ~3 min (12–14 cenas, como os de SSH e Git).
4. **Trilha**: **synth** (tech minimalista, a usada nos vídeos) · lofi · ambiente · piano · sem trilha.

**Rodada 2 (só se ainda não estiver claro):**
- Público: **iniciante** (explica todo termo) ou quem já programa (vai direto ao ponto).
- Voz: **pt-BR-AntonioNeural** (masculina, a usada) ou pt-BR-FranciscaNeural (feminina).
  Rode `narracao.py --vozes` para ver as outras.
- Pontos obrigatórios: o que não pode faltar? Algum exemplo, comando ou história específica?
- Fechamento: resumo/checklist (padrão), chamada "salva esse vídeo" ou pergunta para comentar.

Antes de seguir, confirme em 2 ou 3 linhas: tema, tipo, visual, duração, nº de cenas e trilha.

## Passo 2 — Preparar o computador (uma vez por máquina)

```bash
python SK/video-dev/scripts/checar.py
```
Se faltar algo: `python SK/video-dev/scripts/checar.py --instalar` (instala `edge-tts`, `pillow`,
`imageio-ffmpeg` e `numpy` via pip; o ffmpeg vem dentro do imageio-ffmpeg, sem instalar nada no
sistema). As fontes Bahnschrift e Consolas já vêm no Windows.

Avise o usuário uma vez: **a voz usa a internet**. O texto do roteiro vai para o serviço de voz da
Microsoft. A animação e a música rodam 100% no computador.

Cuidado com caminhos longos no Windows: o Python falha com "File name too long" em pastas muito
fundas (como a pasta temporária do Claude). Trabalhe numa pasta curta.

## Passo 3 — Criar a pasta do vídeo

Prefira uma pasta **fora de pastas sincronizadas** (OneDrive, Dropbox, iCloud): o render grava milhares
de quadros e a sincronização deixa tudo lento. Sugestão: `~/Projetos/videos/<nome-curto>/`. Pergunte
se o usuário preferir outro lugar.

```bash
python SK/video-dev/scripts/novo.py <pasta> --tipo conceito --titulo "O que é Docker" --tema dracula --cenas 12
```
Estrutura (1 fala do roteiro = 1 cena):
```
<pasta>/
  video.json     titulo, nome do arquivo, tema, voz, rate, trilha
  roteiro.json   ["fala da cena 1", "fala da cena 2", ...]
  pronuncia.json opcional: termos do projeto -> grafia para a voz
  cenas.py       def cenas(): return [[elementos da cena 1], ...]
  audio/         cena01.mp3 + cena01.json (tempo de cada palavra)
  saida/         <nome>.mp4, <nome>_trilha.mp4, poster.jpg, preview/
```

## Passo 4 — Roteiro → mostrar ao usuário → aprovar

Escreva o roteiro seguindo a skill do tipo (conceito ou tutorial) e as regras de fala da skill
**narracao-voz**. **Mostre o roteiro antes de animar**: é muito mais barato mudar texto do que
cenas. Só siga depois do ok.

## Passo 5 — Narração

```bash
python SK/narracao-voz/scripts/narracao.py <pasta>
python SK/narracao-voz/scripts/narracao.py <pasta> --tempos 3     # quando cada palavra da cena 3 é dita
```
A narração vem **antes** das cenas, porque a duração de cada cena é a duração da fala + 0,7 s, e
os elementos entram no segundo em que a palavra correspondente é dita.

## Passo 6 — Cenas (animação)

Escreva `cenas.py` usando `from motor import *` (API completa em `references/elementos.md`).
Para cada cena: rode `--tempos N`, escolha o que aparece em cada palavra-chave e use esse tempo
(ou 0,2 s antes) no `t` do elemento.

Confira olhando os quadros, não só lendo o código:
```bash
python SK/video-dev/scripts/render.py <pasta> --preview      # último quadro de cada cena
python SK/video-dev/scripts/render.py <pasta> --cena 4       # cena 4, um quadro por segundo
```
Abra os PNG com a ferramenta Read e verifique: nada cortado nas bordas, nada sobreposto, texto
grande o bastante para ler no celular, nada importante nos 250 px de baixo (onde ficam a legenda
e os botões do TikTok/Reels).

## Passo 7 — Render final + trilha

```bash
python SK/video-dev/scripts/render.py <pasta>                         # saida/<nome>.mp4 + poster.jpg
python SK/trilha-video/scripts/mixar.py <pasta>/saida/<nome>.mp4 synth  # saida/<nome>_trilha.mp4
```
Um vídeo de 3 min leva alguns minutos para renderizar: rode em segundo plano.

## Passo 8 — Conferir e entregar

- Confira com ffmpeg a duração e se há áudio (`ffmpeg -i arquivo.mp4` mostra os streams).
- Extraia 3 ou 4 quadros do MP4 final em pontos diferentes e olhe.
- Entregue com SendUserFile (`display: "render"`) e diga onde a pasta está.
- Se ele quiser uma página para assistir ou compartilhar (como a dos vídeos de SSH e Git),
  publique como Artifact com os MP4 e os scripts em `files`. Só torne público se ele pedir.
- Nada vai para o YouTube/TikTok/GitHub sem autorização do usuário.

## Mudanças comuns depois de pronto

| Pedido | O que fazer |
|---|---|
| Trocar uma frase | editar `roteiro.json` → `narracao.py --so N` → ajustar tempos da cena N → render |
| Pronúncia errada | `pronuncia.json` no projeto → `narracao.py --so N` (veja narracao-voz) |
| Outro visual | `--tema creme` no render, ou mudar `tema` no `video.json` |
| Música alta/baixa | `mixar.py ... --trilha 0.25` (veja trilha-video) |
| Versão curta de um vídeo longo | novo projeto copiando só as cenas-chave e um roteiro enxuto |

Antes de começar, leia `references/licoes.md`: são os erros e acertos dos dois primeiros vídeos.
