MODULO = 2 ** 32


def gerar_semente(chave):
    semente = 5381
    for posicao, caractere in enumerate(chave, start=1):
        semente = (semente * 33 + ord(caractere) * posicao) % MODULO
    return semente


class GeradorPseudoaleatorio:
    def __init__(self, semente):
        self.estado = semente

    def proximo(self):
        self.estado = (self.estado * 1664525 + 1013904223) % MODULO
        return self.estado >> 8

    def inteiro_ate(self, limite):
        return self.proximo() % limite

    def embaralhar(self, itens):
        itens = list(itens)
        for i in range(len(itens) - 1, 0, -1):
            j = self.inteiro_ate(i + 1)
            itens[i], itens[j] = itens[j], itens[i]
        return itens
