# Origem dos dados e limites

## Construção dos arquivos

Os 10 relatos, as 80 frases rotuladas e os 12 casos de desafio foram escritos
para esta simulação acadêmica. Não são prontuários, downloads de relatos reais
ou registros de atendimento. Os textos institucionais da Fase 1 continuam
preservados, mas não foram transformados em exemplos rotulados de pacientes.

O mapa contém 16 pares de expressões e quatro categorias de possíveis
condições. É uma tabela de associações didáticas, não uma ontologia clínica
formal. Vários sintomas são compartilhados por doenças diferentes. A ocorrência
de um par não confirma a condição, e a ausência de correspondência não exclui
doença. Os 10 relatos incluem início, sintomas e impacto na rotina; o programa
extrai os sintomas, sem tentar interpretar automaticamente duração ou gravidade.

## Critérios dos rótulos

- `alto risco`: cenário simulado com sintomas agudos preocupantes, como dor
  torácica persistente com suor frio, dificuldade respiratória importante ou
  perda de consciência.
- `baixo risco`: descrição explicitamente leve ou resolvida, sem sinais de
  alerta relatados no exemplo. Não significa ausência de doença ou dispensa de
  avaliação médica.
- `grupo`: cenário de origem das duas paráfrases; não é atributo preditor.
- `esperado` em `desafios.csv`: rótulo didático para observar comportamento em
  exemplos adicionais; não é padrão-ouro médico.

Os rótulos não foram validados por profissionais da saúde. Eles não são derivados
da coluna `doenca_cardiaca` da Fase 1, nem atribuídos pelo extrator. Balanceamento
de classes foi uma escolha de construção, não uma estimativa de prevalência.

## Limitações concretas

1. As duas frases de cada cenário são dependentes. Por isso, a divisão e a
   validação cruzada mantêm os grupos juntos.
2. Há somente 40 cenários. O teste final tem oito cenários e 16 frases; um erro
   altera a acurácia em 6,25 pontos percentuais.
3. Queixas não cardíacas leves predominam em parte da classe de baixo risco.
   O modelo pode aprender diferença de vocabulário em vez de gravidade.
4. Palavras como “leve”, “forte” e “repouso” podem dominar decisões. Negação,
   ironia, relatos de terceiros, erros ortográficos e sintomas atípicos não são
   compreendidos de forma confiável pelo TF-IDF.
5. O extrator trata apenas negação simples até pontuação ou contraste. Uma frase
   longa com negações e afirmações misturadas pode produzir erro. Ele exige os
   dois sintomas da linha e devolve todas as associações compatíveis.
6. A base não representa uma população por sexo, idade, raça ou região.
   Trocar identidade mantendo sintomas é um teste de sensibilidade, não uma
   avaliação suficiente de fairness.

## Fontes consultadas

Acesso em 08/09/2026. As fontes abaixo orientam a contextualização dos sintomas;
não validam o mapa nem os rótulos produzidos para o exercício.

- Síndrome coronariana aguda/infarto: [Ministério da Saúde — Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto).
- Insuficiência cardíaca: [Ministério da Saúde — orientações ao paciente](https://linhasdecuidado.saude.gov.br/portal/insuficiencia-cardiaca-%28IC%29-no-adulto/sou-paciente).
- Angina: [Biblioteca Virtual em Saúde — Angina](https://bvsms.saude.gov.br/angina/).
- Arritmias: [Secretaria da Saúde do Ceará — sintomas e cuidados](https://www.ce.gov.br/saude/2019/11/06/arritmia-cardiaca-conheca-mais-sobre-a-doenca-e-saiba-como-trata-la-corretamente/).
- Método: [Scikit-learn — prevenção de vazamento de dados](https://scikit-learn.org/stable/common_pitfalls.html).

A base numérica e os ECGs da Fase 1 permanecem disponíveis para continuidade
do projeto, com suas limitações documentadas em `docs/auditoria_dados_fase1.md`.
