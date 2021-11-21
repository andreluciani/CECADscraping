# %% Importando as bibliotecas
import urllib.request
import urllib
import pandas as pd
import time
from tqdm import tqdm

# %% Criando a função


def CECADscraping(lista_UF, lista_dados, lista_municipios):
    schema = "PBF"
    runs = 0
    for uf_ibge in lista_UF:
        runs = runs + len(
            lista_municipios["Código Município Completo"][
                lista_municipios["UF"] == uf_ibge
            ].tolist()
        )
    runs = runs * len(lista_dados)
    pbar = tqdm(total=runs)
    for uf_ibge in lista_UF:
        lista_municipios_UF = lista_municipios["Código Município Completo"][
            lista_municipios["UF"] == uf_ibge
        ].tolist()

        for dado in lista_dados:
            var1 = dado
            var2 = ""
            i = 0
            dados_familia = pd.DataFrame()
            dados_pessoa = pd.DataFrame()
            while i < (len(lista_municipios_UF)):
                try:
                    form_data = urllib.parse.urlencode(
                        {
                            "schema": schema,  # marcação PBF
                            "uf_ibge": uf_ibge,  # seleção geográfica
                            "p_ibge": lista_municipios_UF[i],  # código município
                            "var1": var1,  # variável coluna
                            "var2": var2,
                        }
                    )  # variável linha

                    form_data = form_data.encode("utf-8")
                    page_obj = urllib.request.urlopen(
                        "https://cecad.cidadania.gov.br/tab_cad_table.php?p_tipo=absoluto",
                        form_data,
                    )
                    raw_data = page_obj.read().decode("utf-8")
                    tables_list = pd.read_html(
                        raw_data, index_col=0, thousands="."
                    )  # indexando pela cidade
                    # separa a primeira tabela
                    tab_familia = tables_list[0].dropna()
                    # separa a segunda tabela
                    tab_pessoa = tables_list[1].dropna()
                    dados_familia = dados_familia.append(
                        tab_familia.iloc[[0]]
                    )  # Cria o df para familia
                    dados_pessoa = dados_pessoa.append(
                        tab_pessoa.iloc[[0]]
                    )  # Cria o df para pessoa
                    i += 1
                    pbar.update(1)
                except:
                    print("Esperando 10s pra tentar novamente...")
                    print("Erro na tentativa ", i)
                    time.sleep(10)
                    continue

            dados_familia.to_csv(
                ("./output/num_familias_" + 
                var1 + 
                dados_familia.iloc[[0]].index[0][:2] + 
                ".csv"
                )
            )
            dados_pessoa.to_csv(
                ("./output/num_pessoas_" + 
                var1 + 
                dados_familia.iloc[[0]].index[0][:2] + 
                ".csv"
                )
            )

    pbar.close()

# %% Rodando a função
if __name__ == "__main__":
    lista_municipios = pd.read_excel("./RELATORIO_DTB_BRASIL_MUNICIPIO.xls")
    lista_UF = [35]
    lista_dados = [
        "marc_sit_rua",
        "cod_est_cadastral_fam",
        "fx_rft",
        "fx_rfpc",
        "marc_pbf",
        "marc_sit_rua",
    ]
    CECADscraping(lista_UF, lista_dados, lista_municipios)
# %%
