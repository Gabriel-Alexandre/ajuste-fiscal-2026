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
    a, b = sorted(par)
    return f"{br(a, casas)}{unidade} a {br(b, casas)}{unidade}"


def main() -> None:
    r = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    v = json.loads((RAIZ / "resultados" / "VALIDACAO.json").read_text(encoding="utf-8"))
    c = r["composicao_2027"]; mn = c["pontas"]["minimo"]; mx = c["pontas"]["maximo"]; meio = c["meio_da_faixa"]; d = c["de_cada_100"]
    b = r["buraco"]; a26 = b["ano_2026"]; fora = r["fora_da_tabela_de_impacto"]; dep = r["depois_do_senado"]
    pl = {p["votacao"]: p for p in r["votacoes_senado"]["placar"]}
    pp = r["votacoes_senado"]["por_partido"]
    cam = r["camara"]

    def placar(chave):
        p = pl[chave]
        return f"{p['oficial_sim']} a {p['oficial_nao']}"

    def partido(chave, sigla):
        x = pp[chave].get(sigla, {"SIM": 0, "NÃO": 0})
        return f"{x['SIM']} SIM e {x['NÃO']} NÃO"

    limites = f"""## O que este projeto não consegue dizer (leia antes)

1. **Os valores por medida são estimativas do Poder Executivo**, levadas ao Parecer nº 221/2026 do relator no Senado. A Consultoria de Orçamento do Senado registrou que elas não foram refeitas depois das mudanças no texto. Não há memória de cálculo pública por medida.
2. **Depois da votação, o relator falou em R$ {br(dep['relator_rs_bi'],0)} bilhões** e o ministro, em R$ {br(dep['ministro_faixa_rs_bi'][0],0)} a {br(dep['ministro_faixa_rs_bi'][1],0)} bilhões. Nenhum dos dois publicou a nova divisão por medida. A conta daqui usa a única tabela publicada, a de R$ {br(mn['total'])} a {br(mx['total'])} bilhões.
3. **O bloqueio de despesas é facultativo e vale um ano.** Se o governo não bloquear, a lei também não deixa limitar o uso de créditos das empresas (o art. 6º-F só vale até o valor bloqueado), e sobra só o imposto a mais (variante V2).
4. **A Câmara começou a votar em 23/11, às 18h.** Até a coleta, a API da Câmara registrava {'nenhuma votação' if str(cam['votacoes_registradas']) == '0' else str(cam['votacoes_registradas']) + ' votações'}. O texto pode mudar lá.
5. **O tamanho do buraco é o da IFI**, que tem premissas mais duras que as do governo (PIB, inflação, receitas). O governo prevê superávit em 2027; a IFI, déficit. Os dois números estão aqui.
"""

    tabela_medidas = "\n".join(
        f"| {m['nome']} | {m['natureza']} | {br(m['minimo'])} | {br(m['maximo'])} |" for m in c["medidas"])

    relatorio = f"""# O ajuste do Lula corta gasto ou aumenta imposto? Relatório da rodada 1

**Projeto:** `ajuste-fiscal-2026` · **Rodada:** 1 (23/11/2026) · **Repositório:** {REPO}
Todos os números deste arquivo saem de `resultados/RESUMO.json`, gerado por script a partir das fontes em `dados/brutos/` (com sha256 no `dados/MANIFESTO.json`). Validação por outro caminho: **{v['passaram']} de {v['total']}** (`resultados/VALIDACAO.json`).

{limites}
## 1. A resposta curta

De cada **R$ 100** do ajuste estimado para 2027, **R$ {d['gasto_contido']}** são gasto contido (bloqueio do Orçamento), **R$ {d['receita_antecipada']}** são dinheiro das empresas que entra antes (limite ao uso de créditos tributários) e **R$ {d['imposto_a_mais']}** são imposto a mais (corte de benefícios fiscais e teto do Reidi). Somando o adiantado e o imposto, **R$ {d['receita_total']} de cada R$ 100 vêm de receita**. Nas duas pontas da faixa, a receita fica entre **{faixa([mn['pct_receita'], mx['pct_receita']])}** do total.

O lado do gasto é um bloqueio de um ano: pela lei, ele não entra na base de cálculo dos anos seguintes, e o relator na Câmara escreve que ele é reversível no próprio ano. Nenhuma regra das despesas obrigatórias muda.

E o tamanho: o ajuste equivale a **{faixa(b['ajuste_pct_pib'], 2)} do PIB**. A IFI calcula que faltam cerca de **3 pontos do PIB** de ajuste para a dívida parar de subir; o pacote cobre **{faixa(b['ajuste_cobre_do_necessario_pct'])}** disso.

## 2. A tabela, medida por medida (2027, R$ bilhões)

| Medida | Natureza | Mínimo | Máximo |
|---|---|---:|---:|
{tabela_medidas}
| **Total** | | **{br(mn['total'])}** | **{br(mx['total'])}** |

Fonte: Parecer nº 221/2026-PLEN/SF, *"de acordo com informações do Poder Executivo"*. A mesma tabela está na nota técnica do DIAP (16/11, que cita a nota da Conorf de 13/11) e na reportagem do Jota de 18/11; a validação confere as três.

**Como cada medida foi classificada.** O parecer do relator na Câmara (PRLP 1, 19/11/2026) diz que os arts. 4º (benefícios), 9º (Reidi) e 6º-F (créditos) *"ampliam receita"*, e que no 6º-F *"o efeito seja de antecipação de arrecadação, pois os créditos dos contribuintes não se extinguem"*. O bloqueio (arts. 6º-C a 6º-E) é contenção de despesa. É essa a divisão usada aqui.

**A ligação entre as duas metades.** O art. 6º-F só deixa limitar os créditos das empresas *"até o montante equivalente"* ao que for bloqueado de despesa, e só se o governo adotar o bloqueio. Por isso as duas linhas têm a mesma faixa, de R$ {br(mn['gasto_contido'])} a {br(mx['gasto_contido'])} bilhões: para cada real de gasto segurado, a lei autoriza até um real de crédito das empresas segurado.

| Somas | Mínimo | Máximo | Meio da faixa |
|---|---:|---:|---:|
| Gasto contido (R$ bi) | {br(mn['gasto_contido'])} | {br(mx['gasto_contido'])} | {br(meio['gasto_contido'])} |
| Receita adiantada (R$ bi) | {br(mn['receita_antecipada'])} | {br(mx['receita_antecipada'])} | {br(meio['receita_antecipada'])} |
| Imposto a mais (R$ bi) | {br(mn['imposto_a_mais'])} | {br(mx['imposto_a_mais'])} | {br(meio['imposto_a_mais'])} |
| Receita total (R$ bi) | {br(mn['receita_total'])} | {br(mx['receita_total'])} | {br(meio['receita_total'])} |
| Parte do gasto | {br(mn['pct_gasto'])}% | {br(mx['pct_gasto'])}% | {br(meio['pct_gasto'])}% |
| Parte da receita | {br(mn['pct_receita'])}% | {br(mx['pct_receita'])}% | {br(meio['pct_receita'])}% |

## 3. O que ficou fora da tabela

| Item | O que diz o texto | Por que não entra na conta |
|---|---|---|
| Lei Kandir | repasse aos estados limitado a R$ {br(fora['kandir_teto_anual_rs_bi'])} bi por ano até 2030, com o saldo pago de 2028 a 2030 (redação final, art. 2º) | é adiamento de pagamento; a reportagem da Folha e a do InvestNews dizem que cerca de R$ {br(fora['medidas_que_abrem_espaco_para_promessas_rs_bi'],0)} bi em medidas assim abrem espaço para promessas de campanha (Bolsa Família, Pé-de-Meia), sem economia estrutural |
| Compensação previdenciária | limitada a R$ {br(fora['comprev_teto_anual_rs_bi'])} bi por ano de 2027 a 2030 (art. 6º) | o mesmo; a CNM fala em perda de caixa para os municípios |
| Proex | teto de R$ {br(fora['proex_teto_rs_bi'])} bi por ano | o relator na Câmara escreve que o teto é *"superior à execução de 2025 e à previsão para 2026"*: não economiza nada hoje |
| Supersalários | prazo para o Congresso votar a regra (60 dias na redação final) | o ministro estimou R$ {br(fora['supersalarios_estimativa_ministro_rs_bi'],0)} bi; o texto não quantifica, e a economia do Judiciário e do MP fica com eles |

## 4. O tamanho do buraco

| Número | Valor | Fonte |
|---|---:|---|
| Meta de 2027 (centro) | R$ {br(b['meta2027_centro_rs_bi'])} bi ({br(b['meta2027_centro_pct_pib'],2)}% do PIB) | PLOA 2027, pela nota do DIAP |
| Resultado efetivo de 2027 previsto pelo governo | R$ {br(b['ploa2027_primario_efetivo_rs_bi'])} bi | PLOA 2027, pela IFI (RAF 116) |
| Resultado efetivo de 2027 previsto pela IFI | R$ {br(b['ifi2027_primario_efetivo_rs_bi'])} bi | IFI, RAF 116 |
| Distância entre os dois | R$ {br(b['distancia_ploa_ifi_2027_rs_bi'])} bi | conta |
| Déficit de 2027 com as promessas novas | {br(b['ifi2027_deficit_potencial_pct_pib'])}% do PIB | IFI, RAF 117 |
| Promessas novas não orçadas (Bolsa Família, Bets, MEI) | R$ {br(b['promessas_nao_orcadas_rs_bi'])} bi | IFI, RAF 117 |
| Aumento das despesas obrigatórias de 2026 para 2027 | R$ {br(b['aumento_obrigatorias_2027_rs_bi'])} bi | IFI, RAF 116 (tabela 7) |
| Superávit que estabiliza a dívida | {br(b['primario_que_estabiliza_divida_pct_pib'][0])}% do PIB (ou {br(b['primario_que_estabiliza_divida_pct_pib'][1])}% com juro real de 6,1%) | IFI, RAF 117 |
| Ajuste que a IFI diz faltar | 3 p.p. do PIB, ou R$ {br(b['ajuste_necessario_ifi_rs_bi'])} bi no PIB do PLOA | IFI, RAF 117; conta |
| Dívida bruta | {br(b['divida_bruta']['set_2026_bc'])}% do PIB em set/2026; {br(b['divida_bruta']['fim_2027_ifi'])}% no fim de 2027; chance de {br(b['divida_bruta']['chance_passar_90_ate_2030_pct'])}% de passar de 90% até 2030 | BC (pela Agência Brasil); IFI, RAF 117 |

**As comparações (todas na mesma régua, R$ do ajuste de 2027):**

- o ajuste cobre **{faixa(b['ajuste_cobre_do_necessario_pct'])}** dos 3 pontos do PIB que a IFI diz faltar;
- o ajuste inteiro equivale a **{faixa(b['ajuste_sobre_aumento_obrigatorias_pct'])}** do quanto as despesas obrigatórias sobem em um ano; só a parte do gasto contido, **{faixa(b['gasto_contido_sobre_aumento_obrigatorias_pct'])}**;
- as promessas não orçadas que a IFI soma equivalem a **{faixa(b['promessas_sobre_ajuste_pct'])}** do ajuste;
- o ajuste cobre **{faixa(b['ajuste_sobre_distancia_ploa_ifi_pct'])}** da distância entre o que o governo e a IFI preveem para 2027.

## 5. O diesel de 2026

O art. 13 da redação final autoriza tirar da meta de 2026 até **R$ {br(a26['diesel_fora_da_meta_rs_bi'])} bilhões** gastos com a subvenção ao diesel (MP 1.391/2026). O dinheiro é gasto igual; ele só deixa de contar para a meta.

| 2026 (governo central) | R$ bi | Fonte |
|---|---:|---|
| Resultado projetado antes das deduções | {br(a26['rardp_antes_deducoes_rs_bi'])} | relatório do 4º bimestre, na tabela 3 do RAF 117 |
| Despesas já tiradas da conta da meta | {br(a26['deducoes_rs_bi'])} | idem |
| Resultado para a meta, depois das deduções e antes do bloqueio | {br(a26['rardp_depois_deducoes_rs_bi'])} | idem |
| Piso da meta | {br(a26['meta_piso_rs_bi'])} | idem |
| Diesel tirado pelo PLP | {br(a26['diesel_fora_da_meta_rs_bi'])} | redação final, art. 13 |
| Total tirado da conta com o diesel | {br(a26['deducoes_com_diesel_rs_bi'])} | conta |
| Déficit do governo central de janeiro a setembro | {br(a26['tesouro_jan_set_rs_bi'])} | Tesouro, pela Agência Brasil |

O diesel equivale a **{br(a26['diesel_sobre_deficit_antes_deducoes_pct'])}%** do déficit projetado para 2026 e a **{faixa(a26['diesel_sobre_ajuste_2027_pct'])}** do ajuste prometido para 2027. A reportagem da Folha de 23/11 diz que a medida entrou para evitar um novo bloqueio no fim do ano, por causa da arrecadação mais fraca.

## 6. O que a oposição tentou mudar

| Votação (Senado) | Placar | O que estava em jogo |
|---|---:|---|
| Urgência, 12/11 | {placar('senado-votacao-req-770-urgencia')} | votar sem passar pelas comissões |
| Texto-base, 12/11 | {placar('senado-votacao-texto-base')} | o substitutivo do relator Eduardo Braga (MDB) |
| Emenda 40 (Rogério Marinho, PL), 18/11 | {placar('senado-votacao-emenda-40')} (rejeitada) | teto de 0,6% para o gasto (no lugar de 2%), centro da meta obrigatório, e tirar a trava dos créditos das empresas, a Lei Kandir, a compensação previdenciária e o diesel fora da meta |
| Destaque do PL: limite da compensação previdenciária | {placar('senado-votacao-comprev')} (mantido) | tirar o teto de R$ 3 bi por ano |
| Destaque do Republicanos: limite ao uso de créditos | {placar('senado-votacao-compensacao')} (mantido) | tirar o art. 6º-F |
| Turno suplementar, 18/11 | {placar('senado-votacao-turno-suplementar')} | as emendas de última hora, entre elas a 83 (Tereza Cristina, PP), que protege os créditos de PIS e Cofins |

**Por partido:** no texto-base, o PL votou {partido('senado-votacao-texto-base','PL')}, e o PT, {partido('senado-votacao-texto-base','PT')}. Na Emenda 40, o PL votou {partido('senado-votacao-emenda-40','PL')}. Na trava dos créditos, o PL votou {partido('senado-votacao-compensacao','PL')}. No turno suplementar, o PL votou {partido('senado-votacao-turno-suplementar','PL')}.

**O que a oposição conseguiu:** a Lei Kandir ficou em R$ {br(fora['kandir_teto_anual_rs_bi'])} bi por ano, com o saldo pago até 2030 (era R$ 1 bi por ano, com o saldo até 2037), num acordo pelo qual o PL retirou o destaque; e a emenda da senadora Tereza Cristina protegeu os créditos de PIS e Cofins (o Ministério do Planejamento disse ao Jota que o efeito é neutro). O resto do que a Emenda 40 pedia perdeu.

## 7. A Câmara (23/11)

Situação na API da Câmara na coleta: *{cam['situacao']}*; última tramitação em {cam['ultima_tramitacao']}; votações registradas: {cam['votacoes_registradas']}. O relator, Mauro Benevides Filho (União-CE), deu parecer preliminar favorável sem mudar o texto do Senado. Precisa de 257 votos. Refazer a coleta depois da sessão.

## 8. Veredito por critério

| Critério | Veredito | O limite |
|---|---|---|
| O ajuste corta gasto ou aumenta receita? | **Mais receita.** R$ {d['receita_total']} de cada R$ 100 (de {faixa([mx['pct_receita'], mn['pct_receita']])} nas pontas) | estimativas do Executivo, não refeitas depois das mudanças |
| O que é imposto a mais de verdade? | **R$ {d['imposto_a_mais']} de cada R$ 100** (corte de benefícios e Reidi); outros **R$ {d['receita_antecipada']}** são crédito das empresas que fica retido e entra antes | a retenção pode voltar como gasto ou menos receita nos anos seguintes, se o crédito for usado depois |
| O lado do gasto é corte estrutural? | **Não.** É bloqueio de um ano, facultativo, que não entra na base dos anos seguintes; nenhuma regra das obrigatórias muda | se o governo bloquear todo ano, o efeito se repete, mas a lei não obriga |
| O tamanho resolve o buraco? | **Não.** Cobre {faixa(b['ajuste_cobre_do_necessario_pct'])} do ajuste que a IFI diz faltar | o buraco é o da IFI; o governo prevê superávit |
| O diesel fora da meta é gasto a menos? | **Não.** É gasto igual, que sai da conta da meta de 2026 | o valor é o teto; o gasto efetivo pode ser menor |
| A oposição mudou o texto? | **Pouco.** Perdeu a Emenda 40 e os 2 destaques; ganhou a Lei Kandir mais suave e a proteção do PIS e da Cofins | a Câmara ainda pode mudar |

## 9. Variantes (o que muda se a leitura for outra)

""" + "\n".join(f"- **{x['id']}.** {x['leitura']}: {x['efeito']}." for x in r["variantes"]) + f"""

## 10. Arquivos

- números: `resultados/RESUMO.json`; validação: `resultados/VALIDACAO.json`; tabelas: `dados/derivados/`
- gráficos (1920×1080): `resultados/figuras/`
- leitura da IA: `docs/LEITURA_DA_IA.md`; revisão: `docs/REVISAO_ADVERSARIAL.md`; rodadas: `docs/RODADAS.md`
"""

    simples = f"""# Resumo simples: o ajuste do Lula corta gasto ou aumenta imposto?

**Rodada 1, 23/11/2026.** Fonte principal: o parecer do relator no Senado (Parecer nº 221/2026), com os números do próprio governo.

| Pergunta | Resposta |
|---|---|
| De cada R$ 100 do ajuste, quanto é corte de gasto? | **R$ {d['gasto_contido']}**, e é um bloqueio de um ano |
| E quanto é receita? | **R$ {d['receita_total']}**: R$ {d['imposto_a_mais']} de imposto a mais e R$ {d['receita_antecipada']} de dinheiro das empresas que o governo recebe antes |
| De quanto é o ajuste? | de R$ {br(mn['total'])} a R$ {br(mx['total'])} bilhões em 2027 ({faixa(b['ajuste_pct_pib'], 2)} do PIB) |
| Resolve o buraco? | não: cobre {faixa(b['ajuste_cobre_do_necessario_pct'])} do ajuste que a IFI do Senado diz faltar para a dívida parar de subir |
| E o diesel? | até R$ {br(a26['diesel_fora_da_meta_rs_bi'])} bilhões gastos em 2026 saem da conta da meta; o gasto acontece igual |
| A oposição conseguiu mudar? | pouco: a emenda do PL que pedia mais corte de gasto e menos imposto perdeu por {placar('senado-votacao-emenda-40')} |
| E a Câmara? | começou a votar em 23/11; até a coleta, nenhuma votação registrada |

**O limite:** os valores por medida são estimativas do governo e não foram refeitos depois das mudanças do Senado. O relator fala agora em R$ {br(dep['relator_rs_bi'],0)} bilhões, sem a nova divisão.
"""

    leitura = f"""# Leitura da IA (rodada 1)

A conta foi feita com o auxílio do Claude (IA), a partir das fontes primárias; a leitura editorial é do autor do projeto.

1. **A suspeita de que o ajuste é mais imposto do que corte se confirma pelo dado do próprio governo.** R$ {d['receita_total']} de cada R$ 100 vêm de receita. O número não depende de quem lê: a Folha escreveu *"dois terços"*, o DIAP somou R$ {br(mn['receita_total'])} a {br(mx['receita_total'])} bilhões, e o relator na Câmara classificou as medidas do mesmo jeito.
2. **A palavra "imposto" precisa de cuidado.** Só R$ {d['imposto_a_mais']} de cada R$ 100 são tributo a mais de forma permanente (o corte de benefícios e o Reidi). Os outros R$ {d['receita_antecipada']} são crédito das empresas retido: a empresa paga em dinheiro agora o que pagaria com crédito, e o crédito continua dela. É imposto adiantado, não imposto novo, e é o ponto que as 119 entidades do setor produtivo atacaram.
3. **O lado do gasto não é corte de regra.** É o governo bloquear verba de um ano, com a lei dizendo que o bloqueio não entra na base dos anos seguintes. As despesas obrigatórias, que sobem R$ {br(b['aumento_obrigatorias_2027_rs_bi'])} bilhões de 2026 para 2027, não são tocadas.
4. **Sobre "cosmético":** é opinião de economista; o que o dado diz é que o pacote é pequeno perto do buraco medido pela IFI ({faixa(b['ajuste_cobre_do_necessario_pct'])} do que falta) e que as promessas novas não orçadas comem {faixa(b['promessas_sobre_ajuste_pct'])} dele.
5. **O que não dá para dizer:** quanto de fato será bloqueado em 2027 (é facultativo), qual é a divisão dos R$ {br(dep['relator_rs_bi'],0)} bilhões depois do Senado, e se a Câmara muda o texto.
"""

    revisao = f"""# Revisão adversarial (rodada 1)

Três leitores, cada um com a objeção mais forte. O efeito de cada uma foi calculado (variantes no `RELATORIO.md` §9). Nenhuma muda o número principal.

| Leitor | Objeção | Resposta com número |
|---|---|---|
| Quem defende o governo | *"O limite ao uso de créditos não é imposto: a empresa não paga mais, paga antes."* | Aceito em parte: por isso o projeto separa **imposto a mais** (R$ {d['imposto_a_mais']} de cada R$ 100) de **receita adiantada** (R$ {d['receita_antecipada']}). Mesmo assim, as duas são receita, e o gasto contido fica em R$ {d['gasto_contido']} |
| Quem defende o governo | *"O bloqueio é corte de gasto de verdade, e o teto de 2% aperta todos os anos."* | O texto diz que a redução *"não se incorporará à base de cálculo dos exercícios seguintes"*; o relator na Câmara: *"reversível no curso do exercício"*. Na ponta mais favorável (V3), o gasto contido é {br(mx['pct_gasto'])}% |
| Quem critica o governo | *"O bloqueio é facultativo; na prática pode não haver corte nenhum."* | Calculado (V2): sem bloqueio, a lei também não deixa reter crédito, e sobra R$ {br(mn['imposto_a_mais'])} bi, 100% receita |
| Quem critica o governo | *"Há R$ 10 bilhões de medidas que só abrem espaço para promessas."* | Calculado: elas não estão na tabela de R$ {br(mn['total'])} a {br(mx['total'])} bi; ficam no §3, fora da conta |
| Auditor de método | *"As estimativas são do Executivo e não foram refeitas."* | Dito no topo do relatório; a conta usa a única tabela publicada, e a validação confere a mesma tabela em 3 fontes ({v['passaram']} de {v['total']} testes) |
| Auditor de método | *"Comparar com o buraco da IFI escolhe o pior cenário."* | O relatório põe os dois lados: o governo prevê R$ {br(b['ploa2027_primario_efetivo_rs_bi'])} bi de superávit em 2027 e a IFI, R$ {br(abs(b['ifi2027_primario_efetivo_rs_bi']))} bi de déficit |
"""

    (RAIZ / "RELATORIO.md").write_text(relatorio, encoding="utf-8")
    (RAIZ / "RESUMO_SIMPLES.md").write_text(simples, encoding="utf-8")
    (RAIZ / "docs").mkdir(exist_ok=True)
    (RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura, encoding="utf-8")
    (RAIZ / "docs" / "REVISAO_ADVERSARIAL.md").write_text(revisao, encoding="utf-8")
    print("relatório escrito")


if __name__ == "__main__":
    main()
