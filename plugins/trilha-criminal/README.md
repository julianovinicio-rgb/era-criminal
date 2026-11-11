# Trilha Criminal

Versão 0.8.0, destinada a teste privado e à futura distribuição aos alunos da Trilha Criminal.

O plugin reúne oito habilidades independentes. Use a função correspondente ao pedido, sem impor uma sequência obrigatória ou iniciar atividades não solicitadas.

| Trabalho | Habilidade |
|---|---|
| Estudar autos, confrontar provas, auditar atos e formular estratégia | Trilha Criminal Estudo de Caso |
| Atuar entre a prisão em flagrante e o fim da audiência de custódia, inclusive na primeira peça de liberdade | Trilha Criminal Flagrante e Custódia |
| Planejar, redigir, revisar ou atualizar uma peça defensiva, inclusive memoriais de alegações finais | Trilha Criminal Peças Defensivas |
| Preparar audiência de instrução, perguntas, interrogatório e alegações finais orais, e o plenário do júri | Trilha Criminal Preparação de Audiência |
| Analisar a sentença, planejar, redigir ou revisar a apelação criminal | Trilha Criminal Recurso de Apelação |
| Analisar o constrangimento à liberdade, planejar, redigir, revisar ou atualizar HC, RHC e impugnações relacionadas | Trilha Criminal Habeas Corpus |
| Recurso especial, extraordinário, agravos, embargos, reclamação e tutela de urgência no STJ e no STF | Trilha Criminal Recursos nos Tribunais Superiores |
| Calcular prescrição, prazo processual, pena e requisito temporal da execução, com memória de cálculo | Trilha Criminal Cálculos Penais |

Preventiva decretada depois da custódia é tratada pelas habilidades de Habeas Corpus ou de Peças Defensivas. Habeas corpus e RHC permanecem na habilidade de Habeas Corpus, e a apelação permanece na habilidade própria. A habilidade de Cálculos Penais faz a conta; a escolha do recurso cabível continua na habilidade do recurso.

Quem está começando deve ler o [Guia de início](GUIA-DE-INICIO.md). As condições de uso estão em [LICENSE.md](LICENSE.md).

## Exemplos de uso

- “Estude este processo. Meu cliente é [nome]. Meu objetivo é [objetivo].”
- “Meu cliente foi preso em flagrante há três horas. Faça a triagem do auto e prepare o roteiro da audiência de custódia.”
- “Com base no auto de prisão, redija o pedido de relaxamento ou de liberdade provisória para o juízo da custódia.”
- “Planeje o pedido de revogação da prisão, sem redigir ainda.”
- “Redija os memoriais de alegações finais com base nos documentos deste caso.”
- “Revise juridicamente esta apelação e a correspondência entre fundamentos e pedidos.”
- “Prepare as perguntas por depoente e os cenários de encerramento da audiência.”
- “Analise o cabimento e planeje o habeas corpus deste paciente, sem redigir ainda.”
- “Identifique o recurso cabível e o prazo contra esta decisão monocrática do STJ e redija o agravo.”
- “Revise este recurso especial quanto a prequestionamento, Súmula 7 e impugnação de todos os fundamentos do acórdão.”
- “Calcule se este crime prescreveu, com os marcos destes documentos, e mostre a memória de cálculo.”
- “Confira a dosimetria desta sentença e diga qual tese leva a pena para até quatro anos.”

## Cálculos e script

A habilidade Cálculos Penais traz o arquivo `scripts/calculos.py`, que faz a aritmética de datas, frações e penas e devolve uma memória de cálculo. Ele usa apenas a biblioteca padrão do Python e tem seis comandos: `prazo`, `prescricao`, `pena`, `execucao`, `remicao` e `periodos`.

Nenhum prazo, fração ou percentual legal está fixado no código. Esses valores entram como dado, depois de conferidos em fonte oficial na execução, e o script recusa entrada incompleta ou incoerente em vez de completá-la. As tabelas das referências dessa habilidade são retratos datados da lei e não dispensam a conferência.

A execução do script depende de a conversa permitir execução de código. Sem isso, a habilidade orienta a conta manual pelas mesmas convenções e marca a entrega como não executada pelo script.

## Conferência legislativa

Todas as habilidades têm o arquivo `references/conferencia-legislativa.md`, com conteúdo idêntico. Ele concentra a regra de conferência de artigos de lei: texto em fonte oficial na própria execução, com preferência pelo Planalto na versão compilada e, se ele não puder ser aberto, outra fonte oficial identificada; análise da redação aplicável na data do fato; e registro da fonte e da data na nota ao advogado, fora do texto destinado ao juízo. Alterações futuras dessa regra devem ser feitas nesse arquivo em cada habilidade.

## Núcleo comum

Todas as habilidades têm o arquivo `references/nucleo-comum.md`, com conteúdo idêntico: autorização e sigilo, limites de afirmação, separação entre peça e nota ao advogado, estados de entrega e linguagem. Regra mais específica de cada habilidade prevalece sobre ele.

## Localização de documentos

Todas as habilidades têm também o arquivo `references/localizacao-de-documentos.md`, com conteúdo idêntico. Ele define como indicar documentos, trechos e mídias dos autos: na peça, apenas o identificador do sistema de origem (movimento no Projudi, ID no PJe, evento no eproc, folha no e-SAJ e em autos físicos); em relatórios e notas ao advogado, o identificador e, quando útil, a página do arquivo rotulada como tal. A preferência expressa do usuário prevalece.

## Limites

Relatórios anteriores orientam o trabalho. Afirmações decisivas devem ser conferidas nas fontes acessíveis, com indicação das lacunas e do último ato abrangido. Um pedido de estudo não autoriza automaticamente redigir uma peça.

O pacote contém instruções, referências metodológicas e o script de cálculo da habilidade Cálculos Penais. Não inclui autos, peças reais usadas como amostras, credenciais, catálogo de precedentes verificados, servidor próprio ou ferramentas de protocolo. A leitura, o OCR, a pesquisa e a criação de arquivos dependem das capacidades disponíveis na conversa. Não configura por si só acesso a tribunais, protocolo, escuta automática ou monitoramento de audiência.

Toda jurisprudência é pesquisada e conferida na própria execução. Os poucos julgados lidos na formação do Habeas Corpus ficam em `pistas-de-pesquisa.md`, com data e validade, apenas como ponto de partida. Onde um dado não puder ser conferido, a entrega informa que está pendente de verificação.

Para documentos Word, use o timbrado aprovado quando disponível. O plugin não inclui timbrado de escritório nem uma ferramenta própria de edição de documentos.

As habilidades também podem ser chamadas explicitamente pelo nome disponível no seletor de habilidades. A instalação de um plugin é distinta da instalação avulsa de cada habilidade. O pacote é instalável no Claude e no Codex, com manifestos em `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` e `plugin.json`.

Autoria: Juliano Negreiros. Uso e distribuição sujeitos à autorização do titular, nos termos de [LICENSE.md](LICENSE.md).

## Histórico de versões

- **0.3.1:** incorporação do aperfeiçoamento do Habeas Corpus 1.1.0 a partir do capítulo de Badaró: cognição e prova documental, decisões anteriores, tutela liminar, habeas corpus coletivo e execução da ordem, com distinção entre doutrina e direito vigente. As outras quatro habilidades permaneceram inalteradas.
- **0.3.3:** acréscimos ao Habeas Corpus sobre resposta à orientação que dispensa a enumeração individual das medidas do art. 319; medidas protetivas e monitoração em violência doméstica; prisão mantida na pronúncia com RESE pendente; fase e data de precedentes e vigência de leis; dispensa de informações e vista obrigatória ao Ministério Público; e conferência de arquivos já editados pelo advogado.
- **0.3.4:** versão de base desta atualização. O pacote base não traz registro das mudanças em relação à 0.3.3; descrição pendente de verificação pelo autor.
- **0.4.0:** regra de conferência legislativa unificada em `references/conferencia-legislativa.md` em todas as habilidades, com análise da redação aplicável na data do fato, acesso pelo navegador e registro da data de conferência; links do CPP padronizados para a versão compilada; Peças Defensivas passa a incluir ataque por literalidade, estrutura de memorial de alegações finais e tabela de linguagem com limite de dois precedentes por tese; criação das habilidades Flagrante e Custódia e Recursos nos Tribunais Superiores; manifestos e README atualizados para sete habilidades.
- **0.4.1:** correções de consistência, sem mudança de método. Conferência legislativa passa a admitir fonte oficial alternativa identificada e registra a conferência na nota ao advogado; convenção única de localização de documentos em todas as habilidades; links de legislação da skill de Audiência apontados para o Planalto; regimento do tribunal local generalizado no Habeas Corpus, com o TJAM como exemplo; logo reduzido. Detalhes em [CHANGELOG.md](CHANGELOG.md).
- **0.5.0:** núcleo comum de regras em todas as habilidades; julgados datados do Habeas Corpus reunidos em pistas de pesquisa com validade; matriz de prazos dos tribunais superiores com valores de referência a confirmar; remissões entre Peças Defensivas e as habilidades especializadas.
- **0.6.0:** ampliação de cobertura. Peças Defensivas ganha o módulo de justiça negociada (acordo de não persecução penal, transação e suspensão condicional do processo) e amplia os de júri e de execução penal; Preparação de Audiência ganha o módulo de plenário do júri; Apelação, Habeas Corpus e Recursos nos Tribunais Superiores ganham o módulo de sustentação oral.
- **0.7.0:** um exemplo fictício de entrega em cada habilidade, guia de início para quem instala o plugin e arquivo de condições de uso.
- **0.8.0:** nova habilidade Cálculos Penais, com script próprio para prescrição, prazos processuais, pena e execução, e remissões a ela nas demais habilidades.
