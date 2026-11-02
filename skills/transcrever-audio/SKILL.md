---
name: transcrever-audio
description: Transcreve arquivos de áudio (MP3, WAV, M4A, OGG/OPUS de WhatsApp, gravação de voz, podcast, aula, reunião) em texto com marcação de tempo, sem internet, usando Whisper no computador, e depois limpa, resume ou organiza o texto. Use sempre que o usuário mandar um áudio e pedir "transcreve", "passa pra texto", "o que fala nesse áudio", "resume essa gravação", "ata da reunião", "áudio do zap", ou quiser tirar a fala de um vídeo sem precisar das imagens. Atalho em português para a parte de áudio do plugin watch-video.
---

# Transcrever áudio

> **Caminhos:** `${CLAUDE_PLUGIN_ROOT}` é a raiz deste plugin. Se a variável não estiver definida,
> a raiz fica duas pastas acima do "Base directory" desta skill (`<raiz>/skills/<skill>`). Se as
> skills foram copiadas soltas para `~/.claude/skills`, use `~/.claude/skills` no lugar de
> `${CLAUDE_PLUGIN_ROOT}/skills`.

Usa o `transcribe.py` do plugin **watch-video** através do atalho `wv.py` (da skill
transcrever-video), que acha o plugin sozinho. Roda **offline**: o áudio não sai do computador.

```bash
WV=${CLAUDE_PLUGIN_ROOT}/skills/transcrever-video/scripts/wv.py
python $WV --checar                      # 1ª vez ou se der erro
```

## Transcrever

```bash
mkdir -p C:/tmp/audio-<nome>
python $WV transcribe C:/tmp/audio-<nome> --video "<arquivo de áudio>" --lang pt --model medium
```
- Apesar do nome, `--video` aceita qualquer áudio que o ffmpeg abra: mp3, wav, m4a, ogg, opus, flac.
- O primeiro argumento é a pasta de trabalho. Use um caminho **curto** (C:/tmp/...): o Windows
  quebra o Python em caminhos longos.
- Se a pasta já tiver um `audio.wav` de outra transcrição, use uma pasta nova. O script reaproveita
  o `audio.wav` que encontrar e você transcreveria o áudio antigo.

Escolha do modelo:
| Situação | Modelo |
|---|---|
| Fala técnica, nomes, termos em inglês, reunião de trabalho | `--model medium` (padrão recomendado) |
| Áudio casual de WhatsApp, só quer a ideia | `--model small` (3x mais rápido) |
| Áudio ruim ou muito importante | `--model large-v3` (bem mais lento, ~3 GB) |

Tempo medido nesta máquina: `medium` levou ~3 min para 1 min de áudio na primeira vez, contando o
download do modelo (~1,5 GB, uma vez só). Áudios com mais de 2 min: rode em segundo plano.

Outra língua: `--lang en`, `--lang es`... ou `--lang auto`.

## Resultado

- `<pasta>/transcript.md`: parágrafos com `(_MM:SS_)`.
- `<pasta>/transcript.txt`: um trecho por linha, com o tempo exato.

## Entregar

Leia o `transcript.md` e, antes de mostrar:
1. **Corrija** erros evidentes do Whisper (nomes, termos técnicos, palavras trocadas). Exemplos já
   vistos: "rougou" → roubou; "Tato Ilonen" → Tatu Ylönen. Marque com [?] o que não der para ter
   certeza.
2. Entregue no formato pedido:
   - **Transcrição**: texto corrido e limpo, em parágrafos, com os minutos de cada parte.
   - **Resumo**: 3 a 7 tópicos com o essencial.
   - **Ata de reunião**: decisões, tarefas (quem faz o quê), dúvidas em aberto.
   - **Áudio de WhatsApp**: uma ou duas frases com o recado.
3. Se for longo ou ele pedir arquivo, salve um `.md` na pasta que ele escolher (de preferência fora de pastas sincronizadas).
   Para notas do Obsidian, salve o `.md` direto na pasta do vault.

## Várias pessoas falando

O modelo local não diz quem fala. Para separar falantes há duas opções, ambas exigem configuração
(veja a skill `watch-video:watch-video`, seção multi-speaker):
- `--whisper whisperx`: grátis e local, mas precisa de token do Hugging Face e aceitar termos.
- `--whisper deepgram`: pago e online (manda o áudio para fora). **Só com autorização do usuário.**
Sem isso, transcreva normal e, se der, separe os falantes pelo contexto, avisando que é uma
inferência.

## Problemas conhecidos

| Erro | Solução |
|---|---|
| `unexpected keyword argument 'metadata_errors'` | `python -m pip install "av<16"` |
| `ffprobe`/`ffmpeg` não encontrado | `winget install Gyan.FFmpeg` |
| Transcreveu o áudio errado | a pasta tinha um `audio.wav` antigo: use outra pasta |
| Texto em inglês num áudio em português | faltou `--lang pt` |
