# Dicionário de dados

O arquivo `data/numeric/dataset_pacientes_cardiacos.csv` é uma base simulada.
Os valores foram organizados para exercícios acadêmicos e não devem ser usados
como referência clínica.

| Coluna | Descrição | Valores ou unidade |
| --- | --- | --- |
| `paciente_id` | Identificador fictício do registro | `PAC0001` a `PAC0300` |
| `idade` | Idade simulada | anos |
| `sexo` | Sexo registrado na simulação | 0 = feminino; 1 = masculino |
| `tipo_dor_peito` | Categoria de dor no peito | 0 = assintomático; 1 = angina típica; 2 = angina atípica; 3 = dor não anginosa |
| `pressao_arterial_repouso` | Pressão arterial em repouso | mmHg |
| `colesterol` | Colesterol total | mg/dL |
| `glicemia_jejum_alta` | Glicemia de jejum acima de 120 mg/dL | 0 = não; 1 = sim |
| `ecg_repouso` | Resultado do ECG em repouso | 0 = normal; 1 = alteração ST-T; 2 = hipertrofia ventricular esquerda |
| `freq_cardiaca_maxima` | Frequência máxima simulada em teste de esforço | bpm |
| `angina_exercicio` | Angina induzida por exercício | 0 = não; 1 = sim |
| `oldpeak` | Depressão do segmento ST em relação ao repouso | valor numérico simulado |
| `inclinacao_st` | Inclinação do segmento ST | 0 = descendente; 1 = plana; 2 = ascendente |
| `n_vasos_principais` | Número de vasos principais | 0 a 3 |
| `imc` | Índice de massa corporal | kg/m² |
| `fumante` | Situação de tabagismo simulada | 0 = não; 1 = sim |
| `diabetes` | Presença simulada de diabetes | 0 = não; 1 = sim |
| `historico_familiar` | Histórico familiar de doença cardíaca | 0 = não; 1 = sim |
| `doenca_cardiaca` | Variável indicativa usada no exercício | 0 = ausência; 1 = presença |

`doenca_cardiaca` foi calculada a partir de uma regra probabilística simples.
Ela não é um diagnóstico, nem representa a decisão de um profissional de saúde.
