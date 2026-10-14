import csv  # leitura estruturada de CSV

# Colunas que o CSV precisa ter (a falta de uma delas gera KeyError).
COLUNAS_OBRIGATORIAS = ["nome", "email", "cpf", "telefone", "data_cadastro"]


def ler_clientes(caminho):
    """Le o CSV e devolve uma lista de dicionarios (um por cliente).

    Devolve None se o arquivo nao puder ser lido.
    """
    linhas = None  # fica None se algo der errado
    try:
        # with garante o fechamento do arquivo, mesmo em caso de erro
        with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)  # cada linha vira um dicionario

            # confere se todas as colunas obrigatorias existem
            colunas_encontradas = leitor.fieldnames or []
            faltando = [c for c in COLUNAS_OBRIGATORIAS
                        if c not in colunas_encontradas]
            if faltando:
                # KeyError e a excecao ideal para "chave/coluna inexistente"
                raise KeyError(f"coluna(s) ausente(s): {', '.join(faltando)}")

            linhas = list(leitor)  # carrega todas as linhas na memoria
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{caminho}' nao encontrado.")
    except PermissionError:
        print(f"[ERRO] Sem permissao para ler '{caminho}'.")
    except UnicodeDecodeError:
        print(f"[ERRO] '{caminho}' nao esta em UTF-8.")
    except KeyError as erro:
        # erro.args[0] traz o texto sem as aspas extras do KeyError
        print(f"[ERRO] CSV fora do formato esperado: {erro.args[0]}.")
    else:
        # else roda SO se nenhuma excecao ocorreu no try
        print(f"[OK] {len(linhas)} registro(s) lido(s) de '{caminho}'.")
    finally:
        # finally roda SEMPRE, com ou sem erro
        print("[INFO] Leitura do arquivo encerrada.")
    return linhas