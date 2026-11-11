# Prazos processuais

Use em toda contagem de prazo processual. Esta referência trata da contagem. A escolha do recurso e de seu cabimento pertence à habilidade do recurso: Recurso de Apelação, Habeas Corpus, Recursos nos Tribunais Superiores ou Peças Defensivas.

## Entradas e de onde vêm

| Entrada | Fonte exigida |
|---|---|
| Ato que abre o prazo | A decisão, a sentença ou o acórdão |
| Forma e data da intimação | Certidão, mandado cumprido, termo de audiência, registro do sistema ou edição do diário eletrônico. Data do julgamento não é data de intimação |
| Quem foi intimado e quando | Em sentença condenatória, verifique a intimação do réu e a do defensor, e pesquise de qual delas o prazo corre no caso |
| Prazo em dias | O dispositivo que o fixa, lido na execução |
| Forma de contagem | A norma que a determina. No processo penal, a do art. 798 do CPP, salvo regra específica identificada |
| Dias sem expediente e suspensões | Lei ou ato do tribunal competente: calendário forense, portaria, resolução |
| Situação do réu | Réu preso afasta a suspensão de fim de ano, conforme o art. 798-A |

Sem a certidão de intimação, não há termo final: há simulação condicional, dita como tal.

## Dispositivos lidos na formação desta versão

Lidos no Planalto em 11/11/2026. É um retrato para orientar a leitura e não dispensa a conferência na execução.

| Dispositivo | Conteúdo no retrato |
|---|---|
| CPP, art. 798, caput | Os prazos são contínuos e peremptórios e não se interrompem por férias, domingo ou feriado |
| CPP, art. 798, § 1º | Não se computa o dia do começo; inclui-se o do vencimento |
| CPP, art. 798, § 3º | O prazo que termina em domingo ou feriado considera-se prorrogado até o dia útil imediato |
| CPP, art. 798, § 4º | Não correm os prazos se houver impedimento do juiz, força maior ou obstáculo judicial oposto pela parte contrária |
| CPP, art. 798, § 5º | Salvo os casos expressos, os prazos correm da intimação; da audiência ou sessão em que for proferida a decisão, se a parte estiver presente; ou do dia em que a parte manifestar ciência inequívoca nos autos |
| CPP, art. 798-A | Suspende-se o curso do prazo processual de 20 de dezembro a 20 de janeiro, inclusive, salvo: processos com réus presos, vinculados a essas prisões; procedimentos da Lei Maria da Penha; medidas urgentes, por despacho fundamentado. Incluído pela Lei 14.365/2022 |
| CPP, art. 392, §§ 1º e 2º | Intimação da sentença por edital: prazo do edital de 90 ou 60 dias, e o prazo da apelação corre depois dele |
| Lei 11.419/2006, art. 4º, §§ 3º e 4º | Considera-se data da publicação o primeiro dia útil seguinte ao da disponibilização no diário eletrônico, e os prazos têm início no primeiro dia útil que seguir ao da publicação |
| Lei 11.419/2006, art. 5º, §§ 1º a 3º | Em portal próprio, a intimação se considera realizada no dia da consulta; se a consulta ocorrer em dia não útil, no primeiro dia útil seguinte; a consulta deve ocorrer em até 10 dias corridos do envio, sob pena de a intimação se considerar realizada no término desse prazo |

## Prazos frequentes no retrato

Valores lidos no Planalto em 11/11/2026. Servem para alertar sobre urgência. Antes de afirmar o prazo ao advogado, leia o dispositivo na execução e confira se há regra especial para o rito, para o tribunal ou para a parte.

| Ato | Prazo no retrato | Dispositivo |
|---|---|---|
| Resposta à acusação, ritos ordinário e sumário | 10 dias | CPP, art. 396 |
| Resposta à acusação, primeira fase do júri | 10 dias | CPP, art. 406 |
| Memoriais, quando concedidos | 5 dias, sucessivamente | CPP, art. 403, § 3º |
| Apelação, interposição | 5 dias | CPP, art. 593 |
| Apelação, razões | 8 dias; 3 dias nos processos de contravenção | CPP, art. 600 |
| Recurso em sentido estrito, interposição | 5 dias | CPP, art. 586 |
| Recurso em sentido estrito, razões | 2 dias | CPP, art. 588 |
| Embargos infringentes e de nulidade | 10 dias da publicação do acórdão | CPP, art. 609, parágrafo único |
| Embargos de declaração contra acórdão | 2 dias da publicação | CPP, art. 619 |
| Apelação no juizado especial criminal | 10 dias, com as razões | Lei 9.099/1995, art. 82, § 1º |
| Embargos de declaração no juizado especial criminal | 5 dias | Lei 9.099/1995, art. 83, § 1º |

O art. 197 da LEP, lido na mesma data, prevê o agravo em execução sem fixar o prazo no texto: o prazo vem de súmula, a conferir. Prazos no STJ e no STF estão na matriz da habilidade Recursos nos Tribunais Superiores. Embargos de declaração contra sentença, habeas corpus, revisão criminal e demais atos não listados aqui são conferidos na fonte.

## Passar a contagem ao script

- Intimação pessoal, em audiência, por mandado ou certificada em portal eletrônico: `evento.tipo` igual a `intimacao`, com a data da certidão.
- Publicação em diário eletrônico: `evento.tipo` igual a `disponibilizacao_dje`, com a data da disponibilização. O script acha a publicação e o início da contagem.
- Intimação tácita em portal: o script não calcula os 10 dias. Use a data que o sistema certificou.
- `contagem`: `corridos` é a contagem contínua do art. 798. Use `uteis` apenas quando uma norma determinar dias úteis no caso, e indique a norma na nota.
- `dias_sem_expediente`: cada data com a origem na descrição. O script já trata sábado e domingo.
- `suspensoes`: informe a suspensão de fim de ano somente se o caso não estiver nas exceções do art. 798-A. Processo com réu preso não tem essa suspensão.
- Prazo em dobro ou outra prerrogativa: informe `dias` já ajustado e registre o fundamento.

Dia sem expediente esquecido só antecipa o resultado. Dia incluído sem comprovação o adia, e é esse o erro que perde prazo. Na dúvida sobre um feriado local, rode sem ele e trate a data mais próxima como o termo a cumprir.

## Prazo material não é prazo processual

Decadência, prescrição, duração da pena, período de prova e prazo de prisão seguem o art. 10 do Código Penal: o dia do começo é contado, e o prazo não se prorroga por feriado ou fim de semana. Não use o comando `prazo` para eles. Use `prescricao`, `execucao` ou `periodos`.

## Erros que perdem prazo

- Contar da juntada do mandado ou do aviso de recebimento, quando a regra é contar da intimação.
- Contar em dias úteis um prazo penal sem norma que autorize.
- Aplicar a suspensão de fim de ano a processo de réu preso.
- Confundir disponibilização com publicação no diário eletrônico.
- Tomar a data da sessão de julgamento como intimação do acórdão.
- Esquecer que interposição e razões têm prazos distintos na apelação e no recurso em sentido estrito.
- Supor intimação do réu quando só o defensor foi intimado, ou o contrário.

## Pistas de pesquisa

Não foram conferidas na formação desta versão e não são precedentes verificados. Pesquise o teor e a situação atual em fonte oficial.

- STF, Súmula 310: intimação na sexta-feira e início do prazo.
- STF, Súmula 710: no processo penal, os prazos contam-se da data da intimação.
- STF, Súmula 700: prazo do agravo em execução.
- Prazo em dobro da Defensoria Pública: Lei Complementar 80/1994 e orientação atual do tribunal.
- Intimação do réu e do defensor da sentença condenatória: de qual delas corre o prazo.
- Normas do Conselho Nacional de Justiça e do tribunal sobre comunicação eletrônica e diário de justiça eletrônico nacional.
