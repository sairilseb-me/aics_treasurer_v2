
class DB_Utils:
    def __init__(self, db):
        self.db = db
    
    def get_data(self, query):
        result = self.db.session.execute(query)
        rows = result.fetchall()
        return self.convert_dict(rows)
        
    def convert_dict(self, data):
        output = None
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
             
        return output
       
    
    def get_client_processor_data(self, query):
        result = self.db.session.execute(query)
        row = result.fetchone()
        return self.convert_dict(row)
        
        