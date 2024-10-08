from flask import Flask, request, jsonify
from flask_cors import CORS  # CORSのインポート
import sqlite3

app = Flask(__name__)
CORS(app)  # CORSを有効にする

# /hello エンドポイント
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

# データベース接続
def connect_db():
    return sqlite3.connect('reservations.db')

# 予約データを追加するAPI
@app.route('/reservations', methods=['POST'])
def add_reservation():
    try:
        reservations = request.json['reservations']
        conn = connect_db()
        cursor = conn.cursor()
        for reservation in reservations:
            cursor.execute('INSERT INTO reservations (date, time) VALUES (?, ?)', (reservation['date'], reservation['time']))
        conn.commit()
        conn.close()
        return jsonify({'message': '予約が成功しました！'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # エラーを返す

# 予約データを取得するAPI
@app.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reservations')
        reservations = cursor.fetchall()
        conn.close()
        return jsonify(reservations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # エラーを返す

if __name__ == '__main__':
    app.run(debug=True)
