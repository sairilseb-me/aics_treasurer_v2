from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os
from sqlalchemy import text
from db_utils import DB_Utils


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

db_utils = DB_Utils(db)

@app.route('/api/test', methods=['GET'])
def test():
    query = text("""Select TOP 10 c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName, a.TypeOfAssistance, a.SourceOfFund, a.Amount, a.ReceivedDate, a.Mode from ClientData as c INNER Join AssistanceData as a on c.ControlNumber = a.ControlNumber Where a.Released = 'No' And a.Amount IS NOT NULL;""")
    result = db.session.execute(query)
    rows = result.fetchall()
    # output = []
    
    # for row in rows:
    #     data = {
    #         "ControlNumber": row.ControlNumber,
    #         "RecordNumber": row.RecordNumber,
    #         "FirstName": row.FirstName,
    #         "MiddleName": row.MiddleName,
    #         "LastName": row.LastName,
    #         "TypeOfAssistance": row.TypeOfAssistance,
    #         "SourceOfFund": row.SourceOfFund,
    #         "Amount": row.Amount,
    #         "ReceivedDate": row.ReceivedDate,
    #         "Mode": row.Mode
    #     }
    #     output.append(data)
        
    # tupl_result = [tuple(row) for row in rows]
    return {"message": "output"}, 200
    

@app.route('/api/get-data', methods=['GET'])
def get_data():
    try:
        # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        # Execute the query
        query = text("""
            SELECT c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName, c.Barangay, c.Municipality, c.Province,
                   a.TypeOfAssistance, a.Category, a.SourceOfFund, a.Amount, a.ReceivedDate, a.Mode
            FROM ClientData AS c
            INNER JOIN AssistanceData AS a ON c.ControlNumber = a.ControlNumber
            WHERE a.Released = 'No' AND a.Amount IS NOT NULL;
        """)
        # Convert query results to list of dictionaries
        output = db_utils.get_data(query)

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
    
@app.route('/api/get-client-processor-data', methods=['GET'])
def get_client_processor_data():
    try:
        #Get ControlNumber and RecordNumber from request
        control_number = request.args.get('control_number')
        record_number = request.args.get('record_number')
        dept = request.args.get('dept')
            
        query_assistance = text(f"""
            SELECT * FROM AssistanceData WHERE ControlNumber = '{control_number}' And RecordNumber = '{record_number}' And Released = 'No';
        """)
        
        query_processor = text(f"""
            SELECT * FROM ProcessorData WHERE ControlNumber = '{control_number}' And RecordNumber = '{record_number}';
        """)
        
        budget_dept = ''
        
        if dept == 'Governors Office':
            budget_dept = 'BudgetGO'
        elif dept == 'PDF':
            budget_dept = 'BudgetPDF'
        else:
            budget_dept = 'BudgetPSWDO'
        
        query_budget = text(f"""SELECT * from {budget_dept} Order By DateChange DESC""")
        
        client = db_utils.get_assistance_data(query_assistance)
        processor = db_utils.get_processor_data(query_processor)
        budget_balance = db_utils.get_budget_amount(query_budget)
        return {'client': client, 'processor': processor, 'budget_balance': budget_balance}, 200
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500
    
@app.route('/api/save-comment/<control_number>/<record_number>', methods=['POST'])
def save_comment(control_number, record_number):
    print(control_number, record_number)
    comment = request.json['comment']
    query = text(f"""UPDATE AssistanceData SET ProblemPresented = :comment WHERE ControlNumber = :control_number And RecordNumber = :record_number """)
    
    result = db_utils.save_comment(query, comment, control_number, record_number)
    if result:
        return {"success": result, "message": "Comment has been saved!"}
    
    return {"success": result, "message": "Saving comment failed!"}


@app.route('/api/release-assistance/<control_number>/<record_number>/<department>', methods=['POST'])
def release_assistance(control_number, record_number, department):
    
    result = db_utils.release_client_data(control_number, record_number, department)

    if result['success']:
        return {"message": "Assistance Released!"}, 200
    
    return {'message': 'Failed to release assistance!'}, 500

@app.route('/api/get-released-assistances', methods=['GET'])
def get_released_assistance():
    
    try:
         # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        date_from = None
        date_to = None
        department = None
        
        if request.args.get('date_from'):
            date_from = request.args.get('date_from')
        
        if request.args.get('date_to'):
            date_to = request.args.get('date_to')
        
        if request.args.get('department'):
            department = request.args.get('department')
            
        output = db_utils.get_released_assistances(date_from, date_to, department)


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
        print(f'Error: {str(e)}')
        return {'Error': 'An error occurred!'}, 500
    


@app.route('/api/search-client', methods=['GET'])
def search_client():
    try:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')

        
        # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        query = ""
        
        if (first_name and last_name):
            query = text(f"""SELECT c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName,
                    a.TypeOfAssistance, a.Category, a.SourceOfFund, a.Amount, a.ReceivedDate, a.Mode
                FROM ClientData AS c
                INNER JOIN AssistanceData AS a ON c.ControlNumber = a.ControlNumber
                WHERE c.FirstName LIKE '%{first_name}%' And c.LastName LIKE '%{last_name}%' And a.Released = 'No' AND a.Amount IS NOT NULL;""")
            
        else: query = text(f"""
                        SELECT c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName,
                            a.TypeOfAssistance, a.Category, a.SourceOfFund, a.Amount, a.ReceivedDate, a.Mode
                            FROM ClientData AS c
                            INNER JOIN AssistanceData AS a ON c.ControlNumber = a.ControlNumber
                            WHERE c.LastName LIKE '%{last_name}%' And a.Released = 'No' AND a.Amount IS NOT NULL;
                        """)
        
        output = db_utils.get_data(query)
        
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
        }), 200
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500
    
@app.route('/api/get-released-assistance/', methods=['GET'])
def get_released_assistance_details():
    
    try:
         # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        
        output = db_utils.get_released_assistance(first_name, last_name)
        
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
        }), 200
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500    
    

if __name__ == '__main__':    
    app.run(debug=True)