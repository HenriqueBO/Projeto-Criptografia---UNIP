import unicodedata

from gerador import GeradorPseudoaleatorio, gerar_semente
from rotor import Rotor
from validacao import validar_chave, validar_mensagem

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ACENTUADAS = "ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ"
DIGITOS = "0123456789"
SIMBOLOS = ".,;:!?-_'\"()[]{}@#$%&*+=/\\<>|~^`"

ALFABETO = (
    LETRAS
    + LETRAS.lower()
    + ACENTUADAS
    + ACENTUADAS.lower()
    + DIGITOS
    + SIMBOLOS
)
INDICES = {caractere: indice for indice, caractere in enumerate(ALFABETO)}
QUANTIDADE_ROTORES = 3


class Enigma:
    def __init__(self, chave):
        self.chave = validar_chave(chave)
        self.rotores = self._montar_rotores()
        self.posicoes_iniciais = [rotor.posicao for rotor in self.rotores]

    def _montar_rotores(self):
        gerador = GeradorPseudoaleatorio(gerar_semente(self.chave))
        rotores = []
        for _ in range(QUANTIDADE_ROTORES):
            fiacao = gerador.embaralhar(range(len(ALFABETO)))
            posicao = gerador.inteiro_ate(len(ALFABETO))
            rotores.append(Rotor(fiacao, posicao))
        return rotores

    def _reiniciar(self):
        for rotor, posicao in zip(self.rotores, self.posicoes_iniciais):
            rotor.posicao = posicao

    def _girar_rotores(self):
        for rotor in self.rotores:
            if not rotor.avancar():
                break

    def _cifrar_caractere(self, caractere):
        self._girar_rotores()
        indice = INDICES[caractere]
        for rotor in self.rotores:
            indice = rotor.passar_frente(indice)
        return ALFABETO[indice]

    def _decifrar_caractere(self, caractere):
        self._girar_rotores()
        indice = INDICES[caractere]
        for rotor in reversed(self.rotores):
            indice = rotor.passar_tras(indice)
        return ALFABETO[indice]

    def _processar(self, texto, transformar_caractere):
        self._reiniciar()
        texto = unicodedata.normalize("NFC", texto)
        resultado = []
        for caractere in texto:
            if caractere in INDICES:
                resultado.append(transformar_caractere(caractere))
            else:
                resultado.append(caractere)
        return "".join(resultado)

    def criptografar(self, mensagem):
        validar_mensagem(mensagem)
        return self._processar(mensagem, self._cifrar_caractere)

    def descriptografar(self, mensagem):
        validar_mensagem(mensagem)
        return self._processar(mensagem, self._decifrar_caractere)


def criptografar(mensagem, chave):
    return Enigma(chave).criptografar(mensagem)


def descriptografar(mensagem, chave):
    return Enigma(chave).descriptografar(mensagem)
