---
name: video-tutorial-terminal
description: Roteiro e animação de vídeos TUTORIAL passo a passo com comandos de terminal digitados na tela no ritmo da narração (Git, GitHub CLI, Docker, npm, pip, Linux, SSH keygen, deploy...), para quem quer pausar e digitar junto, no formato vertical 9:16. Use quando o pedido for "tutorial em vídeo de X", "vídeo passo a passo", "vídeo ensinando comandos", "boas práticas de X em vídeo", "vídeo estilo o de Git", ou quando a skill video-dev escolher o tipo tutorial. Use junto com video-dev, que cuida das perguntas, da preparação e do render.
---

# Vídeo tutorial de terminal

> **Caminhos:** `${CLAUDE_PLUGIN_ROOT}` é a raiz deste plugin. Se a variável não estiver definida,
> a raiz fica duas pastas acima do "Base directory" desta skill (`<raiz>/skills/<skill>`). Se as
> skills foram copiadas soltas para `~/.claude/skills`, use `~/.claude/skills` no lugar de
> `${CLAUDE_PLUGIN_ROOT}/skills`.

O modelo é o vídeo **"Boas práticas de Git e GitHub"**: 14 cenas, ~3:37. O projeto completo está
em `${CLAUDE_PLUGIN_ROOT}/skills/video-dev/exemplos/git/` (roteiro.json, cenas.py, pronuncia.json). **Abra o
cenas.py do exemplo antes de escrever o seu.**

Se a skill video-dev ainda não foi seguida (perguntas, preparação, pasta), comece por ela.

## Antes de escrever: os comandos têm de funcionar

Quem assiste vai digitar o que aparece na tela. Liste os comandos do tutorial e, sempre que der,
**rode-os de verdade** numa pasta de teste para confirmar a sintaxe e copiar a saída real (ou uma
versão curta dela). Nunca invente flags. Se um comando precisa de conta, rede ou algo destrutivo
(push, deploy, rm), não rode: confira na documentação oficial.

## Estrutura

| # | Bloco | Conteúdo |
|---|---|---|
| 1 | **Abertura** | Tema + como acompanhar: "1 · pause o vídeo → 2 · digite no terminal → 3 · continue" |
| 2…n-1 | **Passos** | `passo(n, título, cor)` + `Term` com 1–4 comandos + uma caixa de dica ou alerta |
| entre passos | **Dicas** | Cena sem número, com `selo(0.1, "DICA", PINK)`, para boas práticas (ex.: Conventional Commits) |
| n | **Checklist** | Lista numerada com todos os passos + "salve e use no próximo projeto" |

Ordem: do que se faz uma vez (configurar) ao que se faz sempre (fluxo diário) e por fim ao
avançado (rebase, tags). Um passo por cena; se o passo tem mais de 4 comandos, divida em duas cenas.

## Roteiro

- Comece cada fala com "Passo N:" e diga **o que** e **por quê** antes do comando.
- Fale o comando como se lê: "git push, traço u, origin main"; "git switch traço c";
  "feat barra login"; "ponto gitignore". Na tela vai o comando real.
- Alertas importantes ganham frase própria: "Senha e chave de API nunca vão pro repositório."
- Termos em inglês: confira se estão no mapa de pronúncia (veja **narracao-voz**). Se o tema tem
  vocabulário próprio (docker compose, kubectl...), crie `pronuncia.json` no projeto.

## O terminal (`Term`)

```python
Term(1.0, 700, [                                   # t de entrada, y do centro
    (2.4, "$", 'git config --global user.name "Seu Nome"'),   # (tempo, tipo, texto)
    (5.4, "$", 'git config --global user.email "voce@mail.com"'),
    (6.2, "o", "saída do comando em azul"),
    (7.0, "#", "# comentário em cinza"),
])
```
- O tempo de cada linha = o momento em que a fala **começa a dizer** o comando (`--tempos N`).
- Digita 24 caracteres/s (`CPS` no motor). Um comando de 40 letras leva ~1,7 s; deixe a linha
  seguinte começar depois disso.
- Até ~44 caracteres por linha (size=32). Maior que isso: quebre com `\` e continue numa linha `">"`.
- Saídas (`"o"`) curtas e realistas. Encurte: "Initialized empty Git repository".
- Use dados de exemplo neutros: "Seu Nome", "voce@mail.com", "meu-projeto", "voce/meu-projeto.git".
  Nunca dados reais do usuário.

## Elementos de apoio que funcionaram

| Ideia | Como |
|---|---|
| Alerta ("nunca faça") | `Box(t, 540, y, "texto", RED, filled=True)` acima ou abaixo do terminal |
| Lembrete | `Box(t, 540, ~1030, "mesmo e-mail da conta do GitHub", ORANGE)` |
| Onde clicar no site | `Box` PURPLE com o caminho: "github.com: New repository\n(vazio, sem README)" |
| Fluxo de estados | 3 `Box` lado a lado (x 190/540/890, w=290) + `Line` com seta + `Text` mono embaixo (`git add`, `git commit`) |
| Branch saindo da main | `Line` GREEN horizontal (main) + 3 `Line` PURPLE formando um desvio + rótulos |
| Bom x ruim | caixas verdes com exemplos bons + `Text` RED mono com os ruins ("ajustes", "final2") |
| Versão semântica | `Text` grande "v1.4.2" + 3 caixas major/minor/patch com explicação em cinza |
| Checklist final | `lista_vertical(...)` ou Box com w=860 e cores diferentes por item |

## Ritmo

- Selo + título em 0,1–0,2 s. Terminal entra ~1 s, antes do primeiro comando.
- A caixa de dica ou alerta entra quando a fala chega nela, normalmente depois dos comandos.
- Cenas de 12–18 s. Tutoriais toleram cenas um pouco mais longas que vídeos de conceito, porque
  a pessoa está digitando.

## Checklist antes do render final

- [ ] Todo comando na tela foi testado ou conferido na documentação.
- [ ] Nenhuma linha do terminal passa da borda (veja o `--preview`).
- [ ] A numeração dos passos na fala bate com o selo "PASSO n" da tela.
- [ ] O checklist final tem todos os passos, na mesma ordem.
- [ ] Nada de dado pessoal real (e-mail, usuário, token) nos comandos.
