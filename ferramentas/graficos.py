"""Os gráficos do projeto, 1920x1080, só a partir de resultados/RESUMO.json.

Uso:  python ferramentas/graficos.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
FIG = RAIZ / "resultados" / "figuras"
REPO = "github.com/Gabriel-Alexandre/ajuste-fiscal-2026"

COR = {"gasto": "#2E7D5B", "adiantado": "#7E5BA6", "imposto": "#D9822B", "neutro": "#6B6B6B",
       "buraco": "#B03A2E", "fundo": "#FFFFFF", "texto": "#1F1F1F"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22, "axes.edgecolor": "#BBBBBB",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "text.parse_math": False})  # o "R$" não pode virar fórmula


def br(x: float, casas: int = 1) -> str:
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def figura(titulo: str, subtitulo: str):
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=COR["fundo"])
    fig.text(0.05, 0.93, titulo, fontsize=44, weight="bold", color=COR["texto"], va="top")
    fig.text(0.05, 0.845, subtitulo, fontsize=24, color="#444444", va="top")
    return fig


def rodape(fig, fonte: str) -> None:
    fig.text(0.05, 0.035, f"Fonte: {fonte}", fontsize=16, color="#555555")
    fig.text(0.05, 0.008, f"{REPO} · conta feita com o auxílio do Claude (IA)", fontsize=15, color="#777777")


def g01(r: dict) -> None:
    c = r["composicao_2027"]; d = c["de_cada_100"]; mn = c["pontas"]["minimo"]; mx = c["pontas"]["maximo"]
    fig = figura("De cada R$ 100 do ajuste: corte ou imposto?",
                 f"Na tabela do governo, com o bloqueio acionado: de R$ {br(mn['total'])} a R$ {br(mx['total'])} bilhões em 2027 (meio da faixa)")
    ax = fig.add_axes([0.05, 0.36, 0.9, 0.3])
    partes = [("Gasto contido\n(bloqueio do Orçamento)", d["gasto_contido"], COR["gasto"]),
              ("Dinheiro das empresas adiantado\n(limite ao uso de créditos)", d["receita_antecipada"], COR["adiantado"]),
              ("Benefício fiscal cortado\n(imposto a mais)", d["imposto_a_mais"], COR["imposto"])]
    x = 0
    for rotulo, v, cor in partes:
        ax.barh(0, v, left=x, color=cor, height=0.8, edgecolor="white", linewidth=4)
        ax.text(x + v / 2, 0, f"R$ {v}", ha="center", va="center", fontsize=64, weight="bold", color="white")
        ax.text(x + v / 2, -0.75, rotulo, ha="center", va="top", fontsize=22, color=COR["texto"])
        x += v
    ax.set_xlim(0, 100); ax.set_ylim(-1.6, 0.6); ax.axis("off")
    fig.text(0.05, 0.22, f"Receita (adiantada + imposto): R$ {d['receita_total']} de cada R$ 100.", fontsize=26, weight="bold", color=COR["texto"])
    fig.text(0.05, 0.165, f"Nas pontas da faixa, a receita vai de {br(mx['pct_receita'])}% a {br(mn['pct_receita'])}% do total.",
             fontsize=22, color=COR["texto"])
    fig.text(0.05, 0.12, f"Se 2027 correr como o PLOA prevê, o bloqueio não é acionado e sobram R$ {br(mn['imposto_a_mais'])} bi, todos de receita.",
             fontsize=22, color=COR["texto"])
    rodape(fig, "Parecer nº 221/2026-PLEN/SF (relator Eduardo Braga), com dados do Poder Executivo; nota técnica do DIAP (16/11/2026)")
    fig.savefig(FIG / "g01_de_cada_100.png", facecolor=COR["fundo"]); plt.close(fig)


def g02(r: dict) -> None:
    med = r["composicao_2027"]["medidas"]
    nomes = {"contingenciamento": "Bloqueio de despesas\npara buscar o centro da meta",
             "compensacao": "Limite ao uso de créditos\ntributários das empresas",
             "beneficios": "Corte de benefícios fiscais\nde 10% para 20%",
             "reidi": "Teto para o benefício\ndo Reidi"}
    cores = {"gasto contido": COR["gasto"], "receita antecipada": COR["adiantado"], "imposto a mais": COR["imposto"]}
    rotulo_nat = {"gasto contido": "gasto contido", "receita antecipada": "receita adiantada", "imposto a mais": "benefício fiscal cortado"}
    fig = figura("O ajuste, medida por medida", "Impacto estimado em 2027, em R$ bilhões (a barra clara é a faixa entre o mínimo e o máximo)")
    ax = fig.add_axes([0.3, 0.14, 0.62, 0.62])
    for i, m in enumerate(reversed(med)):
        mn, mx = float(m["minimo"]), float(m["maximo"]); cor = cores[m["natureza"]]
        ax.barh(i, mn, color=cor, height=0.6)
        if mx > mn:
            ax.barh(i, mx - mn, left=mn, color=cor, alpha=0.35, height=0.6)
        txt = f"R$ {br(mn)}" + (f" a {br(mx)}" if mx > mn else "")
        ax.text(mx + 0.4, i, txt, va="center", fontsize=26, weight="bold", color=COR["texto"])
        ax.text(-0.6, i, nomes[m["medida"]], va="center", ha="right", fontsize=22, color=COR["texto"])
        ax.text(mx + 0.4, i - 0.36, rotulo_nat[m["natureza"]], va="center", fontsize=17, color=cor)
    ax.set_xlim(0, 25); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=18)
    rodape(fig, "Parecer nº 221/2026-PLEN/SF e Emenda nº 75 (substitutivo); classificação: parecer do relator na Câmara (PRLP 1, 19/11/2026)")
    fig.savefig(FIG / "g02_medida_por_medida.png", facecolor=COR["fundo"]); plt.close(fig)


def g03(r: dict) -> None:
    b = r["buraco"]; c = r["composicao_2027"]["pontas"]
    barras = [
        ("O ajuste (2027)", c["minimo"]["total"], c["maximo"]["total"], COR["gasto"]),
        ("Promessas novas não orçadas\n(Bolsa Família, Bets, MEI)", b["promessas_nao_orcadas_rs_bi"], None, COR["neutro"]),
        ("Distância entre o governo e a IFI\nno resultado de 2027", b["distancia_ploa_ifi_2027_rs_bi"], None, COR["neutro"]),
        ("Quanto as despesas obrigatórias\ncrescem de 2026 para 2027", b["aumento_obrigatorias_2027_rs_bi"], None, COR["neutro"]),
        ("O ajuste que a IFI diz faltar\npara a dívida parar de subir", b["ajuste_necessario_ifi_rs_bi"], None, COR["buraco"]),
    ]
    fig = figura("O ajuste contra o tamanho do buraco", "Em R$ bilhões. O ajuste cobre de "
                 f"{br(b['ajuste_cobre_do_necessario_pct'][0])}% a {br(b['ajuste_cobre_do_necessario_pct'][1])}% do que a IFI diz faltar")
    ax = fig.add_axes([0.33, 0.13, 0.6, 0.64])
    for i, (rot, v, vmax, cor) in enumerate(reversed(barras)):
        ax.barh(i, v, color=cor, height=0.62)
        if vmax:
            ax.barh(i, vmax - v, left=v, color=cor, alpha=0.35, height=0.62)
        fim = vmax or v
        ax.text(fim + 5, i, f"R$ {br(v)}" + (f" a {br(vmax)}" if vmax else ""), va="center", fontsize=26, weight="bold")
        ax.text(-8, i, rot, va="center", ha="right", fontsize=20)
    ax.set_xlim(0, 540); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=18)
    rodape(fig, "Parecer nº 221/2026; IFI, RAF nº 116 (set/2026) e nº 117 (out/2026); PIB de 2027 do PLOA (R$ 14,8 trilhões) para converter 3 p.p. do PIB")
    fig.savefig(FIG / "g03_ajuste_contra_o_buraco.png", facecolor=COR["fundo"]); plt.close(fig)


def g04(r: dict) -> None:
    a = r["buraco"]["ano_2026"]
    fig = figura("O diesel que sai da conta da meta de 2026",
                 "Em R$ bilhões. O gasto acontece igual; ele só deixa de contar para a meta")
    ax = fig.add_axes([0.08, 0.16, 0.86, 0.58])
    rot = ["Déficit projetado\npara 2026", "Despesas já tiradas\nda conta da meta", "Diesel tirado\npelo PLP 299", "Total tirado da\nconta com o diesel"]
    val = [abs(a["rardp_antes_deducoes_rs_bi"]), a["deducoes_rs_bi"], a["diesel_fora_da_meta_rs_bi"], a["deducoes_com_diesel_rs_bi"]]
    cores = [COR["buraco"], COR["neutro"], COR["imposto"], COR["neutro"]]
    ax.bar(range(4), val, color=cores, width=0.6)
    ax.bar(3, a["diesel_fora_da_meta_rs_bi"], bottom=a["deducoes_rs_bi"], color=COR["imposto"], width=0.6)
    for i, v in enumerate(val):
        ax.text(i, v + 2, f"R$ {br(v)}", ha="center", fontsize=30, weight="bold")
    ax.set_xticks(range(4)); ax.set_xticklabels(rot, fontsize=22); ax.set_ylim(0, 100); ax.tick_params(axis="y", labelsize=18)
    rodape(fig, "Relatório bimestral do 4º bimestre de 2026 (MPO e Fazenda), na Tabela 3 do RAF nº 117 da IFI; PLP 299/2026, art. 13 da redação final")
    fig.savefig(FIG / "g04_diesel_2026.png", facecolor=COR["fundo"]); plt.close(fig)


def g05(r: dict) -> None:
    p = r["votacoes_senado"]["placar"]
    fig = figura("Como o Senado votou o ajuste", "Votos SIM e NÃO em cada votação nominal (é preciso 41 votos para aprovar lei complementar)")
    ax = fig.add_axes([0.42, 0.13, 0.52, 0.64])
    for i, v in enumerate(reversed(p)):
        s, n = int(v["oficial_sim"]), int(v["oficial_nao"])
        ax.barh(i, s, color=COR["gasto"], height=0.6); ax.barh(i, n, left=s, color=COR["buraco"], height=0.6)
        ax.text(s / 2, i, str(s), ha="center", va="center", color="white", fontsize=24, weight="bold")
        if n:
            ax.text(s + n / 2, i, str(n), ha="center", va="center", color="white", fontsize=24, weight="bold")
        ax.text(-2, i, v["rotulo"].replace(" · ", "\n"), ha="right", va="center", fontsize=18)
    ax.axvline(41, color="#333333", linestyle="--", linewidth=2); ax.text(41.5, len(p) - 0.45, "41", fontsize=18)
    ax.set_xlim(0, 81); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=18)
    fig.text(0.05, 0.72, "■ SIM", color=COR["gasto"], fontsize=24, weight="bold"); fig.text(0.13, 0.72, "■ NÃO", color=COR["buraco"], fontsize=24, weight="bold")
    rodape(fig, "Senado Federal, listagens das votações nominais de 12 e 18/11/2026 e ficha de tramitação da matéria 176328")
    fig.savefig(FIG / "g05_votacoes_senado.png", facecolor=COR["fundo"]); plt.close(fig)


def g06(r: dict) -> None:
    c = r["composicao_2027"]; m = c["meio_da_faixa"]; b = r["buraco"]
    fig = figura("O ajuste depende de como 2027 vai andar",
                 "Em R$ bilhões, no meio da faixa. O bloqueio e a trava dos créditos só valem abaixo do centro da meta")
    ax = fig.add_axes([0.36, 0.16, 0.58, 0.56])
    rot_ploa = ("Se 2027 correr como o PLOA prevê" + chr(10) + f"(R$ {br(b['ploa2027_resultado_para_meta_rs_bi'])} bi, acima do centro"
                + chr(10) + f"de R$ {br(b['meta2027_centro_rs_bi'])} bi)")
    linhas = [("Tabela do governo" + chr(10) + "(o bloqueio é acionado)", m["gasto_contido"], m["receita_antecipada"], m["imposto_a_mais"]),
              (rot_ploa, 0, 0, m["imposto_a_mais"])]
    for i, (rot, g, a, im) in enumerate(reversed(linhas)):
        x = 0
        for v, cor in ((g, COR["gasto"]), (a, COR["adiantado"]), (im, COR["imposto"])):
            if v:
                ax.barh(i, v, left=x, color=cor, height=0.55, edgecolor="white", linewidth=3)
                ax.text(x + v / 2, i, br(v), ha="center", va="center", color="white", fontsize=26, weight="bold")
            x += v
        total = m["total"] if g else im  # o total do meio da faixa, não a soma das partes arredondadas
        ax.text(x + 0.8, i, f"R$ {br(total)}", va="center", fontsize=28, weight="bold")
        ax.text(-1.5, i, rot, ha="right", va="center", fontsize=20)
    ax.set_xlim(0, 60); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=18)
    fig.text(0.36, 0.76, "■ gasto contido", color=COR["gasto"], fontsize=22, weight="bold")
    fig.text(0.53, 0.76, "■ receita adiantada", color=COR["adiantado"], fontsize=22, weight="bold")
    fig.text(0.74, 0.76, "■ benefício fiscal cortado", color=COR["imposto"], fontsize=22, weight="bold")
    rodape(fig, "Parecer nº 221/2026; arts. 6º-C e 6º-F da redação final; PLOA 2027 pela tabela 8 do RAF nº 116 da IFI")
    fig.savefig(FIG / "g06_cenarios_2027.png", facecolor=COR["fundo"]); plt.close(fig)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    r = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    for g in (g01, g02, g03, g04, g05, g06):
        g(r)
    print("figuras:", sorted(p.name for p in FIG.glob("*.png")))


if __name__ == "__main__":
    main()
