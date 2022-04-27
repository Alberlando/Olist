import os
import pandas as pd
import sqlalchemy

# Parâmetros do banco de dados
user = 'root'
psw = ''
host = '127.0.0.1'
port = '3306'

# Diretórios
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data' )

# Somente arquivos .csv
files_names = [ i for i in os.listdir( DATA_DIR ) if i.endswith('.csv') ]

# Conexão com o banco de dados
connection = sqlalchemy.create_engine( 'mysql+pymysql://{}:{}@{}:{}' .format(user, psw, host, port) )

# Transformando os datasets em tabelas no banco de dados
for i in files_names:
    df_tmp = pd.read_csv( os.path.join( DATA_DIR, i ) )
    table = 'tb_' + i.strip('.csv').replace('olist_', '').replace('_dataset', '')
    df_tmp.to_sql( table, connection, schema='olist', if_exists='replace', index=False )


