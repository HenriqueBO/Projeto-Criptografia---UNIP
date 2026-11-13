import unittest

from enigma import ALFABETO, Enigma, criptografar, descriptografar
from validacao import ChaveInvalidaError, MensagemInvalidaError


class TestEnigma(unittest.TestCase):
    def test_alfabeto_sem_caracteres_repetidos(self):
        self.assertEqual(len(ALFABETO), len(set(ALFABETO)))

    def test_criptografar_e_descriptografar(self):
        mensagem = "ATAQUE AO AMANHECER"
        cifrada = criptografar(mensagem, "1945")
        self.assertNotEqual(cifrada, mensagem)
        self.assertEqual(descriptografar(cifrada, "1945"), mensagem)

    def test_chaves_diferentes_geram_resultados_diferentes(self):
        mensagem = "ATAQUE AO AMANHECER"
        self.assertNotEqual(
            criptografar(mensagem, "1945"), criptografar(mensagem, "1946")
        )

    def test_chave_errada_nao_recupera_mensagem(self):
        mensagem = "ATAQUE AO AMANHECER"
        cifrada = criptografar(mensagem, "1945")
        self.assertNotEqual(descriptografar(cifrada, "1946"), mensagem)

    def test_espacos_e_quebras_de_linha_sao_preservados(self):
        mensagem = "OLA MUNDO\nSEGUNDA LINHA\tFIM"
        cifrada = criptografar(mensagem, "chave1")
        self.assertEqual(cifrada.count(" "), mensagem.count(" "))
        self.assertEqual(cifrada.count("\n"), 1)
        self.assertEqual(cifrada.count("\t"), 1)
        self.assertEqual(cifrada[3], " ")
        self.assertEqual(descriptografar(cifrada, "chave1"), mensagem)

    def test_numeros_sao_criptografados(self):
        mensagem = "1234567890"
        cifrada = criptografar(mensagem, "1945")
        self.assertNotEqual(cifrada, mensagem)
        self.assertEqual(descriptografar(cifrada, "1945"), mensagem)

    def test_acentos_sao_criptografados(self):
        mensagem = "Atenção: reunião às 15h, coração é ação!"
        cifrada = criptografar(mensagem, "1945")
        self.assertNotEqual(cifrada, mensagem)
        self.assertEqual(descriptografar(cifrada, "1945"), mensagem)

    def test_simbolos_sao_criptografados(self):
        mensagem = "usuario@email.com; (senha) #123 - 50% R$ 10,00!"
        cifrada = criptografar(mensagem, "segredo")
        self.assertNotEqual(cifrada, mensagem)
        self.assertEqual(descriptografar(cifrada, "segredo"), mensagem)

    def test_maiusculas_e_minusculas(self):
        mensagem = "Ataque ao Amanhecer"
        cifrada = criptografar(mensagem, "1945")
        self.assertEqual(descriptografar(cifrada, "1945"), mensagem)
        self.assertNotEqual(
            criptografar("a", "1945") + criptografar("A", "1945"), "aa"
        )
        self.assertNotEqual(descriptografar(cifrada, "1945"), mensagem.upper())

    def test_caractere_fora_do_alfabeto_permanece(self):
        mensagem = "Bom dia ☀ ✓"
        cifrada = criptografar(mensagem, "1945")
        self.assertIn("☀", cifrada)
        self.assertIn("✓", cifrada)
        self.assertEqual(descriptografar(cifrada, "1945"), mensagem)

    def test_substituicao_muda_a_cada_caractere(self):
        cifrada = criptografar("A" * 30, "1945")
        self.assertGreater(len(set(cifrada)), 1)

    def test_mensagem_longa_com_giro_completo_dos_rotores(self):
        mensagem = "TESTE DE ROTORES ção 123 " * 100
        cifrada = criptografar(mensagem, "segredo")
        self.assertEqual(descriptografar(cifrada, "segredo"), mensagem)

    def test_mesma_instancia_pode_ser_reutilizada(self):
        maquina = Enigma("1945")
        primeira = maquina.criptografar("TESTE")
        segunda = maquina.criptografar("TESTE")
        self.assertEqual(primeira, segunda)

    def test_chaves_invalidas(self):
        for chave in ["", "   ", "ab", "a" * 33, "chave com espaco", "sênha", "12#4", None, 1945]:
            with self.subTest(chave=chave):
                with self.assertRaises(ChaveInvalidaError):
                    criptografar("TESTE", chave)

    def test_mensagens_invalidas(self):
        for mensagem in ["", "   ", None, 123]:
            with self.subTest(mensagem=mensagem):
                with self.assertRaises(MensagemInvalidaError):
                    criptografar(mensagem, "1945")


if __name__ == "__main__":
    unittest.main()
