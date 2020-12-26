import urllib.request
import urllib
# from bs4 import BeautifulSoup
# import pandas as pd

# 1) Definindo opções pro request
# OPÇÃO : name = value
# MARCAÇÃO PBF: schema = PBF (Com marcação PBF)
# ESTADO/REGIAO: uf_ibge = 12 (AC - Acre)
# CIDADE: p_ibge = 1200013 (Acrelândia)
# VARIAVEL COLUNA: var1 = cod_est_cadastral_fam (Estado cadastral da família)
# VARIAVEL LINHA: var2 = fx_rft (Faixa da renda total da família)

form_data = urllib.parse.urlencode({
    'schema': 'PBF',
    'uf_ibge': 12,
    'p_ibge': 1200013,
    'var1': 'cod_est_cadastral_fam',
    'var2': 'fx_rft'})
form_data = form_data.encode("utf-8")

# 2) Carregando tabelas
page_obj = urllib.request.urlopen(
    "https://cecad.cidadania.gov.br/tab_cad_table.php?p_tipo=absoluto",
    form_data)
raw_data = page_obj.read()

# 3) Convertendo tabelas para dataframe
