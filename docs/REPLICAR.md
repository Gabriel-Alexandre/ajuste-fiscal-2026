# Como refazer tudo

```bash
pip install -r requirements.txt          # e o pdftotext (poppler) no PATH
python ferramentas/coletar.py            # baixa as fontes e grava o MANIFESTO com sha256
python ferramentas/derivar.py            # tira os números do texto (para se não achar o trecho)
python ferramentas/analise.py            # grava resultados/RESUMO.json
python ferramentas/validacao_independente.py   # segundo caminho; sai com erro se falhar
python ferramentas/graficos.py           # resultados/figuras/, 1920x1080
python ferramentas/gerar_relatorio.py    # RELATORIO.md, RESUMO_SIMPLES.md, docs/LEITURA_DA_IA.md, docs/REVISAO_ADVERSARIAL.md
python ferramentas/conferir_linguagem.py
python -m pytest -q
```

Se uma fonte mudar no servidor (a API da Câmara muda depois de cada votação), o sha256 muda e o `git diff` do `MANIFESTO.json` mostra. A rodada nova se registra em `docs/RODADAS.md`.
