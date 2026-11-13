class Rotor:
    def __init__(self, fiacao, posicao=0):
        self.fiacao = list(fiacao)
        self.tamanho = len(self.fiacao)
        self.inversa = [0] * self.tamanho
        for entrada, saida in enumerate(self.fiacao):
            self.inversa[saida] = entrada
        self.posicao = posicao % self.tamanho

    def avancar(self):
        self.posicao = (self.posicao + 1) % self.tamanho
        return self.posicao == 0

    def passar_frente(self, indice):
        entrada = (indice + self.posicao) % self.tamanho
        saida = self.fiacao[entrada]
        return (saida - self.posicao) % self.tamanho

    def passar_tras(self, indice):
        entrada = (indice + self.posicao) % self.tamanho
        saida = self.inversa[entrada]
        return (saida - self.posicao) % self.tamanho
