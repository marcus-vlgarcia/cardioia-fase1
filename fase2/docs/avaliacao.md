# Avaliação do classificador

## Resultado da execução

Configuração fixa: TF-IDF com unigramas e bigramas, Regressão Logística, seed 42.
São 64 frases de treino (32 cenários) e 16 de teste (oito cenários), com as
paráfrases mantidas juntas. O teste não foi usado para escolher parâmetros.

| Medida no teste | Valor |
| --- | ---: |
| Acurácia | 87,5% (14/16) |
| Acurácia do baseline | 50,0% |
| Precisão de alto risco | 87,5% |
| Recall de alto risco | 87,5% |
| F1 de alto risco | 0,875 |
| F1 de baixo risco | 0,875 |
| Falsos negativos de alto risco | 1 |
| Falsos positivos de alto risco | 1 |

A validação cruzada no treino teve acurácias de 81,25%, 87,5%, 68,75% e
93,75% (média 82,81%). Essa variação reforça a sensibilidade à composição da
amostra. O arquivo `outputs/metricas.json` registra versões, hash da base,
divisões e valores completos.

## O que os erros mostram

O relato “Estou com lábios arroxeados e dificuldade para respirar.” recebeu
baixo risco, apesar de seu rótulo didático ser alto risco. O cenário foi
reservado ao teste; os termos e combinações não foram suficientemente cobertos
no treino. Esse erro mostra o limite de generalização do vocabulário, mesmo
com uma acurácia global aparentemente boa.

O relato “Fiquei com irritação discreta no olho após limpar a estante.” recebeu
alto risco, embora seu rótulo fosse baixo risco. A classificação lexical não
compreende que a frase descreve uma queixa leve nesse exemplo.

Nos 12 casos adicionais, houve 10 acertos. As frases “Não tenho falta de ar nem
dor no peito; só espirrei duas vezes.” e “Estou com coriza leve e não sinto dor
no peito.” foram classificadas como alto risco. Manter negações no TF-IDF e
usar bigramas não bastou para interpretar o contexto. Esses casos são expostos
como falhas; não foi acrescentada uma regra para ocultar os resultados do modelo.

## Vieses e próximos passos

O equilíbrio de classes é artificial, muitos exemplos leves possuem vocabulário
não cardíaco e todas as frases têm a mesma origem de construção. A divisão por
cenário reduz a repetição entre conjuntos, mas não elimina esses vieses. O teste
de identidade não substitui uma avaliação demográfica: faltam grupos reais
representativos e rótulos revisados independentemente.

Uma evolução deverá incluir casos linguísticos mais diversos, mais cenários
ambíguos, revisão dos rótulos e avaliação externa. O conjunto de teste atual
deve permanecer como referência desta versão; novos ajustes precisam de um
novo teste reservado para evitar adaptação às respostas já conhecidas.
