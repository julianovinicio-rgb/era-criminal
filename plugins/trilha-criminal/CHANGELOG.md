# Registro de alterações

As versões anteriores à 0.4.1 estão resumidas no histórico do [README](README.md).

## 0.8.1

Correções na habilidade Cálculos Penais, a partir da primeira execução dos casos de teste, em 11/11/2026. O script não mudou.

- O retrato datado das referências não pode ser apresentado como conferência da execução. A regra entra no `SKILL.md` e na abertura de cada retrato, com a fórmula a usar na nota quando nenhuma fonte oficial abrir. Motivo: em um dos casos, a resposta afirmou conferência no Planalto sem ter aberto o site.
- A descrição da habilidade passa a citar dosimetria e a conferência da conta de sentença ou acórdão. Motivo: o pedido de conferir a conta da pena não a acionou. Mudança de comportamento: a habilidade tende a entrar em mais pedidos sobre dosimetria. A crítica jurídica da dosimetria continua em Recurso de Apelação e em Peças Defensivas.
- Súmula e julgado só entram na resposta a partir do portal do tribunal, ou marcados como não conferidos. Site jurídico privado serve para localizar. Motivo: quase todas as respostas citaram julgados por sites privados.
- A nota ao advogado passa a ser exigida também na resposta curta, em duas linhas.
- Pendência conhecida, não tratada nesta versão: o caso de teste A8, de recurso contra decisão de relator do STJ, não acionou Recursos nos Tribunais Superiores.
- Estas correções ainda não foram testadas em conversa.
- Fora do pacote: `testes/casos-de-teste.md` registra a execução de nove casos na 0.8.0 e os achados.

## 0.8.0

Nova habilidade e primeiro script do pacote.

- Nova habilidade Trilha Criminal Cálculos Penais: prescrição, prazos processuais, aritmética de pena e requisitos temporais da execução, com memória de cálculo. A decisão jurídica (prazo, fração, marcos, data-base e lei aplicável) é tomada antes, com documento e lei conferida. A aritmética é feita por script.
- Novo `scripts/calculos.py` na habilidade, só com a biblioteca padrão do Python, com seis comandos (`prazo`, `prescricao`, `pena`, `execucao`, `remicao` e `periodos`) e autoteste. Nenhum prazo, fração ou percentual legal está fixado no código: entram como dado. O script recusa campo desconhecido, data inexistente e períodos sobrepostos.
- Os dispositivos das referências novas foram lidos no Planalto em 11/11/2026 e estão registrados como retrato datado, que não dispensa a conferência na execução: Código Penal, arts. 10, 11, 33, 42, 44, 69 a 71, 75, 77, 83 e 109 a 119; LEP, arts. 111, 112, 126 a 128 e 197; CPP, arts. 366, 392, 396, 403, 406, 586, 588, 593, 600, 609, 619, 798 e 798-A; Lei 9.099/1995, arts. 82, 83 e 89; Lei 11.419/2006, arts. 4º e 5º. Súmulas, temas e orientações de tribunais citados nessas referências são pistas de pesquisa e não foram conferidos.
- Achado da leitura: o art. 112 da LEP foi alterado pelas Leis 15.358 e 15.402, de 2026, e o art. 115 do Código Penal pela Lei 15.160, de 2025. As referências novas registram as duas mudanças. O mapa de institutos de `pecas/execucao-penal.md` já mandava conferir a redação e não foi alterado.
- Remissões à nova habilidade em Estudo de Caso, Peças Defensivas (inclusive no módulo de execução penal), Recurso de Apelação, Habeas Corpus e Recursos nos Tribunais Superiores.
- Mudança de comportamento: a descrição da nova habilidade pode acioná-la em perguntas sobre prescrição e contagem de prazo que antes eram respondidas sem habilidade ou por outra. A escolha do recurso cabível continua nas habilidades próprias.
- Limite conhecido: o script depende de execução de código na conversa. Sem ela, a habilidade orienta a conta manual pelas mesmas convenções e marca a entrega como não executada pelo script.
- Fora do pacote: `ferramentas/verificar.py` passa a exigir os arquivos comuns nas oito habilidades e a rodar o autoteste dos scripts; `ferramentas/empacotar.py` deixa de fora os arquivos de cache do Python. `testes/casos-de-teste.md` ganha casos de acionamento e da nova habilidade. A bateria continua não executada.

## 0.7.0

Qualidade e distribuição. Nenhuma regra de método foi alterada.

- Cada habilidade ganha `references/exemplo-de-entrega.md`, com um exemplo inteiramente fictício de entrega para calibrar formato, proporção e tom.
- Novo `GUIA-DE-INICIO.md`, para quem acabou de instalar o plugin.
- Novo `LICENSE.md`, texto-base de condições de uso, pendente de revisão do titular.
- Fora do pacote: `testes/casos-de-teste.md`, bateria manual de acionamento, regras comuns e casos por habilidade. Ainda não executada.

## 0.6.0

Ampliação de cobertura. Todo dispositivo, súmula ou tema citado nos módulos novos é localizador para conferência na execução; nenhum foi reaberto em fonte oficial na formação desta versão.

- Peças Defensivas: novo módulo `pecas/justica-negociada.md` para acordo de não persecução penal, transação penal e suspensão condicional do processo, com quadro comparativo para a decisão do cliente. Colaboração premiada permanece fora do escopo.
- Peças Defensivas: `pecas/tribunal-do-juri.md` ganha a tabela de peças da segunda fase; `pecas/execucao-penal.md` ganha o mapa de institutos, o agravo em execução e o habeas corpus na execução.
- Preparação de Audiência: novo módulo `plenario-do-juri.md` (calendário de providências, jurados, instrução, debates, quesitos e ata). A descrição da habilidade passa a mencionar o plenário, o que amplia seu acionamento.
- Recurso de Apelação, Habeas Corpus e Recursos nos Tribunais Superiores: novo módulo `sustentacao-oral.md`, idêntico nas três.
- Decisão de projeto: júri e execução penal continuam como módulos, e não como habilidades próprias.

## 0.5.0

Consistência entre as habilidades.

- Novo `references/nucleo-comum.md`, idêntico nas sete habilidades: autorização e sigilo, limites de afirmação, peça e nota ao advogado, estados de entrega, linguagem e formato. Regra específica da habilidade prevalece.
- Mudança de comportamento: a preferência de parágrafo com no máximo um ponto seguido interno, antes presente só em Habeas Corpus e Apelação, passa a valer para todo texto escrito destinado ao juízo. Não se aplica a citações nem a roteiros de fala.
- Mudança de comportamento: os estados de entrega (minuta elaborada, revisada no escopo indicado, com pendências), antes só no Habeas Corpus, passam a valer em todas as habilidades.
- Habeas Corpus: os julgados e normas lidos na formação saem de `base-badaro.md` e `fontes-de-partida.md` e vão para `pistas-de-pesquisa.md`, com data de formação e validade de doze meses.
- Recursos nos Tribunais Superiores: a matriz de prazos passa a trazer valores de referência (REsp, RE, agravos, embargos), sempre marcados como a confirmar. O ponto de atenção sobre decisão da Presidência foi reescrito em termos gerais.
- Recurso de Apelação: retirada a menção ao caso que inspirou a habilidade.
- Peças Defensivas: os módulos de ações autônomas e de liberdade remetem ao Habeas Corpus quando disponível.
- Fora do pacote: `ferramentas/verificar.py` e `ferramentas/empacotar.py` conferem cópias compartilhadas, links, manifestos e geram o zip.

## 0.4.1

Correções de consistência entre as habilidades. Nenhuma mudança de método, de escopo ou de acionamento.

### Conferência legislativa

- `references/conferencia-legislativa.md`, idêntico nas sete habilidades, passa a prever ordem de fontes: Planalto na versão compilada; outra fonte oficial (Senado, Câmara, LexML ou Diário Oficial da União) quando o Planalto não puder ser aberto; texto oficial fornecido pelo usuário.
- O registro da conferência indica a fonte efetivamente aberta e a data, e fica na nota ao advogado ou na seção de fontes do relatório, não no texto destinado ao juízo.
- Sem fonte oficial acessível, o ponto é marcado na minuta como `[CONFIRMAR: ...]`.
- A rotina passa a mencionar expressamente a Constituição, regimentos, resoluções e súmulas.

### Localização de documentos

- Novo arquivo `references/localizacao-de-documentos.md`, idêntico nas sete habilidades.
- Na peça, apenas o identificador do sistema de origem (movimento, ID, evento ou folha). Em relatórios e notas, o identificador e, quando útil, a página do arquivo rotulada como tal.
- Ajustados os trechos que traziam regras diferentes: Estudo de Caso (`SKILL.md`), Flagrante e Custódia (triagem e entregas), Habeas Corpus (confronto literal e triagem), Peças Defensivas (construção argumentativa, fontes e alegações finais), Preparação de Audiência (planejamento) e Recurso de Apelação (`SKILL.md`, sentença e prova, revisão).
- Mudança de comportamento na Apelação: a regra anterior vedava a página do PDF também na nota ao advogado e citava apenas "movimento". Agora a página pode aparecer na nota, rotulada, e o identificador segue o sistema do processo.

### Fontes

- Preparação de Audiência: links do CPP e da Lei 9.099/1995 passam do portal da Câmara para o Planalto.
- Habeas Corpus: `regimentos-tribunais.md` e `fontes-de-partida.md` passam a tratar do tribunal local de forma geral, mantendo o TJAM como exemplo de ficha preenchida.

### Empacotamento

- Logo reduzido de 1254 px para 512 px e cópia duplicada removida. O pacote cai de cerca de 2,3 MB para menos de 0,6 MB.
- `agents/openai.yaml` de Peças Defensivas, Preparação de Audiência e Recurso de Apelação recebem o bloco `policy` já presente nas demais.
- Versão 0.4.1 nos três manifestos.
