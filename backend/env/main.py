from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from models import db, User, Assistance, BudgetGO, BudgetPDF, BudgetPSWDO, Client, LogBook, Processor, RecordComplete, RecordGO, RecordPDF, RecordPSWDO
from dotenv import load_dotenv
import os


load_dotenv()
UID = os.getenv('UID')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mssql+pyodbc://{UID}:{PASSWORD}@{HOST}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=Yes'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)


@app.route('/api/test', methods=['GET'])
def test():
    users = Processor.query.all()
    for user in users:
        if user.ControlNumber is not None:
            print(user.LastName)
    return jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':    
    app.run(debug=True)