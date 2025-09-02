from flask import Flask, jsonify
import psycopg2
app = Flask(__name__)

db_user='postgres'
db_password='Hosozu'
db_host='localhost'
db_port='5432'
db_name='link_manager'

DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['DATABASE_URI'] = DATABASE_URI

@app.route("/")
def Home():
    hello = {"status": "ok", "message": "API Link Manager no ar!"}
    return jsonify(hello)

def conectar_db():
    try:
        print('Conectando ao banco de dados...')
        db_uri = app.config['DATABASE_URI']
        conn = psycopg2.connect(db_uri)
        return conn
    except Exception as e:
        print(f'Não foi possivel conectar ao banco de dados. {e}')
        return None

@app.route('/links', methods=['GET'])
def buscar_dados():
    conn = conectar_db()
    if not conn:
        return jsonify({"ERROR": "A conexão com o banco de dados falhou."}), 500
    
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM links;"
        cursor.execute(query)
        rows = cursor.fetchall()
        links = [{"id":rows[0], "url":rows[1], "title":rows[2], "created_at":rows[3]} for link in rows]
        return jsonify(links)
    
    except Exception as e:
        print(f'Erro ao executar a "query": {e}')
        return jsonify({"error": "Falha ao buscar os dados."}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)