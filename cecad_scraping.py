#%% 0) Importando as bibliotecas
import urllib.request
import urllib
import pandas as pd


#%% 1) Lendo a lista de municípios e transformando em lista (indexável)
uf_ibge=35
lista_municipios=pd.read_excel("./RELATORIO_DTB_BRASIL_MUNICIPIO.xls",sheet_name='DTB_2018_Municipio')
lista_municipios_UF=lista_municipios['Código Município Completo'][lista_municipios['UF']==uf_ibge].tolist()

#%% 2) Definindo opções pro request
# OPÇÃO : name = value
# MARCAÇÃO PBF: schema = PBF (Com marcação PBF)
# ESTADO/REGIAO: uf_ibge = 12 (AC - Acre)
# CIDADE: p_ibge = 1200013 (Acrelândia)
# VARIAVEL COLUNA: var1 = cod_est_cadastral_fam (Estado cadastral da família)
# VARIAVEL LINHA: var2 = fx_rft (Faixa da renda total da família)

schema='PBF'
uf_ibge=35
p_ibge=3500105
var1='cod_est_cadastral_fam'
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



# %%
