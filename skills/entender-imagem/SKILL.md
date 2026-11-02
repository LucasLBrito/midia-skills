---
name: entender-imagem
description: Lê e entende imagens, prints de tela, fotos, diagramas, prints de erro, fotos de documento ou quadro, e quadros tirados de vídeos. Extrai o texto (como um OCR), explica o que aparece, compara imagens, acha bugs visuais em interfaces e transforma prints de tabelas e código em texto editável. Use sempre que o usuário mandar uma imagem ou caminho de imagem (png, jpg, webp, heic, gif, pdf escaneado), disser "olha esse print", "o que diz essa imagem", "lê esse erro", "copia o texto da foto", "captura a tela", "tira um print do vídeo no minuto X", ou quiser entender uma parte específica de um vídeo pela imagem.
---

# Entender imagem

O Claude enxerga imagens diretamente: a ferramenta **Read** abre png, jpg, gif e webp como imagem.
Não é preciso instalar nada para o caso comum. Esta skill organiza os casos e os atalhos.

## De onde vem a imagem

| Origem | Como chegar nela |
|---|---|
| Arquivo ou caminho que o usuário mandou | `Read` no caminho |
| Imagem colada no chat | já está visível; analise direto |
| "Tira um print do vídeo no minuto 2:15" | `ffmpeg -ss 00:02:15 -i video.mp4 -frames:v 1 C:/tmp/quadro.png` e depois `Read` |
| Vários momentos de um vídeo | skill **transcrever-video** (gera quadros com o tempo de cada um) |
| "Captura a minha tela" | ferramenta de screenshot do computador (computer-use) se estiver disponível. Senão, peça para ele usar Win+Shift+S e colar |
| Página da web | screenshot pelo navegador do app (`computer` → screenshot) |
| PDF escaneado | `Read` com `pages` (até 20 páginas por vez); a skill `pdf` ajuda com PDFs grandes |
| HEIC (foto de iPhone) | converta antes: `ffmpeg -i foto.heic foto.jpg` |

## Ler bem

- **Imagem grande ou texto pequeno**: recorte a região antes de ler. Assim o texto fica legível:
  ```bash
  ffmpeg -y -i print.png -vf "crop=LARGURA:ALTURA:X:Y,scale=iw*2:-1" C:/tmp/recorte.png
  ```
  (X e Y = canto superior esquerdo da região, em pixels). Para descobrir o tamanho da imagem:
  `ffprobe -v error -show_entries stream=width,height -of csv=p=0 print.png`.
- **Muitas imagens com texto para procurar** (ex.: 50 quadros de vídeo, pasta de prints): o OCR com
  Tesseract é mais barato que ler uma por uma. Está instalado em `C:\Program Files\Tesseract-OCR`, com
  os idiomas em `~/tessdata` (eng, por; variável `TESSDATA_PREFIX`):
  ```bash
  tesseract imagem.png - -l por+eng --psm 6        # texto na tela (saída no terminal)
  for f in pasta/*.png; do echo "== $f"; tesseract "$f" - -l por+eng --psm 6 2>/dev/null; done > ocr.txt
  ```
  Bom para texto (títulos, terminal, formulários). Ícones e desenhos saem como lixo. Tela escura?
  Funciona, mas inverter as cores ajuda: `ffmpeg -i a.png -vf negate b.png`. Em vídeo, use
  `--ocr --ocr-lang por+eng` da skill transcrever-video.
  Outro idioma: baixe `<lang>.traineddata` de github.com/tesseract-ocr/tessdata_fast para `~/tessdata`.
  Terminal antigo sem `tesseract` no PATH: abra um novo ou use o caminho completo do .exe.
- Na dúvida entre letras parecidas (0/O, 1/l/I, rn/m) em código ou senha, diga que não tem certeza.

## Responder conforme o pedido

| Pedido | Resposta |
|---|---|
| "o que é isso?" | uma frase com o que a imagem mostra + os detalhes que importam |
| Print de erro | a mensagem exata copiada + o que significa + como resolver (siga `superpowers:systematic-debugging` se for bug de projeto) |
| "copia o texto" | o texto fiel, mantendo quebras de linha. Código em bloco de código |
| Print de tabela | tabela em Markdown (ou CSV/planilha com a skill `xlsx` se ele pedir) |
| Diagrama | explicação das partes e das setas. Se ele quiser editável, use `excalidraw-skill` ou Mermaid |
| Interface/tela de app | o que está certo, o que parece bug (alinhamento, texto cortado, cor) e onde |
| Comparar duas imagens | o que mudou, item por item |

## Cuidados

- Prints podem ter dados sensíveis (senha, token, e-mail, documento). Não repita senhas ou tokens na
  resposta. Avise se aparecer algo que não deveria estar no print.
- Não invente o que está ilegível: diga "ilegível" ou recorte e amplie.
