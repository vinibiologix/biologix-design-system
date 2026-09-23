---
name: MySleep
description: >
  App e portal do paciente do grupo Biologix. Cor de marca azul-escura
  (`primary`), cor secundária amarela, botões com arredondamento de 8px
  e escala de padding que cresce até 172px.
---

## Overview da marca

<!--
  PENDENTE: este bloco ainda é placeholder no projeto original e precisa
  ser escrito com o time (ver 05-PROXIMOS-PASSOS.md). Deve descrever
  personalidade, tom e o que a interface comunica ao paciente — não
  repetir valores de token, que já estão no frontmatter.

  Se você já tinha um texto aqui no arquivo antigo, cole-o de volta
  neste lugar.
-->

[placeholder — a definir junto com o time]

## Particularidades da marca

- **Duas cores de marca:** ramp `primary` azul-escura e ramp `secondary`
  amarela, diferente da Biologix, que opera só com a primária.
- **Botões menos arredondados:** `rounded.button` resolve em 8px, não em
  pill.
- **Ramp primária escura:** qualquer degrau da `primary` tem contraste
  alto com branco, então texto claro sobre superfície de marca é seguro
  em toda a escala.

## Do's and Don'ts

### Cor

- Do usar `surface-brand-*` (ramp azul) para ação primária, com
  `text-brand-on-brand` sobre ela.
- Do tratar a ramp `secondary` amarela como acento — destaque, ilustração,
  realce pontual.
- Don't usar a secundária como botão primário alternativo: duas cores de
  ação concorrentes confundem o paciente sobre qual é o próximo passo.
- Don't usar a ramp `data-*` para comunicar ação ou estado de marca — ela
  é exclusiva de visualização de dados.
- Don't usar a ramp da Biologix em nenhuma superfície da MySleep.

### Contraste

As duas ramps se comportam de maneira oposta, e é aí que mora o risco:

- Do usar texto branco sobre a primária a partir de `primary-400`
  (7.6:1). A ramp é escura, então a metade de cima é confortável.
- Do usar **sempre** `text-high` sobre qualquer superfície
  `surface-secondary-*`. A ramp amarela não chega a 4.5:1 com branco em
  degrau nenhum abaixo do `900` — o `secondary-500` dá 1.69:1, contra
  8.67:1 com o texto escuro.
- Don't usar `primary-300` como fundo de texto em nenhuma das duas
  direções: 3.72:1 com branco e 3.93:1 com texto escuro, ou seja, reprova
  dos dois lados. É um degrau para borda e preenchimento, não para texto.
- Don't herdar o `text-brand-on-brand` ao trocar uma superfície de marca
  por uma secundária — a cor do texto precisa mudar junto.

### Forma e espaçamento

- Do usar `rounded.button` (8px) em botão — a MySleep é menos arredondada
  que a Biologix, e isso é intencional.
- Do usar a escala de `padding` semântica (`sm` = 12px, `md` = 16px),
  que é mais compacta que a da Biologix por ser interface de app.
- Don't copiar medida de tela da Biologix direto: a mesma etapa semântica
  resolve para um valor menor aqui.
