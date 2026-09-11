"""Normaliza negações frequentes antes da vetorização textual."""

import re
import unicodedata


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.casefold())
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    return re.sub(r"\s+", " ", texto).strip()


PADROES_NEGACAO = (
    (r"\b(?:nao\s+(?:tenho|sinto|estou com)|sem|nem)\s+(?:dor|pressao|aperto)\s+no\s+(?:peito|torax)\b", "neg_sintoma_toracico"),
    (r"\b(?:nao\s+(?:tenho|sinto|estou com)|sem)\s+(?:falta de ar|dificuldade para respirar)\b", "neg_dificuldade_respiratoria"),
    (r"\b(?:nao\s+(?:tenho|sinto|estou)|sem|nem)\s+(?:suor frio|suando frio|transpiracao fria)\b", "neg_suor_frio"),
    (r"\b(?:nao\s+(?:tenho|sinto)|sem)\s+(?:palpitacoes|coracao acelerado)\b", "neg_palpitacoes"),
    (r"\b(?:nao\s+(?:tenho|sinto)|sem)\s+(?:tontura|sensacao de desmaio|desmaio)\b", "neg_tontura_ou_desmaio"),
    (r"\brespiro normalmente\b", "neg_dificuldade_respiratoria"),
)


def preparar_texto(texto):
    """Marca cinco negações comuns sem tentar interpretar toda a frase."""
    texto = normalizar(texto)
    for padrao, marcador in PADROES_NEGACAO:
        texto = re.sub(padrao, f" {marcador} ", texto)
    return re.sub(r"\s+", " ", texto).strip()
