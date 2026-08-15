# CardioIA — Fase 1: Batimentos de Dados

Projeto acadêmico do curso de Inteligência Artificial (FIAP), desenvolvido
em formato PBL (Project Based Learning). O CardioIA é uma plataforma
digital que simula um ecossistema de cardiologia inteligente, integrando
dados clínicos, Machine Learning, Visão Computacional, IoT e agentes de IA
ao longo de 7 fases.

Nesta primeira fase, o papel assumido é o de **cientista de dados
hospitalar**: o objetivo é levantar, organizar e documentar os três tipos
de dados que alimentarão os módulos inteligentes das próximas fases —
dados numéricos, dados textuais e dados visuais — sempre com atenção à
**Governança de Dados** e a possíveis **vieses** presentes nas bases.

## Objetivo do projeto

- Construir uma base de dados de pacientes cardiológicos com informações
  clinicamente relevantes.
- Reunir textos que possam alimentar futuras análises de NLP sobre saúde
  cardiovascular.
- Reunir imagens que possam alimentar futuras análises de Visão
  Computacional sobre exames cardiológicos.
- Documentar claramente a origem, as limitações e o uso pretendido de
  cada base, como exercício de Governança de Dados em IA.

## Estrutura do repositório

```
cardioia-fase1/
├── README.md
├── data/
│   └── numeric/
│       └── dataset_pacientes_cardiacos.csv
├── assets/
│   ├── textos/
│   │   ├── doenca_arterial_coronariana.txt
│   │   └── hipertensao_arterial_saude_publica.txt
│   └── imagens/
│       └── ecg_mitbih/
│           ├── README.md              # documentação original da base (PhysioNet)
│           ├── manifesto_imagens.csv  # proveniência, split, licença e hash SHA-256 de cada imagem
│           ├── link_externo.txt       # link público de hospedagem (preencher)
│           ├── train/                 # 70 imagens (registros 100–106)
│           ├── validation/            # 20 imagens (registros 107–108)
│           └── test/                  # 10 imagens (registro 109)
├── scripts/
│   ├── gerar_dataset_numerico.py
│   └── gerar_imagens_ecg.py
└── notebooks/        # reservado para os notebooks das próximas fases (Colab/Jupyter)
```

## Parte 1 — Dados numéricos (IoT / clínicos)

**Arquivo:** `data/numeric/dataset_pacientes_cardiacos.csv` (300 linhas, acima do mínimo de 100 exigido)

**Origem dos dados:** dados **simulados**, gerados via
`scripts/gerar_dataset_numerico.py` com `numpy`/`pandas`. Não são dados de
pacientes reais. As faixas de valores e as proporções entre variáveis
foram construídas com base em padrões descritos na literatura médica geral
sobre fatores de risco cardiovascular (ex.: relação entre idade, colesterol,
pressão arterial e risco de doença cardíaca), e não em nenhuma base de
dados protegida.

**Por que simulamos os dados:** dados reais de pacientes são protegidos
por sigilo médico e por legislações como a LGPD, exigindo consentimento e
aprovação ética para uso — mesmo em contexto acadêmico. A simulação
permite treinar e testar pipelines de IA sem esse risco, sendo uma prática
comum em ambientes de aprendizado.

**Variáveis mais relevantes do ponto de vista clínico:**

| Variável | Por que é relevante |
|---|---|
| `idade`, `sexo` | Fatores de risco não modificáveis; a incidência de doença coronariana aumenta com a idade e varia entre sexos. |
| `pressao_arterial_repouso` | Hipertensão é um dos principais fatores de risco cardiovascular. |
| `colesterol` | Está diretamente relacionado à formação de placas de aterosclerose. |
| `tipo_dor_peito`, `angina_exercicio` | Sintomas centrais para triagem de doença coronariana. |
| `freq_cardiaca_maxima`, `oldpeak`, `inclinacao_st` | Indicadores obtidos em teste de esforço, usados clinicamente para estimar risco de isquemia. |
| `n_vasos_principais` | Reflete diretamente o grau de obstrução coronariana. |
| `fumante`, `diabetes`, `historico_familiar`, `imc` | Fatores de risco modificáveis (ou não) amplamente associados a eventos cardíacos. |
| `doenca_cardiaca` | Variável-alvo (0/1), útil para treinar classificadores supervisionados na Fase 2. |

**Nota sobre viés:** por ser sintética e gerada a partir de premissas
simplificadas (ex.: maior prevalência no sexo masculino, reproduzindo
padrões de datasets clássicos como o Heart Disease UCI), esta base carrega
o mesmo tipo de viés de representatividade que bases reais desse domínio
costumam ter. Isso é discutido de propósito aqui como gatilho para a
reflexão sobre Governança de Dados: um modelo treinado nela pode
sub-representar determinados grupos (ex.: mulheres, faixas etárias mais
jovens) e deve ser reavaliado com dados reais e diversos antes de qualquer
uso além do educacional.

## Parte 2 — Dados textuais (NLP)

**Arquivos:** `assets/textos/doenca_arterial_coronariana.txt` e
`assets/textos/hipertensao_arterial_saude_publica.txt`

**Origem dos dados:** textos **originais**, escritos especificamente para
este projeto com base em conhecimento médico geral e de domínio público
sobre doença arterial coronariana e hipertensão arterial (não são cópias
de nenhum artigo específico do SciELO, BVS, SUS ou de outra fonte —
evitando, assim, qualquer questão de direitos autorais sobre o texto de
terceiros).

**Como podem ser explorados por algoritmos de NLP:**

- **Extração de sintomas e fatores de risco:** identificar termos como
  "dor no peito", "colesterol elevado" ou "sedentarismo" via NER
  (Named Entity Recognition) ou busca por palavras-chave.
- **Classificação de tópicos:** treinar um classificador para diferenciar
  textos sobre doença coronariana, hipertensão, diabetes etc., útil para
  organizar automaticamente conteúdos educativos de um app de saúde.
- **Análise de sentimento:** embora estes textos sejam neutros/informativos,
  servem de baseline para comparar com textos de pacientes (ex.: relatos em
  fóruns), medindo tom emocional associado a diferentes condições.
- **Sumarização automática:** gerar resumos curtos que possam ser exibidos
  em um chatbot de orientação ao paciente (Fase 5 do projeto).

**Relevância para IA em saúde:** compreender e estruturar automaticamente
textos médicos é essencial para sistemas de triagem digital, chatbots de
orientação e ferramentas de apoio à decisão clínica — todos objetivos
citados no escopo do CardioIA.

## Parte 3 — Dados visuais (Visão Computacional)

**Arquivos:** `assets/imagens/ecg_mitbih/{train,validation,test}/*.png` (100 imagens)

**Origem dos dados:** imagens **reais**, derivadas da **MIT-BIH Arrhythmia
Database** (PhysioNet, versão 1.0.0, DOI
[`10.13026/C2F305`](https://doi.org/10.13026/C2F305)), licenciada sob
**Open Data Commons Attribution License v1.0**. Cada PNG representa um
segmento de 10 segundos de ECG com dois canais (derivações **MLII** e
**V5**), extraído de registros WFDB reais e renderizado com grade, sem
alteração do sinal original.

**Composição e organização (split por paciente/registro, evitando
vazamento de dados entre conjuntos):**

| Split | Registros (pacientes) | Nº de imagens |
|---|---|---|
| `train/` | 100–106 | 70 |
| `validation/` | 107–108 | 20 |
| `test/` | 109 | 10 |

**Proveniência e integridade:** o arquivo
`assets/imagens/ecg_mitbih/manifesto_imagens.csv` traz, para cada imagem,
o registro de origem, o intervalo de tempo do segmento, as derivações
utilizadas, o split, a URL/DOI da fonte, a licença e o **hash SHA-256**
do arquivo. Todas as 100 imagens foram conferidas contra o manifesto e
100% dos hashes bateram, confirmando que os arquivos não foram
corrompidos ou alterados após a geração.

> **Nota clínica importante:** conforme o `README.md` original da base
> (preservado em `assets/imagens/ecg_mitbih/README.md`), estas são
> **visualizações derivadas para uso acadêmico**, sem rótulo clínico por
> segmento — ou seja, **não substituem exames diagnósticos** e não devem
> ser usadas para qualquer finalidade clínica real.

**Como podem ser analisadas por algoritmos de Visão Computacional:**

- **Detecção de picos R:** localizar os picos de maior amplitude em cada
  canal (MLII/V5) para estimar a frequência cardíaca automaticamente.
- **Classificação de padrões/arritmias:** treinar uma CNN sobre os
  segmentos de `train/`, validar em `validation/` e testar em `test/`
  (split já separado por paciente, evitando vazamento de dados entre
  conjuntos) para reconhecer morfologias associadas a diferentes tipos
  de batimento.
- **Comparação entre derivações:** usar os dois canais (MLII e V5) como
  entradas complementares de um mesmo segmento, útil para modelos
  multi-canal de Visão Computacional.
- **Reconhecimento de bordas e formas:** isolar a curva do traçado da
  grade de fundo, replicando o pré-processamento usado em sistemas reais
  de digitalização de exames em papel.

**Relevância para IA em saúde:** a leitura automatizada de exames de
imagem é um dos pilares de sistemas de diagnóstico assistido por IA,
citado diretamente no escopo do CardioIA (Fase 4 — "Coração em Imagens").
Por serem dados reais do PhysioNet (uma das fontes públicas mais usadas
em pesquisa biomédica), essas imagens dão mais robustez ao projeto do que
uma simulação, mantendo a devida atenção ao uso não-diagnóstico.

**Alternativa sintética (mantida como referência):** o script
`scripts/gerar_imagens_ecg.py` continua no repositório e permite gerar
traçados de ECG sintéticos (ritmo normal, bradicardia, taquicardia e
arritmia com extrassístole). Ele deixou de ser a fonte principal de
imagens desta entrega, mas pode ser útil em fases futuras para criar
dados de teste adicionais ou dados balanceados por classe.

## Governança de Dados e vieses — reflexão do grupo

- Os dados numéricos e os textos desta entrega são **simulados/originais**,
  criados especificamente para fins didáticos, sem uso de dados reais de
  pacientes ou de textos de terceiros, preservando privacidade e
  conformidade com a LGPD. Já as imagens de ECG são **dados reais** do
  PhysioNet — o projeto combina, portanto, dados sintéticos e reais, com
  a origem de cada um claramente documentada nas seções acima.
- A base numérica reproduz, de forma proposital, vieses de
  representatividade comuns em datasets reais da área (ex.: maior
  prevalência de casos no sexo masculino), o que deve ser levado em conta
  ao interpretar qualquer resultado obtido a partir dela.
- Sobre as imagens reais: a licença **Open Data Commons Attribution v1.0**
  exige atribuição à fonte (já registrada no manifesto e neste README);
  o split `train`/`validation`/`test` foi feito **por paciente**, evitando
  vazamento de dados entre conjuntos; e a integridade das 100 imagens foi
  conferida via hash SHA-256 contra o manifesto (100% de correspondência).

## Links para os dados hospedados (preencher)

> Os arquivos completos também estão disponíveis publicamente em:
> - Dados numéricos: `[inserir link do Google Drive/OneDrive aqui]`
> - Textos: `[inserir link do Google Drive/OneDrive aqui]`
> - Imagens: `[inserir link do Google Drive/OneDrive aqui]` — também há um
>   placeholder pronto em `assets/imagens/ecg_mitbih/link_externo.txt`

*(ver instruções de preenchimento na mensagem de entrega deste projeto)*

## Como reproduzir os dados

```bash
cd scripts
python3 gerar_dataset_numerico.py   # gera data/numeric/dataset_pacientes_cardiacos.csv (300 linhas)
python3 gerar_imagens_ecg.py        # gera imagens de ECG sintéticas alternativas (opcional)
```

Dependências: `numpy`, `pandas`, `matplotlib`.

**Gerando mais dados numéricos (opcional):** `gerar_dataset_numerico.py`
aceita argumentos de linha de comando para controlar quantidade, arquivo
de saída e se deve substituir ou anexar ao arquivo existente:

```bash
# Sobrescreve o arquivo padrão com um dataset novo de N linhas
python3 gerar_dataset_numerico.py -n 500

# Gera um CSV totalmente separado, sem tocar no dataset principal
python3 gerar_dataset_numerico.py -n 150 -o ../data/numeric/dataset_extra.csv

# Mantém as linhas já existentes e ACRESCENTA 300 linhas novas ao final
# (paciente_id continua a numeração automaticamente, sem repetir IDs)
python3 gerar_dataset_numerico.py -n 300 -m anexar
```

No modo `anexar`, cada execução usa uma semente aleatória diferente por
padrão (para não repetir os mesmos pacientes); no modo `substituir`
(padrão), a semente é fixa (42), garantindo que rodar o script do zero
sempre reproduza o mesmo dataset original de 300 linhas.

**Gerando mais imagens sintéticas de ECG (opcional):** o script
`gerar_imagens_ecg.py` funciona da mesma forma — quantidade, pasta de
saída e modo substituir/anexar são todos configuráveis:

```bash
# Sobrescreve a pasta padrão com N imagens novas
python3 gerar_imagens_ecg.py -n 50

# Gera uma pasta totalmente nova, separada da principal
python3 gerar_imagens_ecg.py -n 30 -o ../assets/imagens/ecg_extra

# Mantém as imagens já existentes na pasta e ACRESCENTA 40 novas
# (numeração continua automaticamente, ex.: ecg_0101.png, ecg_0102.png...)
python3 gerar_imagens_ecg.py -n 40 -m anexar
```

Assim como no script numérico, `substituir` usa semente fixa (7) por
padrão, e `anexar` usa uma semente diferente a cada execução. As
imagens geradas por este script vão para `assets/imagens/ecg_sintetico/`
(ou a pasta indicada em `-o`), nunca em `assets/imagens/ecg_mitbih/`,
que é reservada às imagens reais do PhysioNet.

As imagens reais de `assets/imagens/ecg_mitbih/` já estão prontas no
repositório; sua proveniência pode ser reconferida a qualquer momento
comparando o hash SHA-256 de cada arquivo com o valor correspondente em
`manifesto_imagens.csv`.

---

Este material foi construído como base para as próximas fases do CardioIA
(diagnóstico automatizado com IA, monitoramento contínuo com IoT, visão
computacional, assistente virtual e previsão de crises), sempre com
atenção à relevância clínica das informações e ao impacto real que
soluções desse tipo podem ter na vida das pessoas.
