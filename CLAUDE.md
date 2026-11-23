# CLAUDE.md, projeto ajuste-fiscal-2026

Comece pelo `ESTADO.md`. A doutrina está em `.cursor/rules/ajuste-fiscal-2026-fundamentos.mdc` (leia antes de mexer).

- Rodada nova: `python ferramentas/coletar.py` → `derivar.py` → `analise.py` → `validacao_independente.py` → `graficos.py` → `gerar_relatorio.py` → `conferir_linguagem.py` → `python -m pytest -q`; registre em `docs/RODADAS.md` e atualize o `ESTADO.md`.
- Commit e push a cada rodada, na `main`.
- O roteiro do vídeo não mora aqui: fica no repositório de documentação do canal, na pasta do VIDEO_030.
