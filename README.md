# CECADscraping

## Descrição

Código para obter dados do site do [cadastro único](https://cecad.cidadania.gov.br/tab_cad.php).

## Autores

André Luciani da Silva @andreluciani  
Ricardo Raspini Motta @ricardormotta

## Funcionalidade

O código baixa e compila os dados de faixa de renda (por família e por pessoa) e de população em situação de rua para todos os municípios do estado de São Paulo, e depois salva em uma planilha de Excel de maneira organizada para pós processamento. Pode ser alterado para download de quaisquer dados disponíveis no CECAD, para todos os município de qualquer dos estados da federação.

### Utilização

A utilização deve ser feita com as linhas finais do arquivo, selecionando as regiões para download dos dados e os dados a serem baixados. Os arquivos [variaveis.txt](./variaveis.txt) e [selecao_geografica.txt](selecao_geografica.txt) mostram as opções disponíveis no site.


## Tecnologias

Código escrito totalmente em Python.  
Utiliza as bibliotecas urllib, pandas, time e tqdm,