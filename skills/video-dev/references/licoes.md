# Lições dos vídeos de SSH e Git

O que deu certo, o que deu errado e por quê. Leia antes de começar um vídeo novo.

## Processo

- **Roteiro primeiro, aprovado.** Mudar uma frase depois da animação pronta obriga a refazer a
  narração e os tempos da cena. Mostre o texto e espere o ok.
- **Narração antes das cenas.** A cena dura o mesmo que a fala + 0,7 s (PAD). Animar antes de ter o
  áudio significa chutar tempos e refazer.
- **Sincronia pela palavra.** Cada elemento entra quando a palavra que ele representa é dita.
  Use `narracao.py --tempos N` e não estime pelo tamanho do texto.
- **Preview sempre.** `render.py --preview` gera um PNG por cena em segundos. O render completo
  leva minutos. Olhe os PNG antes de renderizar o MP4.
- **Uma ideia por cena.** Nos dois vídeos, cada cena tem 10–16 s e uma ideia só. É o que mantém a
  tela legível no celular.

## Visual

- A primeira versão foi no estilo **creme** (fundo papel, como muitos explicativos de tecnologia). As versões finais,
  com trilha, ficaram em **Dracula**, por isso é o padrão. O creme continua disponível.
- **Emoji não funciona**: a Bahnschrift não tem emojis e sai um quadrado vazio. No vídeo de SSH o
  "👁" teve de ser removido. Use palavras ou desenhe um elemento.
- Cores com significado fixo (verde = seguro, vermelho = perigo) fazem quem assiste entender
  antes de ler.
- Os vídeos ficaram com a tela "crescendo" ao longo da cena (cada elemento fica). Não apague
  elementos no meio da cena. Se precisar de tela limpa, comece outra cena.
- Para uma comparação, ponha os dois lados na mesma altura, à esquerda e à direita (L e R).
- Fechamento de cena com uma caixa preenchida (`filled=True`) com a frase-resumo funcionou bem.

## Voz

- `pt-BR-AntonioNeural` com `rate="+8%"`. Na velocidade normal fica arrastado para vídeo curto.
- A voz pt-BR lê termos em inglês como se fossem português. A solução foi um mapa de
  pronúncia (`pronuncia.json`) com grafias abrasileiradas: "comít", "púch", "guít-râb". O mapa base
  está em narracao-voz/scripts/pronuncia_base.json.
- Números e siglas por extenso no roteiro: "mil novecentos e noventa e cinco", "porta vinte e
  dois", "S C P" (letras separadas). A voz lê melhor assim.
- Símbolos de comando por extenso no roteiro: "git push, traço u, origin main"; "feat barra login".
  Na tela aparece o comando real.

## Música

- Trilha composta por código (trilhas.py), sem direitos autorais. **synth** combinou com tema tech.
- Mixagem: trilha 0,32 e voz 0,667, com ducking (a música abaixa quando a voz fala).
- Trilha com a duração exata do vídeo e fade de 3 s no começo e no fim.

## Técnica

- 1080x1920, 30 fps, H.264 crf 18, AAC 192k, `+faststart` (começa a tocar antes de baixar tudo).
- Supersampling 2x (desenha em 2160x3840 e reduz) deixa as bordas suaves. Sem isso o texto fica
  serrilhado.
- Cache de quadros parados: quando nada está animando, o quadro anterior é reaproveitado. É isso
  que deixa o render rápido.
- Os quadros vão direto para o ffmpeg por um pipe, sem salvar milhares de PNGs no disco.
- No Windows, caminhos longos quebram o Python ("File name too long"). Use pastas curtas.
- Fontes: Bahnschrift (variação "Bold SemiCondensed"/"SemiBold SemiCondensed") e Consolas Bold.
