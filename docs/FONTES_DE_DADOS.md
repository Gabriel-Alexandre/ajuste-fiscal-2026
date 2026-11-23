# Fontes de dados

A lista completa, com endereço, hora da coleta, tamanho e sha256, está em `dados/MANIFESTO.json` (fontes primárias, baixadas por `ferramentas/coletar.py` a partir de `ferramentas/fontes.json`) e em `dados/capturas/MANIFESTO_CAPTURAS.json` (o texto das reportagens usadas como segunda fonte; só o texto, sem o HTML da página).

| Grupo | Arquivos |
|---|---|
| Senado | Parecer 221 (tabela de impacto e substitutivo), avulso inicial, Parecer 224 (redação final), Emendas 40 e 83, ficha de tramitação, 6 listagens de votação nominal |
| Câmara | proposição 2655570 (API), tramitações (API), votações (API), parecer preliminar do relator |
| IFI | RAF 116 e RAF 117 |
| Segunda fonte da tabela | nota técnica do DIAP |
| Imprensa (texto) | Jota, Folhapress (A Gazeta e Jornal do Comércio), Gazeta do Povo, Agência Senado, Agência Câmara, Agência Brasil (Folha PE), InfoMoney, InvestNews, Metrópoles, BM&C, Atlas Público, Forbes, Cenário MT, Revista Fórum, Diario de Pernambuco, Sindsep-PE, O Povo |

O texto dos PDFs fica em `dados/textos/` (pdftotext, UTF-8). As tabelas que os scripts leem ficam em `dados/derivados/`, cada linha com o trecho de onde o número saiu.
