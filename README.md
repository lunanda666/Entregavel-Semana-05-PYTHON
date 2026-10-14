# Sistema de Análise de Dados de Clientes — Sprint 5

Projeto desenvolvido na disciplina **Desenvolvimento em Python**, no CEUMA (2026.2), para praticar leitura de arquivos, expressões regulares (*regex*) e tratamento de exceções.

O programa lê um arquivo CSV com dados de clientes, valida os campos, identifica informações inválidas sem interromper a execução e gera relatórios em TXT e JSON.

## Estrutura do projeto

| Arquivo | Função |
|---|---|
| `script_principal.py` | Coordena a leitura, a validação e a geração do relatório. |
| `validacao_regex.py` | Valida e-mail, CPF, telefone e data, além de mascarar CPF. |
| `tratamento_excecoes.py` | Trata erros durante a leitura com `try`, `except`, `else` e `finally`. |
| `excecao_personalizada.py` | Define a exceção `DadoInvalidoError`. |
| `relatorio_formatado.py` | Gera o relatório com f-strings e salva os arquivos TXT e JSON. |
| `clientes.csv` | Arquivo de entrada com exemplos válidos e inválidos. |
| `relatorio.txt` | Relatório gerado pelo programa. |
| `clientes_validos.json` | Dados dos clientes aprovados na validação. |
| `README.md` | Documentação do projeto. |

## Como executar

É necessário ter Python 3.8 ou superior. O projeto utiliza apenas bibliotecas padrão do Python: `csv`, `json`, `re`, `sys` e `datetime`.

```bash
python script_principal.py
python script_principal.py outro_arquivo.csv
```

O arquivo CSV deve conter o cabeçalho:

```csv
nome,email,cpf,telefone,data_cadastro
```

## O que o programa faz

1. Lê o CSV com `with open(..., encoding="utf-8")`, preservando os acentos e fechando o arquivo automaticamente.
2. Valida e-mails, CPFs, telefones e datas usando expressões regulares.
3. Trata erros de leitura e validação sem interromper desnecessariamente o processamento.
4. Usa a exceção personalizada `DadoInvalidoError` para registrar dados fora do formato esperado.
5. Gera um relatório com os registros válidos, os erros encontrados e a quantidade de ocorrências por campo.
6. Salva o relatório em `relatorio.txt` e os clientes aprovados em `clientes_validos.json`.

## Validações com regex

Os padrões utilizam *raw strings* (`r"..."`) e os símbolos `^` e `$` para exigir que o campo inteiro siga o formato esperado.

| Campo | Padrão | O que verifica |
|---|---|---|
| E-mail | `^[\w\.-]+@[\w\.-]+\.\w+$` | Estrutura básica de e-mail, com `@` e domínio. |
| CPF | `^\d{3}\.\d{3}\.\d{3}-\d{2}$` | Formato `000.000.000-00`. |
| Telefone | `^\(\d{2}\)\s\d{4,5}-\d{4}$` | DDD entre parênteses, espaço e telefone fixo ou celular. |
| Data | `^\d{4}-\d{2}-\d{2}$` | Formato `AAAA-MM-DD`, complementado por `datetime.strptime` para verificar se a data existe. |

**Limitação:** as regex verificam o formato, mas não garantem a validade real de todos os dados. Por exemplo, o programa não calcula os dígitos verificadores do CPF.

**Privacidade:** o CPF é mascarado com `re.sub` nos relatórios e nas mensagens de erro, evitando a exposição do número completo.

## Tratamento de exceções

| Exceção | Quando ocorre |
|---|---|
| `FileNotFoundError` | O arquivo informado não existe. |
| `PermissionError` | Não há permissão para ler o arquivo. |
| `UnicodeDecodeError` | O arquivo não pode ser decodificado como UTF-8. |
| `KeyError` | Falta alguma coluna obrigatória no CSV. |
| `ValueError` | Uma data não existe, como `2026-02-30`; é tratada na validação da data. |
| `DadoInvalidoError` | Um campo não segue o formato esperado. O erro é registrado e a validação continua. |
| `OSError` | Ocorre uma falha ao gravar o relatório ou o JSON. |

Os blocos são usados da seguinte forma:

- `try`: executa operações que podem falhar.
- `except`: trata erros específicos.
- `else`: executa quando não ocorre uma exceção.
- `finally`: executa independentemente do resultado.

A exceção `DadoInvalidoError` herda de `Exception` e guarda o número da linha, o campo, o valor e o motivo do erro.

## Exemplo de entrada — `clientes.csv`

```csv
nome,email,cpf,telefone,data_cadastro
Ana Souza,ana@email.com,123.456.789-00,(98) 91234-5678,2026-08-30
João Lima,joao@empresa.com.br,987.654.321-00,(11) 3456-7890,2026-09-01
Bruno Alves,bruno@@email,111.222.333-44,(98) 98888-7777,2026-09-05
Carla Dias,carla@email.com,12345678900,(98) 97777-6666,2026-09-10
Diego Melo,diego@email.com,222.333.444-55,98 99999-0000,2026-09-12
Elisa Rocha,elisa@email.com,333.444.555-66,(86) 95555-4444,2026-02-30
Fabio Nunes,fabio@email.com,444.555.666-77,(86) 94444-3333,30/09/2026
Gabi Torres,gabi@email.com,555.666.777-88,(98) 93333-2222,2026-10-01
```

O arquivo contém cinco registros com erros propositais: e-mail inválido, CPF sem pontuação, telefone fora do formato, data inexistente e data em formato diferente do esperado.

## Exemplo de saída

```text
[OK] 8 registro(s) lido(s) de 'clientes.csv'.
[INFO] Leitura do arquivo encerrada.

========================================================
             RELATORIO DE ANALISE DE DADOS
========================================================
Arquivo analisado : clientes.csv
Total de registros: 8
Registros validos : 3 (37.5%)
Registros invalidos: 5

Erros por campo:
   email           1
   cpf             1
   telefone        1
   data_cadastro   2

Detalhes dos erros:
   - Linha 4: email 'bruno@@email' invalido
   - Linha 5: cpf '***.***.***-**' invalido
   - Linha 6: telefone '98 99999-0000' invalido
   - Linha 7: data_cadastro '2026-02-30' invalido
   - Linha 8: data_cadastro '30/09/2026' invalido

Clientes validos:
   - Ana Souza    ana@email.com          ***.***.***-**
   - João Lima    joao@empresa.com.br    ***.***.***-**
   - Gabi Torres  gabi@email.com         ***.***.***-**
========================================================
[OK] Resultados salvos em 'relatorio.txt' e 'clientes_validos.json'.
```

## Exemplos de erros de arquivo

Arquivo inexistente:

```text
$ python script_principal.py nao_existe.csv
[ERRO] Arquivo 'nao_existe.csv' nao encontrado.
[INFO] Leitura do arquivo encerrada.
```

Colunas obrigatórias ausentes:

```text
$ python script_principal.py sem_colunas.csv
[ERRO] CSV fora do formato esperado: coluna(s) ausente(s): cpf, telefone, data_cadastro.
[INFO] Leitura do arquivo encerrada.
```

## Boas práticas utilizadas

- Uso de `with open(..., encoding="utf-8")` para ler e gravar arquivos.
- Tratamento de exceções específicas, sem `except:` genérico.
- Nomes em `snake_case`, seguindo a PEP 8, e docstrings nas funções.
- Expressões regulares testadas no [regex101](https://regex101.com/).
- Uso de `if __name__ == "__main__":` para permitir importar módulos sem executar o programa principal.
