# Script e convenções

Leia antes de executar qualquer comando. O script faz aritmética de datas, frações e penas. Ele não conhece a lei, o calendário do tribunal nem os autos: tudo isso entra como dado.

## Como executar

```
python scripts/calculos.py modelo <comando>               mostra um modelo de entrada
python scripts/calculos.py <comando> --entrada caso.json  calcula e imprime a memória
python scripts/calculos.py <comando> --entrada caso.json --formato json
python scripts/calculos.py autoteste                      confere o próprio script
```

Comandos: `prazo`, `prescricao`, `pena`, `execucao`, `remicao`, `periodos`. Prefira `--entrada` com arquivo. A opção `--json` aceita a entrada na linha de comando, mas as aspas costumam se perder no terminal.

Datas: `aaaa-mm-dd` ou `dd/mm/aaaa`. Durações: `5a4m10d`, `5 anos e 4 meses`, `64m`, `120d`. Frações: `1/6`, `25%`, `0,25`.

Toda `descricao` vai para a memória. Use-a para dizer o que é o marco e de onde ele vem, por exemplo "recebimento da denúncia (mov. 12.1)".

## O que o script recusa

Campo que ele não conhece, data que não existe, duração sem unidade, entrada obrigatória ausente, marcos fora de ordem e períodos de suspensão sobrepostos. Nesses casos ele não calcula e diz o motivo. A recusa protege contra erro silencioso, como um campo digitado errado que seria ignorado. Corrija a entrada com o documento.

## Convenções embutidas em cada comando

Estas regras estão no código porque são a própria forma de contar. A memória as repete, e cabe a quem executa conferir se são as do caso.

| Comando | Convenção |
|---|---|
| `prazo` | O dia do começo não é contado e o do vencimento é. A contagem começa no primeiro dia útil seguinte ao dia do começo. Na contagem contínua, sábados, domingos e dias sem expediente entram na conta, mas o prazo que termina em um deles passa ao dia útil imediato. Na suspensão, o prazo não corre e retoma no dia seguinte ao último dia suspenso. Com `disponibilizacao_dje`, a publicação é o primeiro dia útil seguinte à disponibilização, e a contagem começa no primeiro dia útil seguinte à publicação. |
| `prescricao` | O dia do começo entra na contagem, e anos e meses seguem o calendário. A cada marco interruptivo o prazo inteiro recomeça no dia do marco. Marco ocorrido até o último dia do prazo, inclusive, conta como ocorrido dentro dele. Na suspensão, o prazo não corre do dia de `inicio` até a véspera de `retomada`, e o saldo em anos, meses e dias volta a correr no dia da retomada. |
| `pena` | Pena convertida em dias com ano de 12 meses e mês de 30 dias, só para aplicar frações. Fração de dia desprezada a cada operação. Aumento multiplica por 1 + fração e diminuição por 1 − fração, na ordem informada. |
| `execucao` | Pena convertida em dias com ano de 365 e mês de 30, salvo outra `conversao` informada. O requisito de cada condenação é pena em dias vezes a fração, somado e arredondado uma só vez. Créditos abatem o requisito. O dia da data-base é contado. Interrupção vai do dia de `inicio` até a véspera de `retomada`. |
| `remicao` | Divisão inteira pela razão informada, com a sobra indicada. Acréscimo e perda aplicados sobre o total, com a fração de dia desprezada. |
| `periodos` | O dia inicial é contado. O dia final é contado, salvo `incluir_dia_final: false`. Dias repetidos entre períodos são apontados e contados uma vez no total. |

Onde a convenção é discutível, o script mostra a alternativa: o segundo critério de arredondamento na `execucao`, o segundo critério de contagem da suspensão na `prescricao`, o último dia do período e o dia seguinte na `execucao`.

## Campos de cada comando

Use `modelo <comando>` para ver a estrutura exata. Os campos em itálico são opcionais.

| Comando | Campos |
|---|---|
| `prazo` | `evento` (`tipo`: `intimacao` ou `disponibilizacao_dje`; `data`), `dias`, `contagem` (`corridos` ou `uteis`), *`dias_sem_expediente`*, *`suspensoes`* (`primeiro_dia`, `ultimo_dia`, `descricao`), *`descricao`* |
| `prescricao` | `prazo`, `termo_inicial` (`data`, `descricao`), *`multiplicadores`* (`fator`, `motivo`), *`marcos`* (`data`, `descricao`), *`suspensoes`* (`inicio`, `retomada`, `descricao`), *`data_corte`*, *`descricao`* |
| `pena` | `cenarios` (`nome`, `pena_inicial`, *`dias_multa_inicial`*, `operacoes`), *`limiares`*, *`descricao`*. Cada operação tem `tipo` (`aumento`, `diminuicao`, `soma`, `subtracao`, `fixar`), `descricao` e `fracao` ou `pena` |
| `execucao` | `data_base` (`data`, `descricao`), `parcelas` (`descricao`, `pena`, `fracao`), *`creditos`* (`descricao`, `dias`), *`interrupcoes`* (`inicio`, `retomada`, `descricao`), *`conversao`*, *`arredondamento`* (`desprezar` ou `cima`), *`termino`* (`pena`, `descricao`), *`data_corte`*, *`descricao`* |
| `remicao` | *`trabalho`* (`dias`, `dias_por_dia_remido`), *`estudo`* (`horas`, `horas_por_dia_remido`, *`acrescimo`*), *`outros`* (`descricao`, `dias`), *`perda`* (`fracao`, `descricao`), *`descricao`* |
| `periodos` | `periodos` (`inicio`, `fim`, `descricao`), *`incluir_dia_final`*, *`data_corte`*, *`descricao`* |

Em `suspensoes` da prescrição e em `interrupcoes` da execução, `retomada` vazia significa que a causa ainda dura: o script não projeta data e informa o saldo. Em `periodos`, `fim` vazio significa período em curso, contado até a `data_corte`.

Informe sempre `data_corte`, que é a data da análise. Sem ela o script usa a data do sistema e avisa.

## Limites

- O script não sabe quais dias não têm expediente. Sábados e domingos são tratados como não úteis; feriados, pontos facultativos e suspensões entram pela entrada, com base em lei ou em ato do tribunal. Dado esquecido só antecipa o resultado do prazo, nunca o adia. Dado incluído sem comprovação adia o resultado e é o erro perigoso.
- O script não calcula a intimação tácita em portal eletrônico. Informe a data de intimação certificada nos autos.
- O script não escolhe entre lei antiga e nova, não examina requisito subjetivo, vedação legal, falta grave nem cabimento.
- Uma conta por crime e por réu. Resultados de casos diferentes não se combinam na mesma entrada.
- A memória é projeção aritmética. Ela não é certidão, cálculo homologado nem reconhecimento de direito.

## Conta manual, quando não houver execução de código

Siga as mesmas convenções da tabela, escreva cada operação com as datas intermediárias e marque a entrega como `cálculo manual, não executado pelo script`. Em soma de meses, confira o último dia do mês de destino. Em contagem de dias, confira os anos bissextos do intervalo.
