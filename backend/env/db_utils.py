
class DB_Utils:
    def __init__(self, db):
        self.db = db
    
    def get_data(self, query):
        result = self.db.session.execute(query)
        rows = result.fetchall()
        dbtype = 'client'
        return self.convert_dict(rows, dbtype)
        
    def convert_dict(self, data, dbtype):
        output = None
        if dbtype == 'client':
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
    
    def get_client_data(self, query):
        result = self.db.session.execute(query)
        row = result.fetchone()
        type = 'client'
        return self.convert_dict(row, type)
        
    def get_processor_data(self, query):
        result = self.db.session.execute(query)
        row = result.fetchone()
        type = 'processor'
        return self.convert_dict(row, type)
        