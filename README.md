# Design System — Biologix + MySleep

Fonte de verdade dos design tokens compartilhados entre as duas marcas
do grupo, e o build que gera os arquivos `DESIGN.md` consumidos pelo
Claude Design.

## Estrutura

```
tokens/                    # export do Zeroheight (um JSON por marca) — NÃO editar à mão
core-tokens.md             # tipografia, components e prosa compartilhada
brands/
  biologix.tokens.md       # nome, descrição, Overview e Do's and Don'ts da Biologix
  mysleep.tokens.md        # idem, MySleep
build_design_md.py         # funde as duas fontes e gera os DESIGN.md
output/
  biologix/DESIGN.md       # gerado — é o arquivo que sobe no Claude Design
  mysleep/DESIGN.md        # gerado
```

## De onde vem cada valor

| O que | Fonte | Como muda |
|---|---|---|
| Cor, spacing, radius | `tokens/*.json` | Variável no Figma → plugin do Zeroheight → PR automático neste repositório |
| Tipografia | `core-tokens.md` | Edição manual (a escala não existe como variável do Figma) |
| `components` | `core-tokens.md` + `brands/` | Edição manual, após extrair o componente real do Figma |
| Overview, Do's and Don'ts | `brands/*.tokens.md` | Edição manual |

Os arquivos em `output/` **nunca** são editados à mão: são regerados
pelo script a cada mudança.

## Rodar o build

```bash
pip install -r requirements.txt          # só na primeira vez
python3 build_design_md.py all           # ou: biologix | mysleep
```

O script aborta se alguma referência (`{colors.x}`) apontar para um
token inexistente, e avisa quando um par fundo/texto de componente fica
abaixo de 4.5:1 de contraste.

## Validar

```bash
npx -p @google/design.md designmd lint output/biologix/DESIGN.md
npx -p @google/design.md designmd lint output/mysleep/DESIGN.md
```

Zero erros antes de commitar. Avisos de *orphaned tokens* são esperados
enquanto a maior parte dos componentes ainda não estiver documentada.

## Fluxo completo de uma mudança

1. Mudança aprovada no Figma (via branch + merge).
2. Editor do Zeroheight roda o plugin de sync → PR automático aqui.
3. Revisar e mergear o PR.
4. `git pull` → `python3 build_design_md.py all` → `designmd lint`.
5. Commit do `output/` regerado.
6. Claude Design → **Remix** no design system existente → anexar o `DESIGN.md`.

Mudanças de tipografia, `components` ou texto pulam os passos 1 a 3:
edita-se o `.md` direto e segue a partir do passo 4.

## Convenção de nomenclatura de token

`categoria / papel / estado` — onde categoria é a propriedade pintada
(`surface`, `text`, `outline`), papel é o significado (`base`, `brand`,
`secondary`) e estado é `default`, `hover`, `active`, `focus` ou
`disabled`. O `default` é sempre explícito.

Não existe família por estado: o estado é sufixo do elemento
(`surface-brand-hover`), nunca um grupo próprio (`state/hover/...`).
