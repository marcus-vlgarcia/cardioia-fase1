# Avaliação do classificador

## Base e método da revisão

A base passou de 80 para 240 frases, em 120 cenários com duas paráfrases:
184 frases de treino, 40 de teste novo e 16 do teste antigo para regressão.
O manifesto mantém as paráfrases juntas em todas as divisões.

Comparamos quatro configurações apenas na validação cruzada do treino: TF-IDF
com n-gramas (1,2) ou (1,3) e Regressão Logística com C=1 ou C=4. O maior F1 macro
selecionou bigramas e C=4. Com seed 42, as acurácias das quatro divisões foram
89,13%, 91,30%, 100% e 86,96% (média 91,85%). Esses valores participaram da
seleção e podem ser otimistas; não substituem o teste reservado.

## Comparação no mesmo teste novo

Reproduzimos a configuração anterior nos mesmos 64 exemplos originais de treino
e avaliamos as duas versões nas mesmas 40 frases novas.

| Medida | Original: 64 frases de treino | Revisado: 184 frases de treino |
| --- | ---: | ---: |
| Acurácia | 70% (28/40) | 82,5% (33/40) |
| Recall de alto risco | 75% | 80% |
| F1 macro | 0,699 | 0,825 |
| Falsos negativos | 5 | 4 |
| Falsos positivos | 7 | 3 |

O baseline que sempre prevê a classe mais frequente acertou 50%. Na revisão,
a precisão de alto risco foi 84,21% e o F1 dessa classe foi 0,821. A matriz tem
17 acertos de baixo risco, três falsos positivos, quatro falsos negativos e
16 acertos de alto risco.

Houve melhora nesse conjunto. Tanto os dados quanto a regularização mudaram;
a comparação não isola o efeito da quantidade de frases. O teste tem apenas
20 cenários e a mesma origem sintética do treino. Um erro representa 2,5 pontos
percentuais. As métricas não validam uso em pacientes.

## Erros que permanecem

Os quatro falsos negativos do teste novo foram:

- A53: negação de dor nas costas seguida de dificuldade respiratória e sonolência.
- A57: duas paráfrases que negam febre e tosse, mas afirmam falta de ar que impede falar.
- A58: dificuldade para respirar com espuma rosada na tosse, em uma das paráfrases.

Os três falsos positivos foram as duas frases B54, que negam sintomas torácicos
e relatam irritação da etiqueta na nuca, e uma frase B55 sobre uma marca de meia
que desapareceu. A classificação ainda depende de vocabulário e não compreende
com segurança o alcance das negações.

## Regressão e histórico

A versão original acertou 14/16 (87,5%) no teste antigo e 10/12 desafios. A revisão
acertou 15/16 (93,75%) no teste antigo e 12/12 desafios. As duas negações que
falhavam nos desafios passaram. A frase sobre lábios arroxeados e dificuldade
para respirar continua sendo um falso negativo no teste antigo.

Os erros conhecidos motivaram a ampliação, então esses conjuntos são regressão,
não nova avaliação independente. Os 87,5% antigos e os 82,5% atuais foram medidos
em testes diferentes. A comparação entre versões é a tabela das mesmas 40 frases.

## Governança e continuidade

As métricas e hashes estão em `outputs/metricas.json`; as configurações avaliadas
estão em `comparacao_cv.csv`; `comparacao_modelos.csv` compara as versões.
`predicoes_teste.csv`, `predicoes_regressao.csv` e `resultados_desafios.csv`
preservam os erros individuais. Os quatro exemplos de troca de identidade no
notebook verificam sensibilidade textual, sem comprovar fairness demográfica.

Os rótulos são didáticos, as classes são artificialmente equilibradas e muitos
casos leves têm vocabulário não cardíaco. As novas frases não tiveram revisão
clínica independente. Mais exemplos da mesma autoria não substituem revisão
dos rótulos, contextos diversos e dados externos. Se os erros do teste atual
orientarem outra versão, ele também deverá ser tratado como regressão, com uma
nova avaliação reservada ou externa.
