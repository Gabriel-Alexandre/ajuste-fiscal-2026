"""Escreve RELATORIO.md, RESUMO_SIMPLES.md, docs/LEITURA_DA_IA.md e docs/REVISAO_ADVERSARIAL.md
a partir de resultados/RESUMO.json e resultados/VALIDACAO.json. Nenhum número é escrito à mão.

Uso:  python ferramentas/gerar_relatorio.py
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Gabriel-Alexandre/ajuste-fiscal-2026"


def br(x, casas=1):
    return f"{float(x):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def faixa(par, casas=1, unidade="%"):
    a, b = sorted(float(x) for x in par)
    return f"{br(a, casas)}{unidade} a {br(b, casas)}{unidade}"


def main() -> None:
    r = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    v = json.loads((RAIZ / "resultados" / "VALIDACAO.json").read_text(encoding="utf-8"))
    c = r["composicao_2027"]; mn = c["pontas"]["minimo"]; mx = c["pontas"]["maximo"]; meio = c["meio_da_faixa"]; d = c["de_cada_100"]
    b = r["buraco"]; a26 = b["ano_2026"]; fora = r["fora_da_tabela_de_impacto"]; dep = r["depois_do_senado"]
    var = {x["id"]: x for x in r["variantes"]}
    pl = {p["votacao"]: p for p in r["votacoes_senado"]["placar"]}
    pp = r["votacoes_senado"]["por_partido"]
    cam = r["camara"]
    nvot = "nenhuma votação" if str(cam["votacoes_registradas"]) == "0" else f"{cam['votacoes_registradas']} votações"

    def placar(chave):
        p = pl[chave]
        return f"{p['oficial_sim']} a {p['oficial_nao']}"

    def partido(chave, sigla):
        x = pp[chave].get(sigla, {"SIM": 0, "NÃO": 0})
        return f"{x['SIM']} SIM e {x['NÃO']} NÃO"

    limites = f"""## O que este projeto não consegue dizer (leia antes)

1. **Os valores por medida são estimativas do Poder Executivo**, levadas ao Parecer nº 221/2026 do relator no Senado. A Consultoria de Orçamento do Senado registrou que elas não foram refeitas depois das mudanças no texto, e não há memória de cálculo pública por medida. O DIAP escreve que os R$ 15 bilhões do corte de benefícios *"necessita ser reavaliada"*, porque o Senado tirou a desoneração da folha, a informática e os semicondutores do corte; parte da arrecadação ainda é dividida com estados e municípios, e os tributos com noventena só pagam a partir do 4º mês depois da lei. **O R$ {d['imposto_a_mais']} de cada R$ 100 é um teto.**
2. **A divisão de 31, 31 e 38 é o cenário da tabela do governo, em que o bloqueio é acionado.** O bloqueio do art. 6º-C só vale quando o resultado de 2027 fica abaixo do centro da meta, e a trava dos créditos (art. 6º-F) só vale se o bloqueio for adotado. O próprio orçamento de 2027 (PLOA) projeta resultado acima do centro; nesse caso sobra só o benefício fiscal cortado (variante V2).
3. **Depois da votação, o relator falou em R$ {br(dep['relator_rs_bi'],0)} bilhões** e o ministro, em R$ {br(dep['ministro_faixa_rs_bi'][0],0)} a {br(dep['ministro_faixa_rs_bi'][1],0)} bilhões. Nenhum dos dois publicou a nova divisão por medida. A conta daqui usa a única tabela publicada, a de R$ {br(mn['total'])} a {br(mx['total'])} bilhões.
4. **A Câmara marcou sessão para 23/11, às 18h.** Até a coleta, a API da Câmara registrava {nvot}. O texto pode mudar lá.
5. **O tamanho do buraco é o da IFI**, que tem premissas mais duras que as do governo (PIB, inflação, receitas). O governo prevê superávit em 2027; a IFI, déficit. Os dois números estão aqui.
"""

    nomes_nat = {"gasto contido": "gasto contido", "receita antecipada": "receita adiantada", "imposto a mais": "benefício fiscal cortado (imposto a mais)"}
    tabela_medidas = "\n".join(
        f"| {m['nome']} | {nomes_nat[m['natureza']]} | {br(m['minimo'])} | {br(m['maximo'])} |" for m in c["medidas"])

    relatorio = f"""# O ajuste do Lula corta gasto ou aumenta imposto? Relatório da rodada 2

**Projeto:** `ajuste-fiscal-2026` · **Rodada:** 2 (23/11/2026, depois da revisão adversarial) · **Repositório:** {REPO}
Todos os números deste arquivo saem de `resultados/RESUMO.json`, gerado por script a partir das fontes em `dados/brutos/` (com sha256 no `dados/MANIFESTO.json`). Validação por outro caminho: **{v['passaram']} de {v['total']}** (`resultados/VALIDACAO.json`).

{limites}
## 1. A resposta curta

**Na tabela do próprio governo**, de cada **R$ 100** do ajuste de 2027, **R$ {d['gasto_contido']}** são gasto contido (bloqueio do Orçamento), **R$ {d['receita_antecipada']}** são dinheiro das empresas que entra antes (limite ao uso de créditos tributários) e **R$ {d['imposto_a_mais']}** são benefício fiscal cortado, que para quem paga é imposto a mais. Somando o adiantado e o benefício cortado, **R$ {d['receita_total']} de cada R$ 100 vêm de receita**. Nas duas pontas da faixa, a receita fica entre **{faixa([mn['pct_receita'], mx['pct_receita']])}** do total.

**Se 2027 correr como o próprio PLOA projeta**, o bloqueio não é acionado, a trava dos créditos também não, e sobra só o benefício fiscal cortado: **R$ {br(var['V2']['total'])} bilhões, 100% receita** ({br(var['V2']['pct_pib'],2)}% do PIB).

**O lado do gasto não é corte de regra.** É bloqueio de um ano: a parte que vira redução do limite não pode ser recomposta no mesmo ano (art. 6º-E, § 2º), mas não entra na base dos anos seguintes (§ 1º), e o art. 12 deixa o valor bloqueado voltar no ano seguinte como investimento, fora do teto. As regras que fazem as maiores despesas obrigatórias crescerem (Previdência, salário mínimo, BPC) não mudam; o texto põe teto em dois repasses (Lei Kandir e compensação previdenciária) e deixa bloquear algumas despesas legais (art. 6º-D).

**E o tamanho:** o ajuste equivale a **{faixa(b['ajuste_pct_pib'], 2)} do PIB**. A IFI calcula que faltam cerca de **3 pontos do PIB**, perto de **R$ 440 bilhões**, para a dívida parar de subir; o pacote cobre **de 10% a 13%** disso (com o PIB do governo ou com o da IFI), ou **{faixa(b['ajuste_cobre_do_necessario_juro61_pct'])}** se o juro real for de 6,1%, a estimativa nova da IFI.

## 2. A tabela, medida por medida (2027, R$ bilhões)

| Medida | Natureza | Mínimo | Máximo |
|---|---|---:|---:|
{tabela_medidas}
| **Total** | | **{br(mn['total'])}** | **{br(mx['total'])}** |

Fonte: Parecer nº 221/2026-PLEN/SF, *"de acordo com informações do Poder Executivo"*. A mesma tabela está na nota técnica do DIAP (16/11, que cita a nota da Conorf de 13/11) e na reportagem do Jota de 18/11; a validação confere as três.

**Como cada medida foi classificada.** O parecer do relator na Câmara (PRLP 1, 19/11/2026) diz que os arts. 4º (benefícios), 9º (Reidi) e 6º-F (créditos) *"ampliam receita"*, e que no 6º-F *"o efeito seja de antecipação de arrecadação, pois os créditos dos contribuintes não se extinguem"*. O bloqueio (arts. 6º-C a 6º-E) é contenção de despesa. É essa a divisão usada aqui. O parecer do Senado chama o corte de benefícios de *"redução do gasto tributário"*; quem prefere essa leitura tem a variante V4.

**A ligação entre as duas metades.** O art. 6º-F só deixa limitar os créditos das empresas se o governo adotar o bloqueio do art. 6º-C, e até a soma da redução de limite com o contingenciamento da Lei de Responsabilidade Fiscal. A tabela do governo põe as duas linhas na mesma faixa, de R$ {br(mn['gasto_contido'])} a {br(mx['gasto_contido'])} bilhões; essa igualdade é uma suposição da estimativa, não um limite da lei.

| Somas | Mínimo | Máximo | Meio da faixa |
|---|---:|---:|---:|
| Gasto contido (R$ bi) | {br(mn['gasto_contido'])} | {br(mx['gasto_contido'])} | {br(meio['gasto_contido'])} |
| Receita adiantada (R$ bi) | {br(mn['receita_antecipada'])} | {br(mx['receita_antecipada'])} | {br(meio['receita_antecipada'])} |
| Benefício fiscal cortado (R$ bi) | {br(mn['imposto_a_mais'])} | {br(mx['imposto_a_mais'])} | {br(meio['imposto_a_mais'])} |
| Receita total (R$ bi) | {br(mn['receita_total'])} | {br(mx['receita_total'])} | {br(meio['receita_total'])} |
| Parte do gasto | {br(mn['pct_gasto'])}% | {br(mx['pct_gasto'])}% | {br(meio['pct_gasto'])}% |
| Parte da receita | {br(mn['pct_receita'])}% | {br(mx['pct_receita'])}% | {br(meio['pct_receita'])}% |

## 3. Três cenários para 2027, pela regra do próprio texto

| Cenário | O que acontece | De cada R$ 100 (gasto, adiantado, benefício cortado) |
|---|---|---|
| A tabela do governo | o resultado fica abaixo do centro da meta e o governo bloqueia | {d['gasto_contido']}, {d['receita_antecipada']}, {d['imposto_a_mais']} (R$ {br(mn['total'])} a {br(mx['total'])} bi) |
| 2027 como o PLOA projeta | resultado para a meta de R$ {br(b['ploa2027_resultado_para_meta_rs_bi'])} bi, acima do centro de R$ {br(b['meta2027_centro_rs_bi'])} bi: o art. 6º-C não se aplica, nem a trava | 0, 0, 100 (R$ {br(var['V2']['total'])} bi) |
| 2027 como a IFI projeta | resultado para a meta de R$ {br(b['ifi2027_resultado_para_meta_rs_bi'])} bi, abaixo do piso de R$ {br(b['meta2027_piso_rs_bi'])} bi: o bloqueio de R$ {br(b['ifi_bloqueio_que_faltaria_2027_rs_bi'])} bi da Lei de Responsabilidade Fiscal já é obrigatório, e o teto da trava dos créditos soma esse bloqueio | não calculável com o que foi publicado; a receita adiantada pode passar dos R$ {br(mx['receita_antecipada'])} bi da tabela |

Fonte: tabela 8 do RAF nº 116 da IFI (o PLOA e a IFI lado a lado; a projeção da IFI é a do RAF nº 113, de junho, repetida ali), e os arts. 5º, 6º-C e 6º-F da redação final.

## 4. O que ficou fora da tabela

| Item | O que diz o texto | Por que não entra na conta |
|---|---|---|
| Lei Kandir | repasse aos estados limitado a R$ {br(fora['kandir_teto_anual_rs_bi'])} bi por ano *"até o exercício de 2030"*, com o saldo recomposto de 2028 a 2030 (redação final, art. 2º; o Jota leu *"apenas para o ano de 2027"*, e o texto é ambíguo porque o limite e a recomposição caem nos mesmos anos) | é adiamento de pagamento; a Folhapress (no Jornal do Comércio) e o InvestNews dizem que cerca de R$ {br(fora['medidas_que_abrem_espaco_para_promessas_rs_bi'],0)} bi em medidas assim abrem espaço para promessas de campanha (Bolsa Família, Pé-de-Meia), sem economia estrutural |
| Compensação previdenciária | teto de R$ {br(fora['comprev_teto_anual_rs_bi'])} bi por ano de 2027 a 2030 (art. 6º); a Folhapress diz que o repasse de 2027 cairia de R$ {br(fora['comprev_2027_sem_teto_rs_bi'])} bi para R$ {br(fora['comprev_teto_anual_rs_bi'])} bi | o texto não diz o que acontece com o que passar do teto; o espaço também vai para as promessas |
| Proex | teto de R$ {br(fora['proex_teto_rs_bi'])} bi por ano | o relator na Câmara escreve que o teto é *"superior à execução de 2025 e à previsão para 2026"*: não economiza nada hoje |
| Supersalários | prazo de 60 dias para o Congresso votar a regra (redação final; o texto-base dizia 120) | o ministro estimou R$ {br(fora['supersalarios_estimativa_ministro_rs_bi'],0)} bi; o texto não quantifica, e a economia do Judiciário e do MP fica com eles |
| Art. 8º | dá por cumprida a regra de compensar gasto novo (art. 17 da Lei de Responsabilidade Fiscal) para as medidas do seguro rural | gasto, sem valor publicado |
| Art. 12 | o valor bloqueado pode voltar no ano seguinte como investimento, fora do teto | gasto no ano seguinte, sem valor publicado |
| Art. 14 | restos a pagar de contratos e convênios só podem ser bloqueados ou cancelados depois de 31/12/2027 | gasto, sem valor publicado |

O relator na Câmara escreve que os arts. 12, 13 e 14 *"são os únicos de sentido expansivo"*.

## 5. O tamanho do buraco

| Número | Valor | Fonte |
|---|---:|---|
| Meta de 2027 (centro e piso) | R$ {br(b['meta2027_centro_rs_bi'])} bi ({br(b['meta2027_centro_pct_pib'],2)}% do PIB) e R$ {br(b['meta2027_piso_rs_bi'])} bi | PLOA 2027, pela tabela 8 do RAF 116 e pela nota do DIAP |
| Resultado efetivo de 2027, governo | R$ {br(b['ploa2027_primario_efetivo_rs_bi'])} bi | PLOA 2027, pela IFI (RAF 116) |
| Resultado efetivo de 2027, IFI | R$ {br(b['ifi2027_primario_efetivo_rs_bi'])} bi | IFI, RAF 113, repetido no RAF 116 |
| Distância entre os dois | R$ {br(b['distancia_ploa_ifi_2027_rs_bi'])} bi | IFI, RAF 116 (soma sem arredondar) |
| Déficit de 2027 com as promessas novas | {br(b['ifi2027_deficit_potencial_pct_pib'])}% do PIB | IFI, RAF 117 |
| Promessas novas não orçadas (Bolsa Família, Bets, MEI) | R$ {br(b['promessas_nao_orcadas_rs_bi'])} bi | IFI, RAF 117 |
| Aumento das despesas obrigatórias de 2026 para 2027 | R$ {br(b['aumento_obrigatorias_2027_rs_bi'])} bi, ou R$ {br(b['aumento_real_obrigatorias_2027_rs_bi'])} bi acima da inflação do PLOA | IFI, RAF 116 (tabela 7); conta |
| Superávit que estabiliza a dívida | {br(b['primario_que_estabiliza_divida_pct_pib'][0])}% do PIB (ou {br(b['primario_que_estabiliza_divida_pct_pib'][1])}% com juro real de 6,1%) | IFI, RAF 117 |
| Ajuste que a IFI diz faltar | 3 p.p. do PIB, cerca de R$ 440 bi (R$ {br(b['ajuste_necessario_ifi_rs_bi'])} bi no PIB do PLOA, R$ {br(b['ajuste_necessario_ifi_pib_ifi_rs_bi'])} bi no da IFI) | IFI, RAF 117; conta |
| Dívida bruta | {br(b['divida_bruta']['set_2026_bc'])}% do PIB em set/2026; {br(b['divida_bruta']['fim_2027_ifi'])}% no fim de 2027; chance de {br(b['divida_bruta']['chance_passar_90_ate_2030_pct'])}% de passar de 90% até 2030 | BC (pela Agência Brasil); IFI, RAF 117 |

**As comparações (todas com o ajuste de 2027 da tabela do governo):**

- o ajuste cobre **{faixa(b['ajuste_cobre_do_necessario_pct'])}** dos 3 pontos do PIB que a IFI diz faltar ({faixa(b['ajuste_cobre_do_necessario_pib_ifi_pct'])} com o PIB da IFI); com o juro real de 6,1% e a mesma lógica da IFI (déficit de 1,0% mais o superávit que estabiliza), faltariam {br(b['ajuste_necessario_juro61_pp_pib'])} pontos e a cobertura cai para **{faixa(b['ajuste_cobre_do_necessario_juro61_pct'])}**. A conta dos 3 pontos é da IFI e soma o déficit do governo central com o superávit que estabiliza a dívida do governo geral;
- as despesas obrigatórias sobem R$ {br(b['aumento_obrigatorias_2027_rs_bi'])} bi em valores correntes, mas caem como parte do PIB (de {br(b['obrigatorias_pct_pib'][0])}% para {br(b['obrigatorias_pct_pib'][1])}%, pela IFI); acima da inflação do PLOA, o aumento é de R$ {br(b['aumento_real_obrigatorias_2027_rs_bi'])} bi. O ajuste inteiro equivale a **{faixa(b['ajuste_sobre_aumento_real_obrigatorias_pct'])}** desse aumento real; só o gasto contido, **{faixa(b['gasto_contido_sobre_aumento_real_obrigatorias_pct'])}**;
- as promessas não orçadas que a IFI soma equivalem a **{faixa(b['promessas_sobre_ajuste_pct'])}** do ajuste (parte delas, como o Bolsa Família, é a mesma que as medidas fora da tabela ajudam a acomodar);
- o ajuste equivale a **{faixa(b['ajuste_sobre_distancia_ploa_ifi_pct'])}** da distância entre o que o governo e a IFI preveem para 2027.

## 6. O diesel de 2026

O art. 13 da redação final autoriza tirar da meta de 2026 até **R$ {br(a26['diesel_fora_da_meta_rs_bi'])} bilhões** gastos com a subvenção ao diesel (MP 1.391/2026). O dinheiro é gasto igual; ele só deixa de contar para a meta. E o efeito prático é liberar bloqueio: no relatório do 4º bimestre, faltavam R$ {br(a26['contingenciamento_rs_bi'])} bilhões de bloqueio para chegar ao piso da meta, e o diesel equivale a **{br(a26['diesel_sobre_contingenciamento_pct'])}%** disso.

| 2026 (governo central) | R$ bi | Fonte |
|---|---:|---|
| Resultado projetado antes das deduções | {br(a26['rardp_antes_deducoes_rs_bi'])} | relatório do 4º bimestre, na tabela 3 do RAF 117 |
| Despesas já tiradas da conta da meta | {br(a26['deducoes_rs_bi'])} | idem |
| Resultado para a meta, depois das deduções e antes do bloqueio | {br(a26['rardp_depois_deducoes_rs_bi'])} | idem |
| Piso da meta | {br(a26['meta_piso_rs_bi'])} | idem |
| Bloqueio anunciado para chegar ao piso | {br(a26['contingenciamento_rs_bi'])} | idem |
| Diesel tirado pelo PLP | {br(a26['diesel_fora_da_meta_rs_bi'])} | redação final, art. 13 |
| Total tirado da conta com o diesel | {br(a26['deducoes_com_diesel_rs_bi'])} | conta |
| Déficit do governo central de janeiro a setembro | {br(a26['tesouro_jan_set_rs_bi'])} | Tesouro, pela Agência Brasil |

O diesel equivale a **{br(a26['diesel_sobre_deficit_antes_deducoes_pct'])}%** do déficit projetado para 2026 e a **{faixa(a26['diesel_sobre_ajuste_2027_pct'])}** do ajuste prometido para 2027. A Folhapress (em A Gazeta, 23/11) diz que a medida entrou para evitar um novo bloqueio no fim do ano, por causa da arrecadação mais fraca.

## 7. O que a oposição tentou mudar

| Votação (Senado) | Placar | O que estava em jogo |
|---|---:|---|
| Urgência, 12/11 | {placar('senado-votacao-req-770-urgencia')} | votar sem passar pelas comissões |
| Texto-base, 12/11 | {placar('senado-votacao-texto-base')} | o substitutivo do relator Eduardo Braga (MDB) |
| Emenda 40 (Rogério Marinho, PL), 18/11 | {placar('senado-votacao-emenda-40')} (rejeitada) | teto de 0,6% para o crescimento do gasto (no lugar de 2%), o centro da meta obrigatório, o corte de despesas obrigatórias, sem a trava dos créditos, sem os adiamentos da Lei Kandir e da compensação previdenciária, sem o diesel fora da meta, e de volta a desvinculação de 40% dos superávits de fundos; o corte de benefícios e o Reidi ficavam |
| Destaque do PL: teto da compensação previdenciária | {placar('senado-votacao-comprev')} (mantido) | tirar o teto de R$ 3 bi por ano |
| Destaque do Republicanos: trava dos créditos | {placar('senado-votacao-compensacao')} (mantida) | tirar o art. 6º-F |
| Turno suplementar, 18/11 | {placar('senado-votacao-turno-suplementar')} | as emendas de última hora, entre elas a 83 (Tereza Cristina, PP), que tira da trava a compensação de créditos de PIS e Cofins com débitos da CBS |

**Por partido:** no texto-base, o PL votou {partido('senado-votacao-texto-base','PL')}, e o PT, {partido('senado-votacao-texto-base','PT')}. Na Emenda 40, o PL votou {partido('senado-votacao-emenda-40','PL')}. Na trava dos créditos, o PL votou {partido('senado-votacao-compensacao','PL')}. No turno suplementar, o PL votou {partido('senado-votacao-turno-suplementar','PL')}.

**O que a oposição conseguiu:** a Lei Kandir ficou em R$ {br(fora['kandir_teto_anual_rs_bi'])} bi por ano, com o saldo pago até 2030 (era R$ 1 bi por ano, com o saldo até 2037), num acordo pelo qual o PL retirou o destaque; e a emenda da senadora Tereza Cristina tirou da trava a compensação de PIS e Cofins com a CBS (o Ministério do Planejamento disse ao Jota que o efeito é neutro). O resto do que a Emenda 40 pedia perdeu.

## 8. A Câmara (23/11)

Situação na API da Câmara na coleta: *{cam['situacao']}*; última tramitação em {cam['ultima_tramitacao']}; {nvot} registrada. A sessão extraordinária foi marcada para as 18h de 23/11, começando pela urgência (REQ 4504/2026). O relator, Mauro Benevides Filho (União-CE), deu parecer preliminar favorável sem mudar o texto do Senado. Precisa de 257 votos. Refazer a coleta depois da sessão.

## 9. Veredito por critério

| Critério | Veredito | O limite |
|---|---|---|
| O ajuste corta gasto ou aumenta receita? | **Mais receita.** Na tabela do governo, R$ {d['receita_total']} de cada R$ 100 (de {faixa([mx['pct_receita'], mn['pct_receita']])} nas pontas); se 2027 correr como o PLOA projeta, 100% | estimativas do Executivo, não refeitas depois das mudanças; o cenário depende do resultado de 2027 |
| O que é imposto a mais de verdade? | **R$ {d['imposto_a_mais']} de cada R$ 100**, no máximo (o benefício fiscal cortado); outros **R$ {d['receita_antecipada']}** são crédito das empresas retido, que entra antes | os R$ 15 bi do corte de benefícios estão provavelmente altos (DIAP); o crédito retido pode voltar como menos receita depois |
| O lado do gasto é corte estrutural? | **Não.** É bloqueio de um ano, que só vale abaixo do centro da meta, não entra na base dos anos seguintes e pode voltar no ano seguinte como investimento (art. 12); as regras da Previdência, do salário mínimo e do BPC não mudam | se o governo bloquear todo ano, o efeito se repete, mas a lei não obriga |
| O tamanho resolve o buraco? | **Não.** Cobre de 10% a 13% do ajuste que a IFI diz faltar; o que fica para sempre (o benefício cortado) cobre {br(var['V5']['pct_do_necessario'])}% | o buraco é o da IFI; o governo prevê superávit |
| O diesel fora da meta é gasto a menos? | **Não.** É gasto igual, que sai da conta da meta de 2026 e libera {br(a26['diesel_sobre_contingenciamento_pct'])}% do bloqueio que faltava | o valor é o teto; o gasto efetivo pode ser menor |
| A oposição mudou o texto? | **Pouco.** Perdeu a Emenda 40 e os 2 destaques; ganhou a Lei Kandir mais suave e a saída do PIS e da Cofins da trava | a Câmara ainda pode mudar |

## 10. Variantes (o que muda se a leitura for outra)

""" + "\n".join(f"- **{x['id']}.** {x['leitura']}: {x['efeito']}." for x in r["variantes"]) + f"""

## 11. Arquivos

- números: `resultados/RESUMO.json`; validação: `resultados/VALIDACAO.json`; tabelas: `dados/derivados/`
- gráficos (1920×1080): `resultados/figuras/`
- leitura da IA: `docs/LEITURA_DA_IA.md`; revisão: `docs/REVISAO_ADVERSARIAL.md`; rodadas: `docs/RODADAS.md`
"""

    simples = f"""# Resumo simples: o ajuste do Lula corta gasto ou aumenta imposto?

**Rodada 2, 23/11/2026.** Fonte principal: o parecer do relator no Senado (Parecer nº 221/2026), com os números do próprio governo.

| Pergunta | Resposta |
|---|---|
| De cada R$ 100 do ajuste, quanto é corte de gasto? | **R$ {d['gasto_contido']}**, na tabela do governo, e é um bloqueio de um ano |
| E quanto é receita? | **R$ {d['receita_total']}**: até R$ {d['imposto_a_mais']} de benefício fiscal cortado (imposto a mais) e R$ {d['receita_antecipada']} de dinheiro das empresas que o governo recebe antes |
| E se 2027 correr como o orçamento do governo prevê? | o bloqueio não é acionado, e sobra só o benefício cortado: R$ {br(var['V2']['total'])} bilhões, 100% receita |
| De quanto é o ajuste? | de R$ {br(mn['total'])} a R$ {br(mx['total'])} bilhões em 2027 ({faixa(b['ajuste_pct_pib'], 2)} do PIB) |
| Resolve o buraco? | não: cobre de 10% a 13% do ajuste que a IFI do Senado diz faltar (cerca de R$ 440 bilhões) para a dívida parar de subir |
| E o diesel? | até R$ {br(a26['diesel_fora_da_meta_rs_bi'])} bilhões gastos em 2026 saem da conta da meta; o gasto acontece igual |
| A oposição conseguiu mudar? | pouco: a emenda do PL, que pedia teto de 0,6% para o gasto e tirava a trava dos créditos, perdeu por {placar('senado-votacao-emenda-40')} |
| E a Câmara? | marcou sessão para 23/11, às 18h; até a coleta, {nvot} registrada |

**O limite:** os valores por medida são estimativas do governo e não foram refeitos depois das mudanças do Senado. O relator fala agora em R$ {br(dep['relator_rs_bi'],0)} bilhões, sem a nova divisão.
"""

    leitura = f"""# Leitura da IA (rodada 2)

A conta foi feita com o auxílio do Claude (IA), a partir das fontes primárias; a leitura editorial é do autor do projeto.

1. **No cenário do próprio governo, o ajuste é mais receita do que corte de despesa direta.** R$ {d['receita_total']} de cada R$ 100 vêm de receita. A Folhapress escreveu *"dois terços"*, o DIAP somou R$ {br(mn['receita_total'])} a {br(mx['receita_total'])} bilhões, e o relator na Câmara classificou as medidas do mesmo jeito.
2. **A palavra "imposto" precisa de cuidado.** No máximo R$ {d['imposto_a_mais']} de cada R$ 100 são tributo a mais de forma permanente (o corte de benefícios e o Reidi). Os outros R$ {d['receita_antecipada']} são crédito das empresas retido: a empresa paga em dinheiro agora o que pagaria com crédito, e o crédito continua dela. É imposto adiantado, não imposto novo, e é o ponto que as 119 entidades do setor produtivo atacaram.
3. **O lado do gasto só existe se 2027 for pior que o centro da meta.** Pelo PLOA, não será, e então o pacote vira só o benefício fiscal cortado, R$ {br(var['V2']['total'])} bilhões. Pela IFI, será bem pior, e o bloqueio já seria obrigatório pela lei de hoje.
4. **O lado do gasto não é corte de regra.** É bloqueio de um ano, que pode voltar no ano seguinte como investimento fora do teto. As regras que fazem a Previdência, o salário mínimo e o BPC crescerem não mudam; o que muda são tetos para repasses a estados e municípios, cujo espaço vai para promessas.
5. **Sobre "cosmético":** é opinião de economista; o que o dado diz é que o pacote é pequeno perto do buraco medido pela IFI (de 10% a 13% do que falta) e que o que fica para sempre cobre {br(var['V5']['pct_do_necessario'])}%.
6. **O que não dá para dizer:** quanto de fato será bloqueado em 2027, qual é a divisão dos R$ {br(dep['relator_rs_bi'],0)} bilhões depois do Senado, quanto os R$ 15 bilhões do corte de benefícios valem depois das exceções, e se a Câmara muda o texto.
"""

    revisao = f"""# Revisão adversarial

## Rodada 1 (23/11): a revisão por um leitor que não fez as contas

Um agente que não escreveu os scripts leu o relatório da rodada 1 e as fontes, em três papéis (quem defende o governo, quem o critica, auditor de método). O que procedeu entrou na rodada 2; nenhuma objeção muda a conta da tabela do governo (31, 31 e 38 de cada R$ 100), mas três mudam o que ela significa.

| Objeção | Procede? | O que mudou na rodada 2 |
|---|---|---|
| O PLOA projeta 2027 acima do centro da meta, e aí o bloqueio e a trava dos créditos não são acionados | sim, a mais forte | o cenário virou o 2º item do topo e a §3; a V2 é o cenário do PLOA (R$ {br(var['V2']['total'])} bi, 100% receita) |
| O art. 12 devolve o bloqueio no ano seguinte, como investimento fora do teto | sim | dito na §1, na §4 e no veredito; a V5 mostra o que fica para sempre ({br(var['V5']['pct_do_necessario'])}% do que falta) |
| Benefício fiscal cortado é corte de gasto tributário, não imposto | em parte | o rótulo virou "benefício fiscal cortado (imposto a mais)"; a V4 mostra a outra leitura |
| A igualdade entre o bloqueio e a trava é suposição, não limite da lei (o teto soma o contingenciamento da LRF) | sim | a frase da §2 foi corrigida; o cenário da IFI fica não calculável |
| "Nenhuma regra das obrigatórias muda" é falso | sim | trocado por: as regras da Previdência, do salário mínimo e do BPC não mudam; há tetos para dois repasses e o art. 6º-D |
| Os R$ 15 bi do corte de benefícios provavelmente estão altos (exceções, noventena, repartição) | em parte | no topo; o 38 virou "no máximo" |
| O diesel libera o bloqueio que faltava em 2026 | em parte | a §6 diz: {br(a26['diesel_sobre_contingenciamento_pct'])}% dos R$ {br(a26['contingenciamento_rs_bi'])} bi |
| Os arts. 8º, 12 e 14 expandem gasto | sim | três linhas na §4 |
| O aumento das obrigatórias é nominal | em parte | a §5 mostra também o aumento acima da inflação (R$ {br(b['aumento_real_obrigatorias_2027_rs_bi'])} bi) e a queda como parte do PIB |
| Safras e PIB misturados; 104,7 no lugar de 104,8 | em parte | a distância usa o 104,8 da IFI; o −86,1 é do RAF 113; a cobertura aparece com os dois PIBs e com o juro de 6,1% |
| A Emenda 40 descrita como "menos imposto" | sim | a §7 descreve o que ela fazia, inclusive o que ficava |
| A Emenda 83 "protege os créditos de PIS e Cofins" | sim | restrito à compensação com a CBS |
| "A Câmara começou a votar" | sim | "marcou sessão" |
| "A Folha escreveu" | em parte | a fonte guardada é a Folhapress no Jornal do Comércio |
| As promessas "comem" o ajuste | em parte | "equivalem a", com a sobreposição dita |

Conferido e certo pelo revisor: os 6 placares, as datas, o partido do relator na Câmara, os 60 dias dos supersalários na redação final, a frase do Proex e a aritmética do `RESUMO.json`.
"""

    (RAIZ / "RELATORIO.md").write_text(relatorio, encoding="utf-8")
    (RAIZ / "RESUMO_SIMPLES.md").write_text(simples, encoding="utf-8")
    (RAIZ / "docs").mkdir(exist_ok=True)
    (RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura, encoding="utf-8")
    (RAIZ / "docs" / "REVISAO_ADVERSARIAL.md").write_text(revisao, encoding="utf-8")
    print("relatório escrito")


if __name__ == "__main__":
    main()
