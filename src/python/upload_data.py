import os
import pandas as pd
import sqlalchemy

# Diretórios
BASE_DIR = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data' )

# Somente arquivos .csv
files_names = [ i for i in os.listdir( DATA_DIR ) if i.endswith('.csv') ]

# Conexão com o banco de dados
connection = sqlalchemy.create_engine( 'sqlite:///{}' .format( os.path.join( DATA_DIR, 'olist.db' ) ) )

# Transformando os datasets em tabelas no banco de dados
for i in files_names:
    df_tmp = pd.read_csv( os.path.join( DATA_DIR, i ) )
    table = 'tb_' + i.strip('.csv').replace('olist_', '').replace('_dataset', '')
    df_tmp.to_sql( table, connection, if_exists='replace', index=False )


