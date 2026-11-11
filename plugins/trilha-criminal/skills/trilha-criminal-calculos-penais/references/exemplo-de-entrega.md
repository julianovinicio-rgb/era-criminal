# Exemplo fictício de entrega

Exemplo inteiramente fictício, para calibrar formato, proporção e tom. Pessoas, processo, datas e identificadores não existem. Não copie fatos, prazos, datas ou conclusões. O exemplo mostra uma conta de prescrição com dois cenários.

Pedido simulado: "O furto do meu cliente, Davi Rocha, já prescreveu? Ele tinha 19 anos na época. Seguem a denúncia, a sentença e a certidão de trânsito para o Ministério Público."

---

## Resposta

Pela pena aplicada, o prazo se esgotou em 09/03/2021, antes da publicação da sentença, em 20/06/2022. O resultado depende de um dado que ainda não está nos autos que recebi: o documento de identidade que comprova a idade de Davi na data do fato. Sem a redução pela idade, o prazo não se esgotou.

## Entradas

| Dado | Valor | Fonte | Situação |
|---|---|---|---|
| Crime e pena aplicada | Furto simples, 1 ano de reclusão | Sentença, mov. 88.1 | Confirmado |
| Data do fato | 14/08/2018 | Denúncia, mov. 1.1 | Confirmado |
| Recebimento da denúncia | 10/03/2019 | Decisão, mov. 12.1 | Confirmado |
| Publicação da sentença | 20/06/2022 | Certidão, mov. 89.1 | Confirmado |
| Trânsito para a acusação | 04/07/2022 | Certidão, mov. 95.1 | Confirmado |
| Nascimento de Davi | 02/05/1999 | Informado por você | Sem documento nos autos recebidos |
| Suspensão do processo ou do prazo | Nenhuma localizada | Leitura dos movimentos 1 a 95 | Confirmado no material recebido |

## Cenários

Rodei o script com cada premissa. Os dois usam a pena aplicada, porque há trânsito para a acusação, e começam no recebimento da denúncia, porque o fato é posterior à lei de 2010 que impede termo inicial anterior à denúncia.

| Cenário | Prazo | Último dia do prazo no intervalo entre a denúncia e a sentença | Resultado |
|---|---|---|---|
| A. Com a redução pela idade | 4 anos, reduzidos à metade: 2 anos | 09/03/2021 | Prazo esgotado antes de 20/06/2022 |
| B. Sem a redução | 4 anos | 09/03/2023 | Prazo não esgotado |

Memória do cenário A, resumida: início em 10/03/2019, dia incluído na contagem; dois anos pelo calendário terminam em 09/03/2021; o marco seguinte, a publicação da sentença, ocorreu em 20/06/2022, um ano, três meses e onze dias depois. Não houve suspensão no intervalo.

O cenário A é a leitura que sustento, desde que a idade seja comprovada. O cenário B é o que o juízo adotará se o documento não for juntado.

## Nota ao advogado

- Estado: conta entregue, com pendência. Nenhuma peça foi redigida.
- Conferidos no Planalto em [data da execução]: arts. 109, 110, 115 e 117 do Código Penal. A ressalva do art. 115 para violência sexual contra a mulher não se aplica a furto.
- O crime é de 2018, posterior à alteração de 2010 no art. 110, § 1º. Por isso não examinei o intervalo entre o fato e o recebimento da denúncia.
- Pesquisa de jurisprudência: não realizada. Não precisei de orientação de tribunal para estas entradas.
- Li os movimentos 1 a 95. Não sei se há ato posterior a 04/07/2022.
- Pendências: `[CONFIRMAR: documento de identidade de Davi Rocha, para a idade em 14/08/2018]` e `[CONFIRMAR: inexistência de recurso da acusação pendente]`.
- O resultado é aritmético. O reconhecimento da prescrição depende de pedido e de decisão.
