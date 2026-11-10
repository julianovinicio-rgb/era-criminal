# Registro de alterações

As versões anteriores à 0.4.1 estão resumidas no histórico do [README](README.md).

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
