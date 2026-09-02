# CardioIA — Fase 1: Batimentos de Dados

Este repositório reúne as bases preparadas para a primeira fase do projeto
CardioIA, desenvolvido no curso de Inteligência Artificial da FIAP. A
proposta é organizar dados que podem ser usados nas próximas etapas do projeto,
envolvendo análise numérica, Processamento de Linguagem Natural (NLP) e Visão
Computacional.

Nesta fase, o foco foi preparar os dados, registrar as fontes e discutir os
limites do seu uso. Nenhum arquivo deste repositório deve ser usado para
diagnóstico ou atendimento em saúde.

## Organização

```
cardioia-fase1/
├── data/numeric/
│   └── dataset_pacientes_cardiacos.csv
├── assets/
│   ├── textos/
│   │   ├── hipertensao_arterial_ministerio_saude.txt
│   │   └── infarto_agudo_miocardio_ministerio_saude.txt
│   └── imagens/ecg_mitbih/
│       ├── train/                 # 70 imagens
│       ├── validation/            # 20 imagens
│       ├── test/                  # 10 imagens
│       ├── manifesto_imagens.csv
│       ├── README.md
│       └── link_externo.txt
├── docs/
│   ├── dicionario_de_dados.md
│   └── fontes.md
├── scripts/
│   ├── gerar_dataset_numerico.py
│   └── gerar_imagens_ecg.py
├── requirements.txt
└── README.md
```

## Parte 1 — Dados numéricos

O arquivo `data/numeric/dataset_pacientes_cardiacos.csv` contém **300 registros
simulados**. A quantidade está acima do mínimo de 100 linhas solicitado na
atividade. Os dados não representam pacientes reais e foram gerados para fins
acadêmicos.

As colunas incluem idade, sexo, pressão arterial em repouso, colesterol,
glicemia, dados de ECG em repouso, frequência cardíaca máxima, angina por
esforço, IMC, tabagismo, diabetes, histórico familiar e uma variável indicativa
de doença cardíaca. As definições e codificações estão em
[`docs/dicionario_de_dados.md`](docs/dicionario_de_dados.md).

O conjunto é útil para exercícios de organização de dados, estatística e
classificação supervisionada. Como os valores são simulados, resultados obtidos
com ele não têm valor clínico e não podem ser generalizados para uma população
real.

## Parte 2 — Dados textuais

Foram selecionados dois textos em português sobre saúde cardiovascular:

- `hipertensao_arterial_ministerio_saude.txt`, a partir de conteúdo público do
  Ministério da Saúde sobre hipertensão;
- `infarto_agudo_miocardio_ministerio_saude.txt`, a partir de conteúdo público
  do Ministério da Saúde sobre infarto agudo do miocárdio.

Cada arquivo informa a fonte, a URL e a data de acesso. Eles podem ser usados
em atividades introdutórias de NLP, como busca de termos relacionados a sintomas
e fatores de risco, classificação por assunto e identificação de entidades de
saúde. As fontes completas constam em [`docs/fontes.md`](docs/fontes.md).

## Parte 3 — Dados visuais

O conjunto visual principal contém **100 imagens PNG de ECG** derivadas da
[MIT-BIH Arrhythmia Database](https://physionet.org/content/mitdb/1.0.0/), do
PhysioNet. As imagens foram separadas por registro para evitar que segmentos de
um mesmo registro apareçam em mais de um conjunto:

| Conjunto | Registros | Imagens |
| --- | --- | ---: |
| Treino | 100 a 106 | 70 |
| Validação | 107 e 108 | 20 |
| Teste | 109 | 10 |

O arquivo `manifesto_imagens.csv` registra a origem, o intervalo de tempo, as
derivações, o conjunto e o hash de cada imagem. Trata-se de material de estudo:
as imagens não substituem exames, nem possuem rótulo clínico por segmento.

Elas podem apoiar exercícios de Visão Computacional, por exemplo na identificação
de traçados, na extração de bordas e na análise de padrões. Uma etapa futura
precisaria de rótulos apropriados e validação clínica para qualquer tarefa de
classificação.

## Acesso aos dados

Além deste repositório, os arquivos da atividade estão disponíveis em pasta
pública para consulta e correção:

[Pasta pública do Google Drive](https://drive.google.com/drive/folders/18jSV0Aq45kVY0TAm7l7XCqzQAQevBpnI?usp=sharing)

A pasta foi indicada para consulta dos arquivos completos. Ela deve permanecer
com permissão de leitura para qualquer pessoa com o link até a correção da atividade.

## Governança, privacidade e vieses

Os dados numéricos são sintéticos, o que evita o uso de informações pessoais e
de prontuários. As imagens são dados públicos do PhysioNet e mantêm a atribuição
à fonte. Ainda assim, as três bases têm limitações:

- o dataset numérico foi criado com distribuições simplificadas e pode reproduzir
  vieses de idade e sexo presentes em bases clássicas;
- os textos são informativos e não representam conversas ou prontuários de
  pacientes;
- a MIT-BIH é uma base histórica, com população e contexto de coleta próprios.

Por isso, qualquer modelo treinado com esses arquivos deve ser tratado como
exercício acadêmico. Antes de uso real, seriam necessários dados representativos,
validação, revisão ética e medidas de segurança compatíveis com a LGPD.

## Como executar os scripts

Os scripts não são necessários para abrir os dados entregues, mas foram mantidos
para mostrar como a base simulada pode ser reproduzida ou ampliada.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Gerar novamente o dataset numérico

```bash
python3 scripts/gerar_dataset_numerico.py
```

O comando recria o arquivo principal com 300 registros e uma semente fixa. Para
gerar uma base separada com mais registros:

```bash
python3 scripts/gerar_dataset_numerico.py -n 500 -o data/numeric/dataset_ampliado.csv
```

Também é possível acrescentar novos registros ao arquivo existente. Nesse modo,
os identificadores continuam a numeração já presente no arquivo:

```bash
python3 scripts/gerar_dataset_numerico.py -n 100 -m anexar
```

### Gerar imagens sintéticas de ECG

As imagens usadas na entrega são as 100 imagens reais do MIT-BIH. O script abaixo
gera traçados sintéticos apenas como material complementar de estudo, sem alterar
o conjunto real:

```bash
python3 scripts/gerar_imagens_ecg.py -n 100
```

Por padrão, os arquivos são criados em `assets/imagens/ecg_sintetico/`. Para
usar outra pasta:

```bash
python3 scripts/gerar_imagens_ecg.py -n 30 -o assets/imagens/exemplos_sinteticos
```

As imagens sintéticas não devem ser apresentadas como exames reais e não fazem
parte das 100 imagens usadas para cumprir o requisito da atividade.

## Referências

As referências completas estão em [`docs/fontes.md`](docs/fontes.md). As fontes
incluem o Ministério da Saúde para os textos e o PhysioNet para as imagens de
ECG.
