TAMANHO_MINIMO_CHAVE = 3
TAMANHO_MAXIMO_CHAVE = 32


class ChaveInvalidaError(ValueError):
    pass


class MensagemInvalidaError(ValueError):
    pass


def validar_chave(chave):
    if not isinstance(chave, str):
        raise ChaveInvalidaError("A chave deve ser um texto.")
    chave = chave.strip()
    if not chave:
        raise ChaveInvalidaError("A chave não pode ser vazia.")
    if len(chave) < TAMANHO_MINIMO_CHAVE:
        raise ChaveInvalidaError(
            f"A chave deve ter pelo menos {TAMANHO_MINIMO_CHAVE} caracteres."
        )
    if len(chave) > TAMANHO_MAXIMO_CHAVE:
        raise ChaveInvalidaError(
            f"A chave deve ter no máximo {TAMANHO_MAXIMO_CHAVE} caracteres."
        )
    if not (chave.isascii() and chave.isalnum()):
        raise ChaveInvalidaError(
            "A chave deve conter apenas letras (sem acento) e números."
        )
    return chave


def validar_mensagem(mensagem):
    if not isinstance(mensagem, str):
        raise MensagemInvalidaError("A mensagem deve ser um texto.")
    if not mensagem.strip():
        raise MensagemInvalidaError("A mensagem não pode ser vazia.")
    return mensagem
