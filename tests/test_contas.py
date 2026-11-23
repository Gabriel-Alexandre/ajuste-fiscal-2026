import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))


def test_as_partes_somam_o_total():
    for ponta in ("minimo", "maximo"):
        p = R["composicao_2027"]["pontas"][ponta]
        assert abs(p["gasto_contido"] + p["receita_total"] - p["total"]) < 0.05
        assert abs(p["pct_gasto"] + p["pct_receita"] - 100) < 0.2


def test_de_cada_100_soma_100():
    d = R["composicao_2027"]["de_cada_100"]
    assert d["gasto_contido"] + d["receita_antecipada"] + d["imposto_a_mais"] == 100


def test_compensacao_igual_ao_bloqueio():
    # o art. 6º-F só vale até o valor bloqueado; a tabela do parecer tem a mesma faixa
    for ponta in ("minimo", "maximo"):
        p = R["composicao_2027"]["pontas"][ponta]
        assert p["receita_antecipada"] == p["gasto_contido"]


def test_placar_oficial_igual_a_contagem_nominal():
    for v in R["votacoes_senado"]["placar"]:
        assert int(v["oficial_sim"]) == int(v["contados_sim"])
        assert int(v["oficial_nao"]) == int(v["contados_nao"])


def test_validacao_independente_passou():
    v = json.loads((RAIZ / "resultados" / "VALIDACAO.json").read_text(encoding="utf-8"))
    assert v["passaram"] == v["total"]


def test_manifesto_tem_hash_de_toda_fonte():
    m = json.loads((RAIZ / "dados" / "MANIFESTO.json").read_text(encoding="utf-8"))
    assert all(len(x["sha256"]) == 64 for x in m.values())
