---
name: video-conceito
description: Roteiro e animação de vídeos explicativos de CONCEITO, sobre como uma tecnologia funciona por dentro (SSH, HTTPS/TLS, DNS, JWT, Docker, cache, OAuth, filas, hash de senha...), com diagramas animados de cliente e servidor, pacotes viajando pela rede e caixas que surgem no ritmo da narração, no formato vertical 9:16. Use quando o pedido for "explica como X funciona em vídeo", "vídeo sobre o que é X", "vídeo estilo o de SSH", ou quando a skill video-dev escolher o tipo conceito. Use junto com video-dev, que cuida das perguntas, da preparação e do render.
---

# Vídeo de conceito

> **Caminhos:** `${CLAUDE_PLUGIN_ROOT}` é a raiz deste plugin. Se a variável não estiver definida,
> a raiz fica duas pastas acima do "Base directory" desta skill (`<raiz>/skills/<skill>`). Se as
> skills foram copiadas soltas para `~/.claude/skills`, use `~/.claude/skills` no lugar de
> `${CLAUDE_PLUGIN_ROOT}/skills`.

O modelo é o vídeo **"O que é SSH"**: 12 cenas, ~3:17. O projeto completo está em
`${CLAUDE_PLUGIN_ROOT}/skills/video-dev/exemplos/ssh/` (roteiro.json + cenas.py). **Abra o cenas.py do exemplo
antes de escrever o seu**: ele é a melhor referência de ritmo, posições e uso de cada elemento.

Se a skill video-dev ainda não foi seguida (perguntas, preparação, pasta), comece por ela.

## Estrutura narrativa (arco que funcionou)

| # | Bloco | O que faz | Exemplo no SSH |
|---|---|---|---|
| 1 | **Gancho** | Situação do dia a dia + promessa: "bora entender o problema, a solução e como funciona" | digitar `ssh` e cair num servidor do outro lado do mundo |
| 2–3 | **Problema** | Como era antes e por que era ruim. Mostre o perigo acontecendo | Telnet em texto puro; espião no Wi-Fi do café lendo a senha |
| 4 | **Origem** | Quem criou, quando e por quê (um fato concreto) | 1995, Finlândia, Tatu Ylönen |
| 5 | **Ideia central** | A solução numa imagem só + anúncio das etapas | túnel criptografado; "3 etapas" |
| 6–10 | **Como funciona** | Uma etapa por cena, sempre com os mesmos atores nas mesmas posições | conexão, Diffie-Hellman, host key, chaves, desafio |
| 11 | **No dia a dia** | Onde a pessoa já usa sem saber | git push, scp, túneis |
| 12 | **Resumo** | Repete as etapas em lista + volta à imagem do gancho | 3 etapas + "< 1 segundo" + o mesmo comando |

Para vídeo curto (≤ 60 s), junte: gancho+problema (1), ideia central (1), como funciona (2–3),
resumo (1).

## Roteiro

- Uma fala por cena, 25–45 palavras (10–16 s com rate +8%).
- Fale com "você", tom de conversa: "bora entender", "sabe aquela mensagem...?", "e o melhor:".
- Cada fala precisa de **algo para desenhar**. Se você não consegue imaginar a imagem de uma frase,
  troque a frase por uma analogia concreta.
- Termine as cenas de "como funciona" com a consequência: "Sem que essa chave nunca tenha passado
  pela rede."
- Regras de escrita para a voz (números, siglas, termos em inglês): veja a skill **narracao-voz**.

## Vocabulário visual

| Ideia | Como desenhar |
|---|---|
| Dois lados conversando | `Laptop(t, L, y, "cliente")` + `Server(t, R, y, "servidor")` + `Line` entre eles |
| Dado indo pela rede | `Packet(t, (L+165, y), (R-135, y), "texto", COR, mono=True)` |
| Resposta voltando | `Packet` de R para L, 40–70 px acima ou abaixo da ida |
| Conexão insegura ou caminho | `Line(..., dashed=True)` |
| Conexão segura | `Box(t, 540, y, " ", GREEN, w=330, h=120, radius=60)` (o "túnel") + pacote embaralhado |
| Perigo/espião | `Box` RED ao lado + `Line` RED tracejada apontando |
| Cadeia de passos | `Box` empilhados em x=330 ligados por `Line` curtas (o caminho dos dados) |
| Resultado igual dos dois lados | mesma `Box(filled=True)` sob L e R + `Text("=")` no meio |
| Data ou número marcante | `Text(t, 540, y, "1995", 200, INK, "bold")` |
| Lista de etapas | `Box` com `w=600` fixo, "1 · ...", "2 · ...", mesma cor de cada etapa no vídeo todo |
| Comando real | `Terminal(t, 540, y, [("$ ssh voce@servidor", GREEN)], typing=1.4)` |
| Frase-resumo da cena | `Box(t, 540, ~1450, "frase", INK, filled=True)` |
| Hub com aplicações | `Logo` no centro + 4 `Line` diagonais + 4 `Box` nos cantos |

Mantenha os atores no mesmo lugar em todas as cenas (cliente sempre à esquerda). Dê a cada etapa
uma cor e use essa mesma cor sempre que a etapa aparecer (no SSH: conexão BLUE, troca de chaves
ORANGE, autenticação PURPLE).

## Ritmo dentro da cena

- 0,1 s: título. 0,6–1,6 s: atores principais (já aparecem enquanto a frase começa).
- Depois, cada elemento no tempo da palavra dele (`narracao.py <pasta> --tempos N`).
- 4 a 9 elementos por cena. Mais que isso vira poluição.
- Um `Packet` leva 1,6–2,0 s. Comece-o quando a fala diz o verbo ("trocam", "manda").
- O último elemento entra até ~1,5 s antes do fim da fala, para dar tempo de ler.

## Checklist antes do render final

- [ ] Todas as cenas têm título.
- [ ] Nenhum elemento abaixo de y≈1700 nem a menos de 40 px das bordas.
- [ ] Cores das etapas consistentes entre as cenas.
- [ ] Nenhum emoji (a fonte não tem).
- [ ] `--preview` conferido nas cenas 1, a do meio e a última.
