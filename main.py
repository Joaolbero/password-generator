import pyperclip
import string
import random

def gerar_senha(tamanho, maiusculas=True, minusculas=True, numeros=True, simbolos=True):
    caracteres = ""

    if maiusculas:
        caracteres += string.ascii_uppercase
    if minusculas:
        caracteres += string.ascii_lowercase
    if numeros:
        caracteres += string.digits
    if simbolos:
        caracteres += string.punctuation

    if not caracteres:
        raise ValueError("Nenhum critério selecionado para gerar a senha!")

    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha


print("===== GERADOR DE SENHAS =====")

tamanho = int(input("Digite o tamanho da senha: "))
quantidade = int(input("Quantas senhas deseja gerar?: "))

usar_maiusculas = input("Incluir letras maiúsculas? (s/n): ").lower() == "s"
usar_minusculas = input("Incluir letras minúsculas? (s/n): ").lower() == "s"
usar_numeros = input("Incluir números? (s/n): ").lower() == "s"
usar_simbolos = input("Incluir símbolos? (s/n): ").lower() == "s"

print("\nSenhas geradas:\n")

senhas = []

for _ in range(quantidade):
    senha_gerada = gerar_senha(
        tamanho,
        usar_maiusculas,
        usar_minusculas,
        usar_numeros,
        usar_simbolos
    )
    senhas.append(senha_gerada)
    print(senha_gerada)

if quantidade == 1:
    pyperclip.copy(senhas[0])
    print("\n✅ Senha copiada para a área de transferência!")
