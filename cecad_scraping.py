#%% 0) Importando as bibliotecas
import urllib.request
import urllib
import pandas as pd


#%% 1) Lendo a lista de municípios e transformando em lista (indexável)
uf_ibge=35
lista_municipios=pd.read_excel("./RELATORIO_DTB_BRASIL_MUNICIPIO.xls")
lista_municipios_UF=lista_municipios['Código Município Completo'][lista_municipios['UF']==uf_ibge].tolist()

#%% 2) Definindo opções pro request
# OPÇÃO : name = value
# MARCAÇÃO PBF: schema = PBF (Com marcação PBF)
# ESTADO/REGIAO: uf_ibge = 12 (AC - Acre)
# CIDADE: p_ibge = 1200013 (Acrelândia)
# VARIAVEL COLUNA: var1 = 'fx_rft' (Faixa da renda familiar per capita)
# VARIAVEL LINHA: var2 = '' (vazio para baixar apenas as faixas de renda familiar)

schema='PBF'
uf_ibge=35
p_ibge=3500105
var1='fx_rfpc' 
var2=''

form_data = urllib.parse.urlencode({
    'schema': schema,
    'uf_ibge': uf_ibge,
    'p_ibge': p_ibge,
    'var1': var1,
    'var2': var2}) 
form_data = form_data.encode("utf-8")

#%% 3) Carregando tabelas
page_obj = urllib.request.urlopen(
    "https://cecad.cidadania.gov.br/tab_cad_table.php?p_tipo=absoluto",
    form_data)
raw_data = page_obj.read().decode("utf-8")   # .decode("utf-8") converte para string
#%% 4) Convertendo tabelas para dataframe
tables_list = pd.read_html(raw_data,index_col=0,thousands='.')  # indexando pela cidade
tab_familia = tables_list[0].dropna()  # separa a primeira tabela
tab_pessoa = tables_list[1].dropna()  # separa a segunda tabela



#%% 5) Laço de repetição para baixar todos os dados
valores_pessoa = pd.DataFrame()
valores_familia = pd.DataFrame()
for i in range(len(lista_municipios_UF)):
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
    valores_familia=valores_familia.append(tab_familia.iloc[[0]]) # Cria o df para familia
    valores_pessoa=valores_pessoa.append(tab_pessoa.iloc[[0]]) # Cria o df para pessoa
    print(i)



# %%
