import sys
import string
import secrets
import argparse
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# -----------------------------------------
# Configurações gerais
# -----------------------------------------
console = Console()
AMBIGUOS = set("Il|1O0o`'\"~ ")

DEFAULTS = {
    "tamanho": 16,
    "quantidade": 1,
    "maiusculas": True,
    "minusculas": True,
    "numeros": True,
    "simbolos": True,
    "evitar_ambig": True,
}
_last_config = DEFAULTS.copy()

# -----------------------------------------
# Utilitários de entrada
# -----------------------------------------
def pedir_int(msg, minimo=1, maximo=None):
    while True:
        try:
            v = int(Prompt.ask(msg))
            if v < minimo:
                console.print(f"⚠ Valor mínimo permitido: {minimo}.")
                continue
            if maximo and v > maximo:
                console.print(f"⚠ Valor máximo permitido: {maximo}.")
                continue
            return v
        except ValueError:
            console.print("⚠ Digite um número inteiro válido.")

def pedir_bool(msg, default=False):
    resp = Prompt.ask(msg + " (s/n)", default="s" if default else "n")
    return resp.strip().lower() in ("s", "sim", "y", "yes")

# -----------------------------------------
# Núcleo de geração
# -----------------------------------------
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
    # remove conjuntos vazios (pode acontecer se tudo foi filtrado)
    conjuntos = [set(c) for c in conjuntos if len(c) > 0]
    return conjuntos

def garantir_variedade(conjuntos, tamanho):
    if not conjuntos:
        raise ValueError("Nenhum critério selecionado.")
    if tamanho < len(conjuntos):
        raise ValueError(f"Tamanho mínimo para os critérios escolhidos: {len(conjuntos)}.")

    # 1) garante 1 char de cada conjunto
    senha_chars = [secrets.choice(tuple(c)) for c in conjuntos]

    # 2) completa com universo total
    universo = set().union(*conjuntos)
    universo_tuple = tuple(universo)
    faltantes = tamanho - len(senha_chars)
    senha_chars.extend(secrets.choice(universo_tuple) for _ in range(faltantes))

    # 3) embaralha (Fisher-Yates)
    for i in range(len(senha_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        senha_chars[i], senha_chars[j] = senha_chars[j], senha_chars[i]

    return "".join(senha_chars)

def avaliar_forca(tamanho, conjuntos_qtd):
    score = 0
    if tamanho >= 16: score += 2
    elif tamanho >= 12: score += 1
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
        senhas.append(garantir_variedade(conjuntos, tamanho))
    return senhas, avaliar_forca(tamanho, len(conjuntos))

# -----------------------------------------
# Saída formatada / execução
# -----------------------------------------
def executar_geracao(tamanho, quantidade, mai, minusc, nums, sims, evitar_ambig, copiar_cli, salvar_arquivo):
    try:
        senhas, forca = gerar_senhas(quantidade, tamanho, mai, minusc, nums, sims, evitar_ambig)
    except ValueError as e:
        console.print(f"[red]Erro:[/red] {e}")
        return

    console.print(Panel(f"[bold]Força estimada:[/bold] {forca}", border_style="magenta"))
    for s in senhas:
        console.print(s)

    if copiar_cli and quantidade == 1:
        pyperclip.copy(senhas[0])
        console.print("[green]✅ Senha copiada para a área de transferência![/green]")
    elif copiar_cli and quantidade > 1:
        pyperclip.copy("\n".join(senhas))
        console.print("[green]✅ Todas as senhas copiadas para a área de transferência![/green]")

    if salvar_arquivo:
        try:
            with open(salvar_arquivo, "w", encoding="utf-8") as f:
                f.write("\n".join(senhas))
            console.print(f"[green]✅ Senhas salvas em: {salvar_arquivo}[/green]")
        except Exception as e:
            console.print(f"[red]⚠ Não foi possível salvar o arquivo:[/red] {e}")

# -----------------------------------------
# Menu Hackerman (modo interativo)
# -----------------------------------------
def menu_hackerman():
    console.clear()
    header = Panel.fit("[bold green]🔐 Gerador de Senhas — Hackerman Mode[/bold green]\n[dim][/dim]", border_style="green")
    console.print(header)

    table = Table(show_header=False, box=None)
    table.add_row("[cyan]1.[/cyan] Gerar senhas (usar configuração atual)")
    table.add_row("[cyan]2.[/cyan] Configurar opções padrão")
    table.add_row("[cyan]3.[/cyan] Mostrar última configuração")
    table.add_row("[cyan]4.[/cyan] Sair")
    console.print(table)

    return Prompt.ask("\nEscolha uma opção", choices=["1","2","3","4"], default="1")

def interactive_configurar():
    # Loop até ter pelo menos 1 critério ativo
    while True:
        console.print("\n[bold]Configuração de geração:[/bold]")
        tamanho = pedir_int("Tamanho da senha (recomendado 12+): ", minimo=4, maximo=256)
        quantidade = pedir_int("Quantidade de senhas: ", minimo=1, maximo=1000)

        mai = pedir_bool("Incluir Maiúsculas?", default=_last_config["maiusculas"])
        minusc = pedir_bool("Incluir Minúsculas?", default=_last_config["minusculas"])
        nums = pedir_bool("Incluir Números?", default=_last_config["numeros"])
        sims = pedir_bool("Incluir Símbolos?", default=_last_config["simbolos"])
        evitar = pedir_bool("Evitar Caracteres ambíguos?", default=_last_config["evitar_ambig"])

        if not any([mai, minusc, nums, sims]):
            console.print("[red]⚠ Você precisa selecionar pelo menos UM critério (maiúsculas/minúsculas/números/símbolos).[/red]")
            continue

        _last_config.update({
            "tamanho": tamanho,
            "quantidade": quantidade,
            "maiusculas": mai,
            "minusculas": minusc,
            "numeros": nums,
            "simbolos": sims,
            "evitar_ambig": evitar
        })
        return tamanho, quantidade, mai, minusc, nums, sims, evitar

# -----------------------------------------
# Argumentos de linha de comando (CLI)
# -----------------------------------------
def cli_args():
    parser = argparse.ArgumentParser(description="Gerador de senhas personalizado (CLI)")
    parser.add_argument("--tamanho", type=int, help="Tamanho da senha (ex: 16)")
    parser.add_argument("--quantidade", type=int, default=1, help="Quantas senhas gerar")

    parser.add_argument("--maiusculas", dest="maiusculas", action="store_true", help="Incluir letras maiúsculas")
    parser.add_argument("--no-maiusculas", dest="maiusculas", action="store_false", help="Excluir letras maiúsculas")

    parser.add_argument("--minusculas", dest="minusculas", action="store_true", help="Incluir letras minúsculas")
    parser.add_argument("--no-minusculas", dest="minusculas", action="store_false", help="Excluir letras minúsculas")

    parser.add_argument("--numeros", dest="numeros", action="store_true", help="Incluir números")
    parser.add_argument("--no-numeros", dest="numeros", action="store_false", help="Excluir números")

    parser.add_argument("--simbolos", dest="simbolos", action="store_true", help="Incluir símbolos")
    parser.add_argument("--no-simbolos", dest="simbolos", action="store_false", help="Excluir símbolos")

    parser.add_argument("--evitar-ambig", dest="evitar_ambig", action="store_true", help="Evitar caracteres ambíguos")
    parser.add_argument("--copiar", dest="copiar", action="store_true", help="Copiar resultado para a área de transferência")
    parser.add_argument("--salvar", type=str, help="Salvar em arquivo (ex: senhas.txt)")

    # OBS: Não setamos defaults aqui (além dos necessários) — usamos DEFAULTS/_last_config
    return parser.parse_args()

# -----------------------------------------
# MAIN
# -----------------------------------------
def main():
    args = cli_args()

    # Se foram passados argumentos (além do nome do script) -> Modo CLI
    if len(sys.argv) > 1:
        tamanho = args.tamanho if args.tamanho is not None else DEFAULTS["tamanho"]
        quantidade = args.quantidade if args.quantidade is not None else DEFAULTS["quantidade"]

        mai = args.maiusculas if args.maiusculas is not None else DEFAULTS["maiusculas"]
        minusc = args.minusculas if args.minusculas is not None else DEFAULTS["minusculas"]
        nums = args.numeros if args.numeros is not None else DEFAULTS["numeros"]
        sims = args.simbolos if args.simbolos is not None else DEFAULTS["simbolos"]

        # Blindagem: requer pelo menos um critério ativo
        if not any([mai, minusc, nums, sims]):
            console.print("[red]⚠ Pelo menos um critério precisa estar ativo (maiúsculas/minúsculas/números/símbolos).[/red]")
            return

        executar_geracao(tamanho, quantidade, mai, minusc, nums, sims, args.evitar_ambig, args.copiar, args.salvar)
        return

    # Sem argumentos -> Menu Hackerman
    while True:
        escolha = menu_hackerman()

        if escolha == "1":
            cfg = _last_config
            if not any([cfg["maiusculas"], cfg["minusculas"], cfg["numeros"], cfg["simbolos"]]):
                console.print("[yellow]⚠ Nenhum critério ativo. Vá em '2 - Configurar opções padrão' e habilite pelo menos um.[/yellow]")
                Prompt.ask("\nPressione Enter para continuar", default="")
                continue
            executar_geracao(cfg["tamanho"], cfg["quantidade"], cfg["maiusculas"], cfg["minusculas"],
                             cfg["numeros"], cfg["simbolos"], cfg["evitar_ambig"], True, None)
            Prompt.ask("\nPressione Enter para voltar ao menu", default="")

        elif escolha == "2":
            cfg = interactive_configurar()
            console.print("[green]Configuração salva![/green]")
            Prompt.ask("Pressione Enter para gerar com essa configuração agora", default="")
            executar_geracao(cfg[0], cfg[1], cfg[2], cfg[3], cfg[4], cfg[5], cfg[6], True, None)
            Prompt.ask("\nPressione Enter para voltar ao menu", default="")

        elif escolha == "3":
            table = Table(title="Última configuração", show_header=False)
            for k, v in _last_config.items():
                table.add_row(str(k), str(v))
            console.print(table)
            Prompt.ask("\nPressione Enter para voltar ao menu", default="")

        elif escolha == "4":
            console.print("[bold red]Saindo...[/bold red]")
            break

if __name__ == "__main__":
    main()