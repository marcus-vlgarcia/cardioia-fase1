# Avaliação do classificador

## Base e separação dos conjuntos

A base contém 288 frases simuladas, organizadas em 144 cenários com duas
paráfrases. São 208 frases de treino, 24 de teste final e 56 de regressão. As
duas frases do mesmo cenário ficam sempre no mesmo conjunto.

Os testes analisados nas versões anteriores foram preservados como regressão:
os grupos A51–A60, B51–B60 e os oito grupos do teste inicial. Eles não entram
no treino, mas seus resultados não são evidência independente porque seus erros
já orientaram a revisão. O teste final é formado pelos grupos A67–A72 e B67–B72.

## Configuração e limiar escolhidos no treino

O classificador usa TF-IDF e Regressão Logística. Antes de consultar o teste
final, a validação cruzada por cenário comparou quatro configurações: n-gramas
(1,2) ou (1,3), com C=1 ou C=4. A seleção por F1 macro escolheu bigramas e C=4.
As acurácias das quatro divisões foram 96,15%, 92,31%, 96,15% e 92,31%, com média
de 94,23%. Esses valores ajudam a escolher o modelo, mas podem ser otimistas.

Também marcamos cinco negações comuns antes da vetorização, como “não sinto dor
no peito” e “sem falta de ar”. O procedimento é limitado: não compreende toda a
estrutura da frase, ironia, dupla negação ou relato indireto complexo.

O limiar de decisão foi escolhido por previsões fora da divisão no treino:

| Limiar para alto risco | Precisão alto risco | Recall alto risco | Falsos negativos | Falsos positivos |
| ---: | ---: | ---: | ---: | ---: |
| 0,35 | 77,61% | 100% | 0 | 30 |
| 0,40 | 81,60% | 98,08% | 2 | 23 |
| 0,45 | 87,18% | 98,08% | 2 | 15 |
| 0,50 | 91,82% | 97,12% | 3 | 9 |

Para esta simulação de triagem, foi selecionado 0,35: é o menor limiar com
precisão de alto risco acima de 75% e o maior recall. Isso privilegia evitar
falsos negativos e, como consequência, pode aumentar falsos positivos.

## Resultado no teste final

| Medida | Resultado |
| --- | ---: |
| Acurácia | 91,7% (22/24) |
| Baseline | 50% |
| Precisão de alto risco | 85,7% |
| Recall de alto risco | 100% |
| F1 de alto risco | 0,923 |
| Falsos negativos | 0 |
| Falsos positivos | 2 |

A matriz de confusão tem 10 acertos de baixo risco, dois falsos positivos,
nenhum falso negativo e 12 acertos de alto risco. Os dois falsos positivos são
as paráfrases do cenário B69: suor após exercício que cessou com descanso. O
modelo deu maior peso ao termo “suor” do que ao contexto de recuperação.

O resultado é promissor para o exercício, mas o teste tem somente 12 cenários e
cada erro altera a acurácia em 4,17 pontos percentuais. Todos os exemplos são
sintéticos e produzidos no mesmo projeto. A métrica não representa desempenho
clínico nem valida uso em atendimento.

## Regressão e desafios

O conjunto de regressão teve 48 acertos em 56 frases (85,7%). Os 12 desafios
adicionais tiveram 12 acertos, inclusive os exemplos de negação que antes eram
classificados como alto risco. A melhoria veio da ampliação de cenários e da
marcação de negações; ela não elimina falhas em frases mais longas ou fora do
vocabulário usado na base.

Os arquivos `predicoes_teste.csv`, `predicoes_regressao.csv` e
`resultados_desafios.csv` guardam cada previsão. `comparacao_limiares.csv`
mostra a escolha do limiar e `metricas.json` registra a seed, versões, hashes e
métricas da execução.

## Continuidade planejada

O teste final atual deve permanecer sem alterações enquanto esta versão existir.
Se seus erros forem usados para treinar outra revisão, ele será apenas regressão
e um novo conjunto reservado ou externo deverá ser criado. Para fases futuras,
o grupo pretende buscar revisão clínica independente dos rótulos, diversidade
de linguagem e dados, avaliação externa e critérios explícitos para o custo de
falsos negativos e falsos positivos.
