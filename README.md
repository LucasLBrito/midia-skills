# midia-skills

Plugin do Claude Code com 8 skills em português para trabalhar com mídia:

- **criar** vídeos explicativos verticais (9:16, Shorts/Reels/TikTok) com animação, narração e
  trilha, tudo gerado em Python, sem programas de edição;
- **gerar** falas (voz neural) e trilhas de fundo sem direitos autorais;
- **transcrever e entender** vídeos, áudios e imagens, offline.

## Skills

| Skill | Para quê | Exemplo de pedido |
|---|---|---|
| `video-dev` | Ponto de partida dos vídeos: perguntas, preparação, pasta, render e entrega | "faz um vídeo explicando o que é DNS" |
| `video-conceito` | Vídeos "como X funciona", com diagramas, cliente/servidor e pacotes na rede | "vídeo sobre como o HTTPS funciona" |
| `video-tutorial-terminal` | Tutoriais com comandos digitados na tela, no ritmo da fala | "tutorial em vídeo de Docker para iniciantes" |
| `narracao-voz` | Narração pt-BR (edge-tts), pronúncia de termos em inglês, tempo de cada palavra | "gera uma fala dizendo..." |
| `trilha-video` | Trilhas por código (synth, lofi, ambiente, piano) e mixagem com ducking | "coloca uma trilha lofi nesse vídeo" |
| `transcrever-video` | Transcrição e quadros de vídeos locais ou de links (YouTube, TikTok...) | "resume esse vídeo do YouTube" |
| `transcrever-audio` | Áudio em texto (mp3, WhatsApp, reunião), offline | "passa esse áudio pra texto" |
| `entender-imagem` | Prints, fotos, diagramas, quadros de vídeo, OCR | "copia o texto desse print" |

Dois vídeos completos vêm como exemplo em `skills/video-dev/exemplos/`: **"O que é SSH"**
(conceito, 12 cenas) e **"Boas práticas de Git e GitHub"** (tutorial, 14 cenas).

## Instalação

### Como plugin

```bash
claude plugin marketplace add <caminho-ou-url-deste-repositório>
claude plugin install midia-skills@midia-skills
```
Ou pelo app: Plugins → adicionar marketplace → apontar para esta pasta.

### Como skills soltas

Copie as pastas de `skills/` para `~/.claude/skills/`. Nos `SKILL.md`, onde aparece
`${CLAUDE_PLUGIN_ROOT}/skills`, leia `~/.claude/skills`.

### Dependências

```bash
python -m pip install -r requirements.txt
```
- **Python 3.10+**.
- **FFmpeg** com ffprobe no PATH, para transcrever. Windows: `winget install Gyan.FFmpeg`. Para
  *criar* vídeos não é preciso, porque o `imageio-ffmpeg` já traz um ffmpeg.
- **Tesseract** (opcional, OCR). Windows: `winget install UB-Mannheim.TesseractOCR`. Para português,
  baixe `por.traineddata` de [tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast) para uma
  pasta (ex.: `~/tessdata`, junto com `eng.traineddata`) e aponte `TESSDATA_PREFIX` para ela.
- **Plugin [watch-video](https://github.com/MarcinSufa/claude-watch-video)** (MIT, de terceiros), que
  as skills de transcrição usam.
  O atalho `skills/transcrever-video/scripts/wv.py` encontra o plugin sozinho.
- Fontes: no Windows, Bahnschrift e Consolas (já vêm instaladas). Em outros sistemas o motor usa
  DejaVu ou a fonte padrão, e o visual muda um pouco.

Conferir tudo de uma vez:
```bash
python skills/video-dev/scripts/checar.py          # criar vídeos
python skills/transcrever-video/scripts/wv.py --checar   # transcrever
```

## Privacidade

- Animação, trilha, transcrição (Whisper local) e OCR rodam **no computador**.
- A **narração** usa o serviço de voz da Microsoft (edge-tts): o texto do roteiro vai para a internet.
- Baixar vídeos de links usa a internet.
- Provedores pagos de transcrição (Groq, OpenAI, Deepgram) só são usados se configurados de propósito.

## Uso rápido sem o Claude

```bash
# vídeo: criar pasta, narrar, prévia, render, trilha
python skills/video-dev/scripts/novo.py meu-video --tipo conceito --titulo "O que é DNS"
python skills/narracao-voz/scripts/narracao.py meu-video        # depois de escrever roteiro.json
python skills/video-dev/scripts/render.py meu-video --preview   # depois de escrever cenas.py
python skills/video-dev/scripts/render.py meu-video
python skills/trilha-video/scripts/mixar.py meu-video/saida/meu-video.mp4 synth

# fala e trilha avulsas
python skills/narracao-voz/scripts/narracao.py --texto "Olá!" --saida ola.mp3
python skills/trilha-video/scripts/trilhas.py lofi 60 minhas-trilhas

# refazer o vídeo de exemplo de SSH (copie a pasta antes)
cp -r skills/video-dev/exemplos/ssh /tmp/ssh
python skills/narracao-voz/scripts/narracao.py /tmp/ssh && python skills/video-dev/scripts/render.py /tmp/ssh
```

## Licença

MIT.
