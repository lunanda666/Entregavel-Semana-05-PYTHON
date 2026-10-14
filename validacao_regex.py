import re
from datetime import datetime  # confere se a data realmente existe

from excecao_personalizada import DadoInvalidoError

# ---------------------------------------------------------------------
# PADROES (raw strings r"..." evitam problemas com a barra invertida)
# ^ e $ exigem que o texto INTEIRO siga o padrao.
# ---------------------------------------------------------------------
# nome@dominio.com : letras, numeros, _, ponto ou hifen antes e depois do @
PADRAO_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
# 000.000.000-00 : 3 digitos, ponto, 3 digitos, ponto, 3 digitos, hifen, 2 digitos
PADRAO_CPF = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
# (00) 0000-0000 ou (00) 00000-0000 : \( e \) casam parenteses literais
PADRAO_TELEFONE = re.compile(r"^\(\d{2}\)\s\d{4,5}-\d{4}$")
# AAAA-MM-DD : so valida o FORMATO; a data real e conferida a parte
PADRAO_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------
# FUNCOES DE VALIDACAO (uma por campo; devolvem True ou False)
# ---------------------------------------------------------------------
def validar_email(email):
    """True se o e-mail seguir o formato nome@dominio.ext."""
    return bool(PADRAO_EMAIL.match(email))


def validar_cpf(cpf):
    """True se o CPF seguir o formato 000.000.000-00 (so o formato)."""
    return bool(PADRAO_CPF.match(cpf))


def validar_telefone(telefone):
    """True se o telefone seguir o formato (00) 00000-0000."""
    return bool(PADRAO_TELEFONE.match(telefone))


def validar_data(data):
    """True se a data estiver em AAAA-MM-DD E existir no calendario."""
    # 1) formato: a regex aceita 2026-02-30, mas essa data nao existe
    if not PADRAO_DATA.match(data):
        return False
    # 2) data real: strptime lanca ValueError se a data for impossivel
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        return False
    return True


# campo do CSV -> funcao que o valida (a ordem define a ordem dos erros)
VALIDADORES = {
    "email": validar_email,
    "cpf": validar_cpf,
    "telefone": validar_telefone,
    "data_cadastro": validar_data,
}

# Texto mostrado quando um campo tem formato invalido.
FORMATOS_ESPERADOS = {
    "email": "nome@dominio.com",
    "cpf": "NNN.NNN.NNN-NN",
    "telefone": "(00) 00000-0000",
    "data_cadastro": "AAAA-MM-DD",
}


def validar_campo(numero_linha, campo, valor):
    """Valida UM campo; lanca DadoInvalidoError se for invalido."""
    if VALIDADORES[campo](valor):
        return  # campo valido: nada a fazer

    # formato certo + invalido so pode ser data impossivel (ex.: 2026-02-30)
    if campo == "data_cadastro" and PADRAO_DATA.match(valor):
        motivo = "data inexistente no calendario"
    else:
        motivo = f"formato esperado: {FORMATOS_ESPERADOS[campo]}"
    raise DadoInvalidoError(numero_linha, campo, valor, motivo)


def validar_clientes(linhas):
    """Valida todos os clientes.

    Devolve (clientes_validos, lista_de_erros, total_de_linhas_invalidas).
    """
    validos = []
    erros = []
    linhas_invalidas = 0

    # start=2 porque a linha 1 do arquivo e o cabecalho
    for numero_linha, cliente in enumerate(linhas, start=2):
        erros_da_linha = []
        for campo in VALIDADORES:
            # .get(...) or "" evita erro se a celula vier vazia/None
            valor = (cliente.get(campo) or "").strip()
            try:
                validar_campo(numero_linha, campo, valor)
            except DadoInvalidoError as erro:
                erros_da_linha.append(erro)  # guarda e segue para o proximo campo

        if erros_da_linha:
            linhas_invalidas += 1
            erros.extend(erros_da_linha)
        else:
            validos.append(cliente)

    return validos, erros, linhas_invalidas


# ---------------------------------------------------------------------
# SUBSTITUICAO COM REGEX (mascara de dado sensivel)
# ---------------------------------------------------------------------
def mascarar_cpf(texto):
    """Troca qualquer CPF do texto por ***.***.***-** (re.sub).

    Os pontos e o hifen sao opcionais (o "?" no padrao), assim tambem
    mascaramos CPFs digitados errado, como 12345678900. O "\\b" marca o
    limite da palavra e evita mascarar pedacos de numeros maiores.
    """
    return re.sub(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", "***.***.***-**", texto)