
import sys  # acesso aos argumentos da linha de comando

from relatorio_formatado import gerar_relatorio, salvar_resultados
from tratamento_excecoes import ler_clientes
from validacao_regex import validar_clientes


def main():
    """Orquestra: ler -> validar -> relatorio -> salvar."""
    # sys.argv[1] e o primeiro argumento digitado; sem ele, usa o padrao
    caminho = sys.argv[1] if len(sys.argv) > 1 else "clientes.csv"

    linhas = ler_clientes(caminho)
    if linhas is None:  # leitura falhou: nao ha o que analisar
        return

    validos, erros, linhas_invalidas = validar_clientes(linhas)
    relatorio = gerar_relatorio(caminho, len(linhas), validos, erros,
                                linhas_invalidas)
    print()
    print(relatorio)
    salvar_resultados(relatorio, validos)


# executa main() apenas quando o arquivo e rodado diretamente
if __name__ == "__main__":
    main()