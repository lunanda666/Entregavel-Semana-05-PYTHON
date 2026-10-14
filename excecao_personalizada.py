
class DadoInvalidoError(Exception):
    """Lancada quando um campo do cliente nao respeita a regra de negocio.

    Herda de Exception e guarda a linha, o campo e o valor com problema,
    para que o relatorio consiga informar exatamente onde esta o erro.
    """

    def __init__(self, numero_linha, campo, valor, motivo):
        # guarda os detalhes como atributos para uso posterior
        self.numero_linha = numero_linha
        self.campo = campo
        self.valor = valor
        self.motivo = motivo
        # a mensagem e o que aparece quando fazemos print(erro)
        super().__init__(
            f"Linha {numero_linha}: {campo} '{valor}' invalido ({motivo})"
        )