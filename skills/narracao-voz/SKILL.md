---
name: narracao-voz
description: Gera narração em português do Brasil com voz neural grátis da Microsoft (edge-tts), um áudio por cena a partir de um roteiro, com correção da pronúncia de termos técnicos em inglês (commit, push, GitHub, Docker...) e o tempo exato de cada palavra para sincronizar animações. Também ensina a escrever um roteiro que soa natural falado. Use sempre que precisar de locução, voz, narração, "texto para fala", TTS, áudio narrado para vídeo, podcast curto ou apresentação, ou quando a voz pronunciar algo errado. Faz parte do fluxo da skill video-dev, mas funciona sozinha.
---

# Narração com voz neural

> **Caminhos:** `${CLAUDE_PLUGIN_ROOT}` é a raiz deste plugin. Se a variável não estiver definida,
> a raiz fica duas pastas acima do "Base directory" desta skill (`<raiz>/skills/<skill>`). Se as
> skills foram copiadas soltas para `~/.claude/skills`, use `~/.claude/skills` no lugar de
> `${CLAUDE_PLUGIN_ROOT}/skills`.

Script: `${CLAUDE_PLUGIN_ROOT}/skills/narracao-voz/scripts/narracao.py`. Precisa de `pip install edge-tts` e
de **internet**: o texto vai para o serviço de voz da Microsoft (grátis e sem chave). Não coloque
no roteiro nada que o usuário não queira mandar para fora.

## Uso

```bash
N=${CLAUDE_PLUGIN_ROOT}/skills/narracao-voz/scripts/narracao.py
python $N <pasta>                    # audio/cena01.mp3 ... + cena01.json (tempos das palavras)
python $N <pasta> --mostrar          # mostra o texto JÁ com as trocas de pronúncia (sem gerar)
python $N <pasta> --so 3 7           # refaz só as cenas 3 e 7
python $N <pasta> --tempos 3         # "  2.41s  chave" ... para sincronizar a animação
python $N <pasta> --voz pt-BR-FranciscaNeural --rate +0%
python $N --vozes                    # lista as vozes em português
```
Entrada: `<pasta>/roteiro.json`, uma lista de strings (uma fala por cena). A voz e o rate podem
ficar no `video.json` (`"voz"`, `"rate"`). Padrão: `pt-BR-AntonioNeural`, `+8%`.

**Fala avulsa** (vinheta, aviso, recado, teste de voz), sem pasta nem roteiro:
```bash
python $N --texto "Fala, pessoal! Hoje o assunto é Docker." --saida C:/tmp/vinheta.mp3
python $N --texto "..." --saida C:/tmp/f.mp3 --voz pt-BR-FranciscaNeural --rate +0%
```
O mapa de pronúncia base vale aqui também. Para várias falas avulsas, prefira uma pasta com
`roteiro.json`: sai um MP3 por fala.

Vozes pt-BR úteis: `pt-BR-AntonioNeural` (masc., a dos vídeos), `pt-BR-FranciscaNeural` (fem.),
`pt-BR-ThalitaMultilingualNeural` (fem., lida melhor com termos em inglês). Lista completa: `--vozes`.
Também há vozes de Portugal (`pt-PT-...`) e de outras línguas.

## Escrever para ser falado

O roteiro é lido por uma máquina. Escreva como se fala, não como se escreve:

| Na tela / na escrita | No roteiro |
|---|---|
| 1995 | mil novecentos e noventa e cinco |
| porta 22 | porta vinte e dois |
| SCP, AWS (siglas soletradas) | S C P, A W S (letras separadas) |
| `git push -u origin main` | git push, traço u, origin main |
| `feat/login` | feat barra login |
| `.gitignore`, `.env` | ponto gitignore, ponto env |
| `~/.ssh/known_hosts` | o arquivo known hosts |
| `<`, `>`, `=` | menos de, mais de, igual a |

- Frases curtas. A vírgula vira pausa: use-a para dar ritmo ("Conexão, troca de chaves, e
  autenticação.").
- Tom de conversa: "bora entender", "sabe aquela...?", "e o melhor:", "resumindo:".
- 25–45 palavras por cena (10–16 s em +8%).
- Evite parênteses e travessões: a voz não sabe o que fazer com eles.

## Pronúncia de termos em inglês

A voz pt-BR lê inglês como português. A correção é trocar o termo por uma grafia que soe certo,
**só no áudio** (o roteiro e a tela continuam com a palavra original).

- Mapa base com ~70 termos de dev: `scripts/pronuncia_base.json` (git, commit, push, GitHub, branch,
  Docker, deploy, API, JSON, frontend, Python, npm...).
- Termos do projeto: `<pasta>/pronuncia.json`, no mesmo formato. **Vence o mapa base.** Para
  desligar uma troca da base, mapeie o termo para ele mesmo: `{"status": "status"}`.
- A troca é por palavra inteira, sem diferenciar maiúsculas, e os termos mais longos são trocados
  primeiro ("Pull Request" antes de "pull").

Como achar a grafia certa:
1. Escreva como um brasileiro leria em voz alta, com acento na sílaba forte: commit → "comít",
   push → "púch", GitHub → "guít-râb", release → "rilís", cache → "kéch".
2. Use hífen para separar partes: "és-és-êitch" (SSH), "ci-él-ái" (CLI).
3. Gere só aquela cena (`--so N`), ouça e ajuste. Se o usuário disser que algo soou errado, corrija
   no `pronuncia.json` do projeto. Se for um termo comum de dev, adicione também no
   `pronuncia_base.json`, assim os próximos vídeos já saem certos.

## Sincronizar com a animação

Cada `audio/cenaNN.json` tem `[{"t": 2.41, "palavra": "chave"}, ...]`, em segundos desde o início
da cena. Use esse `t` (ou 0,2 s antes) como tempo de entrada do elemento que representa a palavra.
A palavra aparece já com a grafia trocada ("comít"), o que é normal.

## Problemas comuns

| Sintoma | Causa / solução |
|---|---|
| `No module named edge_tts` | `python -m pip install edge-tts` |
| Erro de conexão / 403 | sem internet, ou a Microsoft mudou algo: `pip install -U edge-tts` |
| Voz rápida ou lenta demais | `--rate +0%` (mais lenta) ou `+15%` (mais rápida) |
| Termo lido errado | `pronuncia.json` (acima) |
| Cena longa demais (> 20 s) | divida a fala em duas cenas |
