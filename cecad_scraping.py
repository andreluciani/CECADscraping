#%% 0) Importando as bibliotecas
import urllib.request
import urllib
import pandas as pd
import time


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

#%% 5) Laço de repetição para baixar todos os dados de renda

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

#%% 5) Laço de repetição para baixar todos os população de rua
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
writer=pd.ExcelWriter('Faixa de renda pessoa e familia completo.xlsx', engine='xlsxwriter')
renda_familia.to_excel(writer, sheet_name='FaixaRendaFamilia')
renda_pessoa.to_excel(writer, sheet_name='FaixaRendaPessoa')
pop_rua_familia.to_excel(writer, sheet_name='PopRuaFamilia')
pop_rua_pessoa.to_excel(writer, sheet_name='PopRuaPessoa')
writer.save()

