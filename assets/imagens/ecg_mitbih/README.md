# ECGs derivados do MIT-BIH

Esta pasta reúne 100 imagens PNG produzidas a partir de segmentos da MIT-BIH
Arrhythmia Database, do PhysioNet (versão 1.0.0, DOI `10.13026/C2F305`). A
licença da base é Open Data Commons Attribution 1.0.

- `train/`: registros 100 a 106, com 70 imagens;
- `validation/`: registros 107 e 108, com 20 imagens;
- `test/`: registro 109, com 10 imagens.

A divisão foi feita por registro para evitar que segmentos de uma mesma origem
apareçam em conjuntos diferentes. Cada imagem apresenta 10 segundos de ECG e
dois canais. O arquivo `manifesto_imagens.csv` informa a origem, as derivações,
o intervalo de tempo e o hash de cada imagem.

As imagens são visualizações derivadas para uso acadêmico. Elas não são exames
independentes e não possuem rótulo clínico por segmento.
