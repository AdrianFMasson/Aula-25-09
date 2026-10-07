import re


def validar_senha(senha: str) -> bool:
    if len(senha) < 6:
        return False

    if not re.search(r"[A-Z]", senha):
        return False

    if not re.search(r"[a-z]", senha):
        return False

    if not re.search(r"[^A-Za-z0-9]", senha):
        return False

    return True