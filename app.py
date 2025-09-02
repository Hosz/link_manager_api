from flask import Flask, jsonify, request
import psycopg2
import os
app = Flask(__name__)

db_user='postgres'
db_password='Hosozu'
db_host='localhost'
db_port='5432'
db_name='link_manager'

DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['DATABASE_URI'] = DATABASE_URI

@app.route("/")
def home():
    hello = {"status": "ok", "message": "API Link Manager no ar!"}
    return jsonify(hello)

def conectar_db():
    conn = psycopg2.connect(DATABASE_URI)
    return conn

@app.route('/links', methods=['GET'])
def buscar_dados():
    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM links ORDER BY id ASC;")

        linha = cursor.fetchall()
        links = [{"id":l[0], "url":l[1], "title":l[2], "created_at":l[3]} for l in linha]
        cursor.close()
        return jsonify(links)
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Erro ao executar a "query": {e}')
        return jsonify({"error": "Falha ao buscar os dados."}), 500
    finally:
        if conn:
            conn.close()

@app.route('/links', methods=['POST'])
def inserir_dados():
    data = request.get_json()
    url = data.get('url')
    title = data.get('title')

    if not url or not title:
        return jsonify({"error": "URL e Titulo são necessarios"}), 400
    
    conn = None

    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO links (url, title) VALUES (%s, %s) RETURNING *;", (url, title)
                       )

        new_link = cursor.fetchone()

        conn.commit()
        cursor.close()

        formated_new_link = {
            "id": new_link[0],
            "url": new_link[1],
            "title": new_link[2],
            "created_at": new_link[3]
        }
        return jsonify(formated_new_link), 201
    except Exception as error:
        if conn:
            conn.rollback()
        return jsonify({"erro": f'Ocorreu um erro: {error}'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)