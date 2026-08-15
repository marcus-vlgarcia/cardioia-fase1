"""
CardioIA - Fase 1: Batimentos de Dados
Gerador de imagens SIMULADAS de sinais de eletrocardiograma (ECG).

STATUS NESTA ENTREGA: este script NÃO é mais a fonte principal de
imagens do projeto. As imagens usadas em `assets/imagens/ecg_mitbih/`
são REAIS, derivadas da MIT-BIH Arrhythmia Database (PhysioNet) — ver
`assets/imagens/ecg_mitbih/README.md` e `manifesto_imagens.csv` para
proveniência completa.

Este gerador foi a solução inicial adotada enquanto não tínhamos acesso
a imagens reais (o ambiente de desenvolvimento não tem acesso à
internet para baixar datasets). Ele é mantido no repositório como
alternativa/reserva, útil para:
- gerar dados de teste adicionais sem depender de download externo;
- criar exemplos sintéticos balanceados por classe (normal,
  bradicardia, taquicardia, arritmia) para testes rápidos de pipeline
  antes de rodar sobre a base real.

Saída (se executado): assets/imagens/ecg_sintetico/ecg_0001.png ... ecg_0100.png
(pasta separada da base real, para nunca sobrescrever ou se misturar
com as imagens de assets/imagens/ecg_mitbih/)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RNG = np.random.default_rng(seed=7)
N_IMAGENS = 100
OUT_DIR = "../assets/imagens/ecg_sintetico"
os.makedirs(OUT_DIR, exist_ok=True)


def batimento_pqrst(t, offset=0.0, amp_r=1.0):
    """Gera um único ciclo PQRST simplificado centrado em 'offset'."""
    onda = np.zeros_like(t)
    onda += 0.10 * np.exp(-((t - offset - 0.10) ** 2) / (2 * 0.015 ** 2))      # P
    onda -= 0.10 * np.exp(-((t - offset - 0.18) ** 2) / (2 * 0.006 ** 2))      # Q
    onda += amp_r * np.exp(-((t - offset - 0.20) ** 2) / (2 * 0.010 ** 2))     # R
    onda -= 0.25 * np.exp(-((t - offset - 0.22) ** 2) / (2 * 0.008 ** 2))      # S
    onda += 0.20 * np.exp(-((t - offset - 0.35) ** 2) / (2 * 0.03 ** 2))       # T
    return onda


def gerar_traçado(tipo: str, duracao_s: float = 4.0, fs: int = 250):
    t = np.linspace(0, duracao_s, int(duracao_s * fs))
    sinal = np.zeros_like(t)

    if tipo == "normal":
        bpm = RNG.uniform(60, 100)
    elif tipo == "bradicardia":
        bpm = RNG.uniform(35, 59)
    elif tipo == "taquicardia":
        bpm = RNG.uniform(101, 160)
    else:  # arritmia_ectopica
        bpm = RNG.uniform(60, 100)

    intervalo = 60.0 / bpm
    tempo_batida = intervalo
    while tempo_batida < duracao_s:
        amp_r = 1.0
        if tipo == "arritmia_ectopica" and RNG.random() < 0.18:
            tempo_batida += intervalo * 0.55  # extrassístole (batida precoce)
            amp_r = 0.75
        sinal += batimento_pqrst(t, offset=tempo_batida, amp_r=amp_r)
        tempo_batida += intervalo

    # ruído leve simulando captação do eletrodo
    sinal += RNG.normal(0, 0.015, size=t.shape)
    return t, sinal, round(bpm)


def salvar_imagem(t, sinal, tipo, bpm, idx):
    fig, ax = plt.subplots(figsize=(4, 2.4), dpi=100)
    ax.plot(t, sinal, color="black", linewidth=0.9)
    ax.set_facecolor("#fdeeee")
    fig.patch.set_facecolor("#fdeeee")
    # grade estilo "papel de ECG"
    ax.set_xticks(np.arange(0, t[-1], 0.2), minor=False)
    ax.set_yticks(np.arange(-1, 1.6, 0.5), minor=False)
    ax.grid(which="major", color="#e8a0a0", linewidth=0.5)
    ax.set_ylim(-1, 1.8)
    ax.set_xlim(0, t[-1])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(f"ECG simulado | {tipo} | ~{bpm} bpm", fontsize=8)
    fig.tight_layout(pad=0.4)
    fig.savefig(f"{OUT_DIR}/ecg_{idx:04d}.png")
    plt.close(fig)


if __name__ == "__main__":
    tipos = RNG.choice(
        ["normal", "normal", "bradicardia", "taquicardia", "arritmia_ectopica"],
        size=N_IMAGENS,
    )
    for i, tipo in enumerate(tipos, start=1):
        t, sinal, bpm = gerar_traçado(tipo)
        salvar_imagem(t, sinal, tipo, bpm, i)

    print(f"{N_IMAGENS} imagens de ECG simuladas geradas em {OUT_DIR}")
