# O ajuste do Lula corta gasto ou aumenta imposto? Relatório da rodada 1

**Projeto:** `ajuste-fiscal-2026` · **Rodada:** 1 (23/11/2026) · **Repositório:** https://github.com/Gabriel-Alexandre/ajuste-fiscal-2026
Todos os números deste arquivo saem de `resultados/RESUMO.json`, gerado por script a partir das fontes em `dados/brutos/` (com sha256 no `dados/MANIFESTO.json`). Validação por outro caminho: **33 de 33** (`resultados/VALIDACAO.json`).

## O que este projeto não consegue dizer (leia antes)

1. **Os valores por medida são estimativas do Poder Executivo**, levadas ao Parecer nº 221/2026 do relator no Senado. A Consultoria de Orçamento do Senado registrou que elas não foram refeitas depois das mudanças no texto. Não há memória de cálculo pública por medida.
2. **Depois da votação, o relator falou em R$ 50 bilhões** e o ministro, em R$ 46 a 56 bilhões. Nenhum dos dois publicou a nova divisão por medida. A conta daqui usa a única tabela publicada, a de R$ 45,1 a 56,1 bilhões.
3. **O bloqueio de despesas é facultativo e vale um ano.** Se o governo não bloquear, a lei também não deixa limitar o uso de créditos das empresas (o art. 6º-F só vale até o valor bloqueado), e sobra só o imposto a mais (variante V2).
4. **A Câmara começou a votar em 23/11, às 18h.** Até a coleta, a API da Câmara registrava nenhuma votação. O texto pode mudar lá.
5. **O tamanho do buraco é o da IFI**, que tem premissas mais duras que as do governo (PIB, inflação, receitas). O governo prevê superávit em 2027; a IFI, déficit. Os dois números estão aqui.

## 1. A resposta curta

De cada **R$ 100** do ajuste estimado para 2027, **R$ 31** são gasto contido (bloqueio do Orçamento), **R$ 31** são dinheiro das empresas que entra antes (limite ao uso de créditos tributários) e **R$ 38** são imposto a mais (corte de benefícios fiscais e teto do Reidi). Somando o adiantado e o imposto, **R$ 69 de cada R$ 100 vêm de receita**. Nas duas pontas da faixa, a receita fica entre **67,4% a 71,6%** do total.

O lado do gasto é um bloqueio de um ano: pela lei, ele não entra na base de cálculo dos anos seguintes, e o relator na Câmara escreve que ele é reversível no próprio ano. Nenhuma regra das despesas obrigatórias muda.

E o tamanho: o ajuste equivale a **0,31% a 0,38% do PIB**. A IFI calcula que faltam cerca de **3 pontos do PIB** de ajuste para a dívida parar de subir; o pacote cobre **10,2% a 12,6%** disso.

## 2. A tabela, medida por medida (2027, R$ bilhões)

| Medida | Natureza | Mínimo | Máximo |
|---|---|---:|---:|
| Bloqueio de despesas para buscar o centro da meta (art. 6º-C a 6º-E) | gasto contido | 12,8 | 18,3 |
| Limite ao uso de créditos tributários para pagar outros tributos (art. 6º-F) | receita antecipada | 12,8 | 18,3 |
| Corte linear de benefícios fiscais, de 10% para 20% (art. 4º) | imposto a mais | 15,0 | 15,0 |
| Teto para o benefício do Reidi (art. 9º) | imposto a mais | 4,5 | 4,5 |
| **Total** | | **45,1** | **56,1** |

Fonte: Parecer nº 221/2026-PLEN/SF, *"de acordo com informações do Poder Executivo"*. A mesma tabela está na nota técnica do DIAP (16/11, que cita a nota da Conorf de 13/11) e na reportagem do Jota de 18/11; a validação confere as três.

**Como cada medida foi classificada.** O parecer do relator na Câmara (PRLP 1, 19/11/2026) diz que os arts. 4º (benefícios), 9º (Reidi) e 6º-F (créditos) *"ampliam receita"*, e que no 6º-F *"o efeito seja de antecipação de arrecadação, pois os créditos dos contribuintes não se extinguem"*. O bloqueio (arts. 6º-C a 6º-E) é contenção de despesa. É essa a divisão usada aqui.

**A ligação entre as duas metades.** O art. 6º-F só deixa limitar os créditos das empresas *"até o montante equivalente"* ao que for bloqueado de despesa, e só se o governo adotar o bloqueio. Por isso as duas linhas têm a mesma faixa, de R$ 12,8 a 18,3 bilhões: para cada real de gasto segurado, a lei autoriza até um real de crédito das empresas segurado.

| Somas | Mínimo | Máximo | Meio da faixa |
|---|---:|---:|---:|
| Gasto contido (R$ bi) | 12,8 | 18,3 | 15,6 |
| Receita adiantada (R$ bi) | 12,8 | 18,3 | 15,6 |
| Imposto a mais (R$ bi) | 19,5 | 19,5 | 19,5 |
| Receita total (R$ bi) | 32,3 | 37,8 | 35,0 |
| Parte do gasto | 28,4% | 32,6% | 30,8% |
| Parte da receita | 71,6% | 67,4% | 69,2% |

## 3. O que ficou fora da tabela

| Item | O que diz o texto | Por que não entra na conta |
|---|---|---|
| Lei Kandir | repasse aos estados limitado a R$ 2,0 bi por ano até 2030, com o saldo pago de 2028 a 2030 (redação final, art. 2º) | é adiamento de pagamento; a reportagem da Folha e a do InvestNews dizem que cerca de R$ 10 bi em medidas assim abrem espaço para promessas de campanha (Bolsa Família, Pé-de-Meia), sem economia estrutural |
| Compensação previdenciária | limitada a R$ 3,0 bi por ano de 2027 a 2030 (art. 6º) | o mesmo; a CNM fala em perda de caixa para os municípios |
| Proex | teto de R$ 1,0 bi por ano | o relator na Câmara escreve que o teto é *"superior à execução de 2025 e à previsão para 2026"*: não economiza nada hoje |
| Supersalários | prazo para o Congresso votar a regra (60 dias na redação final) | o ministro estimou R$ 3 bi; o texto não quantifica, e a economia do Judiciário e do MP fica com eles |

## 4. O tamanho do buraco

| Número | Valor | Fonte |
|---|---:|---|
| Meta de 2027 (centro) | R$ 73,2 bi (0,50% do PIB) | PLOA 2027, pela nota do DIAP |
| Resultado efetivo de 2027 previsto pelo governo | R$ 18,6 bi | PLOA 2027, pela IFI (RAF 116) |
| Resultado efetivo de 2027 previsto pela IFI | R$ -86,1 bi | IFI, RAF 116 |
| Distância entre os dois | R$ 104,7 bi | conta |
| Déficit de 2027 com as promessas novas | 1,0% do PIB | IFI, RAF 117 |
| Promessas novas não orçadas (Bolsa Família, Bets, MEI) | R$ 40,0 bi | IFI, RAF 117 |
| Aumento das despesas obrigatórias de 2026 para 2027 | R$ 131,4 bi | IFI, RAF 116 (tabela 7) |
| Superávit que estabiliza a dívida | 2,1% do PIB (ou 2,9% com juro real de 6,1%) | IFI, RAF 117 |
| Ajuste que a IFI diz faltar | 3 p.p. do PIB, ou R$ 443,5 bi no PIB do PLOA | IFI, RAF 117; conta |
| Dívida bruta | 82,9% do PIB em set/2026; 86,4% no fim de 2027; chance de 81,6% de passar de 90% até 2030 | BC (pela Agência Brasil); IFI, RAF 117 |

**As comparações (todas na mesma régua, R$ do ajuste de 2027):**

- o ajuste cobre **10,2% a 12,6%** dos 3 pontos do PIB que a IFI diz faltar;
- o ajuste inteiro equivale a **34,3% a 42,7%** do quanto as despesas obrigatórias sobem em um ano; só a parte do gasto contido, **9,7% a 13,9%**;
- as promessas não orçadas que a IFI soma equivalem a **71,3% a 88,7%** do ajuste;
- o ajuste cobre **43,1% a 53,6%** da distância entre o que o governo e a IFI preveem para 2027.

## 5. O diesel de 2026

O art. 13 da redação final autoriza tirar da meta de 2026 até **R$ 10,5 bilhões** gastos com a subvenção ao diesel (MP 1.391/2026). O dinheiro é gasto igual; ele só deixa de contar para a meta.

| 2026 (governo central) | R$ bi | Fonte |
|---|---:|---|
| Resultado projetado antes das deduções | -80,9 | relatório do 4º bimestre, na tabela 3 do RAF 117 |
| Despesas já tiradas da conta da meta | 67,3 | idem |
| Resultado para a meta, depois das deduções e antes do bloqueio | -13,6 | idem |
| Piso da meta | 0,0 | idem |
| Diesel tirado pelo PLP | 10,5 | redação final, art. 13 |
| Total tirado da conta com o diesel | 77,8 | conta |
| Déficit do governo central de janeiro a setembro | -90,2 | Tesouro, pela Agência Brasil |

O diesel equivale a **13,0%** do déficit projetado para 2026 e a **18,7% a 23,3%** do ajuste prometido para 2027. A reportagem da Folha de 23/11 diz que a medida entrou para evitar um novo bloqueio no fim do ano, por causa da arrecadação mais fraca.

## 6. O que a oposição tentou mudar

| Votação (Senado) | Placar | O que estava em jogo |
|---|---:|---|
| Urgência, 12/11 | 40 a 38 | votar sem passar pelas comissões |
| Texto-base, 12/11 | 45 a 31 | o substitutivo do relator Eduardo Braga (MDB) |
| Emenda 40 (Rogério Marinho, PL), 18/11 | 30 a 47 (rejeitada) | teto de 0,6% para o gasto (no lugar de 2%), centro da meta obrigatório, e tirar a trava dos créditos das empresas, a Lei Kandir, a compensação previdenciária e o diesel fora da meta |
| Destaque do PL: limite da compensação previdenciária | 45 a 32 (mantido) | tirar o teto de R$ 3 bi por ano |
| Destaque do Republicanos: limite ao uso de créditos | 49 a 31 (mantido) | tirar o art. 6º-F |
| Turno suplementar, 18/11 | 69 a 2 | as emendas de última hora, entre elas a 83 (Tereza Cristina, PP), que protege os créditos de PIS e Cofins |

**Por partido:** no texto-base, o PL votou 2 SIM e 12 NÃO, e o PT, 8 SIM e 0 NÃO. Na Emenda 40, o PL votou 13 SIM e 1 NÃO. Na trava dos créditos, o PL votou 1 SIM e 14 NÃO. No turno suplementar, o PL votou 10 SIM e 1 NÃO.

**O que a oposição conseguiu:** a Lei Kandir ficou em R$ 2,0 bi por ano, com o saldo pago até 2030 (era R$ 1 bi por ano, com o saldo até 2037), num acordo pelo qual o PL retirou o destaque; e a emenda da senadora Tereza Cristina protegeu os créditos de PIS e Cofins (o Ministério do Planejamento disse ao Jota que o efeito é neutro). O resto do que a Emenda 40 pedia perdeu.

## 7. A Câmara (23/11)

Situação na API da Câmara na coleta: *Aguardando Despacho do Presidente da Câmara dos Deputados (Chancela)*; última tramitação em 2026-11-19T18:47; votações registradas: 0. O relator, Mauro Benevides Filho (União-CE), deu parecer preliminar favorável sem mudar o texto do Senado. Precisa de 257 votos. Refazer a coleta depois da sessão.

## 8. Veredito por critério

| Critério | Veredito | O limite |
|---|---|---|
| O ajuste corta gasto ou aumenta receita? | **Mais receita.** R$ 69 de cada R$ 100 (de 67,4% a 71,6% nas pontas) | estimativas do Executivo, não refeitas depois das mudanças |
| O que é imposto a mais de verdade? | **R$ 38 de cada R$ 100** (corte de benefícios e Reidi); outros **R$ 31** são crédito das empresas que fica retido e entra antes | a retenção pode voltar como gasto ou menos receita nos anos seguintes, se o crédito for usado depois |
| O lado do gasto é corte estrutural? | **Não.** É bloqueio de um ano, facultativo, que não entra na base dos anos seguintes; nenhuma regra das obrigatórias muda | se o governo bloquear todo ano, o efeito se repete, mas a lei não obriga |
| O tamanho resolve o buraco? | **Não.** Cobre 10,2% a 12,6% do ajuste que a IFI diz faltar | o buraco é o da IFI; o governo prevê superávit |
| O diesel fora da meta é gasto a menos? | **Não.** É gasto igual, que sai da conta da meta de 2026 | o valor é o teto; o gasto efetivo pode ser menor |
| A oposição mudou o texto? | **Pouco.** Perdeu a Emenda 40 e os 2 destaques; ganhou a Lei Kandir mais suave e a proteção do PIS e da Cofins | a Câmara ainda pode mudar |

## 9. Variantes (o que muda se a leitura for outra)

- **V1.** só conta como imposto o que aumenta tributo para sempre (benefícios e Reidi); a compensação vira 'adiantamento': o imposto a mais cai para 35% a 43%; o gasto contido continua de 28% a 33%; o resto (28% a 33%) é dinheiro das empresas adiantado.
- **V2.** o bloqueio é facultativo; se o governo não bloquear, a lei também não deixa limitar a compensação (art. 6º-F): sobra só o imposto a mais, R$ 19.5 bilhões, e 100% do ajuste vira receita.
- **V3.** o governo bloqueia o teto da faixa e a compensação vem no teto: é a ponta mais favorável ao lado do gasto, e o gasto contido não passa de um terço.

## 10. Arquivos

- números: `resultados/RESUMO.json`; validação: `resultados/VALIDACAO.json`; tabelas: `dados/derivados/`
- gráficos (1920×1080): `resultados/figuras/`
- leitura da IA: `docs/LEITURA_DA_IA.md`; revisão: `docs/REVISAO_ADVERSARIAL.md`; rodadas: `docs/RODADAS.md`
