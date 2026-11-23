"""Baixa as fontes primárias do projeto, uma por vez, e grava o MANIFESTO com hash.

Uso:  python ferramentas/coletar.py [--so id1,id2]

Cada fonte de ferramentas/fontes.json vai para dados/brutos/<id>.<ext>. O texto do PDF
(pdftotext -layout, ou PyMuPDF se faltar) vai para dados/textos/<id>.txt, que é o que os
scripts leem. O MANIFESTO guarda endereço, hora, tamanho e sha256 do arquivo e do texto.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos"
TEXTOS = RAIZ / "dados" / "textos"
MANIFESTO = RAIZ / "dados" / "MANIFESTO.json"
AGENTE = "Mozilla/5.0 (projeto público ajuste-fiscal-2026)"


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar(url: str, destino: Path, json_api: bool) -> None:
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE, **({"Accept": "application/json"} if json_api else {})})
    with urllib.request.urlopen(pedido, timeout=120) as r, open(destino, "wb") as f:
        shutil.copyfileobj(r, f)


def extrair_texto(pdf: Path, destino: Path) -> None:
    """Texto do PDF em UTF-8. O pdftotext do Git Bash às vezes grava em latin-1; normaliza."""
    if shutil.which("pdftotext"):
        bruto = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, check=True).stdout
        texto = bruto.decode("utf-8", errors="replace")
    else:  # pragma: no cover
        import fitz
        texto = "\n".join(p.get_text() for p in fitz.open(pdf))
    destino.write_text(texto, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", default="")
    ap.add_argument("--so-texto", action="store_true", help="refaz só o texto dos PDFs já baixados")
    args = ap.parse_args()
    fontes = json.loads((RAIZ / "ferramentas" / "fontes.json").read_text(encoding="utf-8"))
    so = {s for s in args.so.split(",") if s}
    BRUTOS.mkdir(parents=True, exist_ok=True)
    TEXTOS.mkdir(parents=True, exist_ok=True)
    manifesto = json.loads(MANIFESTO.read_text(encoding="utf-8")) if MANIFESTO.exists() else {}
    for fonte in fontes:
        if so and fonte["id"] not in so:
            continue
        ext = "json" if fonte["tipo"] == "json" else "pdf"
        destino = BRUTOS / f"{fonte['id']}.{ext}"
        if args.so_texto:
            if ext == "pdf":
                texto = TEXTOS / f"{fonte['id']}.txt"
                extrair_texto(destino, texto)
                manifesto[fonte["id"]]["sha256_texto"] = sha256(texto)
            continue
        baixar(fonte["url"], destino, ext == "json")
        cabeca = destino.read_bytes()[:5]
        if ext == "pdf" and cabeca != b"%PDF-":
            raise SystemExit(f"{fonte['id']}: o servidor não devolveu PDF ({cabeca!r})")
        texto = TEXTOS / f"{fonte['id']}.txt"
        if ext == "pdf":
            extrair_texto(destino, texto)
        else:
            dados = json.loads(destino.read_text(encoding="utf-8"))
            texto.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
        manifesto[fonte["id"]] = {
            **fonte,
            "arquivo": destino.relative_to(RAIZ).as_posix(),
            "texto": texto.relative_to(RAIZ).as_posix(),
            "baixado_em": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "bytes": destino.stat().st_size,
            "sha256": sha256(destino),
            "sha256_texto": sha256(texto),
        }
        print(f"{fonte['id']}: {destino.stat().st_size} bytes, sha256 {manifesto[fonte['id']]['sha256'][:12]}")
        time.sleep(1.5)  # um por vez, sem pressa com os servidores públicos
    MANIFESTO.write_text(json.dumps(manifesto, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
