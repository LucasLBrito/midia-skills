"""Exemplo de TUTORIAL DE TERMINAL: "Boas práticas de Git e GitHub" (14 cenas, ~3:37).

Padrões usados: selo "PASSO n" + título (passo()), Term com comandos digitados no tempo da fala,
caixa de alerta/dica abaixo do terminal, mini-diagramas (staging, branches) e checklist final.
Renderizar: python render.py <esta pasta>
"""
from motor import *


def cenas():
    c = []
    # 1 · abertura
    c.append([
        Title(0.1, [("Git", ORANGE), (" + ", INK), ("GitHub", PURPLE)], y=260, size=110),
        Text(0.8, 540, 390, "boas práticas, passo a passo", 52, INK),
        Logo(1.6, 540, 720, "git", size=260, color=ORANGE),
        Box(6.8, 540, 1080, "1 · pause o vídeo", BLUE, w=620, size=52),
        Line(7.4, (540, 1135), (540, 1205), arrow=True, dur=0.3),
        Box(8.0, 540, 1270, "2 · digite no terminal", GREEN, w=620, size=52),
        Line(8.6, (540, 1325), (540, 1395), arrow=True, dur=0.3),
        Box(9.4, 540, 1460, "3 · continue", PURPLE, w=620, size=52),
    ])
    # 2 · identidade
    c.append(passo(1, [("quem é ", INK), ("você", BLUE)], BLUE) + [
        Term(1.0, 700, [
            (2.4, "$", 'git config --global user.name "Seu Nome"'),
            (5.4, "$", 'git config --global user.email "voce@mail.com"'),
            (10.2, "$", "git config --global init.defaultBranch main"),
        ]),
        Box(7.6, 540, 1030, "mesmo e-mail da conta do GitHub", ORANGE, size=44),
        Text(12.4, 540, 1200, "conferir:", 38, GRAY),
        Text(12.4, 540, 1265, "git config --list", 42, BLUE, "mono"),
    ])
    # 3 · git init
    c.append(passo(2, [("criar o ", INK), ("repositório", GREEN)], GREEN) + [
        Term(1.0, 720, [
            (3.4, "$", "mkdir meu-projeto"),
            (4.8, "$", "cd meu-projeto"),
            (6.2, "$", "git init"),
            (7.0, "o", "Initialized empty Git repository"),
        ]),
        Box(8.4, 540, 1060, "o Git agora acompanha esta pasta", GREEN, filled=True, size=46),
    ])
    # 4 · .gitignore
    c.append(passo(3, [("o arquivo ", INK), (".gitignore", RED)], RED) + [
        Text(2.6, 540, 410, "o que o Git deve ignorar", 44, GRAY),
        Term(3.6, 720, [
            (6.4, "$", 'echo "node_modules/" >> .gitignore'),
            (8.4, "$", 'echo "dist/" >> .gitignore'),
            (10.4, "$", 'echo ".env" >> .gitignore'),
        ]),
        Box(12.6, 540, 1060, "senhas e chaves de API\nnunca vão pro repositório", RED, filled=True, size=46),
    ])
    # 5 · primeiro commit
    c.append(passo(4, [("primeiro ", INK), ("commit", ORANGE)], ORANGE) + [
        Term(1.0, 700, [
            (2.6, "$", "git status"),
            (3.4, "o", "Untracked files: .gitignore index.html"),
            (5.2, "$", "git add ."),
            (7.4, "$", 'git commit -m "chore: estrutura inicial"'),
            (9.6, "o", "[main a1b2c3d] chore: estrutura inicial"),
        ]),
        Box(5.2, 190, 1130, "arquivos", ORANGE, w=290, size=42),
        Line(5.6, (340, 1130), (390, 1130), arrow=True, dur=0.3),
        Box(5.8, 540, 1130, "staging", BLUE, w=290, size=42),
        Line(7.6, (690, 1130), (740, 1130), arrow=True, dur=0.3),
        Box(7.8, 890, 1130, "commit", GREEN, w=290, size=42),
        Text(5.6, 365, 1210, "git add", 34, GRAY, "mono"),
        Text(7.8, 715, 1210, "git commit", 34, GRAY, "mono"),
    ])
    # 6 · mensagens de commit
    c.append([
        Box(0.1, 540, 175, "DICA", PINK, filled=True, size=34, radius=30),
        Title(0.2, [("commits ", INK), ("claros", PINK)], y=285, size=84),
        Text(3.0, 540, 420, "padrão Conventional Commits", 44, GRAY),
        Box(5.6, 540, 560, "feat: adiciona login com Google", GREEN, w=900, size=42),
        Box(7.0, 540, 700, "fix: corrige cálculo do frete", RED, w=900, size=42),
        Box(8.6, 540, 840, "docs: atualiza o README", BLUE, w=900, size=42),
        Box(11.0, 540, 1040, "1 mudança = 1 commit", ORANGE, filled=True, size=56),
        Text(14.6, 540, 1230, "evite:", 40, GRAY),
        Text(14.6, 540, 1310, '"ajustes"   "agora vai"   "final2"', 40, RED, "mono"),
    ])
    # 7 · GitHub
    c.append(passo(5, [("subir pro ", INK), ("GitHub", PURPLE)], PURPLE) + [
        Box(2.0, 540, 470, "github.com: New repository\n(vazio, sem README)", PURPLE, size=42),
        Term(5.0, 820, [
            (6.4, "$", "git remote add origin \\"),
            (7.6, ">", "git@github.com:voce/meu-projeto.git"),
            (12.6, "$", "git push -u origin main"),
        ]),
        Text(9.6, 540, 1080, "endereço em: Code > SSH", 40, BLUE),
    ])
    # 8 · branches
    c.append(passo(6, [("uma ", INK), ("branch", PURPLE), (" por tarefa", INK)], PURPLE) + [
        Box(1.2, 540, 430, "nunca trabalhe direto na main", RED, filled=True, size=44),
        Term(3.6, 680, [
            (4.8, "$", "git switch -c feat/login"),
            (6.0, "o", "Switched to a new branch 'feat/login'"),
        ]),
        Line(4.0, (100, 1180), (980, 1180), GREEN, width=9, dur=0.8),
        Box(4.4, 160, 1250, "main", GREEN, size=36),
        Line(5.2, (300, 1180), (400, 1040), PURPLE, width=9, dur=0.3),
        Line(5.5, (400, 1040), (700, 1040), PURPLE, width=9, dur=0.5),
        Line(6.0, (700, 1040), (800, 1180), PURPLE, width=9, dur=0.3),
        Box(5.6, 550, 960, "feat/login", PURPLE, size=36),
        Text(8.2, 540, 1380, "feat/login", 42, PURPLE, "mono"),
        Text(9.6, 540, 1450, "fix/calculo-frete", 42, RED, "mono"),
        Text(10.6, 540, 1520, "docs/readme", 42, BLUE, "mono"),
    ])
    # 9 · trabalhar na branch
    c.append(passo(7, [("trabalhe na ", INK), ("branch", PURPLE)], PURPLE) + [
        Term(1.0, 720, [
            (2.6, "#", "# edite seus arquivos..."),
            (4.0, "$", "git add src/login.js"),
            (5.2, "$", 'git commit -m "feat: adiciona tela de login"'),
            (11.4, "$", "git push -u origin feat/login"),
        ]),
        Box(7.6, 540, 1060, "quantos commits precisar", GREEN, size=46),
    ])
    # 10 · Pull Request
    c.append(passo(8, [("abra um ", INK), ("Pull Request", GREEN)], GREEN) + [
        Box(3.0, 540, 450, "Compare & pull request", GREEN, filled=True, size=46),
        Box(5.4, 540, 660, "título: feat: tela de login\ndescrição: o que mudou e por quê", INK, w=900, size=40),
        Box(8.0, 540, 860, "revisores: alguém do time", PURPLE, size=42),
        Text(10.6, 540, 1030, "ou pelo terminal (GitHub CLI):", 40, GRAY),
        Term(11.4, 1180, [(12.6, "$", "gh pr create --fill")]),
    ])
    # 11 · depois do merge
    c.append([
        Box(0.1, 540, 175, "DEPOIS DO MERGE", GREEN, filled=True, size=34, radius=30),
        Title(0.2, [("limpar e ", INK), ("atualizar", GREEN)], y=285, size=84),
        Box(1.0, 540, 430, "PR aprovado e mesclado", GREEN, size=44),
        Term(3.0, 700, [
            (3.8, "$", "git switch main"),
            (5.6, "$", "git pull"),
            (8.6, "$", "git branch -d feat/login"),
        ]),
        Box(11.0, 540, 1010, "main sempre estável", BLUE, filled=True, size=50),
        Text(12.0, 540, 1170, "dica: proteja a main em", 38, GRAY),
        Text(12.0, 540, 1230, "Settings > Branches", 40, BLUE, "mono"),
    ])
    # 12 · rebase
    c.append(passo(9, [("branch ", INK), ("atualizada", ORANGE)], ORANGE) + [
        Text(2.0, 540, 410, "a main andou enquanto você trabalhava?", 40, GRAY),
        Term(4.0, 660, [
            (5.6, "$", "git fetch"),
            (7.0, "$", "git rebase origin/main"),
        ]),
        Box(9.4, 540, 900, "conflitos cedo e pequenos", ORANGE, filled=True, size=48),
        Text(11.6, 540, 1060, "deu conflito? resolva e rode:", 38, GRAY),
        Term(11.6, 1240, [
            (12.0, "$", "git add ."),
            (12.6, "$", "git rebase --continue"),
        ]),
    ])
    # 13 · tags
    c.append(passo(10, [("versões com ", INK), ("tags", PINK)], PINK) + [
        Text(1.4, 540, 470, "v1.4.2", 150, INK, "bold"),
        Box(3.8, 190, 680, "major", RED, w=290, size=44),
        Box(4.4, 540, 680, "minor", ORANGE, w=290, size=44),
        Box(5.0, 890, 680, "patch", GREEN, w=290, size=44),
        Text(3.8, 190, 770, "quebra algo", 34, GRAY),
        Text(4.4, 540, 770, "nova função", 34, GRAY),
        Text(5.0, 890, 770, "correção", 34, GRAY),
        Term(6.4, 1010, [
            (7.2, "$", 'git tag -a v1.0.0 -m "primeira versão"'),
            (10.6, "$", "git push origin v1.0.0"),
        ]),
        Box(13.2, 540, 1260, "no GitHub vira uma Release", PURPLE, filled=True, size=46),
    ])
    # 14 · checklist
    itens = [("1 · git config: nome e e-mail", BLUE), ("2 · .gitignore (nada de .env)", RED),
             ("3 · commits pequenos e claros", GREEN), ("4 · uma branch por tarefa", PURPLE),
             ("5 · Pull Request com revisão", ORANGE), ("6 · main sempre estável", BLUE),
             ("7 · tags para cada versão", PINK)]
    tempos = [1.6, 2.8, 4.0, 5.8, 7.2, 8.8, 10.4]
    c.append([Title(0.1, [("checklist", GREEN)], y=250, size=96)] +
             [Box(t, 540, 420 + i * 132, txt, cor, w=860, size=42) for i, ((txt, cor), t) in
              enumerate(zip(itens, tempos))] +
             [Box(12.4, 540, 1420, "salve e use no próximo projeto", GREEN, filled=True, size=46)])
    return c
