import psycopg2
import os

db_user='postgres'
db_password='Hosozu'
db_host='localhost'
db_port='5432'
db_name='link_manager'

DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

try:
    print("Conectando ao banco de dados...")
    conn = psycopg2.connect(DATABASE_URI)
    print('Conexão bem-sucedida!')
except psycopg2.OperationalError as e:
    print(f'Não foi possivel conectar ao banco de dados. {e}')
    exit()

cursor = conn.cursor()

try:
    print('Criando a tabela de "links"...')
    cursor.execute("""
                   CREATE TABLE links(
                   id SERIAL PRIMARY KEY,
                   url VARCHAR(255) NOT NULL,
                   title VARCHAR(255) NOT NULL,
                   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                   );
    """)
    print('Tabela "links" criada com sucesso!')
except psycopg2.errors.DuplicateTable:
    print('A tabela "links" já existe. Nenhuma ação foi tomada.')
except Exception as e:
    print(f'Ocorreu um erro ao criar a tabela: {e}')

conn.commit()

cursor.close()
conn.close()

print('Script finalizado. Conexão com o banco de dados fechada.')