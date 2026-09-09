"""Casos que evitam associações silenciosamente incorretas no extrator."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from extrair_sintomas import analisar, ler_mapa


class TestExtracao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapa = ler_mapa(RAIZ / "data/mapa_conhecimento.csv")

    def test_acento_e_caixa(self):
        self.assertIn("coronariana", analisar("APERTO NO TÓRAX e falta de ar", self.mapa)["associacoes"])

    def test_negacao(self):
        self.assertEqual(analisar("Não sinto dor no peito nem suor frio.", self.mapa)["sintomas"], "")

    def test_contraste(self):
        self.assertIn("arritmia", analisar("Não sinto dor no peito, mas tenho palpitações e tontura", self.mapa)["associacoes"])

    def test_sintoma_isolado(self):
        self.assertIn("insuficiente", analisar("Tenho falta de ar", self.mapa)["associacoes"])

    def test_desconhecido(self):
        self.assertIn("insuficiente", analisar("Meu joelho está estalando", self.mapa)["associacoes"])

    def test_varias_associacoes(self):
        resultado = analisar("Dor no peito e suor frio. Palpitações e tontura.", self.mapa)
        self.assertIn("coronariana", resultado["associacoes"])
        self.assertIn("arritmia", resultado["associacoes"])

    def test_dez_relatos(self):
        frases = (RAIZ / "data/relatos_sintomas.txt").read_text().splitlines()
        self.assertEqual(len(frases), 10)
        for frase in frases:
            self.assertNotIn("insuficiente", analisar(frase, self.mapa)["associacoes"])


if __name__ == "__main__":
    unittest.main()
