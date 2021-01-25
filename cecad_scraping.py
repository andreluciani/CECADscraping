#%% 0) Importando as bibliotecas
import urllib.request
import urllib
import pandas as pd
import time
from tqdm import tqdm
from tqdm import notebook

#%% 1) Lendo a lista de municípios e transformando em lista (indexável)
uf_ibge=35
lista_municipios=pd.read_excel("./RELATORIO_DTB_BRASIL_MUNICIPIO.xls")
lista_municipios_UF=lista_municipios['Código Município Completo'][lista_municipios['UF']==uf_ibge].tolist()

#%% 2) Definição das opções pro request
# OPÇÃO : name = value
# MARCAÇÃO PBF: schema = PBF (Com marcação PBF)
# ESTADO/REGIAO: uf_ibge = 12 (AC - Acre)
# CIDADE: p_ibge = 1200013 (Acrelândia)
# VARIAVEL COLUNA: var1 = 'fx_rft' (Faixa da renda familiar per capita)
# VARIAVEL LINHA: var2 = '' (vazio para baixar apenas as faixas de renda familiar)

#%% 3) Laço de repetição para baixar todos os dados de renda
schema='PBF'
uf_ibge=35
renda_pessoa = pd.DataFrame()
renda_familia = pd.DataFrame()

var1='fx_rfpc' 
var2=''

i=0
while i < (len(lista_municipios_UF)):
    try:
        form_data = urllib.parse.urlencode({
        'schema': schema,
        'uf_ibge': uf_ibge,
        'p_ibge': lista_municipios_UF[i],
        'var1': var1,
        'var2': var2}) 

        form_data = form_data.encode("utf-8")
        page_obj = urllib.request.urlopen(
        "https://cecad.cidadania.gov.br/tab_cad_table.php?p_tipo=absoluto",
        form_data)
        raw_data = page_obj.read().decode("utf-8")
        tables_list = pd.read_html(raw_data,index_col=0,thousands='.')  # indexando pela cidade
        tab_familia = tables_list[0].dropna()  # separa a primeira tabela
        tab_pessoa = tables_list[1].dropna()  # separa a segunda tabela
        renda_familia=renda_familia.append(tab_familia.iloc[[0]]) # Cria o df para familia
        renda_pessoa=renda_pessoa.append(tab_pessoa.iloc[[0]]) # Cria o df para pessoa
        print(i)
        i+=1
    except ValueError:
        print('Esperando 10s pra tentar novamente...')
        print('Erro na tentativa ' , i)
        time.sleep(10)
        continue

#%% 4) Laço de repetição para baixar todos os população de rua
schema='PBF'
uf_ibge=35
var1='marc_sit_rua'

pop_rua_pessoa = pd.DataFrame()
pop_rua_familia = pd.DataFrame()
i=0

while i < (len(lista_municipios_UF)):
    try:
        form_data = urllib.parse.urlencode({
        'schema': schema,
        'uf_ibge': uf_ibge,
        'p_ibge': lista_municipios_UF[i],
        'var1': var1,
        'var2': var2}) 

        form_data = form_data.encode("utf-8")
        page_obj = urllib.request.urlopen(
        "https://cecad.cidadania.gov.br/tab_cad_table.php?p_tipo=absoluto",
        form_data)
        raw_data = page_obj.read().decode("utf-8")
        tables_list = pd.read_html(raw_data,index_col=0,thousands='.')  # indexando pela cidade
        tab_familia = tables_list[0].dropna()  # separa a primeira tabela
        tab_pessoa = tables_list[1].dropna()  # separa a segunda tabela
        pop_rua_familia=pop_rua_familia.append(tab_familia.iloc[[0]]) # Cria o df para familia
        pop_rua_pessoa=pop_rua_pessoa.append(tab_pessoa.iloc[[0]]) # Cria o df para pessoa
        print(i)
        i+=1
    except ValueError:
        print('Esperando 10s pra tentar novamente...')
        print('Erro na tentativa ' , i)
        time.sleep(10)
        continue

#%% 6) Salvando em excel
writer=pd.ExcelWriter('Planilha_Output.xlsx', engine='xlsxwriter')
renda_familia.to_excel(writer, sheet_name='FaixaRendaFamilia')
renda_pessoa.to_excel(writer, sheet_name='FaixaRendaPessoa')
pop_rua_familia.to_excel(writer, sheet_name='PopRuaFamilia')
pop_rua_pessoa.to_excel(writer, sheet_name='PopRuaPessoa')
writer.save()
#%% Criando a função

def CECADscraping(lista_UF,lista_dados):
    runs=0
    for uf_ibge in (lista_UF):
        runs= runs + len(lista_municipios['Código Município Completo'][lista_municipios['UF']==uf_ibge].tolist())
    runs = runs * len(lista_dados)
    pbar=notebook.tqdm(total=runs)
    dfs_familia = []
    dfs_pessoa = []
    estados=[]
    infos=[]
    writer=pd.ExcelWriter('Planilha_Output.xlsx', engine='xlsxwriter')

    for uf_ibge in (lista_UF):
        lista_municipios_UF=lista_municipios['Código Município Completo'][lista_municipios['UF']==uf_ibge].tolist()

        for dado in (lista_dados):
            var1=dado
            var2=''
            i=0
            dados_familia = pd.DataFrame()
            dados_pessoa = pd.DataFrame()
            while i < (len(lista_municipios_UF)):
                try:
                    form_data = urllib.parse.urlencode({
                    'schema': schema,
                    'uf_ibge': uf_ibge,
                    'p_ibge': lista_municipios_UF[i],
                    'var1': var1,
                    'var2': var2}) 

                    form_data = form_data.encode("utf-8")
                    page_obj = urllib.request.urlopen(
                    "https://cecad.cidadania.gov.br/tab_cad_table.php?p_tipo=absoluto",
                    form_data)
                    raw_data = page_obj.read().decode("utf-8")
                    tables_list = pd.read_html(raw_data,index_col=0,thousands='.')  # indexando pela cidade
                    tab_familia = tables_list[0].dropna()  # separa a primeira tabela
                    tab_pessoa = tables_list[1].dropna()  # separa a segunda tabela
                    dados_familia=dados_familia.append(tab_familia.iloc[[0]]) # Cria o df para familia
                    dados_pessoa=dados_pessoa.append(tab_pessoa.iloc[[0]]) # Cria o df para pessoa
                    i+=1
                    pbar.update(1)
                except ValueError:
                    print('Esperando 10s pra tentar novamente...')
                    print('Erro na tentativa ' , i)
                    time.sleep(10)
                    continue
            dados_familia.to_excel(writer,sheet_name=('Num. Famlias') + var1)
            dados_pessoa.to_excel(writer,sheet_name=('Num. Pessoas') + var1)


    writer.save()
    pbar.close()
#%% teste da função
lista_UF=[12]
lista_dados = ['fx_rfpc','marc_sit_rua']
CECADscraping(lista_UF,lista_dados)

# %%
