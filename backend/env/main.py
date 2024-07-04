from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from models import db, User, Assistance, BudgetGO, BudgetPDF, BudgetPSWDO, Client, LogBook, Processor, RecordComplete, RecordGO, RecordPDF, RecordPSWDO
from dotenv import load_dotenv
import os
from sqlalchemy import text


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
    query = text("""Select c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName, a.TypeOfAssistance, a.SourceOfFund, a.Amount, a.ReceivedDate, a.Mode from ClientData as c INNER Join AssistanceData as a on c.ControlNumber = a.ControlNumber Where a.Released = 'No' And a.Amount IS NOT NULL;""")
    result = db.session.execute(query)
    rows = result.fetchall()
    output = []
    
    for row in rows:
        data = {
            "ControlNumber": row.ControlNumber,
            "RecordNumber": row.RecordNumber,
            "FirstName": row.FirstName,
            "MiddleName": row.MiddleName,
            "LastName": row.LastName,
            "TypeOfAssistance": row.TypeOfAssistance,
            "SourceOfFund": row.SourceOfFund,
            "Amount": row.Amount,
            "ReceivedDate": row.ReceivedDate,
            "Mode": row.Mode
        }
        output.append(data)
        
    # tupl_result = [tuple(row) for row in rows]
    

   

    return {"message": "output", "output": output}, 200

if __name__ == '__main__':    
    app.run(debug=True)