import os
import sqlalchemy
import argparse
import pandas as pd
import datetime

# Diretórios
BASE_DIR = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data' )
SQL_DIR = os.path.join( BASE_DIR, 'src', 'sql' )

parser = argparse.ArgumentParser()
parser.add_argument( '--date_end', '-e', help='Data de fim da extração', default='2018-06-01' )
args = parser.parse_args()

date_end = args.date_end
ano = int( date_end.split('-')[0] ) - 1
mes = int( date_end.split('-')[1] )
date_init = f'{ano}-{mes}-01'

# Importando a query
with open( os.path.join( SQL_DIR, 'segmentos.sql' ) ) as query_file:
    query = query_file.read()

query = query.format( date_init=date_init, date_end=date_end )

# Conexão com o banco de dados
connection = sqlalchemy.create_engine( 'sqlite:///{}' .format( os.path.join( DATA_DIR, 'olist.db' ) ) )

create_query = f'''
CREATE TABLE tb_seller_sgmt AS {query};
'''

insert_query = f'''
DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
INSERT INTO tb_seller_sgmt {query};
'''

try:
    connection.execute( create_query )
except:
    for q in insert_query.split(';')[:-1]:
        connection.execute( q )
