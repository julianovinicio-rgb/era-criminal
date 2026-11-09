# Trilha Criminal

Versão 0.4.0, destinada a teste privado e à futura distribuição aos alunos da Trilha Criminal.

O plugin reúne sete habilidades independentes. Use a função correspondente ao pedido, sem impor uma sequência obrigatória ou iniciar atividades não solicitadas.

| Trabalho | Habilidade |
|---|---|
| Estudar autos, confrontar provas, auditar atos e formular estratégia | Trilha Criminal Estudo de Caso |
| Atuar entre a prisão em flagrante e o fim da audiência de custódia, inclusive na primeira peça de liberdade | Trilha Criminal Flagrante e Custódia |
| Planejar, redigir, revisar ou atualizar uma peça defensiva, inclusive memoriais de alegações finais | Trilha Criminal Peças Defensivas |
| Preparar audiência de instrução, perguntas, interrogatório e alegações finais orais | Trilha Criminal Preparação de Audiência |
| Analisar a sentença, planejar, redigir ou revisar a apelação criminal | Trilha Criminal Recurso de Apelação |
| Analisar o constrangimento à liberdade, planejar, redigir, revisar ou atualizar HC, RHC e impugnações relacionadas | Trilha Criminal Habeas Corpus |
| Recurso especial, extraordinário, agravos, embargos, reclamação e tutela de urgência no STJ e no STF | Trilha Criminal Recursos nos Tribunais Superiores |

Preventiva decretada depois da custódia é tratada pelas habilidades de Habeas Corpus ou de Peças Defensivas. Habeas corpus e RHC permanecem na habilidade de Habeas Corpus, e a apelação permanece na habilidade própria.

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

## Conferência legislativa

Todas as habilidades têm o arquivo `references/conferencia-legislativa.md`, com conteúdo idêntico. Ele concentra a regra de conferência de artigos de lei: texto no portal oficial na versão compilada, acesso pelo navegador, análise da redação aplicável na data do fato e registro da data de conferência. Alterações futuras dessa regra devem ser feitas nesse arquivo em cada habilidade.

## Limites

Relatórios anteriores orientam o trabalho. Afirmações decisivas devem ser conferidas nas fontes acessíveis, com indicação das lacunas e do último ato abrangido. Um pedido de estudo não autoriza automaticamente redigir uma peça.

O pacote contém instruções e referências metodológicas. Não inclui autos, peças reais usadas como amostras, credenciais, catálogo de precedentes, servidor próprio ou ferramentas de protocolo. A leitura, o OCR, a pesquisa e a criação de arquivos dependem das capacidades disponíveis na conversa. Não configura por si só acesso a tribunais, protocolo, escuta automática ou monitoramento de audiência.

Toda jurisprudência é pesquisada e conferida na própria execução. Onde um dado não puder ser conferido, a entrega informa que está pendente de verificação.

Para documentos Word, use o timbrado aprovado quando disponível. O plugin não inclui timbrado de escritório nem uma ferramenta própria de edição de documentos.

As habilidades também podem ser chamadas explicitamente pelo nome disponível no seletor de habilidades. A instalação de um plugin é distinta da instalação avulsa de cada habilidade. O pacote é instalável no Claude e no Codex, com manifestos em `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` e `plugin.json`.

Autoria: Juliano Negreiros. Uso e distribuição sujeitos à autorização do titular.

## Histórico de versões

- **0.3.1:** incorporação do aperfeiçoamento do Habeas Corpus 1.1.0 a partir do capítulo de Badaró: cognição e prova documental, decisões anteriores, tutela liminar, habeas corpus coletivo e execução da ordem, com distinção entre doutrina e direito vigente. As outras quatro habilidades permaneceram inalteradas.
- **0.3.3:** acréscimos ao Habeas Corpus sobre resposta à orientação que dispensa a enumeração individual das medidas do art. 319; medidas protetivas e monitoração em violência doméstica; prisão mantida na pronúncia com RESE pendente; fase e data de precedentes e vigência de leis; dispensa de informações e vista obrigatória ao Ministério Público; e conferência de arquivos já editados pelo advogado.
- **0.3.4:** versão de base desta atualização. O pacote base não traz registro das mudanças em relação à 0.3.3; descrição pendente de verificação pelo autor.
- **0.4.0:** regra de conferência legislativa unificada em `references/conferencia-legislativa.md` em todas as habilidades, com análise da redação aplicável na data do fato, acesso pelo navegador e registro da data de conferência; links do CPP padronizados para a versão compilada; Peças Defensivas passa a incluir ataque por literalidade, estrutura de memorial de alegações finais e tabela de linguagem com limite de dois precedentes por tese; criação das habilidades Flagrante e Custódia e Recursos nos Tribunais Superiores; manifestos e README atualizados para sete habilidades.
