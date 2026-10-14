import json  # gravacao dos clientes validos em JSON

from validacao_regex import VALIDADORES, mascarar_cpf

ARQUIVO_RELATORIO = "relatorio.txt"
ARQUIVO_JSON = "clientes_validos.json"


def gerar_relatorio(caminho, total, validos, erros, linhas_invalidas):
    """Monta o relatorio final em uma unica string usando f-strings."""
    # conta quantos erros cada campo teve (dicionario simples)
    erros_por_campo = {campo: 0 for campo in VALIDADORES}
    for erro in erros:
        erros_por_campo[erro.campo] += 1

    percentual = (len(validos) / total * 100) if total else 0.0

    linhas = [
        "=" * 56,
        f"{'RELATORIO DE ANALISE DE DADOS':^56}",
        "=" * 56,
        f"Arquivo analisado : {caminho}",
        f"Total de registros: {total}",
        f"Registros validos : {len(validos)} ({percentual:.1f}%)",
        f"Registros invalidos: {linhas_invalidas}",
        "",
        "Erros por campo:",
    ]
    for campo, quantidade in erros_por_campo.items():
        linhas.append(f"   {campo:<15} {quantidade}")

    linhas.append("")
    linhas.append("Detalhes dos erros:")
    if erros:
        for erro in erros:
            # mascara CPF para nao expor o dado completo no relatorio
            linhas.append(f"   - {mascarar_cpf(str(erro))}")
    else:
        linhas.append("   (nenhum erro encontrado)")

    linhas.append("")
    linhas.append("Clientes validos:")
    for cliente in validos:
        cpf_mascarado = mascarar_cpf(cliente["cpf"])
        linhas.append(f"   - {cliente['nome']:<12} {cliente['email']:<22} {cpf_mascarado}")
    linhas.append("=" * 56)

    return "\n".join(linhas)


def salvar_resultados(relatorio, validos):
    """Grava o relatorio em .txt e os clientes validos em .json."""
    try:
        # modo "w": cria o arquivo ou sobrescreve o existente
        with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as arquivo:
            arquivo.write(relatorio + "\n")

        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            # ensure_ascii=False preserva acentos; indent=2 deixa legivel
            json.dump(validos, arquivo, ensure_ascii=False, indent=2)
    except OSError as erro:  # PermissionError, disco cheio etc.
        print(f"[ERRO] Nao foi possivel salvar os resultados: {erro}")
    else:
        print(f"[OK] Resultados salvos em '{ARQUIVO_RELATORIO}' "
              f"e '{ARQUIVO_JSON}'.")