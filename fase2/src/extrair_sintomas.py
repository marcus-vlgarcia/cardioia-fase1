"""Associa expressões a condições usando um mapa didático, sem diagnóstico clínico."""

import argparse
import csv
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
AVISO = "Simulação acadêmica: as associações não confirmam nem excluem doenças."


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(c for c in texto if not unicodedata.combining(c))


def ler_mapa(caminho):
    with Path(caminho).open(encoding="utf-8", newline="") as arquivo:
        mapa = list(csv.DictReader(arquivo))
    if not mapa or not {"sintoma_1", "sintoma_2", "doenca_associada"} <= mapa[0].keys():
        raise ValueError("Mapa vazio ou sem as três colunas obrigatórias.")
    return mapa


def expressoes_afirmadas(texto, expressoes):
    # Negação simples até a próxima pontuação ou conjunção de contraste.
    # Não resolve negação dupla, fala de terceiros ou contexto temporal complexo.
    trechos = re.split(r"[.,;!?]|\b(?:mas|porem|contudo)\b", normalizar(texto))
    encontrados = set()
    for expressao in expressoes:
        padrao = r"(?<!\w)" + re.escape(normalizar(expressao)) + r"(?!\w)"
        for trecho in trechos:
            for ocorrencia in re.finditer(padrao, trecho):
                prefixo = trecho[:ocorrencia.start()]
                if not re.search(r"\b(?:nao|sem|nego|nega|nem)\b", prefixo):
                    encontrados.add(expressao)
    return sorted(encontrados)


def analisar(frase, mapa):
    expressoes = {r[c] for r in mapa for c in ("sintoma_1", "sintoma_2")}
    sintomas = expressoes_afirmadas(frase, expressoes)
    # Os dois sintomas da linha precisam estar presentes. Todas as associações
    # compatíveis são mantidas: uma palavra isolada não define uma doença.
    condicoes = sorted({r["doenca_associada"] for r in mapa
                        if r["sintoma_1"] in sintomas and r["sintoma_2"] in sintomas})
    return {"frase": frase, "sintomas": " | ".join(sintomas),
            "associacoes": " | ".join(condicoes) or "Associação insuficiente no mapa",
            "aviso": AVISO}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frases", type=Path, default=RAIZ / "data/relatos_sintomas.txt")
    parser.add_argument("--mapa", type=Path, default=RAIZ / "data/mapa_conhecimento.csv")
    parser.add_argument("--saida", type=Path, default=RAIZ / "outputs/diagnosticos_sugeridos.csv")
    args = parser.parse_args()
    frases = [f.strip() for f in args.frases.read_text(encoding="utf-8").splitlines() if f.strip()]
    if not frases:
        parser.error("O arquivo de relatos está vazio.")
    mapa = ler_mapa(args.mapa)
    resultados = [analisar(frase, mapa) for frase in frases]
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with args.saida.open("w", encoding="utf-8", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
    for i, resultado in enumerate(resultados, 1):
        print(f"{i:02d}. {resultado['associacoes']}\n    Sintomas: {resultado['sintomas']}")
    print(AVISO)


if __name__ == "__main__":
    main()
