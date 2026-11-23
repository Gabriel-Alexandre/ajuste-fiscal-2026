# O ajuste do Lula corta gasto ou aumenta imposto? Relatório da rodada 2

**Projeto:** `ajuste-fiscal-2026` · **Rodada:** 2 (23/11/2026, depois da revisão adversarial) · **Repositório:** https://github.com/Gabriel-Alexandre/ajuste-fiscal-2026
Todos os números deste arquivo saem de `resultados/RESUMO.json`, gerado por script a partir das fontes em `dados/brutos/` (com sha256 no `dados/MANIFESTO.json`). Validação por outro caminho: **33 de 33** (`resultados/VALIDACAO.json`).

## O que este projeto não consegue dizer (leia antes)

1. **Os valores por medida são estimativas do Poder Executivo**, levadas ao Parecer nº 221/2026 do relator no Senado. A Consultoria de Orçamento do Senado registrou que elas não foram refeitas depois das mudanças no texto, e não há memória de cálculo pública por medida. O DIAP escreve que os R$ 15 bilhões do corte de benefícios *"necessita ser reavaliada"*, porque o Senado tirou a desoneração da folha, a informática e os semicondutores do corte; parte da arrecadação ainda é dividida com estados e municípios, e os tributos com noventena só pagam a partir do 4º mês depois da lei. **O R$ 38 de cada R$ 100 é um teto.**
2. **A divisão de 31, 31 e 38 é o cenário da tabela do governo, em que o bloqueio é acionado.** O bloqueio do art. 6º-C só vale quando o resultado de 2027 fica abaixo do centro da meta, e a trava dos créditos (art. 6º-F) só vale se o bloqueio for adotado. O próprio orçamento de 2027 (PLOA) projeta resultado acima do centro; nesse caso sobra só o benefício fiscal cortado (variante V2).
3. **Depois da votação, o relator falou em R$ 50 bilhões** e o ministro, em R$ 46 a 56 bilhões. Nenhum dos dois publicou a nova divisão por medida. A conta daqui usa a única tabela publicada, a de R$ 45,1 a 56,1 bilhões.
4. **A Câmara marcou sessão para 23/11, às 18h.** Até a coleta, a API da Câmara registrava nenhuma votação. O texto pode mudar lá.
5. **O tamanho do buraco é o da IFI**, que tem premissas mais duras que as do governo (PIB, inflação, receitas). O governo prevê superávit em 2027; a IFI, déficit. Os dois números estão aqui.

## 1. A resposta curta

**Na tabela do próprio governo**, de cada **R$ 100** do ajuste de 2027, **R$ 31** são gasto contido (bloqueio do Orçamento), **R$ 31** são dinheiro das empresas que entra antes (limite ao uso de créditos tributários) e **R$ 38** são benefício fiscal cortado, que para quem paga é imposto a mais. Somando o adiantado e o benefício cortado, **R$ 69 de cada R$ 100 vêm de receita**. Nas duas pontas da faixa, a receita fica entre **67,4% a 71,6%** do total.

**Se 2027 correr como o próprio PLOA projeta**, o bloqueio não é acionado, a trava dos créditos também não, e sobra só o benefício fiscal cortado: **R$ 19,5 bilhões, 100% receita** (0,13% do PIB).

**O lado do gasto não é corte de regra.** É bloqueio de um ano: a parte que vira redução do limite não pode ser recomposta no mesmo ano (art. 6º-E, § 2º), mas não entra na base dos anos seguintes (§ 1º), e o art. 12 deixa o valor bloqueado voltar no ano seguinte como investimento, fora do teto. As regras que fazem as maiores despesas obrigatórias crescerem (Previdência, salário mínimo, BPC) não mudam; o texto põe teto em dois repasses (Lei Kandir e compensação previdenciária) e deixa bloquear algumas despesas legais (art. 6º-D).

**E o tamanho:** o ajuste equivale a **0,31% a 0,38% do PIB**. A IFI calcula que faltam cerca de **3 pontos do PIB**, perto de **R$ 440 bilhões**, para a dívida parar de subir; o pacote cobre **de 10% a 13%** disso (com o PIB do governo ou com o da IFI), ou **7,8% a 9,7%** se o juro real for de 6,1%, a estimativa nova da IFI.

## 2. A tabela, medida por medida (2027, R$ bilhões)

| Medida | Natureza | Mínimo | Máximo |
|---|---|---:|---:|
| Bloqueio de despesas para buscar o centro da meta (art. 6º-C a 6º-E) | gasto contido | 12,8 | 18,3 |
| Limite ao uso de créditos tributários para pagar outros tributos (art. 6º-F) | receita adiantada | 12,8 | 18,3 |
| Corte linear de benefícios fiscais, de 10% para 20% (art. 4º) | benefício fiscal cortado (imposto a mais) | 15,0 | 15,0 |
| Teto para o benefício do Reidi (art. 9º) | benefício fiscal cortado (imposto a mais) | 4,5 | 4,5 |
| **Total** | | **45,1** | **56,1** |

Fonte: Parecer nº 221/2026-PLEN/SF, *"de acordo com informações do Poder Executivo"*. A mesma tabela está na nota técnica do DIAP (16/11, que cita a nota da Conorf de 13/11) e na reportagem do Jota de 18/11; a validação confere as três.

**Como cada medida foi classificada.** O parecer do relator na Câmara (PRLP 1, 19/11/2026) diz que os arts. 4º (benefícios), 9º (Reidi) e 6º-F (créditos) *"ampliam receita"*, e que no 6º-F *"o efeito seja de antecipação de arrecadação, pois os créditos dos contribuintes não se extinguem"*. O bloqueio (arts. 6º-C a 6º-E) é contenção de despesa. É essa a divisão usada aqui. O parecer do Senado chama o corte de benefícios de *"redução do gasto tributário"*; quem prefere essa leitura tem a variante V4.

**A ligação entre as duas metades.** O art. 6º-F só deixa limitar os créditos das empresas se o governo adotar o bloqueio do art. 6º-C, e até a soma da redução de limite com o contingenciamento da Lei de Responsabilidade Fiscal. A tabela do governo põe as duas linhas na mesma faixa, de R$ 12,8 a 18,3 bilhões; essa igualdade é uma suposição da estimativa, não um limite da lei.

| Somas | Mínimo | Máximo | Meio da faixa |
|---|---:|---:|---:|
| Gasto contido (R$ bi) | 12,8 | 18,3 | 15,6 |
| Receita adiantada (R$ bi) | 12,8 | 18,3 | 15,6 |
| Benefício fiscal cortado (R$ bi) | 19,5 | 19,5 | 19,5 |
| Receita total (R$ bi) | 32,3 | 37,8 | 35,0 |
| Parte do gasto | 28,4% | 32,6% | 30,8% |
| Parte da receita | 71,6% | 67,4% | 69,2% |

## 3. Três cenários para 2027, pela regra do próprio texto

| Cenário | O que acontece | De cada R$ 100 (gasto, adiantado, benefício cortado) |
|---|---|---|
| A tabela do governo | o resultado fica abaixo do centro da meta e o governo bloqueia | 31, 31, 38 (R$ 45,1 a 56,1 bi) |
| 2027 como o PLOA projeta | resultado para a meta de R$ 83,4 bi, acima do centro de R$ 73,2 bi: o art. 6º-C não se aplica, nem a trava | 0, 0, 100 (R$ 19,5 bi) |
| 2027 como a IFI projeta | resultado para a meta de R$ 0,9 bi, abaixo do piso de R$ 36,6 bi: o bloqueio de R$ 35,7 bi da Lei de Responsabilidade Fiscal já é obrigatório, e o teto da trava dos créditos soma esse bloqueio | não calculável com o que foi publicado; a receita adiantada pode passar dos R$ 18,3 bi da tabela |

Fonte: tabela 8 do RAF nº 116 da IFI (o PLOA e a IFI lado a lado; a projeção da IFI é a do RAF nº 113, de junho, repetida ali), e os arts. 5º, 6º-C e 6º-F da redação final.

## 4. O que ficou fora da tabela

| Item | O que diz o texto | Por que não entra na conta |
|---|---|---|
| Lei Kandir | repasse aos estados limitado a R$ 2,0 bi por ano *"até o exercício de 2030"*, com o saldo recomposto de 2028 a 2030 (redação final, art. 2º; o Jota leu *"apenas para o ano de 2027"*, e o texto é ambíguo porque o limite e a recomposição caem nos mesmos anos) | é adiamento de pagamento; a Folhapress (no Jornal do Comércio) e o InvestNews dizem que cerca de R$ 10 bi em medidas assim abrem espaço para promessas de campanha (Bolsa Família, Pé-de-Meia), sem economia estrutural |
| Compensação previdenciária | teto de R$ 3,0 bi por ano de 2027 a 2030 (art. 6º); a Folhapress diz que o repasse de 2027 cairia de R$ 8,3 bi para R$ 3,0 bi | o texto não diz o que acontece com o que passar do teto; o espaço também vai para as promessas |
| Proex | teto de R$ 1,0 bi por ano | o relator na Câmara escreve que o teto é *"superior à execução de 2025 e à previsão para 2026"*: não economiza nada hoje |
| Supersalários | prazo de 60 dias para o Congresso votar a regra (redação final; o texto-base dizia 120) | o ministro estimou R$ 3 bi; o texto não quantifica, e a economia do Judiciário e do MP fica com eles |
| Art. 8º | dá por cumprida a regra de compensar gasto novo (art. 17 da Lei de Responsabilidade Fiscal) para as medidas do seguro rural | gasto, sem valor publicado |
| Art. 12 | o valor bloqueado pode voltar no ano seguinte como investimento, fora do teto | gasto no ano seguinte, sem valor publicado |
| Art. 14 | restos a pagar de contratos e convênios só podem ser bloqueados ou cancelados depois de 31/12/2027 | gasto, sem valor publicado |

O relator na Câmara escreve que os arts. 12, 13 e 14 *"são os únicos de sentido expansivo"*.

## 5. O tamanho do buraco

| Número | Valor | Fonte |
|---|---:|---|
| Meta de 2027 (centro e piso) | R$ 73,2 bi (0,50% do PIB) e R$ 36,6 bi | PLOA 2027, pela tabela 8 do RAF 116 e pela nota do DIAP |
| Resultado efetivo de 2027, governo | R$ 18,6 bi | PLOA 2027, pela IFI (RAF 116) |
| Resultado efetivo de 2027, IFI | R$ -86,1 bi | IFI, RAF 113, repetido no RAF 116 |
| Distância entre os dois | R$ 104,8 bi | IFI, RAF 116 (soma sem arredondar) |
| Déficit de 2027 com as promessas novas | 1,0% do PIB | IFI, RAF 117 |
| Promessas novas não orçadas (Bolsa Família, Bets, MEI) | R$ 40,0 bi | IFI, RAF 117 |
| Aumento das despesas obrigatórias de 2026 para 2027 | R$ 131,4 bi, ou R$ 53,2 bi acima da inflação do PLOA | IFI, RAF 116 (tabela 7); conta |
| Superávit que estabiliza a dívida | 2,1% do PIB (ou 2,9% com juro real de 6,1%) | IFI, RAF 117 |
| Ajuste que a IFI diz faltar | 3 p.p. do PIB, cerca de R$ 440 bi (R$ 443,5 bi no PIB do PLOA, R$ 436,0 bi no da IFI) | IFI, RAF 117; conta |
| Dívida bruta | 82,9% do PIB em set/2026; 86,4% no fim de 2027; chance de 81,6% de passar de 90% até 2030 | BC (pela Agência Brasil); IFI, RAF 117 |

**As comparações (todas com o ajuste de 2027 da tabela do governo):**

- o ajuste cobre **10,2% a 12,6%** dos 3 pontos do PIB que a IFI diz faltar (10,3% a 12,9% com o PIB da IFI); com o juro real de 6,1% e a mesma lógica da IFI (déficit de 1,0% mais o superávit que estabiliza), faltariam 3,9 pontos e a cobertura cai para **7,8% a 9,7%**. A conta dos 3 pontos é da IFI e soma o déficit do governo central com o superávit que estabiliza a dívida do governo geral;
- as despesas obrigatórias sobem R$ 131,4 bi em valores correntes, mas caem como parte do PIB (de 15,9% para 15,6%, pela IFI); acima da inflação do PLOA, o aumento é de R$ 53,2 bi. O ajuste inteiro equivale a **84,8% a 105,5%** desse aumento real; só o gasto contido, **24,1% a 34,4%**;
- as promessas não orçadas que a IFI soma equivalem a **71,3% a 88,7%** do ajuste (parte delas, como o Bolsa Família, é a mesma que as medidas fora da tabela ajudam a acomodar);
- o ajuste equivale a **43,0% a 53,5%** da distância entre o que o governo e a IFI preveem para 2027.

## 6. O diesel de 2026

O art. 13 da redação final autoriza tirar da meta de 2026 até **R$ 10,5 bilhões** gastos com a subvenção ao diesel (MP 1.391/2026). O dinheiro é gasto igual; ele só deixa de contar para a meta. E o efeito prático é liberar bloqueio: no relatório do 4º bimestre, faltavam R$ 13,6 bilhões de bloqueio para chegar ao piso da meta, e o diesel equivale a **77,2%** disso.

| 2026 (governo central) | R$ bi | Fonte |
|---|---:|---|
| Resultado projetado antes das deduções | -80,9 | relatório do 4º bimestre, na tabela 3 do RAF 117 |
| Despesas já tiradas da conta da meta | 67,3 | idem |
| Resultado para a meta, depois das deduções e antes do bloqueio | -13,6 | idem |
| Piso da meta | 0,0 | idem |
| Bloqueio anunciado para chegar ao piso | 13,6 | idem |
| Diesel tirado pelo PLP | 10,5 | redação final, art. 13 |
| Total tirado da conta com o diesel | 77,8 | conta |
| Déficit do governo central de janeiro a setembro | -90,2 | Tesouro, pela Agência Brasil |

O diesel equivale a **13,0%** do déficit projetado para 2026 e a **18,7% a 23,3%** do ajuste prometido para 2027. A Folhapress (em A Gazeta, 23/11) diz que a medida entrou para evitar um novo bloqueio no fim do ano, por causa da arrecadação mais fraca.

## 7. O que a oposição tentou mudar

| Votação (Senado) | Placar | O que estava em jogo |
|---|---:|---|
| Urgência, 12/11 | 40 a 38 | votar sem passar pelas comissões |
| Texto-base, 12/11 | 45 a 31 | o substitutivo do relator Eduardo Braga (MDB) |
| Emenda 40 (Rogério Marinho, PL), 18/11 | 30 a 47 (rejeitada) | teto de 0,6% para o crescimento do gasto (no lugar de 2%), o centro da meta obrigatório, o corte de despesas obrigatórias, sem a trava dos créditos, sem os adiamentos da Lei Kandir e da compensação previdenciária, sem o diesel fora da meta, e de volta a desvinculação de 40% dos superávits de fundos; o corte de benefícios e o Reidi ficavam |
| Destaque do PL: teto da compensação previdenciária | 45 a 32 (mantido) | tirar o teto de R$ 3 bi por ano |
| Destaque do Republicanos: trava dos créditos | 49 a 31 (mantida) | tirar o art. 6º-F |
| Turno suplementar, 18/11 | 69 a 2 | as emendas de última hora, entre elas a 83 (Tereza Cristina, PP), que tira da trava a compensação de créditos de PIS e Cofins com débitos da CBS |

**Por partido:** no texto-base, o PL votou 2 SIM e 12 NÃO, e o PT, 8 SIM e 0 NÃO. Na Emenda 40, o PL votou 13 SIM e 1 NÃO. Na trava dos créditos, o PL votou 1 SIM e 14 NÃO. No turno suplementar, o PL votou 10 SIM e 1 NÃO.

**O que a oposição conseguiu:** a Lei Kandir ficou em R$ 2,0 bi por ano, com o saldo pago até 2030 (era R$ 1 bi por ano, com o saldo até 2037), num acordo pelo qual o PL retirou o destaque; e a emenda da senadora Tereza Cristina tirou da trava a compensação de PIS e Cofins com a CBS (o Ministério do Planejamento disse ao Jota que o efeito é neutro). O resto do que a Emenda 40 pedia perdeu.

## 8. A Câmara (23/11)

Situação na API da Câmara na coleta: *Aguardando Despacho do Presidente da Câmara dos Deputados (Chancela)*; última tramitação em 2026-11-19T18:47; nenhuma votação registrada. A sessão extraordinária foi marcada para as 18h de 23/11, começando pela urgência (REQ 4504/2026). O relator, Mauro Benevides Filho (União-CE), deu parecer preliminar favorável sem mudar o texto do Senado. Precisa de 257 votos. Refazer a coleta depois da sessão.

## 9. Veredito por critério

| Critério | Veredito | O limite |
|---|---|---|
| O ajuste corta gasto ou aumenta receita? | **Mais receita.** Na tabela do governo, R$ 69 de cada R$ 100 (de 67,4% a 71,6% nas pontas); se 2027 correr como o PLOA projeta, 100% | estimativas do Executivo, não refeitas depois das mudanças; o cenário depende do resultado de 2027 |
| O que é imposto a mais de verdade? | **R$ 38 de cada R$ 100**, no máximo (o benefício fiscal cortado); outros **R$ 31** são crédito das empresas retido, que entra antes | os R$ 15 bi do corte de benefícios estão provavelmente altos (DIAP); o crédito retido pode voltar como menos receita depois |
| O lado do gasto é corte estrutural? | **Não.** É bloqueio de um ano, que só vale abaixo do centro da meta, não entra na base dos anos seguintes e pode voltar no ano seguinte como investimento (art. 12); as regras da Previdência, do salário mínimo e do BPC não mudam | se o governo bloquear todo ano, o efeito se repete, mas a lei não obriga |
| O tamanho resolve o buraco? | **Não.** Cobre de 10% a 13% do ajuste que a IFI diz faltar; o que fica para sempre (o benefício cortado) cobre 4,4% | o buraco é o da IFI; o governo prevê superávit |
| O diesel fora da meta é gasto a menos? | **Não.** É gasto igual, que sai da conta da meta de 2026 e libera 77,2% do bloqueio que faltava | o valor é o teto; o gasto efetivo pode ser menor |
| A oposição mudou o texto? | **Pouco.** Perdeu a Emenda 40 e os 2 destaques; ganhou a Lei Kandir mais suave e a saída do PIS e da Cofins da trava | a Câmara ainda pode mudar |

## 10. Variantes (o que muda se a leitura for outra)

- **V2.** 2027 corre como o PLOA projeta: o resultado para a meta fica acima do centro, então o bloqueio do art. 6º-C não é acionado e a trava dos créditos (art. 6º-F) também não: sobra só o benefício fiscal cortado, R$ 19,5 bilhões (0,13% do PIB), e 100% do ajuste é receita.
- **V4.** benefício fiscal cortado conta como corte de gasto tributário (o nome técnico do benefício é gasto tributário): de cada R$ 100, R$ 69 viram corte (R$ 31 de despesa e R$ 38 de benefício) e R$ 31 ficam como receita adiantada; para quem paga, o benefício cortado continua sendo tributo a mais.
- **V5.** só conta o que fica: o bloqueio pode voltar no ano seguinte como investimento fora do teto (art. 12) e o crédito retido continua da empresa: o que fica para sempre é o benefício fiscal cortado, R$ 19,5 bilhões, 4,4% do ajuste que a IFI diz faltar.

## 11. Arquivos

- números: `resultados/RESUMO.json`; validação: `resultados/VALIDACAO.json`; tabelas: `dados/derivados/`
- gráficos (1920×1080): `resultados/figuras/`
- leitura da IA: `docs/LEITURA_DA_IA.md`; revisão: `docs/REVISAO_ADVERSARIAL.md`; rodadas: `docs/RODADAS.md`
