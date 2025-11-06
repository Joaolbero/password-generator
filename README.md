# Secure Password Generator 🔐 / Gerador de Senhas Seguro 🔐

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-production-green)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-yellowgreen)](./LICENSE)

---

## SOBRE / ABOUT

**Português (PT-BR)**  
Ferramenta em Python para gerar senhas fortes e personalizáveis. Funciona tanto via menu interativo ("Hackerman Mode") quanto via linha de comando (CLI). Ideal para portfólio, automação e demonstração de boas práticas de segurança.

**English (EN)**  
Python tool to generate strong, customizable passwords. Works both with an interactive menu ("Hackerman Mode") and via command-line (CLI). Great for portfolios, automation tasks and showcasing security-aware practices.

---

## RECURSOS / FEATURES

**Português (PT-BR)**  
- Tamanho configurável  
- Incluir/excluir: maiúsculas, minúsculas, números e símbolos  
- Evitar caracteres ambíguos (ex.: `I`, `l`, `0`, `O`)  
- Garante pelo menos 1 caractere de cada categoria selecionada  
- Modo CLI com flags (para uso em scripts)  
- Menu interativo bonito com `rich` (Hackerman Mode)  
- Copiar para área de transferência (clipboard) via `pyperclip`  
- Salvar saída em `.txt`  
- Medidor simples de força da senha (heurística)

**English (EN)**  
- Configurable length  
- Include/exclude: uppercase, lowercase, digits and symbols  
- Option to avoid ambiguous characters (e.g. `I`, `l`, `0`, `O`)  
- Ensures at least 1 character from each selected class  
- CLI mode with flags (for scripting/automation)  
- Interactive menu (Hackerman Mode) using `rich`  
- Copy to clipboard via `pyperclip`  
- Save output to `.txt`  
- Simple password strength meter (heuristic)

---

## REQUISITOS / REQUIREMENTS

**Português (PT-BR)**  
- Python 3.10+  
- Dependências listadas em `requirements.txt`

**English (EN)**  
- Python 3.10+  
- Dependencies listed in `requirements.txt`

Instalar dependências:
```bash
pip install -r requirements.txt
# ou
pip install pyperclip rich