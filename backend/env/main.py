from flask import Flask, request, jsonify, send_file, make_response
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os
from sqlalchemy import text
from db_utils import DB_Utils
import csv
import io
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta




load_dotenv()
UID = os.getenv('UID')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mssql+pyodbc://{UID}:{PASSWORD}@{HOST}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=Yes'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=9)

CORS(app, resources={r"/api/*": {"origins": "*"}}, expose_headers=["X-Custom-Header"])

jwt = JWTManager(app)

db.init_app(app)

db_utils = DB_Utils(db)

revoked_tokens = set()  # Set to store revoked tokens

@app.route('/api/test', methods=['GET'])
def test():
    
    return {"message": "Hello World"}, 200


# Error handling for expired tokens
@jwt.expired_token_loader
def expired_token_callback(expired_token, err):
    try:
        expired_token = expired_token['typ']
        return jsonify({
            'message': f'The {expired_token} token has expired',
            'error': 'token expired'
        }), 401
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500
    
@app.route('/api/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        
        query = text("""SELECT UserName, Password from TreasurerLogin Where UserName = :username And Password = :password;""")
        
        result = db.session.execute(query, {'username': username, 'password': password})
        
        row = result.fetchone()
        
        if row:
            access_token = create_access_token(identity=username)
            return jsonify({"message": "Login Success!", "access_token": access_token, "username": username}), 200
        
        return jsonify({"message": "Login Failed! Please check your credentials."}), 400

    except Exception as e:
        app.logger.error(f'Error: {e}')

        return jsonify({"message": "Login Failed! Please check your credentials."}), 400

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    revoked_tokens.add(jti)
    return jsonify({"message": "Access token has been revoked. User is logged out"}), 200


@app.route('/api/get-data', methods=['GET'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def save_comment(control_number, record_number):
    print(control_number, record_number)
    comment = request.json['comment']
    query = text(f"""UPDATE AssistanceData SET ProblemPresented = :comment WHERE ControlNumber = :control_number And RecordNumber = :record_number """)
    
    result = db_utils.save_comment(query, comment, control_number, record_number)
    if result:
        return {"success": result, "message": "Comment has been saved!"}
    
    return {"success": result, "message": "Saving comment failed!"}


@app.route('/api/release-assistance/<control_number>/<record_number>/<department>', methods=['POST'])
@jwt_required()
def release_assistance(control_number, record_number, department):
    
    try:
        print(control_number, record_number, department)
        result = db_utils.release_client_data(control_number, record_number, department)

        if result['success']:
            return jsonify({"message": "Assistance Released!"}), 200
        else:
            print(result['message'])
            return jsonify({"message": "Failed to release assistance!"}), 500
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'message': 'Failed to release assistance!'}), 500
    

@app.route('/api/get-released-assistances', methods=['GET'])
@jwt_required()
def get_released_assistances():
    
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
            
        if date_from is not None and date_to is None:
            return jsonify({'error': 'Date range is required'}), 400
            
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
@jwt_required()
def search_client():
    try:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')

        
        # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        query = ""
        
        if (first_name and last_name):
            query = text(f"""SELECT c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName, c.Barangay, c.Municipality, c.Province,
                    a.TypeOfAssistance, a.Category, a.SourceOfFund, a.Amount, a.ReceivedDate, a.Mode
                FROM ClientData AS c
                INNER JOIN AssistanceData AS a ON c.ControlNumber = a.ControlNumber
                WHERE c.FirstName LIKE '%{first_name}%' And c.LastName LIKE '%{last_name}%' And a.Released = 'No' AND a.Amount IS NOT NULL;""")
            
        else: query = text(f"""
                        SELECT c.ControlNumber, a.RecordNumber, c.FirstName, c.MiddleName, c.LastName, c.Barangay, c.Municipality, c.Province,
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


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    
@app.route('/api/get-specific-released-assistances/', methods=['GET'])
@jwt_required()
def get_specific_released_assistances():
    
    try:    
         # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        
        print(first_name, last_name)
        
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
        print(str(e))
        return jsonify({'error': 'An error occurred'}), 500    
    

@app.route('/api/export-released-assistances/', methods=['GET'])
@jwt_required()
def export_released_assistance():
    
    try:
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        department = request.args.get('department')
        
        if date_from is None or date_to is None:
            return jsonify({'error': 'Date range is required'}), 400
        
        data = db_utils.get_released_assistances(date_from, date_to, department)
        
        headers = data[0].keys()
        
        total_amount = sum(item['Amount'] for item in data)
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
        total_row = {header: '' for header in headers}
        total_row['Amount'] = total_amount
        writer.writerow(total_row)
        
        filename = f'{date_from}_{date_to}_released_assistance.csv'
        
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        response.headers['Content-type'] = 'text/csv'
        
        return response, 200
        
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500
    
if __name__ == '__main__':    
    app.run(debug=True)