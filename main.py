[18:07, 28/2/2019] ~: # Importa o módulo pandas com o alias 'pd'
import pandas as pd

# Lê o arquivo .csv e atribui o objeto a variável 'participantes'
participantes = pd.read_csv('../csv/EXEC_FINANC_ED_BAS_2017.csv',
                            encoding='utf-8', sep=';')

# Lê o arquivo .csv e atribui o objeto a variável 'censo_email'
'''O arquivo cadastro .csv possui o censo das escolas do Brasil
com email das escolas que participaram do censo 2017
'''
censo_email = pd.read_csv('../csv/cadastro.csv', encoding='utf-8')

# Lê o arquivo .csv e e atribui o objeto a variável 'cadastro_geral'
'''Difenrentemente do arquivo cadastro.csv, o csv citado abaixo possui
dados mais completo, com exceção de email
'''
cadastro_geral = pd.read_csv('../csv/todas_cadastro.csv', low_memory=False)

'''Similar ao PROCV do excel, a função pandas.merge() retorna os dados especificados
presentes nos dois objetos.
Retorna as colunas especificadas dentro dos colchetes quando os dados forem iguais
na coluna cod_inep atribuindo o resultado à variável final
'''
email_column = pd.merge(participantes, censo_email[[
    'cod_inep', 'E-mail']], on='cod_inep', how='inner')
final = pd.merge(participantes, cadastro_geral[[
    'cod_inep', 'terra_indigena', 'endereco', 'num_endereco', 'complemento', 'bairro', 'cep', 'ddd', 'fone1', 'fone2']], on='cod_inep', how='inner')


# Preenche as linhas NaN com 0 para fazer a converão de tipos
final[['fone1', 'ddd']] = final[['fone1', 'ddd']].fillna(
    '0').astype(float).astype(int).astype(str)

# Substitui as linhas com 0 por None(nulo)
final['fone1'] = final['fone1'].replace({'0': None})

# Concatena colunas
final['fone1'] = final['ddd'] + '-' + final['fone1']
final['fone2'] = final['ddd'] + '-' + final['fone2']

# Chamada da função str.strip() para formatar as colunas
final[['bairro', 'endereco']] = final[[
    'bairro', 'endereco']].apply(lambda x: x.str.strip())

# Concatena colunas
final['endereco_escola'] = final['endereco'] + ' ' + \
    final['num_endereco'] + ', ' + final['bairro']

# Preenche as linhas NaN com 0
final['cnpj_uex'] = final['cnpj_uex'].fillna(
    '0').astype(str)
final['cnpj_copy'] = final['cnpj_uex']

''' Formata as colunas especificadas para que cada linha possua 14 dígitos
Nas linhas onde o numero de dígitos forem < 14, serão adicionados 0 a esquerda
'''
final['cnpj_uex'] = final['cnpj_uex'].apply(
    lambda x: '{0:0>14}'.format(x))

# Deleta as colunas especificadas
final.drop(['ddd', 'num_endereco', 'bairro',
            'DT_INI_VINC_DIR', 'cnpj_copy', 'endereco'], axis=1, inplace=True)

final['email'] = email_column['E-mail']

# Renomeia todas as colunas
final.columns = ['uf', 'nome_municipio', 'cod_municipio', 'nome_escola', 'cod_inep', 'qtd_alunos', 'rede', 'nome_uex', 'dirigente_uex',
                 'custeio', 'capital', 'complemento_area', 'complemento_zona', 'cep_escola', 'fone1_escola', 'fone2_escola', 'endereco_escola', 'cnpj_uex', 'email']

# Reordena as colunas
final = final[['uf', 'nome_municipio', 'cod_municipio', 'rede', 'nome_escola', 'complemento_area', 'complemento_zona', 'cod_inep', …
[18:07, 28/2/2019] ~: import pandas as pd

participantes = pd.read_csv(
    '../csv/EXEC_FINANC_ED_BAS_2017.csv', encoding='iso-8859-1', sep=';')

censo_email = pd.read_csv('../csv/cadastro.csv', encoding='utf-8', sep=',')

cadastro_geral = pd.read_csv(
    '../csv/todas_cadastro.csv', encoding='utf-8', low_memory=False)

email_column = pd.merge(
    participantes, censo_email[['cod_inep', 'E-mail']], on='cod_inep', how='outer')

final = pd.merge(participantes, cadastro_geral[[
    'cod_inep', 'terra_indigena', 'endereco', 'num_endereco', 'complemento', 'bairro', 'cep', 'ddd', 'fone1', 'fone2', 'tipo_área']], on='cod_inep', how='left')

final[['fone1', 'ddd']] = final[['fone1', 'ddd']].fillna(
    '0').astype(float).astype(int).astype(str)

final['fone1'] = final['fone1'].replace({'0': None})

# Concatena colunas
final['fone1'] = final['ddd'] + '-' + final['fone1']
final['fone2'] = final['ddd'] + '-' + final['fone2']

# Deleta colunas
final.drop(['ddd'], axis=1, inplace=True)

final[['bairro', 'endereco']] = final[[
    'bairro', 'endereco']].apply(lambda x: x.str.strip())

final['endereco_escola'] = final['endereco'] + ' ' + \
    final['num_endereco'] + '. ' + final['bairro']

final.drop(['num_endereco', 'bairro',
            'DT_INI_VINC_DIR', 'endereco'], axis=1, inplace=True)

final['email'] = email_column['E-mail']

final.columns = ['uf', 'nome_municipio', 'cod_municipio', 'nome_escola', 'cod_inep', 'qtd_alunos', 'rede', 'cnpj_uex', 'nome_uex',
                 'dirigente', 'custeio', 'capital', 'complemento_area', 'complemento_zona', 'cep', 'fone1', 'fone2', 'tipo_zona', 'endereco_escola', 'email']

final = final[['uf', 'nome_municipio', 'cod_municipio', 'rede', 'nome_escola', 'tipo_zona', 'complemento_area', 'complemento_zona', 'cod_inep', 'qtd_alunos',
               'endereco_escola', 'cep', 'fone1', 'fone2', 'email', 'cnpj_uex', 'nome_uex', 'dirigente', 'custeio', 'capital']]

final['cep'] = final['cep'].fillna('00000000').astype(int).astype(str).apply(lambda x: '{0:0>8}'.format(x))
final['cep'] = final['cep'].replace({'00000000': None})

final.to_csv('../csv/cadastros_pdde.csv', encoding='iso-8859-1')
