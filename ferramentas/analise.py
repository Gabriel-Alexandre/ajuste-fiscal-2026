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


def variantes(comp: dict) -> list[dict]:
    """As leituras alternativas que a revisão pediu, cada uma com o número."""
    mn, mx = comp["pontas"]["minimo"], comp["pontas"]["maximo"]
    imposto = mn["imposto_a_mais"]
    return [
        {"id": "V1", "leitura": "só conta como imposto o que aumenta tributo para sempre (benefícios e Reidi); a compensação vira 'adiantamento'",
         "pct_imposto_min": mn["pct_imposto_a_mais"], "pct_imposto_max": mx["pct_imposto_a_mais"],
         "efeito": "o imposto a mais cai para 35% a 43%; o gasto contido continua de 28% a 33%; o resto (28% a 33%) é dinheiro das empresas adiantado"},
        {"id": "V2", "leitura": "o bloqueio é facultativo; se o governo não bloquear, a lei também não deixa limitar a compensação (art. 6º-F)",
         "total": imposto, "pct_receita": 100.0,
         "efeito": f"sobra só o imposto a mais, R$ {imposto:.1f} bilhões, e 100% do ajuste vira receita"},
        {"id": "V3", "leitura": "o governo bloqueia o teto da faixa e a compensação vem no teto",
         "pct_gasto": mx["pct_gasto"], "pct_receita": mx["pct_receita"],
         "efeito": "é a ponta mais favorável ao lado do gasto, e o gasto contido não passa de um terço"},
    ]


def buraco(comp: dict, b: dict, outras: dict, depois: dict) -> dict:
    mn, mx = comp["pontas"]["minimo"]["total"], comp["pontas"]["maximo"]["total"]
    gmn, gmx = comp["pontas"]["minimo"]["gasto_contido"], comp["pontas"]["maximo"]["gasto_contido"]
    pib = b["pib2027_ploa"]
    ajuste_nec = b["ajuste_necessario_pp_pib"] / 100 * pib
    aumento_obrig = r1(b["obrigatorias_2027"] - b["obrigatorias_2026"])
    gap_ploa_ifi = r1(b["ploa2027_primario_efetivo"] - b["ifi2027_primario_efetivo"])
    diesel = outras["diesel_fora_da_meta_2026"]
    return {
        "ajuste_pct_pib": [round(100 * mn / pib, 2), round(100 * mx / pib, 2)],
        "ajuste_necessario_ifi_rs_bi": r1(ajuste_nec),
        "ajuste_cobre_do_necessario_pct": [r1(100 * mn / ajuste_nec), r1(100 * mx / ajuste_nec)],
        "aumento_obrigatorias_2027_rs_bi": aumento_obrig,
        "ajuste_sobre_aumento_obrigatorias_pct": [r1(100 * mn / aumento_obrig), r1(100 * mx / aumento_obrig)],
        "gasto_contido_sobre_aumento_obrigatorias_pct": [r1(100 * gmn / aumento_obrig), r1(100 * gmx / aumento_obrig)],
        "promessas_nao_orcadas_rs_bi": b["promessas_nao_orcadas"],
        "promessas_sobre_ajuste_pct": [r1(100 * b["promessas_nao_orcadas"] / mx), r1(100 * b["promessas_nao_orcadas"] / mn)],
        "distancia_ploa_ifi_2027_rs_bi": gap_ploa_ifi,
        "ajuste_sobre_distancia_ploa_ifi_pct": [r1(100 * mn / gap_ploa_ifi), r1(100 * mx / gap_ploa_ifi)],
        "ifi_bloqueio_que_faltaria_2027_rs_bi": b["ifi2027_contingenciamento_necessario"],
        "meta2027_centro_rs_bi": b["meta2027_centro"],
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
        "variantes": variantes(comp),
        "buraco": buraco(comp, b, outras, depois),
        "fora_da_tabela_de_impacto": {
            "kandir_teto_anual_rs_bi": outras["kandir_teto_anual"],
            "comprev_teto_anual_rs_bi": outras["comprev_teto_anual"],
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
