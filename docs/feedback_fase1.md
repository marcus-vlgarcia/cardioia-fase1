# Evolução da Fase 1 a partir da avaliação

## Objetivo desta atualização

A Fase 1 foi avaliada como uma entrega completa e organizada. A principal
recomendação foi tornar mais visíveis os limites de representatividade dos dados
e evitar que resultados futuros de Machine Learning sejam confundidos com
evidência clínica. Este documento registra como o feedback foi incorporado ao
projeto antes do início da Fase 2.

## Pontos observados e resposta do projeto

| Observação da avaliação | Atualização adotada | Diretriz para as próximas fases |
| --- | --- | --- |
| A base numérica usa distribuições artificiais, inclusive uma proporção de sexo inspirada em bases clássicas. | Foi criada uma auditoria quantitativa com a distribuição observada de sexo, idade, alvo e fatores de risco. | Sempre apresentar a composição da base antes de discutir métricas de modelos. |
| `doenca_cardiaca` é calculada a partir de variáveis presentes no próprio dataset. | A regra geradora e o risco de o modelo reaprender essa regra foram destacados no README e na auditoria. | Não interpretar desempenho nessa variável como capacidade de diagnóstico; priorizar bases reais e rotuladas quando o objetivo for avaliação clínica. |
| O score sintético usa sexo como um de seus componentes. | A associação foi identificada explicitamente como escolha didática do gerador, não como regra clínica. | Avaliar resultados por grupo e não usar o atributo para justificar decisões automatizadas. |
| As 100 imagens de ECG derivam de apenas 10 registros. | O README passou a diferenciar quantidade de arquivos de quantidade de registros de origem. | Ampliar a diversidade de registros e manter a separação por registro para evitar vazamento. |
| Não há rótulos clínicos por segmento de ECG. | A expressão “reconhecimento de anomalias” foi restrita a estudo exploratório futuro. | Não treinar ou alegar validação de um classificador clínico sem rótulos confiáveis e revisão adequada. |

## Compromissos para a Fase 2

1. Manter dados simulados claramente identificados como material acadêmico.
2. Reportar tamanho, distribuição de classes e possíveis desequilíbrios antes do
   treinamento de qualquer modelo.
3. Separar dados de treino e teste de forma reproduzível e evitar frases ou
   registros repetidos entre os conjuntos.
4. Avaliar mais do que acurácia, incluindo erros por classe e limitações dos
   dados utilizados.
5. Tratar os resultados como apoio didático à triagem e à organização de
   informações, nunca como diagnóstico médico.

## Escopo preservado

Esta atualização não modifica o dataset nem tenta corrigir artificialmente suas
distribuições. Alterar os dados após a avaliação prejudicaria a rastreabilidade
da entrega original. A melhoria adotada foi documentar, medir e considerar as
limitações de forma explícita nas próximas etapas do CardioIA.
