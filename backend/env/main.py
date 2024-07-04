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
    

@app.route('/api/get-data', methods=['GET'])
def get_data():
    try:
        # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        # Execute the query
        query = text("""
            SELECT c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName,
                   a.TypeOfAssistance, a.Category, a.SourceOfFund, a.Amount, a.ReceivedDate, a.Mode
            FROM ClientData AS c
            INNER JOIN AssistanceData AS a ON c.ControlNumber = a.ControlNumber
            WHERE a.Released = 'No' AND a.Amount IS NOT NULL;
        """)
        result = db.session.execute(query)
        rows = result.fetchall()

        # Convert query results to list of dictionaries
        output = []
        for row in rows:
            data = {
                "ControlNumber": row.ControlNumber,
                "RecordNumber": row.RecordNumber,
                "FirstName": row.FirstName,
                "MiddleName": row.MiddleName,
                "LastName": row.LastName,
                "TypeOfAssistance": row.TypeOfAssistance,
                "Category": row.Category,
                "SourceOfFund": row.SourceOfFund,
                "Amount": row.Amount,
                "ReceivedDate": row.ReceivedDate,
                "Mode": row.Mode
            }
            output.append(data)

        # Calculate total items and pages
        total_items = len(output)
        total_pages = (total_items + per_page - 1) // per_page

        # Slice the output based on page and per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_output = output[start:end]

        # Return paginated results with metadata
        return jsonify({
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page,
            'data': paginated_output
        })
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':    
    app.run(debug=True)