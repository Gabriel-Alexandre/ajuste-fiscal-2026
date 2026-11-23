"""Validação por um segundo caminho. Não importa analise.py nem lê dados/derivados para refazer
as contas: lê o texto bruto das fontes por outro caminho (outro documento ou outra parte do
mesmo documento) e compara com o RESUMO.json.

Uso:  python ferramentas/validacao_independente.py   (sai com erro se algum teste falhar)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
T = RAIZ / "dados" / "textos"
C = RAIZ / "dados" / "capturas"


def plano(caminho: Path) -> str:
    return re.sub(r"\s+", " ", caminho.read_text(encoding="utf-8"))


def n(s: str) -> float:
    return float(s.replace(".", "").replace(",", "."))


def main() -> None:
    r = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    comp = r["composicao_2027"]["pontas"]
    testes = []

    def teste(nome, esperado, obtido, tol=0.05):
        ok = abs(float(esperado) - float(obtido)) <= tol
        testes.append({"teste": nome, "esperado": esperado, "obtido": obtido, "passou": ok})

    # 1. a tabela pelo Jota (3ª leitura, reportagem que cita o relatório do relator)
    j = plano(C / "jota-segue-camara.txt")
    m = re.search(r"conten\S+o de despesas devem gerar entre R\$ ([\d,]+) bilh\S+ e R\$ ([\d,]+) bilh\S+; a trava nas compensa\S+es tribut\S+rias deve elevar a arrecada\S+o entre R\$ ([\d,]+) bilh\S+ e R\$ ([\d,]+) bilh\S+; a redu\S+o de gastos tribut\S+rios, R\$ ([\d,]+) bilh\S+; e a limita\S+o do Regime Especial.{0,90}?outros R\$ ([\d,]+) bilh", j)
    assert m, "Jota: trecho da tabela não achado"
    teste("Jota: gasto contido, mínimo", n(m[1]), comp["minimo"]["gasto_contido"])
    teste("Jota: gasto contido, máximo", n(m[2]), comp["maximo"]["gasto_contido"])
    teste("Jota: receita total, mínimo", n(m[3]) + n(m[5]) + n(m[6]), comp["minimo"]["receita_total"])
    teste("Jota: receita total, máximo", n(m[4]) + n(m[5]) + n(m[6]), comp["maximo"]["receita_total"])

    # 2. a soma das receitas como o DIAP escreve
    d = plano(T / "diap-nota-tecnica.txt")
    m = re.search(r"efeito estimado situa-se entre R\$ ([\d,]+) bilh\S+ e R\$ ([\d,]+) bilh\S+\. A economia por conten\S+o de despesas corresponde ao intervalo de R\$ ([\d,]+) bilh\S+ a R\$ ([\d,]+) bilh", d)
    assert m, "DIAP: soma não achada"
    teste("DIAP: receita mínima", n(m[1]), comp["minimo"]["receita_total"])
    teste("DIAP: receita máxima", n(m[2]), comp["maximo"]["receita_total"])
    teste("DIAP: gasto mínimo", n(m[3]), comp["minimo"]["gasto_contido"])
    teste("DIAP: gasto máximo", n(m[4]), comp["maximo"]["gasto_contido"])

    # 3. a Folha (via Jornal do Comércio): "dois terços" vindo de receita
    f = plano(C / "jc-rejeita-tres-mudancas.txt")
    m = re.search(r"De R\$ ([\d,]+) bilh\S+ a R\$ ([\d,]+) bilh\S+ vir\S+o de medidas arrecadat\S+rias - ou seja, dois ter\S+os", f)
    assert m, "Folha: trecho não achado"
    teste("Folha: receita mínima (a Folha parte de R$ 46 bi, por isso a tolerância)", n(m[1]), comp["minimo"]["receita_total"], tol=1.0)
    teste("Folha: receita máxima", n(m[2]), comp["maximo"]["receita_total"], tol=1.0)
    teste("Folha: 'dois terços' contra a nossa parte da receita no meio da faixa (%)", 66.7, r["composicao_2027"]["meio_da_faixa"]["pct_receita"], tol=3.0)

    # 4. os placares pela ficha de tramitação (outro documento do Senado)
    tr = plano(T / "senado-tramitacao.txt")
    achados = {
        "senado-votacao-req-770-urgencia": r"Requerimento n\S+ 770/2026\)\. Verifica\S+o de vota\S+o: \(Sim: (\d+); N\S+o: (\d+)",
        "senado-votacao-texto-base": r"Substitutivo, emenda n\S+ 75, aprovado.{0,60}?\(Sim: (\d+); N\S+o: (\d+)",
        "senado-votacao-emenda-40": r"Emenda n\S+ 40 do projeto, destacada, rejeitada \(Sim: (\d+); N\S+o: (\d+)",
        "senado-votacao-comprev": r"Art\. 7\S+ do projeto \(correspondente ao art\. 6\S+ do Substitutivo\), destacado, aprovado \(Sim: (\d+); N\S+o: (\d+)",
        "senado-votacao-compensacao": r"destacado, aprovado \(Sim: (\d+); N\S+o: (\d+); Absten\S+o: 0; Presidente: 1; Total: 81\)",
        "senado-votacao-turno-suplementar": r"rejeitadas as demais emendas \(Sim: (\d+); N\S+o: (\d+)",
    }
    placar = {p["votacao"]: p for p in r["votacoes_senado"]["placar"]}
    for chave, padrao in achados.items():
        m = re.search(padrao, tr)
        assert m, f"tramitação: {chave} não achado"
        teste(f"tramitação × listagem nominal: {chave} (sim)", int(m[1]), int(placar[chave]["contados_sim"]), tol=0)
        teste(f"tramitação × listagem nominal: {chave} (não)", int(m[2]), int(placar[chave]["contados_nao"]), tol=0)

    # 5. contas de conferência dentro das fontes da IFI
    r116 = plano(T / "ifi-raf-116.txt")
    m = re.search(r"Obrigat\S+rias sujeitas ([\d.,]+) ([\d.,]+) 15,9%", r116)
    assert m, "RAF 116 tabela 7 não achada"
    teste("RAF 116: tabela 7 refaz o aumento das obrigatórias", round(n(m[2]) - n(m[1]), 1), r["buraco"]["aumento_obrigatorias_2027_rs_bi"])
    a26 = r["buraco"]["ano_2026"]
    teste("RAF 117: 2026, antes das deduções + deduções = depois", round(a26["rardp_antes_deducoes_rs_bi"] + a26["deducoes_rs_bi"], 1), a26["rardp_depois_deducoes_rs_bi"])
    teste("meta de 2027 sobre o PIB do PLOA = 0,5%", 0.5, r["buraco"]["meta2027_centro_pct_pib"], tol=0.01)
    ag = plano(C / "agenciabrasil-4bim-2026.txt")
    m = re.search(r"O resultado negativo projetado passou de R\$ [\d,]+ bilh\S+ para R\$ ([\d,]+) bilh\S+, sem considerar despesas que podem ser abatidas", ag)
    assert m, "Agência Brasil: trecho não achado"
    teste("Agência Brasil: o déficit de 2026 antes das deduções (4º bimestre, R$ bi)", n(m[1]), abs(a26["rardp_antes_deducoes_rs_bi"]))

    # 6. o parecer da Câmara classifica as medidas como nós
    cam = plano(T / "camara-parecer-preliminar.txt")
    teste("Câmara: arts. 4º, 9º e 6º-F ampliam receita", 1, int(bool(re.search(r"os arts\. 4\S+, 9\S+ e o art\. 6\S+-F da Lei Complementar n\S+ 200/2023 ampliam receita", cam))), tol=0)
    teste("Câmara: o 6º-F é antecipação de arrecadação", 1, int(bool(re.search(r"6\S+-F, o efeito seja de antecipa\S+o de arrecada\S+o", cam))), tol=0)
    teste("Câmara: o bloqueio é reversível no curso do exercício", 1, int(bool(re.search(r"revers\S+vel no curso do exerc\S+cio", cam))), tol=0)

    # 7. a Emenda 40 é a do Marinho e trazia o teto de 0,6% e a supressão do 6º-F
    e40 = plano(T / "senado-emenda-40.txt")
    teste("Emenda 40: teto de 0,6%", 1, int("0,6% a.a." in e40), tol=0)
    teste("Emenda 40: suprime o 6º-F (compensação)", 1, int(bool(re.search(r"Art\. 6\S+-F\. \(Suprimir\)", e40))), tol=0)
    teste("Emenda 40: tira o diesel da meta", 1, int(bool(re.search(r"subs\S+dio\s+do diesel", e40))), tol=0)

    ok = all(t["passou"] for t in testes)
    (RAIZ / "resultados" / "VALIDACAO.json").write_text(json.dumps({"passaram": sum(t["passou"] for t in testes), "total": len(testes), "testes": testes}, ensure_ascii=False, indent=1), encoding="utf-8")
    for t in testes:
        print(("OK   " if t["passou"] else "FALHA"), t["teste"], t["esperado"], t["obtido"])
    print(f"{sum(t['passou'] for t in testes)} de {len(testes)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
