# Plano (rodada 0)

**Pergunta:** o ajuste fiscal do governo Lula (PLP 299/2026, o "Plano Moretti") corta gasto ou aumenta imposto? E qual é o tamanho dele perto do buraco que promete fechar?

**Por que este projeto existe:** nos canais de direita circula, nesta semana, que o ajuste é "cosmético", que é um "tributaço" e que rachou a base do governo. A conta que ninguém publicou separada, medida por medida, é quanto do pacote é gasto que deixa de sair e quanto é dinheiro que entra a mais, com a fonte primária de cada número.

**Método (jornalismo de dados):** fonte primária com hash; número tirado do texto por script, nunca digitado; validação por um segundo caminho (outro documento com o mesmo dado); revisão adversarial por três leitores; relatório gerado por script; o que o dado não diz no topo.

## Dados

| Dado | Fonte primária | Segunda fonte |
|---|---|---|
| A tabela de impacto por medida | Parecer nº 221/2026-PLEN/SF (relator Eduardo Braga) | nota técnica do DIAP (16/11, cita a nota da Conorf de 13/11); Jota (18/11) |
| A classificação de cada medida (despesa ou receita) | parecer preliminar do relator na Câmara (PRLP 1, 19/11) | o próprio texto da redação final |
| O texto final | Parecer nº 224/2026-PLEN/SF (redação final) | autógrafo na Câmara |
| As votações | listagens nominais do Senado | ficha de tramitação da matéria 176328 |
| O tamanho do buraco | IFI, RAF 116 (set/2026) e 117 (out/2026) | Agência Brasil (Tesouro e BC); InfoMoney |
| O diesel | redação final, art. 13 | parecer da Câmara; Agência Senado |
| A situação na Câmara | API de dados abertos da Câmara | Folhapress (A Gazeta, 23/11) |

## Classificação

- **gasto contido**: o bloqueio de despesas (arts. 6º-C a 6º-E da LC 200, como alterada);
- **receita antecipada**: o limite ao uso de créditos tributários para pagar outros tributos (art. 6º-F), porque o crédito não se extingue;
- **imposto a mais**: o corte linear de benefícios fiscais de 10% para 20% (art. 4º) e o teto do Reidi (art. 9º).

Fora da conta, com o porquê: Lei Kandir, compensação previdenciária e Proex (limites que abrem espaço ou não economizam), supersalários (sem valor no texto), diesel (sai da meta de 2026, não é economia).

## Sem pré-registro

É o padrão de rodadas (o projeto não é previsão nem teste de alegação eleitoral). Cada mudança vai para `docs/RODADAS.md`.
