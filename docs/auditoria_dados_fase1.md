# Auditoria dos dados da Fase 1

## Finalidade e método

Esta auditoria descreve o arquivo
`data/numeric/dataset_pacientes_cardiacos.csv` tal como entregue na Fase 1. Ela
foi incluída após a avaliação para quantificar limitações que antes apareciam
principalmente de forma qualitativa. Os números abaixo podem ser reproduzidos
com `python3 scripts/auditar_dados_fase1.py`.

O arquivo possui **300 registros**, **18 colunas** e dados totalmente
simulados. Os percentuais foram arredondados para uma casa decimal.

## Perfil observado

| Variável | Distribuição observada |
| --- | --- |
| Sexo | 106 feminino (35,3%); 194 masculino (64,7%) |
| Idade | 29 a 79 anos; média de 53,9 anos; mediana de 54 anos |
| Faixas etárias | 29–39: 62 (20,7%); 40–49: 50 (16,7%); 50–59: 73 (24,3%); 60–69: 69 (23,0%); 70–79: 46 (15,3%) |
| `doenca_cardiaca` | 106 ausência (35,3%); 194 presença (64,7%) |
| Diabetes | 47 sim (15,7%); 253 não (84,3%) |
| Tabagismo | 89 sim (29,7%); 211 não (70,3%) |
| Histórico familiar | 90 sim (30,0%); 210 não (70,0%) |
| Glicemia de jejum alta | 50 sim (16,7%); 250 não (83,3%) |
| Angina por exercício | 103 sim (34,3%); 197 não (65,7%) |

## Comparação descritiva com a variável-alvo

Os dados seguintes são apenas descrições do arquivo simulado. Eles não medem
efeito clínico, causalidade, risco real ou justiça de um modelo.

| Grupo | Registros com `doenca_cardiaca = 1` |
| --- | ---: |
| Sexo feminino | 74 de 106 (69,8%) |
| Sexo masculino | 120 de 194 (61,9%) |
| Sem diabetes | 162 de 253 (64,0%) |
| Com diabetes | 32 de 47 (68,1%) |
| Não fumante | 135 de 211 (64,0%) |
| Fumante | 59 de 89 (66,3%) |

As diferenças observadas podem mudar em outra execução, pois o dataset é
pequeno e aleatório. Além disso, o próprio gerador usa sexo, diabetes e
tabagismo — entre outras variáveis — na construção probabilística do alvo.
Portanto, essas diferenças não podem ser usadas para concluir que um grupo tem
maior risco na população real.

## Risco de aprendizado artificial

A variável `doenca_cardiaca` é calculada no script a partir de idade, sexo,
colesterol, pressão arterial, angina por exercício, `oldpeak`, tipo de dor no
peito, número de vasos, histórico familiar, tabagismo e diabetes, acrescida de
ruído aleatório. Um modelo treinado e testado nesse mesmo mecanismo pode obter
boa pontuação por reproduzir a lógica definida no código. Por isso:

- métricas nessa base servem para demonstrar um fluxo de ciência de dados;
- elas não validam diagnóstico ou estratificação clínica;
- qualquer comparação entre grupos deve considerar que sexo foi inserido
  manualmente no score e que a amostra não representa uma população real.

## Auditoria do conjunto visual

O manifesto visual contém **100 imagens**, divididas em 70 de treino, 20 de
validação e 10 de teste. Elas derivam de **10 registros de origem** da MIT-BIH:
100 a 109, com 10 segmentos por registro. A divisão por registro impede que
segmentos da mesma origem apareçam em mais de um conjunto, o que reduz
vazamento. Ainda assim, não transforma os 100 arquivos em 100 exames ou 100
pacientes independentes.

As imagens não possuem rótulo clínico por segmento. Nesta etapa, seu uso é
exploratório: visualização, pré-processamento e estudo da organização dos
dados. Uma tarefa de classificação ou detecção clínica exigiria rótulos
confiáveis, mais registros e validação específica.
