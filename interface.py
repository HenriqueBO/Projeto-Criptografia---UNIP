from enigma import criptografar, descriptografar
from validacao import ChaveInvalidaError, MensagemInvalidaError

MENU = """
=== Enigma Educacional ===
1 - Criptografar mensagem
2 - Descriptografar mensagem
3 - Sair
"""

OPERACOES = {
    "1": (criptografar, "Mensagem: "),
    "2": (descriptografar, "Mensagem criptografada: "),
}


def executar_operacao(operacao, texto_pergunta):
    mensagem = input(texto_pergunta)
    chave = input("Chave (3 a 32 letras/números): ")
    try:
        resultado = operacao(mensagem, chave)
    except (ChaveInvalidaError, MensagemInvalidaError) as erro:
        print(f"\nErro: {erro}")
        return
    print(f"\nResultado: {resultado}")


def executar():
    try:
        while True:
            print(MENU)
            escolha = input("Opção: ").strip()
            if escolha == "3":
                print("Encerrando.")
                break
            if escolha in OPERACOES:
                operacao, texto_pergunta = OPERACOES[escolha]
                executar_operacao(operacao, texto_pergunta)
            else:
                print("\nOpção inválida. Digite 1, 2 ou 3.")
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando.")
