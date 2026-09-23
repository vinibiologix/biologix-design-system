---
name: Core Tokens — Biologix Group
description: >
  Camada compartilhada do design system das marcas Biologix e MySleep.
  Este arquivo é fonte APENAS da escala tipográfica, do bloco `components`
  e da prosa compartilhada. Cor, spacing e radius vêm de `tokens/*.json`
  (export do Zeroheight a partir das variáveis do Figma) e não devem ser
  declarados aqui.
version: alpha
typography:
  display-lg:
    fontFamily: Lato
    fontSize: 100px
    fontWeight: 900
    lineHeight: 1.1
  display-md:
    fontFamily: Lato
    fontSize: 80px
    fontWeight: 900
    lineHeight: 1.1
  display-sm:
    fontFamily: Lato
    fontSize: 64px
    fontWeight: 900
    lineHeight: 1.15
  heading-2xl:
    fontFamily: Lato
    fontSize: 50px
    fontWeight: 700
    lineHeight: 1.2
  heading-xl:
    fontFamily: Lato
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.2
  heading-lg:
    fontFamily: Lato
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.25
  heading-md:
    fontFamily: Lato
    fontSize: 25px
    fontWeight: 700
    lineHeight: 1.3
  heading-sm:
    fontFamily: Lato
    fontSize: 20px
    fontWeight: 700
    lineHeight: 1.35
  heading-xs:
    fontFamily: Lato
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.4
  body-lg:
    fontFamily: Lato
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.5
  body-md:
    fontFamily: Lato
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Lato
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.45
  label-lg:
    fontFamily: Lato
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.3
  label-md:
    fontFamily: Lato
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.3
  label-sm:
    fontFamily: Lato
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.3
  caption:
    fontFamily: Lato
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
components:
  button-primary:
    backgroundColor: "{colors.surface-brand-default}"
    textColor: "{colors.text-brand-on-brand}"
    rounded: "{rounded.button}"
    padding: "{spacing.24}"
    height: 48px
    typography: "{typography.label-lg}"
  button-primary-hover:
    backgroundColor: "{colors.surface-brand-hover}"
    textColor: "{colors.text-brand-on-brand}"
    rounded: "{rounded.button}"
    padding: "{spacing.24}"
    height: 48px
    typography: "{typography.label-lg}"
  button-primary-active:
    backgroundColor: "{colors.surface-brand-active}"
    textColor: "{colors.text-brand-on-brand}"
    rounded: "{rounded.button}"
    padding: "{spacing.24}"
    height: 48px
    typography: "{typography.label-lg}"
  button-primary-disabled:
    backgroundColor: "{colors.surface-base-disabled}"
    textColor: "{colors.text-brand-disabled}"
    rounded: "{rounded.button}"
    padding: "{spacing.24}"
    height: 48px
    typography: "{typography.label-lg}"
  button-secondary:
    backgroundColor: "{colors.surface-base-elevated}"
    textColor: "{colors.text-brand-default}"
    rounded: "{rounded.button}"
    padding: "{spacing.padding-sm}"
    typography: "{typography.label-lg}"
  input-field:
    backgroundColor: "{colors.surface-base-elevated}"
    textColor: "{colors.text-high}"
    rounded: "{rounded.component-sm}"
    padding: "{spacing.padding-xs}"
    typography: "{typography.body-md}"
  card:
    backgroundColor: "{colors.surface-base-elevated}"
    rounded: "{rounded.component-md}"
    padding: "{spacing.padding-md}"
  badge:
    backgroundColor: "{colors.surface-brand-subtle}"
    textColor: "{colors.text-brand-default}"
    rounded: "{rounded.pill}"
    padding: "{spacing.padding-xxs}"
    typography: "{typography.label-sm}"
  modal:
    backgroundColor: "{colors.surface-base-elevated}"
    rounded: "{rounded.component-lg}"
    padding: "{spacing.padding-lg}"
  toast-error:
    backgroundColor: "{colors.feedback-error-surface}"
    textColor: "{colors.feedback-error-on-surface}"
    rounded: "{rounded.component-sm}"
    padding: "{spacing.padding-sm}"
    typography: "{typography.body-sm}"
  toast-warning:
    backgroundColor: "{colors.feedback-warning-surface}"
    textColor: "{colors.feedback-warning-on-surface}"
    rounded: "{rounded.component-sm}"
    padding: "{spacing.padding-sm}"
    typography: "{typography.body-sm}"
  toast-success:
    backgroundColor: "{colors.feedback-success-surface}"
    textColor: "{colors.feedback-success-on-surface}"
    rounded: "{rounded.component-sm}"
    padding: "{spacing.padding-sm}"
    typography: "{typography.body-sm}"
  toast-info:
    backgroundColor: "{colors.feedback-info-surface}"
    textColor: "{colors.feedback-info-on-surface}"
    rounded: "{rounded.component-sm}"
    padding: "{spacing.padding-sm}"
    typography: "{typography.body-sm}"
  data-grid-header:
    backgroundColor: "{colors.surface-base-subtle}"
    textColor: "{colors.text-medium}"
    typography: "{typography.label-md}"
  data-grid-row:
    backgroundColor: "{colors.surface-base-elevated}"
    textColor: "{colors.text-high}"
    typography: "{typography.body-sm}"
---

## Overview

Este documento define a camada compartilhada do design system do grupo
Biologix. Ele cobre o que é fisicamente idêntico entre as duas marcas e
o que não existe como variável do Figma.

Os valores de cor, espaçamento e radius **não moram mais neste arquivo**.
Eles vêm de `tokens/*.json`, gerado pelo Zeroheight a partir das
variáveis do Figma, e são injetados no `DESIGN.md` final pelo
`build_design_md.py`. Declarar um valor de cor aqui criaria uma segunda
fonte de verdade que ninguém consegue manter sincronizada.

O que este arquivo é fonte:

- a **escala tipográfica** (os 16 estilos), que existe como text style
  no Figma e não como variável;
- o bloco **`components`**, que o Figma não exporta;
- a prosa compartilhada (este Overview e os Do's and Don'ts abaixo).

## Convenção de nomenclatura

Token de cor se nomeia `categoria / papel / estado`:

- **categoria** é a propriedade que ele pinta — `surface`, `text`, `outline`;
- **papel** é o que aquilo significa — `base`, `brand`, `secondary`, `disabled`;
- **estado** é `default`, `hover`, `active`, `focus` ou `disabled`, sempre
  explícito, nunca implícito.

O estado é sufixo do elemento (`surface-brand-hover`), nunca um grupo
próprio. Não existe família por estado: agrupar por estado cria uma
matriz estado × elemento que nunca fecha, espalha o componente por vários
lugares da árvore e impede que o par fundo/texto seja auditado junto para
contraste.

## Papéis semânticos compartilhados

A coleção "Semantics" do Figma tem modos Biologix e MySleep. A maior
parte dos papéis resolve para o mesmo valor nas duas marcas:

- `surface-base-*` — fundo, hover, active, disabled, focus da superfície neutra
- `text-*` — hierarquia de texto (high/medium/low/placeholder/disabled/on-inverse)
- `outline-*` — bordas e divisores
- `feedback-{error,warning,success,info}-*` — toda a linguagem de status
- `chart-{normal,low,moderate,severe}-*` — severidade em visualização de dados

O que resolve diferente por marca: `surface-brand-*`, `surface-secondary-*`,
`outline-brand-*`, `text-brand-*`, `chart-accent-*`, a escala de `padding`
semântica e os radius semânticos de componente.

## Tipografia

**Fonte única: Lato**, compartilhada entre Biologix e MySleep.

Escala nomeada por peso visual, nunca por posição semântica de documento
(H1/H2), para manter o token desacoplado da tag HTML usada em cada tela:

| Token | Tamanho | Peso | Uso |
|---|---|---|---|
| `display-lg` | 100px | Black | Hero de marketing, telas 100% visuais |
| `display-md` | 80px | Black | Métrica de destaque grande |
| `display-sm` | 64px | Bold/Black | Métrica de destaque, hero secundário |
| `heading-2xl` | 50px | Bold | Título de maior peso da hierarquia |
| `heading-xl` | 40px | Bold | Título de página |
| `heading-lg` | 32px | Bold | Título de seção |
| `heading-md` | 25px | Bold | Subtítulo, título de card |
| `heading-sm` | 20px | Bold | Título de componente |
| `heading-xs` | 16px | Bold | Título de componente menor |
| `body-lg` | 18px | Regular | Introdução, texto de destaque |
| `body-md` | 16px | Regular | Texto corrido padrão |
| `body-sm` | 14px | Regular | Texto secundário, metadados |
| `label-lg` | 16px | Bold | Texto de botão (acessível) |
| `label-md` | 14px | Bold | Tags, chips, inputs |
| `label-sm` | 12px | Bold | Badges, indicadores compactos |
| `caption` | 12px | Regular | Legendas, disclaimers, timestamps |

> **Atenção:** os cortes 200 (Light) e 600 (Medium) documentados no Figma
> não são pesos nativos do Lato do Google Fonts (100/300/400/700/900 +
> itálicos). Se o arquivo de fonte carregado no produto não incluir esses
> cortes, o navegador renderiza um *faux bold/light* sintético. Confirmar
> com quem versiona a fonte antes de usá-los em produção.

## Do's and Don'ts

- Do editar cor, spacing e radius **na variável do Figma**, nunca neste
  arquivo — o valor chega aqui pelo PR do Zeroheight.
- Do editar a escala tipográfica e o bloco `components` **aqui**, porque
  eles não existem como variável e não vêm pelo pipeline.
- Do rodar `python3 build_design_md.py all` e `designmd lint` antes de
  commitar qualquer mudança.
- Don't declarar `colors`, `spacing` ou `rounded` no frontmatter deste
  arquivo ou dos `brands/*.tokens.md` — o build ignora e avisa, mas a
  duplicação confunde quem lê.
- Don't editar nada dentro de `output/` — é regerado a cada build.
- Don't usar `display-*` como hierarquia de conteúdo padrão; é reservado
  para momentos de destaque visual.
- Don't usar nenhuma tipografia além de Lato, em nenhuma hipótese — mesmo
  que um arquivo de referência visual anexado (ex: export do Figma,
  mockup) use outra fonte (ex: Dosis). Lato é a única tipografia de marca
  nas duas marcas; qualquer fonte diferente vista em material de
  referência deve ser ignorada.
