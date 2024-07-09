from sqlalchemy import text
from datetime import datetime

class DB_Utils:
    def __init__(self, db):
        self.db = db
    
    def get_data(self, query):
        result = self.db.session.execute(query)
        rows = result.fetchall()
        dbtype = 'assistance'
        return self.convert_dict(rows, dbtype)
        
    def convert_dict(self, data, dbtype):
        output = None
        if dbtype == 'assistance':
            if type(data) == list:
                output = []
                for row in data:
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
            else: 
                output = {
                        "ControlNumber": data.ControlNumber,
                        "RecordNumber": data.RecordNumber,
                        "ProcessorFirstName": data.FirstName,
                        "ProcessorMiddleName": data.MiddleName,
                        "ProcessorLastName": data.LastName,
                        "TypeOfAssistance": data.TypeOfAssistance,
                        "Category": data.Category,
                        "SourceOfFund": data.SourceOfFund,
                        "Amount": data.Amount,
                        "ReceivedDate": data.ReceivedDate,
                        "ClassType": data.ClassType,
                        "Mode": data.Mode,
                        "Released": data.Released,
                        "Hospital": data.Hospital,
                        "ProblemPresented": data.ProblemPresented,
                    }
        elif dbtype == 'client':
            output = {
                "FirstName": data.FirstName,
                "MiddleName": data.MiddleName,
                "LastName": data.LastName,
                "Gender": data.Gender,
                "BirthDate": data.Birthdate,
                "Age": data.Age,
                "CivilStatus": data.CivilStatus,
                "Barangay": data.Barangay,
                "Municipality": data.Municipality,
                "Province": data.Province
            }
        elif dbtype == 'processor':
            output = {
                "FirstName": data.FirstName,
                "MiddleName": data.MiddleName,
                "LastName": data.LastName,
                "Gender": data.Gender,
                "Barangay": data.Barangay,
                "Municipality": data.Municipality,
                "Province": data.Province,
                "Relationship": data.Relationship,
                "PhoneNumber": data.PhoneNumber,
                "Work": data.Work,
                "Income": data.Income,
                "IDPresented": data.IDPresented,
                "IDNumber": data.IDNumber,
                "DatePresented": data.DatePresented,
            }
       
        return output
    
    def get_assistance_data(self, query):
        result = self.db.session.execute(query)
        row = result.fetchone()
        type = 'assistance'
        if row:
            return self.convert_dict(row, type)
        
    def get_client_data(self, query, control_number):
        result = self.db.session.execute(query, {'control_number': control_number})
        row = result.fetchone()
        type = 'client'
        return self.convert_dict(row, type)
        
        
    def get_processor_data(self, query):
        result = self.db.session.execute(query)
        row = result.fetchone()
        type = 'processor'
        return self.convert_dict(row, type)
    
    def get_budget_amount(self, query):
        result = self.db.session.execute(query)
        row = result.fetchone()
        return row.BudgetBalance
    
    def save_comment(self, query, comment, control_number, record_number):
        result = self.db.session.execute(query, {'comment': comment, 'control_number': control_number, 'record_number': record_number})
        self.db.session.commit()
        if result:
            return True
        return False
    
    def release_client_data(self, control_number, record_number, dept):
        
        try:
            budget_dept = ''
            record_dept = ''
            
            if dept == 'Governors Office':
                budget_dept = 'BudgetGO'
                record_dept = 'RecordGO'
            elif dept == 'PDF':
                budget_dept = 'BudgetPDF'
                record_dept = 'RecordPDF'
            else:
                budget_dept = 'BudgetPSWDO'
                record_dept = 'RecordPSWDO'
                
            get_budget_query = text(f"""SELECT * from {budget_dept} Order By DateChange DESC""")
            get_assistance_query = text(f"""
                SELECT * FROM AssistanceData WHERE ControlNumber = '{control_number}' And RecordNumber = '{record_number}' And Released = 'No';
            """)
            
            get_client_data_query = text(f"""
                                        Select * from ClientData where ControlNumber = :control_number
                                    """)
            
            client_data = self.get_client_data(get_client_data_query, control_number)
            
            budget_balance = float(self.get_budget_amount(get_budget_query))
            client_assistance_data = self.get_assistance_data(get_assistance_query)
            deduct_amount = float(client_assistance_data['Amount'])
            user_data = 'vgabaleo'
            current_date_time = datetime.now()
            
            new_budget = float(budget_balance - deduct_amount)
            
            set_budget_query = text(f"""
                                        Insert INTO {budget_dept} (ControlNumber, RecordNumber, AmountDeducted, BudgetBalance, DateChange) VALUES 
                                        (:control_number, :record_number, :deduct_amount, :budget_balance, :date_change)  
                                    """)
            
            set_record_query = text(
                f"""
                    Insert INTO {record_dept} (ControlNumber, RecordNumber, FirstName, MiddleName, LastName, TypeOfAssistance, Category, SourceOfFund, Amount, 
                    ReceivedDate, Mode, ClassType, Released, Balance, DateRelease) values
                    (:control_number, :record_number, :first_name, :middle_name, :last_name, 
                    :type_of_assistance, :category, :source_of_fund, :amount, :received_date, :mode, :class_type, :released, :balance, :date_release)
                """
            )
            
            set_complete_record_query = text("""
                                                 Insert INTO RecordComplete (ControlNumber, RecordNumber, FirstName, MiddleName, LastName, TypeOfAssistance, Category, SourceOfFund, Amount, 
                                                ReceivedDate, Mode, ClassType, Released, Balance, DateRelease) values
                                                (:control_number, :record_number, :first_name, :middle_name, :last_name, 
                                                :type_of_assistance, :category, :source_of_fund, :amount, :received_date, :mode, :class_type, :released, 
                                                :balance, :date_release)
                                             """)
            
            update_assistance_query = text("""
                                            UPDATE AssistanceData SET Released = 'Yes', DateRelease = :date_release WHERE ControlNumber = :control_number And RecordNumber = :record_number
                                           """)
            
            
            set_log_query = text("""
                                    INSERT INTO LogBook (UserID, DateAndTime, Action) Values
                                    (:user_id, :date_time, :action)
                                 """)
            
            
            result_budget_query = self.db.session.execute(set_budget_query, {'control_number': control_number, 'record_number': record_number, 
                                                                             'deduct_amount': deduct_amount, 'budget_balance': new_budget, 'date_change': current_date_time})
            
            result_record_query = self.db.session.execute(set_record_query, {'control_number': client_assistance_data['ControlNumber'], 
                                                                             'record_number': client_assistance_data['RecordNumber'], 'first_name': client_data['FirstName'], 
                                                                             'middle_name': client_data['MiddleName'], 'last_name': client_data['LastName'], 
                                                                             'type_of_assistance': client_assistance_data['TypeOfAssistance'], 'category': client_assistance_data['Category'], 
                                                                             'source_of_fund': client_assistance_data['SourceOfFund'], 'amount': client_assistance_data['Amount'], 
                                                                             'received_date': client_assistance_data['ReceivedDate'], 'mode': client_assistance_data['Mode'], 
                                                                             'class_type': 'Released', 'released': 'Yes', 'balance': new_budget, 
                                                                             'date_release': current_date_time})
            
            
            result_complete_record_query = self.db.session.execute(set_complete_record_query, {'control_number': client_assistance_data['ControlNumber'], 
                                                                             'record_number': client_assistance_data['RecordNumber'], 'first_name': client_data['FirstName'], 
                                                                             'middle_name': client_data['MiddleName'], 'last_name': client_data['LastName'], 
                                                                             'type_of_assistance': client_assistance_data['TypeOfAssistance'], 'category': client_assistance_data['Category'], 
                                                                             'source_of_fund': client_assistance_data['SourceOfFund'], 'amount': client_assistance_data['Amount'], 
                                                                             'received_date': client_assistance_data['ReceivedDate'], 'mode': client_assistance_data['Mode'], 
                                                                             'class_type': 'Released', 'released': 'Yes', 'balance': new_budget, 
                                                                             'date_release': current_date_time})
            
            
            
            result_update_assistance_query = self.db.session.execute(update_assistance_query, {'control_number': client_assistance_data['ControlNumber'], 
                                                                                               'record_number': client_assistance_data['RecordNumber'], 
                                                                                               'date_release': current_date_time})
            
            
            result_log_query = self.db.session.execute(set_log_query, {'user_id': user_data, 'date_time': current_date_time, 'action': 'Released Client Assistance'})
            
            
            self.db.session.commit()
            return {'success': True, 'message': 'Client Assistance has been released!'}
        except Exception as e:
            self.db.session.rollback()
            return {'success': False, 'message': str(e) }
            
       
        
        
        
      

      
        
        
        
            
        
        
        