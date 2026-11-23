"""Confere o texto que o público lê: palavras proibidas do assunto e travessão.

Uso:  python ferramentas/conferir_linguagem.py   (sai com erro se achar algo)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVOS = ["README.md", "ESTADO.md", "RELATORIO.md", "RESUMO_SIMPLES.md", "docs/LEITURA_DA_IA.md",
            "docs/REVISAO_ADVERSARIAL.md", "docs/RODADAS.md", "docs/PLANO.md", "docs/FONTES_DE_DADOS.md", "docs/REPLICAR.md"]
PROIBIDAS = [r"\bmentiu\b", r"\bmentira\b", r"\bfraude\b", r"\broubo\b", r"\broubou\b", r"\bgolpe\b", r"\bvote em\b",
             r"\bcalote\b(?!s? da União contra)"]
TRAVESSAO = re.compile(r"[—–]")


def main() -> None:
    erros = []
    for nome in ARQUIVOS:
        p = RAIZ / nome
        if not p.exists():
            continue
        for i, linha in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if TRAVESSAO.search(linha):
                erros.append(f"{nome}:{i}: travessão")
            for pal in PROIBIDAS:
                # citação literal entre aspas é permitida (é a fala de quem disse)
                fora_de_aspas = re.sub(r'"[^"]*"|\*"[^"]*"\*', "", linha)
                if re.search(pal, fora_de_aspas, flags=re.I):
                    erros.append(f"{nome}:{i}: {pal}")
    for e in erros:
        print(e)
    print("LINGUAGEM OK" if not erros else f"{len(erros)} problemas")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
