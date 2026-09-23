---
name: Biologix
description: >
  Portal clínico B2B do grupo Biologix, usado por profissionais de saúde
  para diagnóstico do sono. Cor de marca verde (`primary`), botões com
  arredondamento total (pill), escala de padding que cresce até 172px.
---

## Overview da marca

<!--
  PENDENTE: este bloco ainda é placeholder no projeto original e precisa
  ser escrito com o time (ver 05-PROXIMOS-PASSOS.md). Deve descrever
  personalidade, tom e o que a interface comunica ao profissional de
  saúde — não repetir valores de token, que já estão no frontmatter.

  Se você já tinha um texto aqui no arquivo antigo, cole-o de volta
  neste lugar.
-->

[placeholder — a definir junto com o time]

## Particularidades da marca

- **Cor única:** a Biologix opera só com a ramp `primary`. Não existe
  cor secundária — a ramp `secondary` foi removida dos primitivos, e os
  papéis `surface-secondary-*` resolvem para os mesmos valores de
  `surface-brand-*`.
- **Botões em pill:** `rounded.button` resolve como arredondamento total,
  diferente da MySleep.
- **Escala de padding longa:** vai até 172px, para telas densas de portal
  clínico com muita respiração entre blocos de dados.

## Do's and Don'ts

### Cor

- Do usar `surface-brand-*` para superfície de ação primária, com
  `text-brand-on-brand` como cor do texto sobre ela.
- Do tratar `surface-secondary-*` como sinônimo de `surface-brand-*`
  nesta marca. Se um dia os dois divergirem, é erro, não intenção.
- Don't introduzir uma segunda cor de marca sem revisar esta seção: a
  ausência dela é decisão explícita do time, não omissão.
- Don't usar a ramp `data-*` para comunicar ação ou estado de marca —
  ela é exclusiva de visualização de dados.
- Don't usar a ramp da MySleep em nenhuma superfície da Biologix, nem
  como acento ou ilustração.

### Contraste

A ramp primária é verde de luminosidade média, então o texto claro só é
seguro na metade escura da escala:

- Do usar texto branco a partir de `primary-600` (4.5:1). De `600` para
  baixo o texto tem que ser escuro.
- Do usar `text-high` sobre `primary-100` a `primary-400`, onde o
  contraste vai de 8.3:1 a 12:1.
- Don't usar branco sobre `primary-500` — dá 3.53:1 e reprova no WCAG AA.
  É o caso do hover do botão hoje, ainda pendente de decisão do time.
- Don't confiar no `primary-600` como margem de segurança: ele passa
  exatamente em 4.5:1, sem folga nenhuma para um ajuste futuro de tom.

### Forma e espaçamento

- Do usar `rounded.button` (arredondamento total) em botão — é o que
  distingue a Biologix da MySleep na forma.
- Do usar a escala de `padding` semântica (`sm` = 16px, `md` = 24px),
  nunca um valor de spacing cru escolhido a olho.
- Don't usar valor fora da escala: a razão de `24` existir é que `20` já
  foi tentado no botão e foi corrigido na origem por estar fora dela.
