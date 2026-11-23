# Rodadas

## Rodada 1 (23/11/2026, manhã)

- **O que se fez:** coleta das fontes primárias (Senado, Câmara, IFI), a tabela de impacto do Parecer 221 tirada do texto por script, a classificação de cada medida pelo parecer do relator na Câmara, o tamanho do buraco pelos RAF 116 e 117 da IFI, o diesel pela redação final, as 6 votações nominais do Senado contadas nome a nome, a situação na Câmara pela API.
- **Resultado:** de cada R$ 100 do ajuste de 2027, R$ 31 são gasto contido, R$ 31 são receita adiantada e R$ 38 são imposto a mais; o ajuste cobre de 10,2% a 12,6% do que a IFI diz faltar.
- **Validação:** 33 de 33 (`resultados/VALIDACAO.json`).
- **Achado de método:** a Emenda 40 do senador Rogério Marinho trazia, ao mesmo tempo, o teto de 0,6% para o gasto, a supressão da trava dos créditos, da Lei Kandir, da compensação previdenciária e do diesel, e a desvinculação de superávits. As reportagens descreviam só uma das partes cada; o texto da emenda resolve.
- **Achado de método:** a redação final da Lei Kandir é "até o exercício de 2030", com R$ 2 bilhões por ano; o Jota escreveu "apenas 2027". Vale o texto.
- **A refazer:** a Câmara (sessão de 23/11 às 18h), e a divisão por medida dos R$ 50 bilhões do relator, se for publicada.

## Rodada 2 (23/11/2026, tarde): a revisão adversarial

- **O que se fez:** um leitor que não escreveu os scripts revisou o relatório e as fontes em três papéis; o que procedeu entrou nesta rodada (lista completa em `docs/REVISAO_ADVERSARIAL.md`).
- **O que mudou no significado (a conta da tabela não mudou):**
  1. a divisão 31, 31 e 38 é o cenário da tabela do governo, com o bloqueio acionado; o bloqueio do art. 6º-C só vale abaixo do centro da meta, e o PLOA projeta 2027 acima dele (R$ 83,4 bi para a meta contra o centro de R$ 73,2 bi). Nesse caso, sobra só o benefício fiscal cortado, R$ 19,5 bi, 100% receita (V2, gráfico `g06`);
  2. o art. 12 deixa o valor bloqueado voltar no ano seguinte como investimento fora do teto; o que fica para sempre é o benefício cortado, 4,4% do ajuste que a IFI diz faltar (V5);
  3. o rótulo "imposto a mais" virou "benefício fiscal cortado (imposto a mais)", com a leitura do gasto tributário na V4;
  4. a igualdade entre o bloqueio e a trava dos créditos é suposição da estimativa, não limite da lei.
- **Correções de fato e de método:** "nenhuma regra das obrigatórias muda" trocado (há tetos para a Lei Kandir e a compensação previdenciária e o art. 6º-D); o aumento das obrigatórias também acima da inflação (R$ 53,2 bi) e como parte do PIB (cai de 15,9% para 15,6%); a distância PLOA × IFI pelo número da IFI (104,8); a cobertura com os dois PIBs (10,2% a 12,9%) e com o juro de 6,1% (7,8% a 9,7%); o diesel libera 77,2% do bloqueio que faltava em 2026; os arts. 8º, 12 e 14 listados como expansivos; a Emenda 40 descrita por inteiro; a Emenda 83 restrita à compensação com a CBS; "a Câmara marcou sessão".
- **Novo dado tirado das fontes:** a tabela 8 do RAF 116 (PLOA e IFI lado a lado), o piso da meta de 2027, o bloqueio de 2026, o IPCA e o PIB da IFI, o teto da compensação previdenciária (de R$ 8,3 bi para R$ 3 bi em 2027, pela Folhapress).
- **Validação:** 33 de 33.
