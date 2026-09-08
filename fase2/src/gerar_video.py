"""Monta uma demonstração legendada a partir dos resultados executados."""
import csv
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = RAIZ / "fase2/outputs"


def main():
    subprocess.run([sys.executable, str(RAIZ / "fase2/src/extrair_sintomas.py")], check=True)
    metricas = json.loads((SAIDA / "metricas.json").read_text())
    with (SAIDA / "diagnosticos_sugeridos.csv").open() as f:
        resultados = list(csv.DictReader(f))
    relato = resultados[0]["frase"]
    acuracia = metricas["relatorio"]["accuracy"] * 100
    cenas = [
        ("PulseIA | CardioIA — Fase 2", [
            "Diagnóstico Automatizado — IA no Estetoscópio Digital",
            "Grupo PulseIA: Erik Criscuolo; Marcus Vinícius Loureiro Garcia; Sidney William de Paula Dias.",
            "Duas etapas: associação de sintomas por regras e classificação de risco com Machine Learning.",
            "Demonstração dos resultados executados. Dados simulados; sem uso clínico."]),
        ("1. Relatos completos", [
            "Arquivo: fase2/data/relatos_sintomas.txt — 10 relatos",
            relato,
            "O exemplo informa início, sintomas e impacto na rotina.",
            "Os demais relatos incluem cansaço, edema, palpitações e sintomas durante esforço."]),
        ("2. Mapa de conhecimento", [
            "16 linhas: sintoma_1 | sintoma_2 | doenca_associada",
            "dor no peito + suor frio → possível síndrome coronariana aguda",
            "O código normaliza acentos e letras e exige os dois sintomas da linha.",
            "Negações simples são verificadas. Sem par compatível: associação insuficiente; não significa ausência de doença."]),
        ("3. Execução do extrator", [
            "python fase2/src/extrair_sintomas.py",
            "Saída executada para o primeiro relato:",
            "Sintomas: " + resultados[0]["sintomas"],
            "Associação: " + resultados[0]["associacoes"],
            "Os 10 resultados são salvos em diagnosticos_sugeridos.csv."]),
        ("4. Base de classificação", [
            "80 frases rotuladas: 40 de alto risco e 40 de baixo risco.",
            "40 cenários, cada um com duas paráfrases. Cada cenário fica inteiro em um conjunto.",
            "Treino: 64 frases / 32 cenários. Teste: 16 frases / 8 cenários.",
            "Seed 42. Os rótulos são didáticos e não vêm do alvo numérico artificial da Fase 1."]),
        ("5. TF-IDF e treinamento", [
            'Pipeline: TfidfVectorizer(ngram_range=(1, 2)) → LogisticRegression',
            'modelo.fit(treino.frase, treino.situacao)',
            'predicoes = modelo.predict(teste.frase)',
            "O TF-IDF aprende apenas no treino. Validação cruzada em quatro divisões por cenário.",
            "O notebook salva tabelas, métricas e previsões para conferência."]),
        ("6. Avaliação no teste", [
            f"Acurácia: {acuracia:.1f}% — 14 de 16 frases.".replace("87.5", "87,5"),
            "Baseline: 50%. Recall de alto risco: 87,5%.",
            "Matriz de confusão (linhas reais; colunas previstas):",
            "                           Baixo risco    Alto risco",
            "Baixo risco                      7                    1",
            "Alto risco                         1                    7"]),
        ("7. Erros e vieses", [
            "Falso negativo: o relato com lábios arroxeados e dificuldade para respirar recebeu baixo risco.",
            "Dois desafios com negação receberam alto risco incorretamente.",
            "Vocabulário limitado e rótulos simulados podem facilitar ou distorcer a tarefa.",
            "Amostra pequena: resultados não comprovam desempenho clínico nem justiça entre grupos."]),
        ("8. Reproduzir e conferir", [
            "python fase2/src/executar_notebook.py",
            "O repositório contém os dados, código, notebook executado, métricas, testes e fontes.",
            "github.com/marcus-vlgarcia/cardioia-fase1 — branch fase2",
            "O feedback da Fase 1 orientou a análise de vieses e a separação por origem.",
            "PulseIA • Simulação acadêmica de apoio à triagem."])
    ]
    fontes = [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),
              Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    fonte = next((p for p in fontes if p.exists()), None)
    if fonte is None:
        raise RuntimeError("Instale Arial ou DejaVu Sans para gerar as legendas.")
    titulo = ImageFont.truetype(str(fonte), 42)
    corpo = ImageFont.truetype(str(fonte), 29)
    pequeno = ImageFont.truetype(str(fonte), 22)
    caminho = SAIDA / "demonstracao_fase2.mp4"
    escritor = imageio_ffmpeg.write_frames(str(caminho), (1280, 720), fps=1,
        codec="libx264", pix_fmt_in="rgb24", pix_fmt_out="yuv420p",
        output_params=["-movflags", "+faststart"])
    escritor.send(None)
    try:
        for i, (cabecalho, paragrafos) in enumerate(cenas):
            quadro = Image.new("RGB", (1280, 720), "#111b2b")
            desenho = ImageDraw.Draw(quadro)
            desenho.rectangle((0, 0, 1280, 10), fill="#ed145b")
            desenho.text((60, 44), cabecalho, font=titulo, fill="white")
            y = 130
            for paragrafo in paragrafos:
                for linha in textwrap.wrap(paragrafo, width=76):
                    desenho.text((60, y), linha, font=corpo, fill="#dce7f4")
                    y += 38
                y += 20
            if i == 6:
                # Exibe a matriz efetivamente exportada pelo notebook.
                desenho.rectangle((0, 235, 1280, 655), fill="#111b2b")
                grafico = Image.open(SAIDA / "matriz_confusao.png").convert("RGB")
                grafico.thumbnail((700, 400))
                quadro.paste(grafico, ((1280 - grafico.width) // 2, 245))
            if y > 650:
                raise ValueError(f"Texto excede a tela na cena {i + 1}: {y}")
            desenho.text((60, 677), "FIAP • Grupo PulseIA • Dados simulados", font=pequeno, fill="#9db4cc")
            desenho.text((1100, 677), f"{i + 1}/9", font=pequeno, fill="#9db4cc")
            quadro.save(SAIDA / f"video_preview_{i + 1}.png")
            for segundo in range(20):
                frame = quadro.copy()
                ImageDraw.Draw(frame).rectangle((0, 710, int(1280 * (i * 20 + segundo + 1) / 180), 719), fill="#ed145b")
                escritor.send(frame.tobytes())
    finally:
        escritor.close()
    print("Vídeo legendado de 180 segundos:", caminho)


if __name__ == "__main__":
    main()
