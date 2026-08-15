"""
CardioIA - Fase 1: Batimentos de Dados
Gerador de dataset numérico SIMULADO de pacientes cardíacos.

Este script NÃO utiliza dados reais de pacientes. Ele gera uma base
sintética, mas estatisticamente plausível, inspirada em variáveis
clínicas comumente usadas em estudos de cardiologia (ex.: datasets
públicos como o "Heart Disease UCI"), respeitando faixas de valores
realistas descritas na literatura médica geral.

Motivo de usarmos dados simulados:
- Dados reais de pacientes são protegidos por sigilo médico, LGPD/HIPAA
  e exigem aprovação de comitês de ética para uso, mesmo em pesquisa.
- Para fins didáticos (curso de IA), a simulação permite treinar,
  testar e demonstrar pipelines de ML sem risco de vazamento de dados
  sensíveis reais — um exercício direto de Governança de Dados.

Saída: data/numeric/dataset_pacientes_cardiacos.csv
"""

import numpy as np
import pandas as pd

# Seed fixa para reprodutibilidade (qualquer pessoa que rodar o script
# gera exatamente a mesma base de dados)
RNG = np.random.default_rng(seed=42)

N_PACIENTES = 300  # acima do mínimo de 100 exigido no enunciado


def gerar_dataset(n: int) -> pd.DataFrame:
    idade = RNG.integers(29, 80, size=n)

    # Sexo: 0 = feminino, 1 = masculino (aprox. distribuição do dataset
    # clássico Heart Disease UCI, ~68% masculino)
    sexo = RNG.choice([0, 1], size=n, p=[0.32, 0.68])

    # Tipo de dor no peito (chest pain type)
    # 0: assintomático | 1: angina típica | 2: angina atípica | 3: dor não anginosa
    tipo_dor_peito = RNG.choice([0, 1, 2, 3], size=n, p=[0.47, 0.16, 0.17, 0.20])

    # Pressão arterial de repouso (mmHg) - correlacionada levemente com a idade
    pressao_arterial_repouso = np.clip(
        RNG.normal(loc=120 + (idade - 50) * 0.5, scale=17), 90, 200
    ).round(0)

    # Colesterol total (mg/dL)
    colesterol = np.clip(
        RNG.normal(loc=246 + (idade - 50) * 0.6, scale=51), 120, 570
    ).round(0)

    # Glicemia de jejum > 120 mg/dL (0 = não, 1 = sim)
    glicemia_jejum_alta = RNG.choice([0, 1], size=n, p=[0.85, 0.15])

    # Resultado do eletrocardiograma de repouso
    # 0: normal | 1: anormalidade onda ST-T | 2: hipertrofia ventricular esquerda
    ecg_repouso = RNG.choice([0, 1, 2], size=n, p=[0.50, 0.01, 0.49])

    # Frequência cardíaca máxima atingida em teste de esforço
    freq_cardiaca_maxima = np.clip(
        RNG.normal(loc=220 - idade - RNG.normal(0, 8, size=n), scale=10), 70, 210
    ).round(0)

    # Angina induzida por exercício (0 = não, 1 = sim)
    angina_exercicio = RNG.choice([0, 1], size=n, p=[0.68, 0.32])

    # Depressão do segmento ST induzida pelo exercício em relação ao repouso
    oldpeak = np.clip(RNG.exponential(scale=1.0, size=n), 0, 6.2).round(1)

    # Inclinação do segmento ST no pico do exercício
    # 0: descendente | 1: plana | 2: ascendente
    inclinacao_st = RNG.choice([0, 1, 2], size=n, p=[0.14, 0.47, 0.39])

    # Número de vasos principais coloridos por fluoroscopia (0-3)
    n_vasos_principais = RNG.choice([0, 1, 2, 3], size=n, p=[0.58, 0.22, 0.13, 0.07])

    # IMC (kg/m2)
    imc = np.clip(RNG.normal(loc=27, scale=4.5, size=n), 16, 45).round(1)

    # Fumante (0 = não, 1 = sim)
    fumante = RNG.choice([0, 1], size=n, p=[0.72, 0.28])

    # Diabetes (0 = não, 1 = sim)
    diabetes = RNG.choice([0, 1], size=n, p=[0.83, 0.17])

    # Histórico familiar de doença cardíaca (0 = não, 1 = sim)
    historico_familiar = RNG.choice([0, 1], size=n, p=[0.65, 0.35])

    # --- Variável-alvo: presença de doença cardíaca (0 = não, 1 = sim) ---
    # Construída a partir de um score de risco simplificado combinando
    # fatores de risco conhecidos na literatura médica, apenas para dar
    # coerência estatística à base simulada (NÃO é um modelo diagnóstico).
    score_risco = (
        0.03 * (idade - 50)
        + 0.9 * sexo
        + 0.02 * (colesterol - 200)
        + 0.02 * (pressao_arterial_repouso - 120)
        + 1.1 * angina_exercicio
        + 0.5 * oldpeak
        + 0.6 * (tipo_dor_peito == 0)
        + 0.8 * n_vasos_principais
        + 0.4 * historico_familiar
        + 0.3 * fumante
        + 0.3 * diabetes
        + RNG.normal(0, 1.3, size=n)
    )
    prob_doenca = 1 / (1 + np.exp(-0.35 * (score_risco - 2)))
    doenca_cardiaca = (RNG.random(n) < prob_doenca).astype(int)

    df = pd.DataFrame(
        {
            "paciente_id": [f"PAC{str(i).zfill(4)}" for i in range(1, n + 1)],
            "idade": idade,
            "sexo": sexo,  # 0 = feminino, 1 = masculino
            "tipo_dor_peito": tipo_dor_peito,
            "pressao_arterial_repouso": pressao_arterial_repouso.astype(int),
            "colesterol": colesterol.astype(int),
            "glicemia_jejum_alta": glicemia_jejum_alta,
            "ecg_repouso": ecg_repouso,
            "freq_cardiaca_maxima": freq_cardiaca_maxima.astype(int),
            "angina_exercicio": angina_exercicio,
            "oldpeak": oldpeak,
            "inclinacao_st": inclinacao_st,
            "n_vasos_principais": n_vasos_principais,
            "imc": imc,
            "fumante": fumante,
            "diabetes": diabetes,
            "historico_familiar": historico_familiar,
            "doenca_cardiaca": doenca_cardiaca,  # variável-alvo (0/1)
        }
    )
    return df


if __name__ == "__main__":
    df = gerar_dataset(N_PACIENTES)
    out_path = "../data/numeric/dataset_pacientes_cardiacos.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Dataset gerado com {len(df)} linhas -> {out_path}")
    print(df["doenca_cardiaca"].value_counts(normalize=True))
