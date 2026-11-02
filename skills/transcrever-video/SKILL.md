---
name: transcrever-video
description: Assiste e transcreve vídeos em português ou outra língua, de um arquivo no computador ou de um link (YouTube, TikTok, Instagram, Loom, Vimeo, X e ~1500 sites), tirando quadros (imagens) com marcação de tempo e a transcrição da fala, para resumir, responder perguntas sobre o vídeo, achar um momento, copiar comandos que aparecem na tela ou analisar um bug gravado. Use sempre que o usuário mandar um vídeo ou link de vídeo e pedir "transcreve", "resume esse vídeo", "o que ele fala", "assiste isso", "em que minuto...", "pega os comandos do vídeo", "legenda", mesmo sem dizer "skill". Atalho em português para o plugin watch-video.
---

# Transcrever e entender vídeo

> **Caminhos:** `${CLAUDE_PLUGIN_ROOT}` é a raiz deste plugin. Se a variável não estiver definida,
> a raiz fica duas pastas acima do "Base directory" desta skill (`<raiz>/skills/<skill>`). Se as
> skills foram copiadas soltas para `~/.claude/skills`, use `~/.claude/skills` no lugar de
> `${CLAUDE_PLUGIN_ROOT}/skills`.

Usa o plugin **watch-video** através do atalho `wv.py`, que acha a pasta do plugin sozinho (ela
muda entre sessões). As regras completas do plugin estão na skill `watch-video:watch-video`.
Leia-a se precisar de algo fora do que está aqui (Jira, falantes, lote de vídeos).

```bash
WV=${CLAUDE_PLUGIN_ROOT}/skills/transcrever-video/scripts/wv.py
python $WV --checar          # confere ffmpeg, faster-whisper, yt-dlp, av (1ª vez ou se der erro)
```

## Escolher as opções (decida sem perguntar)

| Situação | Opções |
|---|---|
| Vídeo falado em português | `--lang pt` (sempre: a detecção automática erra em trechos curtos) |
| Conteúdo técnico em PT (programação, termos em inglês) | `--lang pt --model medium` (o `small` escreve "SS-7" no lugar de SSH) |
| Conversa casual, só quer a ideia geral | `--lang pt` (modelo small, 3x mais rápido) |
| Pergunta específica ("em que minuto ele fala de X?") | acrescente `--highlights-prompt "<a pergunta>"` |
| Vídeo longo (> 10 min) e só interessa um trecho | `--start MM:SS --end MM:SS` |
| Tela com código, terminal ou texto pequeno | `--resolution 1280` |
| Quer economizar (vídeo com tela parada) | `--dedup` |
| Precisa procurar texto escrito na tela em muitos quadros | `--ocr --ocr-lang por+eng` → gera `ocr.txt` para buscar com grep. Tesseract instalado, idiomas em `~/tessdata` (eng, por). Ícones viram lixo; texto sai bom |
| Vídeo sem fala | `--no-audio` |

```bash
python $WV watch_video "<arquivo-ou-link>" --lang pt --model medium --dedup --workdir C:/tmp/watch-<nome>
```
Sempre passe `--workdir` com um caminho **curto** (C:/tmp/...). O Windows quebra o Python em caminhos
muito longos, como a pasta temporária do Claude.

Rode em segundo plano se o vídeo tiver mais de 3 minutos ou se for a primeira vez com `medium`
(o modelo tem ~1,5 GB e é baixado uma vez só).

## Ler o resultado

Na pasta de trabalho ficam:
- `transcript.md`: fala em parágrafos com `(_MM:SS_)`. É o principal.
- `transcript.txt`: um trecho por linha, para achar o segundo exato.
- `frames/t_NNN.jpg`: quadros. Os tempos estão em `meta.json` → `frames.timestamps_by_frame`.
- `report.html`: transcrição e quadros juntos numa página. Bom para mandar ao usuário.

Leia a transcrição inteira e de 6 a 10 quadros espalhados (com a ferramenta Read). Se a pergunta é
sobre um momento, leia mais quadros perto dele.

**Corrija a transcrição antes de citar.** O Whisper erra nomes e termos técnicos ("Diffie-Elma" =
Diffie-Hellman, "meio endemido" = man-in-the-middle). Use os quadros e o contexto para corrigir e
avise quando uma correção for um palpite.

## Responder

- Primeiro uma linha dizendo do que o vídeo trata.
- Depois o que foi pedido (resumo, resposta, comandos, passos), com os minutos: "(02:14)".
- Comandos ou código que aparecem na tela: copie dos quadros, não da fala, e diga se algum
  trecho ficou ilegível.
- Se o usuário quiser a transcrição em arquivo, salve um `.md` limpo (sem os erros do Whisper) na
  pasta que ele escolher.

## Problemas conhecidos

| Erro | Solução |
|---|---|
| `open() got an unexpected keyword argument 'metadata_errors'` | `python -m pip install "av<16"` (PyAV 16+ é incompatível com faster-whisper 1.2) |
| `ffprobe` não encontrado | `winget install Gyan.FFmpeg`. O wv.py já procura na pasta do winget |
| `File name too long` | use `--workdir C:/tmp/...` |
| Link privado ou que pede login | peça ao usuário para baixar o vídeo e passe o arquivo |
| Termos técnicos errados | `--model medium` (ou `large-v3`, mais lento ainda) |

O vídeo e o áudio ficam no computador: a transcrição local não manda nada para a internet. O
download de links usa a internet, naturalmente.
