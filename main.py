import string
import secrets
import pyperclip

AMBIGUOS = set("Il|1O0o`'\"~ ")

def pedir_int(msg, minimo=1, maximo=None):
    while True:
        try:
            v = int(input(msg))
            if v < minimo:
                print(f"⚠ Valor mínimo permitido: {minimo}.")
                continue
            if maximo and v > maximo:
                print(f"⚠ Valor máximo permitido: {maximo}.")
                continue
            return v
        except ValueError:
            print("⚠ Digite um número inteiro válido.")

def pedir_bool(msg):
    return input(msg).strip().lower() in ("s", "sim", "y", "yes")

def montar_conjuntos(usar_maiusculas, usar_minusculas, usar_numeros, usar_simbolos, evitar_ambig):
    conjuntos = []
    if usar_maiusculas:
        c = set(string.ascii_uppercase)
        conjuntos.append(c - AMBIGUOS if evitar_ambig else c)
    if usar_minusculas:
        c = set(string.ascii_lowercase)
        conjuntos.append(c - AMBIGUOS if evitar_ambig else c)
    if usar_numeros:
        c = set(string.digits)
        conjuntos.append(c - AMBIGUOS if evitar_ambig else c)
    if usar_simbolos:
        
        base = set("!@#$%^&*()-_=+[]{};:,.?/")
        conjuntos.append(base - AMBIGUOS if evitar_ambig else base)
    
    conjuntos = [set(c) for c in conjuntos if len(c) > 0]
    return conjuntos

def garantir_variedade(conjuntos, tamanho):
    """
    Gera senha garantindo ao menos 1 char de cada conjunto selecionado
    e completa o restante com o universo total.
    """
    if not conjuntos:
        raise ValueError("Nenhum critério selecionado.")
    if tamanho < len(conjuntos):
        raise ValueError(f"Tamanho mínimo para os critérios escolhidos: {len(conjuntos)}.")

    # 1) Escolhe 1 de cada conjunto
    senha_chars = [secrets.choice(tuple(c)) for c in conjuntos]

    # 2) Universo total
    universo = set().union(*conjuntos)
    universo_tuple = tuple(universo)

    # 3) Completa restante
    faltantes = tamanho - len(senha_chars)
    senha_chars.extend(secrets.choice(universo_tuple) for _ in range(faltantes))

    # 4) Embaralha
    for i in range(len(senha_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        senha_chars[i], senha_chars[j] = senha_chars[j], senha_chars[i]

    return "".join(senha_chars)

def avaliar_forca(tamanho, conjuntos_qtd):
    score = 0
    # tamanho
    if tamanho >= 16: score += 2
    elif tamanho >= 12: score += 1
    # variedade
    if conjuntos_qtd >= 4: score += 2
    elif conjuntos_qtd >= 3: score += 1

    if score >= 4: return "Muito forte"
    if score == 3: return "Forte"
    if score == 2: return "Média"
    return "Fraca"

def gerar_senhas(qtd, tamanho, usar_maiusculas, usar_minusculas, usar_numeros, usar_simbolos, evitar_ambig):
    conjuntos = montar_conjuntos(usar_maiusculas, usar_minusculas, usar_numeros, usar_simbolos, evitar_ambig)
    if not conjuntos:
        raise ValueError("Nenhum conjunto de caracteres disponível. Ajuste os critérios.")

    senhas = []
    for _ in range(qtd):
        senha = garantir_variedade(conjuntos, tamanho)
        senhas.append(senha)
    return senhas, avaliar_forca(tamanho, len(conjuntos))

def main():
    print("===== GERADOR DE SENHAS 🔐 =====")

    tamanho = pedir_int("Digite o tamanho da senha (recomendado 12+): ", minimo=4, maximo=256)
    quantidade = pedir_int("Quantas senhas deseja gerar?: ", minimo=1, maximo=1000)

    usar_maiusculas = pedir_bool("Incluir letras maiúsculas? (s/n): ")
    usar_minusculas = pedir_bool("Incluir letras minúsculas? (s/n): ")
    usar_numeros    = pedir_bool("Incluir Números? (s/n): ")
    usar_simbolos   = pedir_bool("Incluir Símbolos? (s/n): ")
    evitar_ambig    = pedir_bool("Evitar caracteres ambíguos (l I O 0 1 | ...)? (s/n): ")

    # impede seleção vazia
    if not any([usar_maiusculas, usar_minusculas, usar_numeros, usar_simbolos]):
        print("⚠ Você precisa selecionar pelo menos UM critério. Tente novamente.")
        return

    try:
        senhas, forca = gerar_senhas(
            quantidade, tamanho,
            usar_maiusculas, usar_minusculas, usar_numeros, usar_simbolos,
            evitar_ambig
        )
    except ValueError as e:
        print(f"Erro: {e}")
        return

    print(f"\nForça estimada (heurística): {forca}")
    print("\n===== SENHAS GERADAS =====\n")
    for s in senhas:
        print(s)

    # Clipboard
    if quantidade == 1:
        pyperclip.copy(senhas[0])
        print("\n✅ Senha copiada para a área de transferência!")
    else:
        if pedir_bool("\nCopiar TODAS para a área de transferência (uma por linha)? (s/n): "):
            pyperclip.copy("\n".join(senhas))
            print("✅ Todas as senhas foram copiadas para a área de transferência!")

    # Salvar em arquivo
    if pedir_bool("\nDeseja salvar as senhas em um arquivo .txt? (s/n): "):
        nome = input("Nome do arquivo (ex.: senhas.txt): ").strip() or "senhas.txt"
        try:
            with open(nome, "w", encoding="utf-8") as f:
                f.write("\n".join(senhas))
            print(f"✅ Senhas salvas em: {nome}")
        except Exception as e:
            print(f"⚠ Não foi possível salvar o arquivo: {e}")

if __name__ == "__main__":
    main()
