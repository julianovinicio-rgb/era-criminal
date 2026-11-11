# Prescrição

Use em toda conta de prescrição. A conta só começa depois de respondidas as perguntas abaixo, cada uma com documento ou dispositivo conferido. O script soma datas; quem escolhe prazo, termo inicial e marcos é a análise.

## Perguntas que definem as entradas

1. **Qual pretensão?** Punitiva, antes do trânsito em julgado, ou executória, depois dele.
2. **Qual pena regula o prazo?** O máximo cominado, antes de sentença com trânsito para a acusação, ou a pena aplicada, depois. A conta é feita crime a crime.
3. **Qual a data do fato e qual redação da lei incide?** As regras de prescrição mudaram mais de uma vez. Redação mais gravosa não alcança fato anterior.
4. **Qual o termo inicial?** Consumação, cessação da atividade ou da permanência, ou outra hipótese do art. 111. Na executória, a hipótese do art. 112, com a orientação atual pesquisada.
5. **Quais marcos interromperam o prazo, e em que data exata?** Recebimento da denúncia, e não oferecimento. Publicação da sentença, e não a data em que foi assinada. Cada data com o identificador do documento.
6. **Houve período em que o prazo não correu?** Suspensão do processo, acordo em cumprimento, outra causa legal, com data de início e de retomada.
7. **Há causa que altere o prazo?** Idade do acusado na data do fato ou da sentença, comprovada por documento. Reincidência, na executória.

Faltando resposta a alguma delas, a conta é condicional e a condição é escrita no resultado.

## Dispositivos lidos na formação desta versão

Lidos no Planalto, na versão compilada do Código Penal, em 11/11/2026. É um retrato para orientar a leitura. Não dispensa a conferência na execução, feita conforme [Conferência legislativa](conferencia-legislativa.md), nem a análise da redação vigente na data do fato.

| Dispositivo | Conteúdo no retrato | Atenção |
|---|---|---|
| Art. 109 | Antes do trânsito, o prazo regula-se pelo máximo da pena cominada: 20 anos se superior a 12; 16 se superior a 8 e não excede 12; 12 se superior a 4 e não excede 8; 8 se superior a 2 e não excede 4; 4 se igual a 1 ano ou, sendo superior, não excede 2; 3 anos se inferior a 1 ano | O inciso VI tem redação da Lei 12.234/2010. Para fato anterior, confira a redação da época |
| Art. 109, parágrafo único | Penas restritivas de direitos seguem os mesmos prazos | |
| Art. 110, caput | Depois do trânsito, regula-se pela pena aplicada, nos prazos do art. 109, aumentados de um terço se o condenado é reincidente | No script, multiplicador `4/3` |
| Art. 110, § 1º | Depois de sentença com trânsito para a acusação ou de improvido o recurso dela, regula-se pela pena aplicada e não pode ter por termo inicial data anterior à da denúncia ou queixa | Redação da Lei 12.234/2010, que também revogou o § 2º. Para fato anterior, analise a redação da época |
| Art. 111 | Termo inicial antes do trânsito: consumação; na tentativa, o dia em que cessou a atividade; no crime permanente, o dia em que cessou a permanência; bigamia e falsificação de registro civil, a data em que o fato se tornou conhecido; crimes contra a dignidade sexual ou com violência contra criança e adolescente, a data em que a vítima completar 18 anos, salvo se já proposta a ação | O inciso V tem redação da Lei 14.344/2022 |
| Art. 112 | Termo inicial depois da condenação: o dia em que transita em julgado a sentença para a acusação, ou a que revoga o sursis ou o livramento; ou o dia em que se interrompe a execução | O texto fala em trânsito para a acusação. Pesquise a orientação atual do STF sobre o tema antes de escolher a data |
| Art. 113 | Na evasão ou na revogação do livramento, a prescrição é regulada pelo tempo que resta da pena | O prazo muda: use a pena restante para achar o prazo |
| Art. 114 | Multa: 2 anos quando for a única cominada ou aplicada; o mesmo prazo da privativa de liberdade quando alternativa ou cumulativa | |
| Art. 115 | Prazos reduzidos de metade se o agente era menor de 21 anos ao tempo do crime ou maior de 70 na data da sentença, salvo se o crime envolver violência sexual contra a mulher | A ressalva final tem redação da Lei 15.160/2025. Compare a data do fato com a vigência dessa lei. No script, multiplicador `1/2` |
| Art. 116 | Antes do trânsito, a prescrição não corre: enquanto não resolvida questão prejudicial em outro processo; enquanto o agente cumpre pena no exterior; na pendência de embargos de declaração ou de recursos aos tribunais superiores, quando inadmissíveis; enquanto não cumprido ou não rescindido o acordo de não persecução penal | Incisos III e IV incluídos pela Lei 13.964/2019 |
| Art. 116, parágrafo único | Depois do trânsito, não corre enquanto o condenado está preso por outro motivo | |
| Art. 117 | Interrompem: recebimento da denúncia ou queixa; pronúncia; decisão confirmatória da pronúncia; publicação da sentença ou acórdão condenatórios recorríveis; início ou continuação do cumprimento da pena; reincidência | O inciso IV tem redação da Lei 11.596/2007 |
| Art. 117, §§ 1º e 2º | A interrupção alcança todos os autores, salvo nos incisos V e VI. Interrompida a prescrição, todo o prazo recomeça do dia da interrupção, salvo no inciso V | |
| Art. 118 | As penas mais leves prescrevem com as mais graves | |
| Art. 119 | No concurso de crimes, a extinção da punibilidade incide sobre a pena de cada um, isoladamente | Uma conta por crime |
| Art. 10 | O dia do começo inclui-se no prazo; dias, meses e anos contam-se pelo calendário comum | É a convenção do script |

Fora do Código Penal, lidos na mesma data: o art. 366 do CPP suspende o processo e o prazo prescricional quando o acusado citado por edital não comparece nem constitui advogado; o art. 89, § 6º, da Lei 9.099/1995 diz que não corre a prescrição durante a suspensão condicional do processo.

## Montar os cenários

Rode um cenário para cada prazo e para cada crime. Os mais comuns:

| Cenário | Prazo | Termo inicial e marcos |
|---|---|---|
| Pretensão punitiva pela pena em abstrato | O do art. 109 para o máximo cominado, com as causas de aumento e de diminuição que alteram esse máximo conforme a orientação pesquisada | Termo inicial do art. 111; marcos do art. 117, I a IV, na ordem em que ocorreram; data de corte |
| Pretensão punitiva pela pena em concreto | O do art. 109 para a pena aplicada ao crime, sem o acréscimo do concurso | Exige trânsito para a acusação ou recurso dela improvido. Examine cada intervalo entre marcos já ocorridos, respeitado o limite do art. 110, § 1º, na redação aplicável ao fato |
| Depois da sentença condenatória | O mesmo da pena em concreto | Início na publicação da sentença ou do acórdão condenatório; verifique os incisos III e IV do art. 116 |
| Pretensão executória | O do art. 109 para a pena aplicada, com o multiplicador `4/3` se reincidente | Termo inicial do art. 112; marcos do art. 117, V e VI; suspensão do art. 116, parágrafo único |
| Evasão ou revogação do livramento | O do art. 109 para o tempo que resta da pena | Início no dia da evasão ou da revogação |

Entre dois cenários que usam prazos diferentes, compare os resultados lado a lado. A pena em concreto costuma abrir prescrição em intervalo que a pena em abstrato não alcança.

Suspensão por tempo indeterminado é informada com `retomada` vazia. Se houver limite de duração da suspensão segundo a orientação pesquisada, informe a data em que ele se completa como `retomada` e diga isso na descrição.

## Erros que mudam o resultado

- Usar o oferecimento da denúncia no lugar do recebimento, ou a data da sentença no lugar da publicação.
- Somar as penas do concurso de crimes para achar o prazo.
- Aplicar a metade do art. 115 sem documento de idade, ou sem verificar a ressalva introduzida em 2025.
- Aumentar de um terço, pela reincidência, o prazo da pretensão punitiva. O art. 110 fala em prescrição depois do trânsito.
- Contar tempo em que o prazo estava suspenso.
- Tratar acórdão que apenas confirma a condenação como irrelevante ou como marco, sem pesquisar a orientação atual.
- Aplicar a redação atual do art. 110, § 1º, a fato anterior à Lei 12.234/2010 sem examinar a redação da época.

## Pistas de pesquisa

Não foram conferidas na formação desta versão. Servem para orientar a busca em fonte oficial e não são precedentes verificados. Pesquise o teor e a situação atual de cada uma antes de usar.

- STF, Súmula 146: prescrição pela pena concretizada quando não há recurso da acusação.
- STF, Súmula 497: no crime continuado, prescrição pela pena imposta, sem o acréscimo da continuação.
- STJ, Súmula 191: efeito interruptivo da pronúncia mesmo com desclassificação posterior pelo júri.
- STJ, Súmula 220: reincidência e prazo da prescrição da pretensão punitiva.
- STJ, Súmula 415: limite do período de suspensão do prazo prescricional.
- STJ, Súmula 438: prescrição com base em pena hipotética.
- STF, tema de repercussão geral sobre o termo inicial da prescrição da pretensão executória (art. 112, I).
- STF, tema de repercussão geral sobre o limite da suspensão do art. 366 do CPP.
- STF e STJ, orientação sobre o acórdão confirmatório da condenação como marco interruptivo (art. 117, IV).
