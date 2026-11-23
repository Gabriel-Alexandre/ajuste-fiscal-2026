"""A conta do projeto: quanto do ajuste é gasto contido e quanto é receita, e o tamanho do buraco.

Lê só dados/derivados/*.csv (que saem de derivar.py) e grava resultados/RESUMO.json.
Uso:  python ferramentas/analise.py
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DER = RAIZ / "dados" / "derivados"
RES = RAIZ / "resultados"


def tabela(nome: str) -> list[dict]:
    with open(DER / nome, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def valores(nome: str) -> dict[str, float]:
    return {l["chave"]: float(l["valor"]) for l in tabela(nome)}


def r1(x: float) -> float:
    return round(x + 0.0, 1)


def composicao(medidas: list[dict]) -> dict:
    """Soma por natureza, nas pontas mínima e máxima e no meio da faixa."""
    itens = [m for m in medidas if m["medida"] != "total_declarado"]
    total_decl = next(m for m in medidas if m["medida"] == "total_declarado")
    saida = {"pontas": {}}
    for ponta in ("minimo", "maximo"):
        por = Counter()
        for m in itens:
            por[m["natureza"]] += float(m[ponta])
        total = sum(por.values())
        assert abs(total - float(total_decl[ponta])) < 0.05, f"a soma das medidas ({total}) não bate com o total do parecer ({total_decl[ponta]})"
        receita = por["receita antecipada"] + por["imposto a mais"]
        saida["pontas"][ponta] = {
            "total": r1(total),
            "gasto_contido": r1(por["gasto contido"]),
            "receita_antecipada": r1(por["receita antecipada"]),
            "imposto_a_mais": r1(por["imposto a mais"]),
            "receita_total": r1(receita),
            "pct_gasto": r1(100 * por["gasto contido"] / total),
            "pct_receita": r1(100 * receita / total),
            "pct_receita_antecipada": r1(100 * por["receita antecipada"] / total),
            "pct_imposto_a_mais": r1(100 * por["imposto a mais"] / total),
        }
    mn, mx = saida["pontas"]["minimo"], saida["pontas"]["maximo"]
    meio = {k: r1((mn[k] + mx[k]) / 2) for k in ("total", "gasto_contido", "receita_antecipada", "imposto_a_mais", "receita_total")}
    meio["pct_gasto"] = r1(100 * meio["gasto_contido"] / meio["total"])
    meio["pct_receita"] = r1(100 * meio["receita_total"] / meio["total"])
    meio["pct_receita_antecipada"] = r1(100 * meio["receita_antecipada"] / meio["total"])
    meio["pct_imposto_a_mais"] = r1(100 * meio["imposto_a_mais"] / meio["total"])
    saida["meio_da_faixa"] = meio
    # "de cada R$ 100" arredondado para somar 100
    g = round(meio["pct_gasto"]); a = round(meio["pct_receita_antecipada"]); i = 100 - g - a
    saida["de_cada_100"] = {"gasto_contido": g, "receita_antecipada": a, "imposto_a_mais": i,
                            "receita_total": a + i}
    saida["medidas"] = [{k: m[k] for k in ("medida", "nome", "natureza", "minimo", "maximo", "fonte")} for m in itens]
    return saida


def variantes(comp: dict, b: dict) -> list[dict]:
    """As leituras alternativas que a revisão adversarial pediu, cada uma com o número."""
    mn, mx = comp["pontas"]["minimo"], comp["pontas"]["maximo"]; d = comp["de_cada_100"]
    imposto = mn["imposto_a_mais"]
    pib = b["pib2027_ploa"]; nec = b["ajuste_necessario_pp_pib"] / 100 * pib
    f = lambda x, c=1: f"{x:.{c}f}".replace(".", ",")
    return [
        {"id": "V2", "leitura": "2027 corre como o PLOA projeta: o resultado para a meta fica acima do centro, então o bloqueio do art. 6º-C não é acionado e a trava dos créditos (art. 6º-F) também não",
         "total": imposto, "pct_receita": 100.0, "pct_pib": round(100 * imposto / pib, 2), "pct_do_necessario": r1(100 * imposto / nec),
         "efeito": f"sobra só o benefício fiscal cortado, R$ {f(imposto)} bilhões ({f(100 * imposto / pib, 2)}% do PIB), e 100% do ajuste é receita"},
        {"id": "V4", "leitura": "benefício fiscal cortado conta como corte de gasto tributário (o nome técnico do benefício é gasto tributário)",
         "gasto_direto_mais_tributario": d["gasto_contido"] + d["imposto_a_mais"], "receita_antecipada": d["receita_antecipada"],
         "efeito": f"de cada R$ 100, R$ {d['gasto_contido'] + d['imposto_a_mais']} viram corte (R$ {d['gasto_contido']} de despesa e R$ {d['imposto_a_mais']} de benefício) e R$ {d['receita_antecipada']} ficam como receita adiantada; para quem paga, o benefício cortado continua sendo tributo a mais"},
        {"id": "V5", "leitura": "só conta o que fica: o bloqueio pode voltar no ano seguinte como investimento fora do teto (art. 12) e o crédito retido continua da empresa",
         "total": imposto, "pct_pib": round(100 * imposto / pib, 2), "pct_do_necessario": r1(100 * imposto / nec),
         "efeito": f"o que fica para sempre é o benefício fiscal cortado, R$ {f(imposto)} bilhões, {f(100 * imposto / nec)}% do ajuste que a IFI diz faltar"},
    ]


def cenarios(comp: dict, b: dict) -> list[dict]:
    """Quando cada parte do ajuste é acionada, pela própria regra do texto."""
    d = comp["de_cada_100"]; imposto = comp["pontas"]["minimo"]["imposto_a_mais"]
    return [
        {"id": "executivo", "nome": "a tabela do governo (o bloqueio é acionado)",
         "condicao": "o resultado de 2027 fica abaixo do centro da meta",
         "de_cada_100": [d["gasto_contido"], d["receita_antecipada"], d["imposto_a_mais"]],
         "total_rs_bi": [comp["pontas"]["minimo"]["total"], comp["pontas"]["maximo"]["total"]]},
        {"id": "ploa", "nome": "2027 como o PLOA projeta",
         "condicao": f"resultado para a meta de R$ {b['ploa2027_resultado_para_meta']} bi, acima do centro de R$ {b['meta2027_centro_raf116']} bi: o art. 6º-C não se aplica",
         "de_cada_100": [0, 0, 100], "total_rs_bi": [imposto, imposto]},
        {"id": "ifi", "nome": "2027 como a IFI projeta",
         "condicao": f"resultado para a meta de R$ {b['ifi2027_resultado_para_meta']:.1f} bi, abaixo do piso de R$ {b['meta2027_piso']:.1f} bi: o bloqueio de R$ {b['ifi2027_contingenciamento_necessario']:.1f} bi da Lei de Responsabilidade Fiscal já é obrigatório, e o teto da trava dos créditos soma esse bloqueio",
         "de_cada_100": None, "total_rs_bi": None,
         "nota": "a divisão não é calculável com o que foi publicado; a parte de receita adiantada pode passar dos R$ 18,3 bi da tabela"},
    ]


def buraco(comp: dict, b: dict, outras: dict, depois: dict) -> dict:
    mn, mx = comp["pontas"]["minimo"]["total"], comp["pontas"]["maximo"]["total"]
    gmn, gmx = comp["pontas"]["minimo"]["gasto_contido"], comp["pontas"]["maximo"]["gasto_contido"]
    pib = b["pib2027_ploa"]
    ajuste_nec = b["ajuste_necessario_pp_pib"] / 100 * pib
    aumento_obrig = r1(b["obrigatorias_2027"] - b["obrigatorias_2026"])
    aumento_real = r1(b["obrigatorias_2027"] - b["obrigatorias_2026"] * (1 + b["ipca2027_ploa"] / 100))
    gap_ploa_ifi = b["distancia_ploa_ifi_declarada"]  # a IFI soma os números sem arredondar
    nec_ifi_pib = b["ajuste_necessario_pp_pib"] / 100 * b["pib2027_ifi"]
    # mesma lógica da IFI (déficit potencial + primário que estabiliza), com o juro real de 6,1%
    nec_juro61_pp = b["ifi2027_deficit_potencial_pib"] + b["primario_que_estabiliza_pib_juro61"]
    nec_juro61 = nec_juro61_pp / 100 * pib
    diesel = outras["diesel_fora_da_meta_2026"]
    return {
        "ajuste_pct_pib": [round(100 * mn / pib, 2), round(100 * mx / pib, 2)],
        "ajuste_necessario_ifi_rs_bi": r1(ajuste_nec),
        "ajuste_cobre_do_necessario_pct": [r1(100 * mn / ajuste_nec), r1(100 * mx / ajuste_nec)],
        "ajuste_necessario_ifi_pib_ifi_rs_bi": r1(nec_ifi_pib),
        "ajuste_cobre_do_necessario_pib_ifi_pct": [r1(100 * mn / nec_ifi_pib), r1(100 * mx / nec_ifi_pib)],
        "ajuste_necessario_juro61_pp_pib": r1(nec_juro61_pp),
        "ajuste_cobre_do_necessario_juro61_pct": [r1(100 * mn / nec_juro61), r1(100 * mx / nec_juro61)],
        "aumento_obrigatorias_2027_rs_bi": aumento_obrig,
        "ajuste_sobre_aumento_obrigatorias_pct": [r1(100 * mn / aumento_obrig), r1(100 * mx / aumento_obrig)],
        "gasto_contido_sobre_aumento_obrigatorias_pct": [r1(100 * gmn / aumento_obrig), r1(100 * gmx / aumento_obrig)],
        "aumento_real_obrigatorias_2027_rs_bi": aumento_real,
        "obrigatorias_pct_pib": [b["obrigatorias_2026_pib"], b["obrigatorias_2027_pib"]],
        "ajuste_sobre_aumento_real_obrigatorias_pct": [r1(100 * mn / aumento_real), r1(100 * mx / aumento_real)],
        "gasto_contido_sobre_aumento_real_obrigatorias_pct": [r1(100 * gmn / aumento_real), r1(100 * gmx / aumento_real)],
        "promessas_nao_orcadas_rs_bi": b["promessas_nao_orcadas"],
        "promessas_sobre_ajuste_pct": [r1(100 * b["promessas_nao_orcadas"] / mx), r1(100 * b["promessas_nao_orcadas"] / mn)],
        "distancia_ploa_ifi_2027_rs_bi": gap_ploa_ifi,
        "ajuste_sobre_distancia_ploa_ifi_pct": [r1(100 * mn / gap_ploa_ifi), r1(100 * mx / gap_ploa_ifi)],
        "ifi_bloqueio_que_faltaria_2027_rs_bi": b["ifi2027_contingenciamento_necessario"],
        "meta2027_centro_rs_bi": b["meta2027_centro"],
        "meta2027_piso_rs_bi": b["meta2027_piso"],
        "ploa2027_resultado_para_meta_rs_bi": b["ploa2027_resultado_para_meta"],
        "ifi2027_resultado_para_meta_rs_bi": b["ifi2027_resultado_para_meta"],
        "meta2027_centro_pct_pib": round(100 * b["meta2027_centro"] / pib, 2),
        "ploa2027_primario_efetivo_rs_bi": b["ploa2027_primario_efetivo"],
        "ifi2027_primario_efetivo_rs_bi": b["ifi2027_primario_efetivo"],
        "ifi2026_deficit_pct_pib": b["ifi2026_deficit_pib"],
        "ifi2027_deficit_potencial_pct_pib": b["ifi2027_deficit_potencial_pib"],
        "primario_que_estabiliza_divida_pct_pib": [b["primario_que_estabiliza_pib"], b["primario_que_estabiliza_pib_juro61"]],
        "divida_bruta": {"set_2026_bc": depois["bc_divida_bruta_set_2026"], "fim_2027_ifi": b["divida2027_pib"],
                          "chance_passar_90_ate_2030_pct": b["prob_divida_90"]},
        "ano_2026": {
            "tesouro_jan_set_rs_bi": depois["tesouro_deficit_jan_set_2026"],
            "rardp_antes_deducoes_rs_bi": b["primario2026_antes_deducoes"],
            "deducoes_rs_bi": b["deducoes2026"],
            "rardp_depois_deducoes_rs_bi": b["primario2026_depois_deducoes"],
            "meta_piso_rs_bi": b["meta2026_piso"],
            "diesel_fora_da_meta_rs_bi": diesel,
            "diesel_sobre_deficit_antes_deducoes_pct": r1(100 * diesel / abs(b["primario2026_antes_deducoes"])),
            "contingenciamento_rs_bi": b["contingenciamento2026"],
            "diesel_sobre_contingenciamento_pct": r1(100 * diesel / b["contingenciamento2026"]),
            "deducoes_com_diesel_rs_bi": r1(b["deducoes2026"] + diesel),
            "diesel_sobre_ajuste_2027_pct": [r1(100 * diesel / mx), r1(100 * diesel / mn)],
        },
    }


def votacoes() -> dict:
    placar = tabela("votacoes_senado_placar.csv")
    nominal = tabela("votacoes_senado_nominal.csv")
    por_partido = {}
    for v in ("senado-votacao-texto-base", "senado-votacao-emenda-40", "senado-votacao-compensacao", "senado-votacao-turno-suplementar"):
        c = Counter((l["partido"], l["voto"]) for l in nominal if l["votacao"] == v)
        por_partido[v] = {p: {"SIM": c[(p, "SIM")], "NÃO": c[(p, "NÃO")]} for p in sorted({p for p, _ in c})}
    return {"placar": placar, "por_partido": por_partido}


def main() -> None:
    comp = composicao(tabela("medidas_2027.csv"))
    b = valores("buraco.csv")
    outras = valores("outras_medidas.csv")
    depois = {l["chave"]: float(l["valor"]) for l in tabela("depois_do_senado.csv")}
    camara = tabela("camara_situacao.csv")[0]
    depois_antes = next(float(l["antes"]) for l in tabela("depois_do_senado.csv") if l["chave"] == "estimativa_pos_senado_ministro")
    resumo = {
        "gerado_por": "ferramentas/analise.py",
        "composicao_2027": comp,
        "variantes": variantes(comp, b),
        "cenarios": cenarios(comp, b),
        "buraco": buraco(comp, b, outras, depois),
        "fora_da_tabela_de_impacto": {
            "kandir_teto_anual_rs_bi": outras["kandir_teto_anual"],
            "comprev_teto_anual_rs_bi": outras["comprev_teto_anual"],
            "comprev_2027_sem_teto_rs_bi": next(float(l["antes"]) for l in tabela("depois_do_senado.csv") if l["chave"] == "comprev_2027_com_teto"),
            "proex_teto_rs_bi": outras["proex_teto_acima_da_execucao"],
            "medidas_que_abrem_espaco_para_promessas_rs_bi": depois["medidas_que_acomodam_promessas"],
            "supersalarios_estimativa_ministro_rs_bi": outras["supersalarios_estimativa_ministro"],
        },
        "depois_do_senado": {"relator_rs_bi": depois["estimativa_pos_senado_relator"],
                              "ministro_faixa_rs_bi": [depois["estimativa_pos_senado_ministro"], depois_antes]},
        "votacoes_senado": votacoes(),
        "camara": camara,
    }
    RES.mkdir(exist_ok=True)
    (RES / "RESUMO.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    m = comp["meio_da_faixa"]; d = comp["de_cada_100"]
    print(f"meio da faixa: R$ {m['total']} bi; gasto {m['pct_gasto']}%, receita {m['pct_receita']}%")
    print(f"de cada R$ 100: gasto {d['gasto_contido']}, adiantado {d['receita_antecipada']}, imposto {d['imposto_a_mais']}")


if __name__ == "__main__":
    main()
