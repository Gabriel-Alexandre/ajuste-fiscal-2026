"""Tira os números do texto das fontes e grava as tabelas leves em dados/derivados/.

Regra do projeto: nenhum número é digitado. Cada valor sai de um trecho do texto oficial,
achado por expressão regular; se o trecho não for achado, o script para. A coluna `trecho`
guarda a frase de onde o número saiu, para conferência.

Uso:  python ferramentas/derivar.py
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TEXTOS = RAIZ / "dados" / "textos"
CAPTURAS = RAIZ / "dados" / "capturas"
DERIVADOS = RAIZ / "dados" / "derivados"


def ler(nome: str, pasta: Path = TEXTOS) -> str:
    texto = (pasta / nome).read_text(encoding="utf-8")
    return re.sub(r"[ \t ]+", " ", texto)


def num(s: str) -> float:
    return float(s.replace(".", "").replace(",", "."))


def achar(texto: str, padrao: str, fonte: str, linhas: bool = False) -> re.Match:
    """Procura o trecho. Sem `linhas`, a quebra de linha do PDF vira espaço."""
    if not linhas:
        texto = re.sub(r"\s+", " ", texto)
    m = re.search(padrao, texto, flags=re.S | re.I)
    if not m:
        raise SystemExit(f"[{fonte}] trecho não achado: {padrao}")
    return m


def trecho(m: re.Match) -> str:
    return re.sub(r"\s+", " ", m.group(0)).strip()[:260]


# ---------------------------------------------------------------- 1. as medidas
def medidas() -> list[dict]:
    """A tabela de impacto de 2027, em duas leituras independentes do mesmo dado."""
    p = ler("senado-parecer-221.txt")
    linhas = []
    m = achar(p, r"conten\S*o de despesas\s+em cerca de R\$ ([\d,]+) bilh\S+ a R\$ ([\d,]+) bilh", "parecer 221")
    linhas.append(dict(medida="contingenciamento", nome="Bloqueio de despesas para buscar o centro da meta (art. 6º-C a 6º-E)",
                       natureza="gasto contido", minimo=num(m[1]), maximo=num(m[2]), fonte="senado-parecer-221", trecho=trecho(m)))
    m = achar(p, r"compensa\S+o entre d\S+bitos e cr\S+ditos.{0,80}?aumento da arrecada\S+o entre R\$ ([\d,]+) bilh\S+ e R\$ ([\d,]+) bilh", "parecer 221")
    linhas.append(dict(medida="compensacao", nome="Limite ao uso de créditos tributários para pagar outros tributos (art. 6º-F)",
                       natureza="receita antecipada", minimo=num(m[1]), maximo=num(m[2]), fonte="senado-parecer-221", trecho=trecho(m)))
    m = achar(p, r"redu\S+o do gasto tribut\S+rio em 10%.{0,40}?aumento da arrecada\S+o de\s+R\$ ([\d,]+) bilh", "parecer 221")
    linhas.append(dict(medida="beneficios", nome="Corte linear de benefícios fiscais, de 10% para 20% (art. 4º)",
                       natureza="imposto a mais", minimo=num(m[1]), maximo=num(m[1]), fonte="senado-parecer-221", trecho=trecho(m)))
    m = achar(p, r"Demonstrativo de\s+Gastos Tribut\S+rios.{0,120}?aumento da\s+arrecada\S+o de R\$ ([\d,]+) bilh", "parecer 221")
    linhas.append(dict(medida="reidi", nome="Teto para o benefício do Reidi (art. 9º)",
                       natureza="imposto a mais", minimo=num(m[1]), maximo=num(m[1]), fonte="senado-parecer-221", trecho=trecho(m)))
    m = achar(p, r"melhora o resultado prim\S+rio entre R\$ ([\d,]+) bilh\S+ e ([\d,]+) bilh", "parecer 221")
    total = dict(medida="total_declarado", nome="Total declarado pelo parecer", natureza="total",
                 minimo=num(m[1]), maximo=num(m[2]), fonte="senado-parecer-221", trecho=trecho(m))
    return linhas + [total]


def medidas_diap() -> list[dict]:
    """A mesma tabela, lida na nota técnica do DIAP (que cita o parecer e a nota da Conorf)."""
    d = ler("diap-nota-tecnica.txt")
    saida = []
    padroes = {
        "contingenciamento": r"Contingenciamento adicional para aproxima\S+o do centro\s+R\$ ([\d,]+) a ([\d,]+) bilh",
        "compensacao": r"Limita\S+o de compensa\S+es tribut\S+rias\s+R\$ ([\d,]+) a ([\d,]+) bilh",
        "beneficios": r"Redu\S+o adicional dos benef\S+cios tribut\S+rios\s+R\$ ([\d,]+) bilh",
        "reidi": r"Limita\S+o do Reidi\s+R\$ ([\d,]+) bilh",
        "total_declarado": r"Total estimado\s+R\$ ([\d,]+) a ([\d,]+) bilh",
    }
    for medida, padrao in padroes.items():
        m = achar(d, padrao, "DIAP")
        mn = num(m[1]); mx = num(m[2]) if m.lastindex and m.lastindex >= 2 else mn
        saida.append(dict(medida=medida, minimo=mn, maximo=mx, fonte="diap-nota-tecnica", trecho=trecho(m)))
    m = achar(d, r"tr\S+s componentes relacionados \S+ arrecada\S+o, o efeito\s+estimado situa-se entre R\$ ([\d,]+) bilh\S+ e R\$ ([\d,]+) bilh", "DIAP")
    saida.append(dict(medida="receita_somada_pelo_diap", minimo=num(m[1]), maximo=num(m[2]), fonte="diap-nota-tecnica", trecho=trecho(m)))
    return saida


# ---------------------------------------------------------------- 2. o buraco
def buraco() -> list[dict]:
    r116 = ler("ifi-raf-116.txt")
    r117 = ler("ifi-raf-117.txt")
    d = ler("diap-nota-tecnica.txt")
    s = []

    def add(chave, valor, unidade, fonte, m, descricao):
        s.append(dict(chave=chave, valor=valor, unidade=unidade, descricao=descricao, fonte=fonte, trecho=trecho(m)))

    m = achar(r116, r"proposta de or\S+amento prev\S+ um super\S+vit prim\S+rio de\s+R\$ ([\d,]+) bilh\S+\. A IFI prev\S+ um d\S+ficit prim\S+rio de R\$ ([\d,]+) bilh", "RAF 116")
    add("ploa2027_primario_efetivo", num(m[1]), "R$ bi", "ifi-raf-116", m, "PLOA 2027: superávit primário efetivo previsto pelo governo")
    add("ifi2027_primario_efetivo", -num(m[2]), "R$ bi", "ifi-raf-116", m, "IFI: resultado primário efetivo projetado para 2027 (déficit)")
    m = achar(r116, r"necessidade de\s+contingenciamento de\s+R\$ ([\d,]+) bilh\S+ para o cumprimento da meta", "RAF 116")
    add("ifi2027_contingenciamento_necessario", num(m[1]), "R$ bi", "ifi-raf-116", m, "IFI: bloqueio que faltaria em 2027 para cumprir o piso da meta")
    m = achar(r116, r"obrigat\S+rias sujeitas aos limites est\S+o estimadas em R\$ ([\d.,]+) bilh\S+.{0,40}?programadas em R\$ ([\d.,]+) bilh\S+ \(15,6% do PIB\) para 2027", "RAF 116")
    add("obrigatorias_2026", num(m[1]), "R$ bi", "ifi-raf-116", m, "Despesas obrigatórias sujeitas ao limite, 2026 (3º bimestre)")
    add("obrigatorias_2027", num(m[2]), "R$ bi", "ifi-raf-116", m, "Despesas obrigatórias sujeitas ao limite, PLOA 2027")
    m = achar(r116, r"as despesas obrigat\S+rias aumentam R\$ ([\d,]+) bilh\S+ no per\S+odo", "RAF 116")
    add("obrigatorias_aumento_declarado", num(m[1]), "R$ bi", "ifi-raf-116", m, "Aumento das obrigatórias de 2026 para 2027, como a IFI escreve")
    m = achar(r116, r"O PLOA estima PIB de R\$ ([\d.,]+) bilh\S+ em 2027", "RAF 116")
    add("pib2027_ploa", num(m[1]), "R$ bi", "ifi-raf-116", m, "PIB nominal de 2027 no PLOA")
    m = achar(d, r"meta de super\S+vit prim\S+rio de R\$ ([\d,]+) bilh\S+ proposta para 2027", "DIAP")
    add("meta2027_centro", num(m[1]), "R$ bi", "diap-nota-tecnica", m, "Centro da meta de 2027 (0,5% do PIB)")

    m = achar(r117, r"projeta um d\S+ficit\s+prim\S+rio equivalente a ([\d,]+)% do PIB, em 2026", "RAF 117")
    add("ifi2026_deficit_pib", num(m[1]), "% do PIB", "ifi-raf-117", m, "IFI: déficit primário de 2026")
    m = achar(r117, r"d\S+ficit prim\S+rio\s+efetivo potencial de ([\d,]+)% do PIB, em 2027", "RAF 117")
    add("ifi2027_deficit_potencial_pib", num(m[1]), "% do PIB", "ifi-raf-117", m, "IFI: déficit potencial de 2027 com as promessas novas")
    m = achar(r117, r"representam R\$ ([\d,]+) bilh\S+es de desequil\S+brio\s+adicional n\S+o or\S+ado", "RAF 117")
    add("promessas_nao_orcadas", num(m[1]), "R$ bi", "ifi-raf-117", m, "Bolsa Família, Bets e MEI: desequilíbrio não orçado")
    m = achar(r117, r"super\S+vit prim\S+rio de ([\d,]+)% do PIB para estabilizar a rela\S+o d\S+vida p\S+blica/PIB, esse\s+quadro indica a necessidade de um ajuste fiscal equivalente a algo como ([\d,]+) p\.p\. do PIB", "RAF 117")
    add("primario_que_estabiliza_pib", num(m[1]), "% do PIB", "ifi-raf-117", m, "IFI: superávit que estabiliza a dívida (juro real de 5%)")
    add("ajuste_necessario_pp_pib", num(m[2]), "p.p. do PIB", "ifi-raf-117", m, "IFI: tamanho do ajuste necessário")
    m = achar(r117, r"prim\S+rio necess\S+rio passa de 2,1% do PIB, com o juro real de 5%, para ([\d,]+)% com", "RAF 117")
    add("primario_que_estabiliza_pib_juro61", num(m[1]), "% do PIB", "ifi-raf-117", m, "IFI: superávit que estabiliza a dívida com juro real de 6,1%")
    m = achar(r117, r"d\S+vida bruta do governo geral alcan\S+a ([\d,]+)% do PIB, em 2027", "RAF 117")
    add("divida2027_pib", num(m[1]), "% do PIB", "ifi-raf-117", m, "IFI: dívida bruta no fim de 2027")
    m = achar(r117, r"d\S+vida superar 90% do PIB at\S+ 2030 passa de [\d,]+% para ([\d,]+)%", "RAF 117")
    add("prob_divida_90", num(m[1]), "%", "ifi-raf-117", m, "IFI: chance de a dívida passar de 90% do PIB até 2030")

    # a linha de 2026 da Tabela 3 do RAF 117 (RARDP do 4º bimestre)
    m = achar(r117, r"\(16\) Total das dedu\S+es do Governo Central.{0,600}?\(18\) Meta de resultado prim\S+rio do governo central \(limite inferior\)\s+([-\d, ]+)\n.{0,200}?\(19\) Resultado prim\S+rio apurado do governo central \(antes das\s+([-\d, ]+)\n\s*dedu\S+es\)\s+([-\d, ]+)", "RAF 117 tabela 3", linhas=True)
    meta = m[1].split(); antes = m[2].split(); depois = m[3].split()
    add("meta2026_piso", num(meta[-1]), "R$ bi", "ifi-raf-117", m, "Meta de 2026, piso da banda")
    add("primario2026_antes_deducoes", num(antes[-1]), "R$ bi", "ifi-raf-117", m, "2026: resultado primário projetado antes das deduções (RARDP 4º bim.)")
    add("primario2026_depois_deducoes", num(depois[-1]), "R$ bi", "ifi-raf-117", m, "2026: resultado para a meta, depois das deduções, antes do bloqueio")
    # no PDF, a linha do total das deduções (16) sai colada ao rótulo da linha (15)
    m2 = achar(r117, r"\(ADPF n\S+ 1\.236\) ([-\d, ]+?)\n", "RAF 117 tabela 3 deduções", linhas=True)
    ded = m2[1].split()
    add("deducoes2026", num(ded[-1]), "R$ bi", "ifi-raf-117", m2, "2026: total das deduções da meta antes do diesel")
    return s


# ---------------------------------------------------------------- 3. diesel, Kandir e o que fica fora
def outras_medidas() -> list[dict]:
    f = ler("senado-parecer-224-redacao-final.txt")
    c = ler("camara-parecer-preliminar.txt")
    s = []
    m = achar(f, r"Art\. 13\. Em car\S+ter excepcional.{0,600}?at\S+ o limite de R\$ ([\d.,]+)", "redação final")
    s.append(dict(chave="diesel_fora_da_meta_2026", valor=num(m[1]) / 1e9, unidade="R$ bi", fonte="senado-parecer-224-redacao-final", trecho=trecho(m)))
    m = achar(f, r"entrega de que trata o inciso I do\s+caput fica limitada a R\$ ([\d.,]+)", "redação final")
    s.append(dict(chave="kandir_teto_anual", valor=num(m[1]) / 1e9, unidade="R$ bi", fonte="senado-parecer-224-redacao-final", trecho=trecho(m)))
    d = ler("diap-nota-tecnica.txt")
    m = achar(d, r"supersal\S+rios poder\S+ produzir economia de aproximadamente R\$ (\d+) bilh", "DIAP")
    s.append(dict(chave="supersalarios_estimativa_ministro", valor=float(m[1]), unidade="R$ bi", fonte="diap-nota-tecnica", trecho=trecho(m)))
    m = achar(f, r"limitada a R\$ 3\.000\.000\.000,00", "redação final")
    s.append(dict(chave="comprev_teto_anual", valor=3.0, unidade="R$ bi", fonte="senado-parecer-224-redacao-final", trecho=trecho(m)))
    m = achar(c, r"Proex, em\s+R\$ 1 bilh\S+o por ano, valor superior \S+ execu\S+o de 2025 e \S+ previs\S+o para 2026", "parecer da Câmara")
    s.append(dict(chave="proex_teto_acima_da_execucao", valor=1.0, unidade="R$ bi", fonte="camara-parecer-preliminar", trecho=trecho(m)))
    m = achar(c, r"ampliam receita, embora, no caso do art\. 6\S+-F, o\s+efeito seja de antecipa\S+o de arrecada\S+o", "parecer da Câmara")
    s.append(dict(chave="camara_classifica_6F_antecipacao", valor=1, unidade="sim", fonte="camara-parecer-preliminar", trecho=trecho(m)))
    m = achar(f, r"6\S+-F.{0,900}?at\S+ o montante equivalente \S+quele decorrente da redu\S+o de limite", "redação final")
    s.append(dict(chave="compensacao_limitada_ao_bloqueio", valor=1, unidade="sim", fonte="senado-parecer-224-redacao-final", trecho=trecho(m)))
    m = achar(f, r"n\S+o se incorporar\S+ \S+ base de c\S+lculo dos exerc\S+cios seguintes", "redação final")
    s.append(dict(chave="bloqueio_nao_entra_na_base", valor=1, unidade="sim", fonte="senado-parecer-224-redacao-final", trecho=trecho(m)))
    return s


# ---------------------------------------------------------------- 4. as votações
VOTO = r"(SIM|NÃO|ABSTENÇÃO|AP|P-NRV|P-OD|LS|LP|NCom|MIS|Presidente \(art\. 51 RISF\))"


def votacoes() -> tuple[list[dict], list[dict]]:
    arquivos = {
        "senado-votacao-req-770-urgencia": "12/11 · urgência (Req. 770)",
        "senado-votacao-texto-base": "12/11 · texto-base (substitutivo)",
        "senado-votacao-emenda-40": "18/11 · Emenda 40 (Marinho)",
        "senado-votacao-comprev": "18/11 · destaque: limite da compensação previdenciária",
        "senado-votacao-compensacao": "18/11 · destaque: limite da compensação tributária",
        "senado-votacao-turno-suplementar": "18/11 · turno suplementar (texto final)",
    }
    placar, nominal = [], []
    for arq, rotulo in arquivos.items():
        t = ler(f"{arq}.txt")
        m = achar(t, r"ABST\.: ?(\d+) PRESIDENTE: ?(\d+) TOTAL: ?(\d+)\s+SIM: ?(\d+) N\S+O: ?(\d+)", arq)
        oficial = dict(sim=int(m[4]), nao=int(m[5]), abst=int(m[1]), presidente=int(m[2]), total=int(m[3]))
        contagem = {"SIM": 0, "NÃO": 0, "ABSTENÇÃO": 0}
        vistos = set()
        for linha in t.splitlines():
            ml = re.match(rf"^\s*(\S+) ([A-Z]{{2}}) (.+?) {VOTO}\s*$", linha)
            if not ml:
                continue
            partido, uf, nome, voto = ml.groups()
            if (nome, uf) in vistos:
                continue
            vistos.add((nome, uf))
            nominal.append(dict(votacao=arq, rotulo=rotulo, partido=partido, uf=uf, senador=nome.strip(), voto=voto))
            if voto in contagem:
                contagem[voto] += 1
        placar.append(dict(votacao=arq, rotulo=rotulo, **{f"oficial_{k}": v for k, v in oficial.items()},
                           contados_sim=contagem["SIM"], contados_nao=contagem["NÃO"], contados_abst=contagem["ABSTENÇÃO"]))
    return placar, nominal


# ---------------------------------------------------------------- 5. o que a imprensa mudou depois
def capturas() -> list[dict]:
    s = []
    j = ler("jota-segue-camara.txt", CAPTURAS)
    m = achar(j, r"reduziram de R\$ (\d+) bilh\S+ para R\$ (\d+) bilh\S+ a estimativa de impacto fiscal em 2027", "Jota")
    s.append(dict(chave="estimativa_pos_senado_relator", valor=float(m[2]), antes=float(m[1]), fonte="jota-segue-camara", trecho=trecho(m)))
    a = ler("agazeta-camara-23-11.txt", CAPTURAS)
    m = achar(a, r"pot\S+ncia fiscal do projeto, calculada entre R\$ (\d+) bilh\S+ e R\$ (\d+) bilh", "Folhapress/A Gazeta")
    s.append(dict(chave="estimativa_pos_senado_ministro", valor=float(m[1]), antes=float(m[2]), fonte="agazeta-camara-23-11", trecho=trecho(m)))
    m = achar(a, r"Outros R\$ (\d+) bilh\S+ em medidas, como o adiamento de repasses da Lei Kandir", "Folhapress/A Gazeta")
    s.append(dict(chave="medidas_que_acomodam_promessas", valor=float(m[1]), antes=None, fonte="agazeta-camara-23-11", trecho=trecho(m)))
    i = ler("investnews-medidas.txt", CAPTURAS)
    m = achar(i, r"Os outros R\$ (\d+) bilh\S+ acomodam despesas e compromissos do Executivo", "InvestNews")
    s.append(dict(chave="medidas_que_acomodam_promessas_2", valor=float(m[1]), antes=None, fonte="investnews-medidas", trecho=trecho(m)))
    t = ler("folhape-tesouro-setembro.txt", CAPTURAS)
    m = achar(t, r"d\S+ficit prim\S+rio de R\$ ([\d,]+) bilh\S+.{0,40}?entre janeiro e setembro", "Folha PE/Agência Brasil")
    s.append(dict(chave="tesouro_deficit_jan_set_2026", valor=-num(m[1]), antes=None, fonte="folhape-tesouro-setembro", trecho=trecho(m)))
    b = ler("folhape-divida-829.txt", CAPTURAS)
    m = achar(b, r"([\d,]+)% do PIB", "Folha PE/Agência Brasil")
    s.append(dict(chave="bc_divida_bruta_set_2026", valor=num(m[1]), antes=None, fonte="folhape-divida-829", trecho=trecho(m)))
    return s


def gravar(nome: str, linhas: list[dict]) -> None:
    DERIVADOS.mkdir(parents=True, exist_ok=True)
    campos = list(dict.fromkeys(k for l in linhas for k in l))
    with open(DERIVADOS / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)
    print(f"{nome}: {len(linhas)} linhas")


def main() -> None:
    gravar("medidas_2027.csv", medidas())
    gravar("medidas_2027_diap.csv", medidas_diap())
    gravar("buraco.csv", buraco())
    gravar("outras_medidas.csv", outras_medidas())
    placar, nominal = votacoes()
    gravar("votacoes_senado_placar.csv", placar)
    gravar("votacoes_senado_nominal.csv", nominal)
    gravar("depois_do_senado.csv", capturas())
    cam = json.loads((RAIZ / "dados" / "brutos" / "camara-votacoes.json").read_text(encoding="utf-8"))
    st = json.loads((RAIZ / "dados" / "brutos" / "camara-proposicao.json").read_text(encoding="utf-8"))["dados"]["statusProposicao"]
    gravar("camara_situacao.csv", [dict(votacoes_registradas=len(cam["dados"]), situacao=st["descricaoSituacao"],
                                       ultima_tramitacao=st["dataHora"], despacho=st["despacho"][:200])])


if __name__ == "__main__":
    main()
