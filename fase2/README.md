# PulseIA — Fase 2

## Diagnóstico Automatizado — IA no Estetoscópio Digital

O módulo possui duas partes independentes: associação de sintomas a possíveis
condições por regras e classificação de frases em alto ou baixo risco com
TF-IDF e Regressão Logística. O projeto é uma simulação acadêmica de apoio à
triagem; não realiza diagnóstico médico.

## Entregáveis

| Critério do enunciado | Arquivo |
| --- | --- |
| 10 relatos completos de sintomas | [relatos_sintomas.txt](data/relatos_sintomas.txt) |
| Mapa de conhecimento | [mapa_conhecimento.csv](data/mapa_conhecimento.csv) — 43 associações possíveis |
| Código de extração funcional | [extrair_sintomas.py](src/extrair_sintomas.py) |
| Base de frases e rótulos | [frases_risco.csv](data/frases_risco.csv) — 80 frases, 40 por classe |
| Notebook com TF-IDF, treinamento e avaliação | [classificador_risco.ipynb](notebooks/classificador_risco.ipynb) |
| Resultados da extração | [diagnosticos_sugeridos.csv](outputs/diagnosticos_sugeridos.csv) |
| Avaliação do modelo | [metricas.json](outputs/metricas.json) e [predicoes_teste.csv](outputs/predicoes_teste.csv) |
| Governança e fontes | [dados_e_limites.md](docs/dados_e_limites.md) |
| Demonstração em vídeo | Publicação no YouTube como **não listado** pendente; o link deve ser inserido no README principal antes da entrega. |

## Execução

Na raiz do repositório, com Python 3.13:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r fase2/requirements.txt
python fase2/src/extrair_sintomas.py
python fase2/src/executar_notebook.py
python -m unittest discover -s fase2/tests -v
```

O primeiro script lê o `.txt` e o mapa e salva as dez associações. É possível
usar outros arquivos com `--frases`, `--mapa` e `--saida`. Para demonstrar um
novo relato, execute `python fase2/src/extrair_sintomas.py --interativo`: três
campos pedem sintomas, impacto na rotina e tempo de início. O programa formula
a frase no padrão dos relatos e acrescenta sua análise ao CSV de saída, sem
alterar o arquivo original com os dez exemplos. O segundo executa
todas as células e salva o notebook com tabelas e gráficos, além dos arquivos
em `outputs`. Também é possível abrir o notebook no VS Code ou Jupyter usando
o mesmo ambiente e executar todas as células em ordem.

## Como funciona

O extrator normaliza acentos e maiúsculas, procura expressões inteiras e verifica
negação simples. Cada linha do mapa exige os dois sintomas. Não havendo um par
compatível, retorna “Associação insuficiente no mapa”. O mapa foi ampliado para
registrar mais de uma possibilidade para sintomas parecidos. Um relato pode
receber mais de uma associação; nenhuma delas é um diagnóstico confirmado.

O classificador usa 64 frases de treino e 16 de teste, separadas por cenário com
seed 42. As paráfrases de cada cenário ficam juntas. O TF-IDF é ajustado apenas
no treino, dentro de um Pipeline. A validação cruzada usa quatro divisões por
grupo no treino, sem reutilizar o teste para selecionar parâmetros.

O notebook apresenta acurácia, precisão, recall e F1 por classe, matriz de
confusão, baseline e erros individuais. Também inspeciona termos aprendidos e
testa 12 frases adicionais. Todos os rótulos são simulados. A análise detalhada
de limitações inclui vieses lexicais e a falta de representatividade demográfica.

## Continuidade da Fase 1

A auditoria da Fase 1 orientou a divisão por grupos, a identificação explícita
dos rótulos sintéticos e a análise de erros. A variável numérica artificial não
é usada como alvo deste classificador textual. O portal e a MLP são atividades
opcionais posteriores.
