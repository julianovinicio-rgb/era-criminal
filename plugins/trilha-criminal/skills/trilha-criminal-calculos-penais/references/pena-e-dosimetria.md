# Pena e dosimetria

Use para refazer a conta de uma sentença ou de um acórdão, comparar a pena aplicada com um cenário defensivo e medir a distância até os limiares que mudam regime, substituição ou prazo prescricional. A crítica jurídica da dosimetria, como fundamentação de vetorial ou dupla valoração, pertence à habilidade de Recurso de Apelação ou de Peças Defensivas. Aqui se faz a aritmética.

## Reconstruir a conta da decisão

Transcreva para o comando `pena` exatamente o que a decisão fez, etapa por etapa, com a fonte de cada uma na descrição:

1. `pena_inicial`: a pena de onde a decisão partiu, normalmente o mínimo cominado.
2. Cada acréscimo ou redução vira uma operação `aumento` ou `diminuicao`, com a fração que a decisão usou.
3. Quando a decisão fixa o acréscimo em tempo, e não em fração, use `soma` ou `subtracao` com o tempo.
4. Quando a pena é reconduzida a um limite, como o mínimo legal na segunda fase, use `fixar` e escreva o fundamento na descrição.
5. Concurso de crimes: `soma` das penas no concurso material; `aumento` sobre a pena mais grave no concurso formal e no crime continuado.

Se o resultado do script divergir do da decisão, não corrija em silêncio. A divergência é um achado: localize a etapa, mostre os dois números e diga qual operação a decisão parece ter feito.

Multa: informe `dias_multa_inicial` para acompanhar a mesma sequência. Se a decisão fixou a multa por outro critério, calcule-a à parte.

## Montar os cenários defensivos

Cada tese que altera uma etapa vira um cenário, com nome que diga a tese: "afastada a vetorial X", "majorante na fração mínima", "reconhecida a atenuante". Uma tese por cenário permite ver o efeito isolado de cada uma. Um cenário final pode reunir as teses compatíveis.

Informe os `limiares` relevantes para o caso. O script diz, para cada cenário, se a pena final fica acima, igual ou abaixo de cada um e a que distância. Isso mostra qual tese, sozinha, muda a consequência, e orienta a ordem dos pedidos subsidiários.

A comparação é numérica. A lei usa expressões diferentes em cada limiar, como "superior a", "não superior a" e "igual ou inferior a", e pena exatamente igual ao limiar pode cair de um lado ou de outro conforme o dispositivo. Leia o texto.

## Dispositivos lidos na formação desta versão

Lidos no Planalto, na versão compilada do Código Penal, em 11/11/2026. É um retrato para orientar a leitura e não dispensa a conferência na execução nem a análise da redação vigente na data do fato.

| Dispositivo | Conteúdo no retrato | Uso na conta |
|---|---|---|
| Art. 11 | Desprezam-se as frações de dia nas penas privativas de liberdade e restritivas de direitos | Convenção do script |
| Art. 33, § 2º | Pena superior a 8 anos: início em regime fechado. Não reincidente com pena superior a 4 e que não exceda 8: pode iniciar no semiaberto. Não reincidente com pena igual ou inferior a 4: pode iniciar no aberto | Limiares de 4 e 8 anos |
| Art. 44, I | Substituição quando a pena não é superior a 4 anos e o crime não foi cometido com violência ou grave ameaça, ou, qualquer que seja a pena, se culposo | Limiar de 4 anos |
| Art. 44, § 2º | Condenação igual ou inferior a 1 ano: multa ou uma restritiva; superior a 1 ano: uma restritiva e multa, ou duas restritivas | Limiar de 1 ano |
| Art. 69 | Concurso material: penas aplicadas cumulativamente | Operação `soma` |
| Art. 70 | Concurso formal: a mais grave das penas, ou uma delas se iguais, aumentada de um sexto até metade; cumulativamente se houver desígnios autônomos. A pena não pode exceder a que caberia pela regra do art. 69 | `aumento`; rode também o cenário da soma para conferir o limite |
| Art. 71 | Crime continuado: pena de um só dos crimes, ou a mais grave, aumentada de um sexto a dois terços. No parágrafo único, até o triplo, observados os arts. 70, parágrafo único, e 75 | `aumento` |
| Art. 75 | O tempo de cumprimento não pode ser superior a 40 anos | Redação da Lei 13.964/2019. Para fato anterior, confira a redação da época |
| Art. 77 | Suspensão condicional da pena não superior a 2 anos; no § 2º, não superior a 4 anos para maior de 70 ou por razões de saúde | Limiares de 2 e 4 anos |
| Art. 83 | Livramento condicional para pena igual ou superior a 2 anos | Limiar de 2 anos |
| Art. 109 | Faixas de pena que definem o prazo prescricional: 1, 2, 4, 8 e 12 anos | Limiares de prescrição pela pena em concreto |

O art. 109 pesa mais do que parece. Reduzir a pena de um crime para uma faixa menor reduz o prazo prescricional calculado pela pena em concreto. Quando um cenário cruza uma dessas faixas, rode a conta de prescrição com o novo prazo.

## O que a lei não fixa

A lei não traz fração para cada vetorial da primeira fase nem para agravantes e atenuantes da segunda. As frações usuais vêm da jurisprudência e variam. Não as apresente como regra legal: indique a fração que a decisão usou, a que a defesa sustenta e a orientação pesquisada que apoia cada uma.

Nas causas de aumento e de diminuição, o intervalo vem do tipo ou da norma específica. Leia o dispositivo e a redação da data do fato antes de escolher a fração do cenário.

## Erros que mudam o resultado

- Aplicar a fração da terceira fase sobre a pena-base, e não sobre o resultado da segunda fase, ou o inverso do que a decisão fez.
- Somar frações de etapas diferentes antes de aplicar, quando a decisão as aplicou em sequência.
- Arredondar para cima uma fração de dia.
- Usar o acréscimo do concurso de crimes para achar o prazo prescricional.
- Comparar com o limiar sem ler se a lei diz "superior a" ou "igual ou superior a".
- Tratar a soma do art. 69 como irrelevante no concurso formal, sem conferir o limite do parágrafo único do art. 70.

## Pistas de pesquisa

Não foram conferidas na formação desta versão e não são precedentes verificados. Pesquise o teor e a situação atual em fonte oficial.

- STJ, Súmula 231: atenuante e pena abaixo do mínimo legal.
- STJ, Súmula 443: fundamentação do aumento na terceira fase do roubo.
- STJ, Súmula 444: inquéritos e ações em curso na pena-base.
- STJ, Súmulas 269 e 440, e STF, Súmulas 718 e 719: regime inicial.
- Orientação atual do STJ sobre a fração por vetorial na primeira fase e por agravante ou atenuante na segunda.
- CPP, art. 387, § 2º: tempo de prisão provisória na fixação do regime inicial. Dispositivo não relido nesta formação.
