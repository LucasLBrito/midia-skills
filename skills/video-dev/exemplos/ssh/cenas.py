"""Exemplo de VÍDEO DE CONCEITO: "O que é SSH" (12 cenas, ~3:17).

Padrões usados: cliente x servidor (Laptop/Server em L e R), pacotes viajando (Packet),
caixas que surgem no ritmo da fala, terminal ilustrativo (Terminal) e resumo em lista.
Renderizar: python render.py <esta pasta>
"""
from motor import *


def cenas():
    c = []
    # 1 · abertura
    c.append([
        Title(0.1, [("o que é ", INK), ("SSH", GREEN), ("?", INK)]),
        Terminal(1.0, 540, 560, [("$ ssh voce@servidor", GREEN), ("Welcome to Ubuntu 24.04", WHITE)], typing=2.2),
        Laptop(4.0, L, 1000, "você"),
        Server(4.6, R, 1000, "outro lado do mundo"),
        Line(5.3, (L + 165, 1000), (R - 135, 1000), dashed=True, dur=0.8),
        Packet(6.2, (L + 165, 1000), (R - 135, 1000), "ssh", GREEN, dur=1.6),
        Box(9.0, 540, 1380, "o problema", RED, size=46),
        Box(9.8, 540, 1520, "a solução", GREEN, size=46),
        Box(10.6, 540, 1660, "como funciona", BLUE, size=46),
    ])
    # 2 · Telnet
    c.append([
        Title(0.1, [("o problema: ", INK), ("Telnet", ORANGE)]),
        Text(1.2, 540, 400, "anos 90", 54, GRAY),
        Laptop(2.0, L, 780, "você"),
        Server(2.5, R, 780, "máquina remota"),
        Line(3.2, (L + 165, 780), (R - 135, 780), dur=0.7),
        Box(3.8, 540, 640, "Telnet", ORANGE, size=44),
        Box(6.2, 540, 1080, "tudo em texto puro", INK, filled=True, size=50),
        Packet(8.2, (L + 165, 780), (R - 135, 780), "user: ana", BLUE, dur=1.8, mono=True, size=36),
        Packet(9.6, (L + 165, 780), (R - 135, 780), "senha: 123456", RED, dur=1.8, mono=True, size=36),
        Packet(11.2, (L + 165, 780), (R - 135, 780), "sudo rm -rf logs", INK, dur=1.8, mono=True, size=36),
        Text(9.6, 540, 1300, "user: ana", 52, BLUE, "mono"),
        Text(10.6, 540, 1400, "senha: 123456", 52, RED, "mono"),
        Text(12.2, 540, 1500, "sudo rm -rf logs", 52, INK, "mono"),
    ])
    # 3 · man in the middle
    ys = [520, 790, 1060, 1330]
    c.append([
        Title(0.1, [("o caminho dos ", INK), ("dados", BLUE)]),
        Box(1.0, 330, ys[0], "você", BLUE, w=330),
        Line(1.6, (330, ys[0] + 50), (330, ys[1] - 50), dur=0.4),
        Box(2.0, 330, ys[1], "roteador", INK, w=330),
        Line(2.8, (330, ys[1] + 50), (330, ys[2] - 50), dur=0.4),
        Box(3.2, 330, ys[2], "Wi-Fi do café", ORANGE, w=330),
        Line(4.0, (330, ys[2] + 50), (330, ys[3] - 50), dur=0.4),
        Box(4.4, 330, ys[3], "provedor", INK, w=330),
        Line(5.0, (330, ys[3] + 50), (330, ys[3] + 170), dur=0.4),
        Box(5.4, 330, 1560, "servidor", GREEN, w=330),
        Box(7.6, 820, ys[2], "espião\nlendo tudo", RED, w=330, size=46),
        Line(8.2, (655, ys[2]), (500, ys[2]), RED, dashed=True, dur=0.5),
        Packet(8.8, (330, ys[0]), (330, 1560), "senha: 123456", RED, dur=3.0, mono=True, size=32),
        Box(12.0, 540, 1760, "ataque man-in-the-middle", RED, filled=True, size=50),
    ])
    # 4 · história
    c.append([
        Title(0.1, [("a origem do ", INK), ("SSH", GREEN)]),
        Text(0.6, 540, 520, "1995", 200, INK, "bold"),
        Text(1.4, 540, 680, "Finlândia", 56, GRAY),
        Box(3.2, 540, 840, "milhares de senhas roubadas", RED, size=48),
        Box(7.0, 540, 1040, "Tatu Ylönen", BLUE, size=54),
        Line(8.0, (540, 1100), (540, 1230), arrow=True, dur=0.5),
        Box(9.0, 540, 1320, "SSH = Secure Shell", GREEN, filled=True, size=60),
        Box(11.8, 340, 1520, "Telnet", ORANGE, size=48),
        Text(12.2, 540, 1520, "+", 70, INK, "bold"),
        Box(12.6, 760, 1520, "criptografia", PURPLE, size=48),
    ])
    # 5 · túnel
    c.append([
        Title(0.1, [("o ", INK), ("túnel", GREEN), (" criptografado", INK)]),
        Laptop(1.0, L, 760, "cliente"),
        Server(1.6, R, 760, "servidor"),
        Box(2.6, 540, 760, " ", GREEN, w=330, h=120, radius=60),
        Packet(4.0, (L + 140, 760), (R - 110, 760), "x8#Kq!9", GREEN, dur=2.0, mono=True, size=34),
        Box(5.4, 540, 470, "quem olha de fora vê:\na7$Gz@&2pQ...", RED, size=40),
        Line(5.9, (540, 545), (540, 690), RED, dashed=True, dur=0.4),
        Text(8.6, 540, 1080, "3 etapas", 64, INK, "bold"),
        Box(9.6, 540, 1240, "1 · conexão", BLUE, w=600, size=52),
        Box(10.4, 540, 1400, "2 · troca de chaves", ORANGE, w=600, size=52),
        Box(11.2, 540, 1560, "3 · autenticação", PURPLE, w=600, size=52),
    ])
    # 6 · conexão
    c.append([
        Title(0.1, [("etapa 1: ", INK), ("conexão", BLUE)]),
        Laptop(0.8, L, 640, "cliente"),
        Server(1.2, R, 640, "servidor"),
        Line(2.0, (L + 165, 640), (R - 135, 640), BLUE, arrow=True, dur=0.6),
        Box(2.6, 540, 520, "porta 22", BLUE, size=44),
        Box(5.0, 540, 980, "negociação de algoritmos", INK, filled=True, size=48),
        Box(6.8, 540, 1150, "criptografia: AES / ChaCha20", BLUE, w=820, size=44),
        Box(8.0, 540, 1300, "troca de chaves: curve25519", ORANGE, w=820, size=44),
        Box(9.4, 540, 1450, "integridade: HMAC-SHA2", PURPLE, w=820, size=44),
    ])
    # 7 · Diffie-Hellman
    c.append([
        Title(0.1, [("etapa 2: ", INK), ("Diffie-Hellman", ORANGE)]),
        Laptop(1.2, L, 640, "cliente"),
        Server(1.6, R, 640, "servidor"),
        Box(3.6, L, 900, "segredo a", PURPLE, size=42),
        Box(3.9, R, 900, "segredo b", PURPLE, size=42),
        Text(4.6, 540, 900, "(nunca saem\nda máquina)", 36, GRAY),
        Line(5.0, (L + 165, 640), (R - 135, 640), dashed=True, dur=0.5),
        Packet(5.6, (L + 165, 610), (R - 135, 610), "número A", BLUE, dur=1.6, size=36),
        Packet(7.2, (R - 135, 680), (L + 165, 680), "número B", BLUE, dur=1.6, size=36),
        Text(9.0, 540, 560, "números públicos", 40, BLUE),
        Line(9.4, (L, 960), (L, 1100), arrow=True, dur=0.4),
        Line(9.4, (R, 960), (R, 1100), arrow=True, dur=0.4),
        Box(10.0, L, 1180, "chave X", GREEN, filled=True, size=48),
        Box(10.0, R, 1180, "chave X", GREEN, filled=True, size=48),
        Text(10.8, 540, 1180, "=", 80, INK, "bold"),
        Box(12.6, 540, 1450, "a chave nunca passa pela rede", INK, filled=True, size=48),
    ])
    # 8 · host key / fingerprint
    c.append([
        Title(0.1, [("o servidor ", INK), ("prova quem é", ORANGE)]),
        Server(1.0, R, 560, "servidor"),
        Box(1.8, R, 820, "chave do host", ORANGE, size=42),
        Laptop(1.4, L, 560, "cliente"),
        Line(3.0, (R - 135, 560), (L + 165, 560), ORANGE, arrow=True, dur=0.6),
        Box(3.6, 540, 440, "assinatura", ORANGE, size=40),
        Terminal(6.5, 540, 1180, [
            ("The authenticity of host", WHITE),
            ("'servidor' can't be established.", WHITE),
            ("ED25519 key fingerprint is", WHITE),
            ("SHA256:x9F2kQ7...aP1", ORANGE),
            ("Continue connecting (yes/no)? yes", GREEN),
        ], size=34, typing=3.5),
        Line(13.6, (540, 1400), (540, 1500), arrow=True, dur=0.4),
        Box(14.2, 540, 1590, "~/.ssh/known_hosts", BLUE, size=48),
    ])
    # 9 · autenticação: par de chaves
    c.append([
        Title(0.1, [("etapa 3: ", INK), ("quem é você?", PURPLE)]),
        Box(1.6, 540, 450, "senha (já criptografada)", GRAY, size=46),
        Text(3.0, 540, 560, "funciona... mas dá pra melhorar", 40, GRAY),
        Terminal(5.0, 540, 760, [("$ ssh-keygen -t ed25519", GREEN)], typing=1.4),
        Laptop(7.8, L, 1080, "seu computador"),
        Server(8.4, R, 1080, "servidor"),
        Box(9.6, L, 1370, "chave\nprivada", RED, size=48),
        Text(10.4, L, 1520, "fica só com você", 38, RED),
        Box(12.0, R, 1370, "chave\npública", GREEN, size=48),
        Text(12.8, R, 1520, "vai pro servidor", 38, GREEN),
        Line(12.4, (L + 140, 1370), (R - 140, 1370), GREEN, dashed=True, arrow=True, dur=0.6),
    ])
    # 10 · desafio
    c.append([
        Title(0.1, [("desafio e ", INK), ("assinatura", PURPLE)]),
        Laptop(0.6, L, 600, "cliente"),
        Server(0.9, R, 600, "servidor"),
        Packet(1.6, (R - 135, 560), (L + 165, 560), "desafio", ORANGE, dur=1.6, size=36),
        Box(3.6, L, 860, "assina com a\nprivada", RED, size=40),
        Packet(6.0, (L + 165, 650), (R - 135, 650), "assinatura", PURPLE, dur=1.6, size=36),
        Box(8.0, R, 860, "confere com a\npública", GREEN, size=40),
        Box(10.0, 540, 1120, "acesso liberado", GREEN, filled=True, size=62),
        Box(12.2, 540, 1340, "a chave privada nunca\nsai da sua máquina", INK, filled=True, size=46),
        Text(14.0, 540, 1520, "nada de senha pra roubar", 44, GRAY),
    ])
    # 11 · dia a dia
    c.append([
        Title(0.1, [("SSH no ", INK), ("dia a dia", GREEN)]),
        Logo(0.8, 540, 900),
        Line(2.8, (430, 790), (300, 600), dur=0.4),
        Box(3.0, 260, 560, "git push", BLUE, size=50),
        Line(6.4, (650, 790), (780, 600), dur=0.4),
        Box(6.6, 800, 560, "scp", GREEN, size=50),
        Line(9.6, (430, 1010), (300, 1200), dur=0.4),
        Box(9.8, 260, 1240, "túneis", ORANGE, size=50),
        Line(11.6, (650, 1010), (780, 1200), dur=0.4),
        Box(11.8, 800, 1240, "redirecionar\nportas", PURPLE, size=46),
        Box(13.6, 540, 1500, "serviços internos com segurança", INK, filled=True, size=44),
    ])
    # 12 · resumo
    c.append([
        Title(0.1, [("resumindo", INK)]),
        Box(1.4, 540, 470, "rede insegura vira conversa segura", INK, filled=True, size=46),
        Box(6.4, 540, 700, "1 · conexão", BLUE, w=620, size=54),
        Line(6.9, (540, 760), (540, 840), arrow=True, dur=0.3),
        Box(7.4, 540, 910, "2 · troca de chaves", ORANGE, w=620, size=54),
        Line(7.9, (540, 970), (540, 1050), arrow=True, dur=0.3),
        Box(8.6, 540, 1120, "3 · autenticação", PURPLE, w=620, size=54),
        Text(11.2, 540, 1330, "< 1 segundo", 110, GREEN, "bold"),
        Terminal(13.0, 540, 1580, [("$ ssh voce@servidor", GREEN)], typing=1.6),
    ])
    return c
