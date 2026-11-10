# Registro de alterações

As versões anteriores à 0.4.1 estão resumidas no histórico do [README](README.md).

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
