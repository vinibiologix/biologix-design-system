#!/usr/bin/env python3
"""
build_design_md.py

Gera o DESIGN.md final de cada marca a partir de duas fontes:

  1. tokens/*.json  — export do Zeroheight (um arquivo por modo do Figma).
     É a FONTE DE VERDADE de cor, spacing e radius. Não editar à mão:
     esses arquivos chegam via PR do Zeroheight quando uma variável
     muda no Figma.

  2. core-tokens.md e brands/<marca>.tokens.md — fonte do que NÃO existe
     como variável do Figma: a escala tipográfica, o bloco `components`,
     o Overview e os Do's and Don'ts. Esses sim são editados à mão.

O DESIGN.md (spec google-labs-code/design.md) é autocontido: não tem
import nem herança. Por isso ele é gerado, nunca editado.

Uso:
    python3 build_design_md.py biologix
    python3 build_design_md.py all
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent
TOKENS_DIR = BASE_DIR / "tokens"
BRANDS_DIR = BASE_DIR / "brands"
CORE_PATH = BASE_DIR / "core-tokens.md"
OUTPUT_DIR = BASE_DIR / "output"

MARCAS_CONHECIDAS = ("biologix", "mysleep")

# Nomes que divergem entre o Figma e o que os .md já usam. Mantido
# explícito e pequeno de propósito: cada linha aqui é uma divergência
# que idealmente devia ser corrigida na origem (no Figma) e removida
# daqui depois.
RENOMEIA_ROUNDED = {"buttons": "button"}

# Contraste mínimo WCAG AA para texto normal.
CONTRASTE_MINIMO = 4.5

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n(.*)$", re.DOTALL)
REFERENCIA_RE = re.compile(r"\{([a-zA-Z0-9_.\-]+)\}")


# ---------------------------------------------------------------- leitura


def separa_frontmatter(texto: str):
    m = FRONTMATTER_RE.match(texto)
    if not m:
        raise ValueError("Arquivo sem frontmatter YAML válido (--- ... ---).")
    fm_raw, corpo = m.groups()
    return yaml.safe_load(fm_raw) or {}, corpo.strip()


def folhas(obj, caminho=""):
    """Percorre a árvore DTCG e devolve (caminho, valor) de cada token."""
    if not isinstance(obj, dict):
        return
    if "$value" in obj:
        yield caminho, obj["$value"]
        return
    for chave, valor in obj.items():
        if chave.startswith("$"):
            continue
        yield from folhas(valor, f"{caminho}/{chave}" if caminho else chave)


def detecta_marca(tokens: dict, origem: Path) -> str:
    """O export do Zeroheight não guarda o nome do modo em lugar nenhum:
    os dois arquivos têm $extensions idênticos. A marca só aparece no
    caminho das referências, então é de lá que ela é deduzida."""
    sonda = tokens.get("Semantics/color/surface/brand/default")
    if not isinstance(sonda, str):
        raise ValueError(
            f"{origem.name}: não achei 'surface/brand/default' para identificar a marca."
        )
    for marca in MARCAS_CONHECIDAS:
        if f".brand.{marca}." in sonda:
            return marca
    raise ValueError(f"{origem.name}: marca não reconhecida em {sonda!r}.")


def carrega_exports() -> dict:
    """Varre tokens/*.json, identifica a marca de cada um pelo conteúdo e
    confere se o nome do arquivo bate com o que foi detectado."""
    if not TOKENS_DIR.exists():
        raise FileNotFoundError(f"Pasta {TOKENS_DIR} não existe.")

    achados = {}
    for caminho in sorted(TOKENS_DIR.glob("*.json")):
        tokens = dict(folhas(json.loads(caminho.read_text(encoding="utf-8"))))
        marca = detecta_marca(tokens, caminho)

        if marca not in caminho.name.lower():
            avisa(
                f"{caminho.name} contém tokens da marca '{marca}', mas o nome do "
                f"arquivo não menciona isso. Seguindo pelo conteúdo."
            )
        if marca in achados:
            raise ValueError(f"Dois arquivos em tokens/ para a marca '{marca}'.")

        achados[marca] = tokens

    if not achados:
        raise FileNotFoundError(f"Nenhum .json encontrado em {TOKENS_DIR}.")
    return achados


# ------------------------------------------------------------- nomeação


def achata(segmentos) -> str:
    """['chart','normal','normal-default'] -> 'chart-normal-default'.
    O Figma repete o nome do grupo dentro da folha em alguns lugares;
    sem isso viraria 'chart-normal-normal-default'."""
    partes = []
    for seg in segmentos:
        if partes and seg.startswith(partes[-1] + "-"):
            seg = seg[len(partes[-1]) + 1 :]
        partes.append(seg)
    return "-".join(partes)


def classifica(caminho: str, marca: str):
    """Traduz o caminho do Figma para (categoria, nome) do DESIGN.md.
    Devolve None para o que não deve entrar no arquivo desta marca."""
    seg = caminho.split("/")

    if seg[:2] == ["Primitives", "pallete"]:
        resto = seg[2:]
        if resto[0] in ("white", "black"):
            return "colors", resto[0]
        if resto[0] == "status":  # status/error/500 -> error-500
            return "colors", achata(resto[1:])
        if resto[0] == "brand":
            if resto[1] != marca:  # a ramp da outra marca não entra aqui
                return None
            nome = achata(resto[2:])
            # 'surface-base' primitivo da marca vira 'brand-surface-base'
            # para não ser confundido com a família semântica surface-base-*.
            return "colors", f"brand-{nome}" if nome == "surface-base" else nome
        return "colors", achata(resto)  # neutral/500, data/blue/500

    if seg[:2] == ["Primitives", "radius"]:
        nome = seg[2]
        return "rounded", RENOMEIA_ROUNDED.get(nome, nome)

    if seg[:2] == ["Primitives", "spacing"]:
        return "spacing", seg[2]

    if seg[:2] == ["Primitives", "typeface"]:
        return None  # tipografia vem do .md, não das variáveis

    if seg[:3] == ["Semantics", "color", "background"]:
        return "colors", achata(seg[2:])

    if seg[:2] == ["Semantics", "color"]:
        return "colors", achata(seg[2:])

    if seg[:3] == ["Semantics", "spacing", "padding"]:
        return "spacing", achata(seg[2:])

    if seg[:3] == ["Semantics", "spacing", "radius"]:
        nome = seg[3]
        return "rounded", RENOMEIA_ROUNDED.get(nome, nome)

    avisa(f"Caminho não classificado, ignorado: {caminho}")
    return None


# ------------------------------------------------------------- resolução


def para_hex(valor) -> str:
    if isinstance(valor, dict) and "hex" in valor:
        return valor["hex"].upper()
    return valor


def resolve_literal(tokens: dict, valor, visitados=None):
    """Segue a cadeia de alias até chegar num valor concreto."""
    visitados = visitados or set()
    if isinstance(valor, str) and valor.startswith("{"):
        alvo = valor.strip("{}").replace(".", "/")
        if alvo in visitados:
            raise ValueError(f"Referência circular em {alvo}.")
        visitados.add(alvo)
        if alvo not in tokens:
            raise ValueError(f"Referência quebrada: {valor}")
        return resolve_literal(tokens, tokens[alvo], visitados)
    return para_hex(valor)


def monta_arvore(tokens: dict, marca: str):
    """Monta {colors, spacing, rounded} já com os nomes finais. Alias vira
    referência {categoria.nome} quando o alvo também está no arquivo; se
    o alvo tiver ficado de fora (ramp da outra marca), vira valor literal."""
    arvore = {"colors": {}, "spacing": {}, "rounded": {}}
    mapa = {}  # caminho do Figma -> "categoria.nome"

    for caminho in tokens:
        destino = classifica(caminho, marca)
        if destino:
            mapa[caminho] = f"{destino[0]}.{destino[1]}"

    for caminho, valor in tokens.items():
        destino = classifica(caminho, marca)
        if not destino:
            continue
        categoria, nome = destino

        if isinstance(valor, str) and valor.startswith("{"):
            alvo = valor.strip("{}").replace(".", "/")
            if alvo in mapa:
                arvore[categoria][nome] = "{" + mapa[alvo] + "}"
                continue
            arvore[categoria][nome] = resolve_literal(tokens, valor)
            continue

        bruto = para_hex(valor)
        if categoria in ("spacing", "rounded") and isinstance(bruto, (int, float)):
            bruto = f"{int(bruto)}px"
        arvore[categoria][nome] = bruto

    for categoria in arvore:
        arvore[categoria] = dict(sorted(arvore[categoria].items()))
    return arvore


def resolve_na_arvore(arvore: dict, valor, profundidade=0):
    """Resolve {colors.x} contra a árvore final já montada."""
    if profundidade > 10 or not isinstance(valor, str):
        return valor
    m = REFERENCIA_RE.fullmatch(valor.strip())
    if not m:
        return valor
    categoria, _, nome = m.group(1).partition(".")
    alvo = arvore.get(categoria, {}).get(nome)
    if alvo is None:
        return None
    return resolve_na_arvore(arvore, alvo, profundidade + 1)


# ------------------------------------------------------------- validação


def luminancia(hexa: str) -> float:
    hexa = hexa.lstrip("#")
    canais = [int(hexa[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    canais = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * canais[0] + 0.7152 * canais[1] + 0.0722 * canais[2]


def contraste(a: str, b: str) -> float:
    l1, l2 = sorted((luminancia(a), luminancia(b)), reverse=True)
    return round((l1 + 0.05) / (l2 + 0.05), 2)


def valida(arvore: dict, marca: str):
    """Duas checagens baratas que o designmd lint não substitui:
    referência apontando pra token inexistente, e par fundo/texto de
    componente abaixo do mínimo WCAG AA."""
    erros = []

    for categoria in ("typography", "components"):
        for nome, bloco in arvore.get(categoria, {}).items():
            if not isinstance(bloco, dict):
                continue
            for prop, valor in bloco.items():
                if not (isinstance(valor, str) and REFERENCIA_RE.fullmatch(valor.strip())):
                    continue
                if resolve_na_arvore(arvore, valor) is None:
                    erros.append(f"{categoria}.{nome}.{prop} aponta para {valor}, que não existe.")

    for nome, bloco in arvore.get("components", {}).items():
        if not isinstance(bloco, dict):
            continue
        fundo = resolve_na_arvore(arvore, bloco.get("backgroundColor"))
        texto = resolve_na_arvore(arvore, bloco.get("textColor"))
        if not (isinstance(fundo, str) and fundo.startswith("#")):
            continue
        if not (isinstance(texto, str) and texto.startswith("#")):
            continue
        razao = contraste(fundo, texto)
        if razao < CONTRASTE_MINIMO:
            avisa(f"[{marca}] {nome}: contraste {razao}:1 (mínimo {CONTRASTE_MINIMO}) — {texto} sobre {fundo}")

    return erros


def avisa(msg: str):
    print(f"  ! {msg}", file=sys.stderr)


# ------------------------------------------------------------------ build


def carrega_md(caminho: Path):
    if not caminho.exists():
        raise FileNotFoundError(f"Não encontrei {caminho}.")
    return separa_frontmatter(caminho.read_text(encoding="utf-8"))


def build(marca: str, exports: dict):
    if marca not in exports:
        raise ValueError(f"Não há export em tokens/ para a marca '{marca}'.")

    arvore = monta_arvore(exports[marca], marca)

    core_fm, core_corpo = carrega_md(CORE_PATH)
    marca_fm, marca_corpo = carrega_md(BRANDS_DIR / f"{marca}.tokens.md")

    # cor, spacing e radius agora vêm do JSON; se ainda estiverem nos .md,
    # é resíduo do modelo antigo e seria fonte dupla de verdade.
    for fonte, fm in (("core-tokens.md", core_fm), (f"brands/{marca}.tokens.md", marca_fm)):
        for chave in ("colors", "spacing", "rounded"):
            if chave in fm:
                avisa(f"{fonte} ainda declara '{chave}' no frontmatter — ignorado (a fonte é tokens/*.json).")

    arvore["typography"] = core_fm.get("typography", {})
    componentes = dict(core_fm.get("components", {}))
    componentes.update(marca_fm.get("components", {}))
    arvore["components"] = componentes

    erros = valida(arvore, marca)
    if erros:
        for e in erros:
            print(f"  ✖ {e}", file=sys.stderr)
        raise SystemExit(f"Build de '{marca}' abortado: {len(erros)} referência(s) inválida(s).")

    saida = {
        "name": marca_fm.get("name", marca),
        "description": marca_fm.get("description", ""),
    }
    saida.update(arvore)

    carimbo = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # O comentário de proveniência precisa morar DENTRO do bloco YAML: a
    # spec exige que a primeira linha do arquivo seja exatamente "---".
    cabecalho = (
        "# ARQUIVO GERADO AUTOMATICAMENTE — NÃO EDITE NADA AQUI.\n"
        f"# Cor, spacing e radius: tokens/ (export do Zeroheight, marca {marca})\n"
        "# Tipografia, components e textos: core-tokens.md + brands/\n"
        f"# Gerado em: {carimbo}\n"
        f"# Para atualizar: edite a fonte certa e rode `python3 build_design_md.py {marca}`.\n"
    )
    fm_yaml = yaml.dump(saida, allow_unicode=True, sort_keys=False, default_flow_style=False)
    corpo = f"{core_corpo}\n\n{marca_corpo}".strip()

    destino = OUTPUT_DIR / marca
    destino.mkdir(parents=True, exist_ok=True)
    arquivo = destino / "DESIGN.md"
    arquivo.write_text(f"---\n{cabecalho}{fm_yaml}---\n\n{corpo}\n", encoding="utf-8")

    print(
        f"✔ {arquivo}  "
        f"({len(arvore['colors'])} cores, {len(arvore['spacing'])} spacing, "
        f"{len(arvore['rounded'])} radius, {len(arvore['typography'])} estilos, "
        f"{len(arvore['components'])} componentes)"
    )
    return arquivo


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python3 build_design_md.py <{'|'.join(MARCAS_CONHECIDAS)}|all>")
        raise SystemExit(1)

    exports = carrega_exports()
    alvo = sys.argv[1]
    for m in sorted(exports) if alvo == "all" else [alvo]:
        build(m, exports)
