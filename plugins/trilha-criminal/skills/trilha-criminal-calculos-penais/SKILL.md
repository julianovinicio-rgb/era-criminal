---
name: trilha-criminal-calculos-penais
description: "Calcula, com memória conferível, prescrição penal, prazos processuais, dosimetria e aritmética de pena, e requisitos temporais da execução (progressão, livramento, remição, detração e término de pena) em casos criminais brasileiros. Use quando o usuário pedir uma conta de datas, prazos, frações ou penas, quiser conferir a conta da dosimetria de uma sentença ou acórdão, o cálculo de cartório ou o do juízo da execução, ou perguntar se um crime prescreveu, quando vence um prazo já identificado ou quando o cliente atinge o requisito temporal de um benefício. Executa script próprio para a aritmética; prazo, fração, marcos e lei aplicável são conferidos em fonte oficial antes da conta. Não escolhe o recurso cabível, não redige peça e não substitui o cálculo homologado."
---

# Trilha Criminal Cálculos Penais

## Resultado e escopo

Entregue a conta pedida com uma memória de cálculo que o advogado consiga refazer: entradas com fonte, regra aplicada, operações, resultado e o que ainda precisa de confirmação.

O trabalho tem duas partes que não se misturam. A decisão jurídica vem antes: qual prazo, qual fração, qual marco, qual data-base, qual redação da lei. Ela é tomada com o documento e com a lei conferida em fonte oficial. A aritmética vem depois e é feita pelo script desta habilidade, nunca de cabeça.

Esta habilidade faz contas. Ela não decide qual recurso cabe, não redige peça, não declara prescrição reconhecida, benefício concedido ou data adquirida. O resultado é projeção aritmética sobre as entradas informadas, e é dito assim.

Funcione de forma autônoma ou a serviço de outra habilidade da Trilha. Quando a conta for parte de um estudo, de uma peça ou de um recurso, devolva a memória para ser usada lá, sem assumir o trabalho da outra habilidade.

## Escolher a conta

| Pedido | Comando do script | Referência a ler antes |
|---|---|---|
| Quando vence um prazo processual já identificado | `prazo` | [Prazos processuais](references/prazos-processuais.md) |
| Se e quando a pretensão punitiva ou a executória prescreve | `prescricao` | [Prescrição](references/prescricao.md) |
| Refazer ou comparar dosimetria, concurso de crimes e limiares de pena | `pena` | [Pena e dosimetria](references/pena-e-dosimetria.md) |
| Data do requisito temporal de progressão ou livramento, e término de pena | `execucao` | [Execução penal](references/execucao-penal.md) |
| Dias remidos por trabalho, estudo ou outra origem, e perda por falta | `remicao` | [Execução penal](references/execucao-penal.md) |
| Duração de uma prisão ou soma de períodos, para detração ou excesso de prazo | `periodos` | [Script e convenções](references/script-e-convencoes.md) |

Pergunta simples sobre a regra, como "qual o prazo da apelação?", não exige o script: responda com o dispositivo conferido. O script entra quando há data para somar, fração para aplicar ou períodos para comparar.

Conferir a conta de uma dosimetria é trabalho desta habilidade mesmo quando parece simples. Duas ou três frações em sequência já produzem erro de cabeça, e a divergência com a decisão precisa de memória que o advogado consiga refazer.

## Regras permanentes

- **Nenhuma conta de cabeça.** Soma de datas, fração de pena, contagem de dias e conversão entre anos, meses e dias passam pelo script. Se o ambiente não executa código, veja a etapa 3.
- **Nenhuma entrada presumida.** Data de intimação, publicação, recebimento da denúncia, trânsito em julgado, nascimento, prisão e soltura vêm de documento identificado. Faltando o documento, não há resultado definitivo: há cenário condicional, com a condição escrita, ou há pedido do dado.
- **Nenhum número legal de memória.** Prazo prescricional, fração de progressão, razão de remição, prazo recursal e forma de contagem são lidos na execução, conforme [Conferência legislativa](references/conferencia-legislativa.md), com atenção à redação vigente na data do fato. As tabelas desta habilidade são retratos datados que orientam a leitura e não a substituem.
- **Retrato não é conferência.** A data que aparece nas tabelas é a da formação desta habilidade, e não a da sua execução. Só escreva que um dispositivo foi conferido se você o abriu em fonte oficial agora. Se nenhuma fonte oficial abrir, faça a conta com o texto do retrato e registre na nota: `não reconferido nesta execução; texto do retrato da habilidade, datado de dd/mm/aaaa`. Nunca troque essa fórmula por "conferido no Planalto".
- **Súmula e julgado só de fonte oficial.** Site jurídico privado, blog e resumo de busca servem para localizar o enunciado ou o acórdão, não para afirmá-lo. O que entra na resposta foi aberto no portal do tribunal nesta execução, com classe, número e data, ou vem marcado como não conferido. As pistas de pesquisa das referências seguem a mesma regra.
- **Um cenário por premissa controvertida.** Se o termo inicial, a fração ou a data-base admite mais de uma leitura, rode cada uma, identifique a premissa de cada resultado e diga qual é a leitura defensiva sustentável e qual é a mais provável de ser adotada pelo juízo.
- **O resultado não é mais certo do que a entrada mais fraca.** Uma data informada pelo usuário sem documento contamina toda a conta, e a entrega diz isso.
- **Cálculo oficial se confere, não se copia.** Havendo cálculo do cartório, da sentença ou do juízo da execução, compare, localize a diferença e explique a causa, em vez de apresentar apenas outro total.

## Referências

| Referência | Quando consultar |
|---|---|
| [Script e convenções](references/script-e-convencoes.md) | Antes de executar qualquer comando: campos de entrada, convenções embutidas, recusas e limites |
| [Prescrição](references/prescricao.md) | Toda conta de prescrição |
| [Prazos processuais](references/prazos-processuais.md) | Toda contagem de prazo processual |
| [Pena e dosimetria](references/pena-e-dosimetria.md) | Conferência de dosimetria, concurso de crimes e limiares |
| [Execução penal](references/execucao-penal.md) | Progressão, livramento, remição, detração, data-base e término de pena |
| [Conferência legislativa](references/conferencia-legislativa.md) | Toda menção, citação, transcrição ou análise de artigo de lei brasileira |
| [Localização de documentos](references/localizacao-de-documentos.md) | Toda indicação de documento, trecho ou mídia dos autos |
| [Núcleo comum](references/nucleo-comum.md) | Regras de autorização, sigilo, nota ao advogado, estados de entrega e linguagem, iguais em toda a Trilha |
| [Exemplo de entrega](references/exemplo-de-entrega.md) | Calibrar formato, proporção e tom antes de entregar; exemplo fictício, cujos fatos e conclusões não se copiam |

## 1. Delimitar a conta e reunir as entradas

Identifique o que o advogado precisa decidir com o número: recorrer hoje ou amanhã, alegar prescrição, pedir progressão, impugnar a dosimetria. Isso define a conta e a precisão exigida.

Monte um quadro de entradas antes de qualquer operação: dado, valor, documento de origem com identificador do sistema e situação (confirmado no documento, informado pelo usuário, ausente). Separe data do ato, data da publicação, data da intimação e data da juntada, que produzem efeitos diferentes. Em processo com mais de um réu ou mais de um crime, a conta é individual.

Verifique cedo a urgência. Prazo que vence hoje ou nos próximos dias, ou prescrição a poucos dias de se consumar ou de ser interrompida, é dito no topo da resposta, antes da memória.

Pergunte apenas pelo dado que impede a conta. Com o restante, avance em cenário condicional.

## 2. Conferir a regra

Leia a referência do tipo de conta e confira na fonte oficial os dispositivos que definem cada entrada. Registre dispositivo, fonte aberta e data, para a nota ao advogado. Se o Planalto não abrir, tente a fonte oficial alternativa prevista na conferência legislativa. Se nenhuma abrir, a conta segue com o texto do retrato, e o dispositivo vai para a nota como não reconferido.

Compare a data do fato com a data de cada alteração legislativa relevante. Regra penal mais gravosa não alcança fato anterior, e a mais benéfica alcança. Se duas redações disputam a incidência, cada uma vira um cenário.

Quando a entrada depender de orientação de tribunal, como termo inicial da prescrição executória ou data-base após falta grave, pesquise a orientação atual em fonte oficial. As pistas de pesquisa das referências não são precedentes verificados. Sem pesquisa possível, mantenha o cenário e marque o ponto como pendente.

## 3. Executar o script

O script é [scripts/calculos.py](scripts/calculos.py), na pasta desta habilidade. Use o caminho completo da pasta em que este arquivo foi lido. Ele usa apenas a biblioteca padrão do Python.

1. Veja os campos do comando: `python scripts/calculos.py modelo prescricao`.
2. Grave a entrada do caso em um arquivo JSON, com a descrição de cada marco e de cada crédito.
3. Execute: `python scripts/calculos.py prescricao --entrada entrada.json`.

O script recusa campo desconhecido, data inexistente, períodos sobrepostos e entrada obrigatória ausente, e nesse caso não calcula. Corrija a entrada com o documento. Não contorne a recusa completando o dado por suposição.

Confira a seção de entradas da memória gerada contra o quadro da etapa 1 antes de usar o resultado: erro de digitação em data é a falha mais comum.

Se o ambiente não executa código, diga isso ao advogado, faça a conta à mão seguindo as convenções de [Script e convenções](references/script-e-convencoes.md), mostre cada operação e marque a entrega como `cálculo manual, não executado pelo script`, com recomendação de conferência antes do uso.

## 4. Ler o resultado e montar cenários

Leia os avisos da memória. Eles dizem o que o script não examinou.

Rode um cenário por premissa. Na prescrição, pena em abstrato e pena em concreto são cenários diferentes, assim como cada crime. Na execução, cada leitura da fração ou da data-base é um cenário. Na pena, cada tese que altera uma etapa é um cenário, comparado com os limiares que mudam regime, substituição ou prazo prescricional.

Resultado a poucos dias de um marco pede conferência redobrada das datas e do critério de contagem. Quando a memória apontar dois critérios com resultados diferentes, exponha os dois.

Não transforme o resultado em afirmação jurídica. "O prazo se esgotou em tal data, segundo estas entradas" é o que a conta permite. "A punibilidade está extinta" depende de decisão.

## 5. Entregar

Entregue, nesta ordem: a resposta em uma ou duas frases, com a urgência se houver; o quadro de entradas com as fontes; a memória de cálculo, que pode ser a gerada pelo script, enxugada ao que importa; os cenários lado a lado quando houver mais de um; e a nota ao advogado.

A nota ao advogado registra os dispositivos conferidos, com fonte e data, os que não foram reconferidos, as entradas sem documento, as premissas de cada cenário, a comparação com o cálculo oficial quando existir e as pendências, no formato `[CONFIRMAR: data da intimação do defensor]`. Súmula ou julgado citado traz o portal do tribunal em que foi aberto, ou a marca de não conferido.

A nota existe também na resposta curta. Nesse caso bastam duas linhas: o que foi conferido, onde e quando, e o que não foi.

Se a conta for para uma peça, o texto destinado ao juízo recebe apenas a demonstração necessária, com datas, operação e resultado. A memória completa e as ressalvas ficam na nota. Use um dos estados de entrega do núcleo comum e nenhum mais otimista do que a conferência feita.
