---
name: trilha-video
description: Compõe trilhas de fundo calmas por código, sem direitos autorais e sem internet (estilos lofi, ambiente, piano e synth), e mixa a música por baixo da narração de um vídeo com ducking (a música abaixa sozinha quando a voz fala), sem recodificar a imagem. Use quando pedirem música de fundo, trilha, "coloca uma música", "som ambiente", "a música tá alta/baixa", mixar voz e música, ou na etapa de trilha da skill video-dev. Funciona com qualquer MP4 narrado, não só os vídeos do motor.
---

# Trilha de fundo e mixagem

> **Caminhos:** `${CLAUDE_PLUGIN_ROOT}` é a raiz deste plugin. Se a variável não estiver definida,
> a raiz fica duas pastas acima do "Base directory" desta skill (`<raiz>/skills/<skill>`). Se as
> skills foram copiadas soltas para `~/.claude/skills`, use `~/.claude/skills` no lugar de
> `${CLAUDE_PLUGIN_ROOT}/skills`.

Scripts em `${CLAUDE_PLUGIN_ROOT}/skills/trilha-video/scripts/`:
- `trilhas.py`: compõe a música com numpy (síntese de instrumentos + reverb). Não usa samples.
- `mixar.py`: junta música e voz com ducking usando o ffmpeg do `imageio-ffmpeg`.

Precisa de `numpy` e `imageio-ffmpeg` (veja `video-dev/scripts/checar.py`).

## Estilos

| Estilo | Clima | Bom para |
|---|---|---|
| **synth** | arpejo eletrônico em 16 avos, sub-baixo, 92 BPM | tech, programação (**usado nos vídeos de SSH e Git**) |
| lofi | piano elétrico, bateria suave, chiado de vinil, 72 BPM | tutoriais longos, clima de estudo |
| ambiente | camadas longas e sinos esparsos, sem bateria | conceitos densos, segurança, voz em primeiro plano |
| piano | arpejos lentos de piano, 66 BPM | histórias, temas mais emocionais |

Se o usuário não souber qual escolher, gere amostras de 30 s de todos e mande para ele ouvir:
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/trilha-video/scripts/trilhas.py preview <pasta>/trilha
# -> opcao_lofi.mp3, opcao_ambiente.mp3, opcao_piano.mp3, opcao_synth.mp3
```

## Mixar (o normal)

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/trilha-video/scripts/mixar.py <video.mp4> synth
# -> <video>_trilha.mp4  (compõe a trilha com a duração exata do vídeo e mixa)
```
Opções:
- Um arquivo no lugar do estilo: `mixar.py video.mp4 minha_musica.mp3`. Só use música própria ou
  com licença livre. Na dúvida, use uma trilha composta pelo script.
- Saída com outro nome: `mixar.py video.mp4 synth final.mp4`.
- Volumes: `--trilha 0.32 --voz 0.667` (padrão, os níveis que ficaram bons nos vídeos de SSH e Git).

Ajuste fino:
| Reclamação | Faça |
|---|---|
| "música alta" | `--trilha 0.22` |
| "música some" | `--trilha 0.4` |
| "voz baixa" | `--voz 0.85` (até 1.0; acima disso pode distorcer, há um limitador no final) |

Só a faixa de áudio é refeita. A imagem é copiada sem perda, então mixar de novo leva segundos.

## Compor uma trilha avulsa

```bash
python trilhas.py synth 222 <pasta>      # 222 s -> <pasta>/synth_full.wav (fade de 3 s nas pontas)
```

## Como funciona o ducking

A voz é dividida em duas cópias: uma vai para a mixagem, a outra comanda um compressor
(`sidechaincompress`) aplicado à música. Quando há voz, a música abaixa (ratio 4, ataque de 30 ms,
volta em 450 ms). Nas pausas entre as cenas, ela sobe sozinha. Isso dá a sensação de "trilha
profissional" sem precisar ajustar volume à mão.

## Criar um estilo novo

Em `trilhas.py`, escreva uma função `meu_estilo(sec)` que devolve um array numpy em 44,1 kHz,
usando os instrumentos que já existem (`rhodes`, `piano`, `pad`, `pluck`, `bass`, `kick`,
`snare`, `hat`) e os efeitos (`lowpass`, `highpass`, `reverb`). Registre em `ESTILOS`. Mantenha a
música calma e sem melodia chamativa: ela fica por baixo de uma voz.
