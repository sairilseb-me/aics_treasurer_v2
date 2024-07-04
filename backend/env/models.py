from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'TreasurerLogin'
    __table_args__ = (
        db.PrimaryKeyConstraint('UserName', 'Password', name='user_pk'),
    )
    UserName = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    FirstName = db.Column(db.String(50), nullable=True)
    LastName = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f'User {self.UserName}'
    
class Assistance(db.Model):
    __tablename__ = 'AssistanceData'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=False)
    TypeOfAssistance = db.Column(db.String, nullable=True)
    Category = db.Column(db.String, nullable=True)
    Amount = db.Column(db.Float, nullable=True)
    SourceOfFund = db.Column(db.String, nullable=True)
    ReceivedDate = db.Column(db.DateTime, nullable=True)
    Hospital = db.Column(db.String, nullable=True)
    Doctor = db.Column(db.String, nullable=True)
    ClassType = db.Column(db.String, nullable=True)
    Mode = db.Column(db.String, nullable=True)
    Released = db.Column(db.Text, nullable=True)
    ProblemPresented = db.Column(db.String, nullable=True)
    RecordNumber = db.Column(db.String, nullable=True)
    FirstName = db.Column(db.String, nullable=True)
    MiddleName = db.Column(db.String, nullable=True)
    LastName = db.Column(db.String, nullable=True)
    DateRelease = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'Assistance {self.ControlNumber}'
    
class BudgetGO(db.Model):
    __tablename__ = 'BudgetGO'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=False)
    RecordNumber = db.Column(db.String, nullable=False)
    BudgetAdded = db.Column(db.Float, nullable=True)
    AmountDeducted = db.Column(db.Float, nullable=True)
    BudgetBalance = db.Column(db.Float, nullable=True)
    DateAdded = db.Column(db.DateTime, nullable=True)
    Comment = db.Column(db.String, nullable=True)
    DateChange = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'BudgetGO {self.ControlNumber}'
    
class BudgetPDF(db.Model):
    __tablename__ = 'BudgetPDF'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=False)
    RecordNumber = db.Column(db.String, nullable=True)
    BudgetAdded = db.Column(db.Float, nullable=True)
    AmountDeducted = db.Column(db.Float, nullable=True)
    BudgetBalance = db.Column(db.Float, nullable=True)
    BudgetAddedBy = db.Column(db.String, nullable=True)
    DateAdded = db.Column(db.DateTime, nullable=True)
    Comment = db.Column(db.String, nullable=True)
    DateChange = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'BudgetPDF {self.ControlNumber}'
    
class BudgetPSWDO(db.Model):
    __tablename__ = 'BudgetPSWDO'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=True)
    RecordNumber = db.Column(db.String, nullable=True)
    BudgetAdded = db.Column(db.Float, nullable=True)
    AmountDeducted = db.Column(db.Float, nullable=True)
    BudgetBalance = db.Column(db.Float, nullable=True)
    BudgetAddedBy = db.Column(db.String, nullable=True)
    DateAdded = db.Column(db.DateTime, nullable=True)
    Comment = db.Column(db.String, nullable=True)
    DateChange = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'BudgetPSWDO {self.ControlNumber}'
    
class Client(db.Model):
    __tablename__ = 'ClientData'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', name='client_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=False)
    FirstName = db.Column(db.String, nullable=True)
    MiddleName = db.Column(db.String, nullable=True)
    LastName = db.Column(db.String, nullable=True)
    Gender = db.Column(db.String, nullable=True)
    BirthDate = db.Column(db.Date, nullable=True)
    Age = db.Column(db.String, nullable=True)
    CivilStatus = db.Column(db.String, nullable=True)
    Barangay = db.Column(db.String, nullable=True)
    Municipality = db.Column(db.String, nullable=True)
    Province = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'Client {self.ControlNumber}'
    
class LogBook(db.Model):
    __tablename__ = 'LogBook'
    __table_args__ = (
        db.PrimaryKeyConstraint('UserID', name='userid_pk'),
    )
    UserID = db.Column(db.String, nullable=False)
    DateAndTime = db.Column(db.DateTime, nullable=True)
    Action = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'LogBook {self.UserID}'
    
class Processor(db.Model):
    __tablename__ = 'ProcessorData'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    FirstName = db.Column(db.String, nullable=True)
    MiddleName = db.Column(db.String, nullable=True)
    LastName = db.Column(db.String, nullable=True)
    Gender = db.Column(db.String, nullable=True)
    Barangay = db.Column(db.String, nullable=True)
    Municipality = db.Column(db.String, nullable=True)
    Province = db.Column(db.String, nullable=True)
    Relationship = db.Column(db.String, nullable=True)
    PhoneNumber = db.Column(db.String, nullable=True)
    Work = db.Column(db.String, nullable=True)
    Income = db.Column(db.Integer, nullable=True)
    IDPresented = db.Column(db.String, nullable=True)
    IDNumber = db.Column(db.String, nullable=True)
    DatePresented = db.Column(db.Date, nullable=True)
    ControlNumber = db.Column(db.String, nullable=False)
    Comment = db.Column(db.Text, nullable=True)
    RecordNumber = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'Processor {self.ControlNumber}'
    
class RecordComplete(db.Model):
    __tablename__ = 'RecordComplete'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=True)
    RecordNumber = db.Column(db.String, nullable=True)
    FirstName = db.Column(db.String, nullable=True)
    MiddleName = db.Column(db.String, nullable=True)
    LastName = db.Column(db.String, nullable=True)
    TypeOfAssistance = db.Column(db.String, nullable=True)
    Category = db.Column(db.String, nullable=True)
    SourceOfFund = db.Column(db.String, nullable=True)
    Amount = db.Column(db.Float, nullable=True)
    ReceivedDate = db.Column(db.DateTime, nullable=True)
    ClassType = db.Column(db.String, nullable=True)
    Mode = db.Column(db.String, nullable=True)
    Released = db.Column(db.String, nullable=True)
    Balance = db.Column(db.Float, nullable=True)
    DateRelease = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'RecordComplete {self.ControlNumber}'
    
class RecordGO(db.Model):
    __tablename__ = 'RecordGO'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=True)
    RecordNumber = db.Column(db.String, nullable=True)
    FirstName = db.Column(db.String, nullable=True)
    MiddleName = db.Column(db.String, nullable=True)
    LastName = db.Column(db.String, nullable=True)
    TypeOfAssistance = db.Column(db.String, nullable=True)
    Category = db.Column(db.String, nullable=True)
    SourceOfFund = db.Column(db.String, nullable=True)
    Amount = db.Column(db.Float, nullable=True)
    ReceivedDate = db.Column(db.DateTime, nullable=True)
    Mode = db.Column(db.String, nullable=True)
    ClassType = db.Column(db.String, nullable=True)
    Released = db.Column(db.String, nullable=True)
    Balance = db.Column(db.Float, nullable=True)
    DateRelease = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'RecordGO {self.ControlNumber}'
    
class RecordPDF(db.Model):
    __tablename__ = 'RecordPDF'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=True)
    RecordNumber = db.Column(db.String, nullable=True)
    FirstName = db.Column(db.String, nullable=True)
    MiddleName = db.Column(db.String, nullable=True)
    LastName = db.Column(db.String, nullable=True)
    TypeOfAssistance = db.Column(db.String, nullable=True)
    Category = db.Column(db.String, nullable=True)
    SourceOfFund = db.Column(db.String, nullable=True)
    Amount = db.Column(db.Float, nullable=True)
    ReceivedDate = db.Column(db.DateTime, nullable=True)
    ClassType = db.Column(db.String, nullable=True)
    Mode = db.Column(db.String, nullable=True)
    Released = db.Column(db.String, nullable=True)
    Balance = db.Column(db.Float, nullable=True)
    DateRelease = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'RecordPDF {self.ControlNumber}'
    
class RecordPSWDO(db.Model):
    __tablename__ = 'RecordPSWDO'
    __table_args__ = (
        db.PrimaryKeyConstraint('ControlNumber', 'RecordNumber', name='control_record_pk'),
    )
    ControlNumber = db.Column(db.String, nullable=True)
    RecordNumber = db.Column(db.String, nullable=True)
    FirstName = db.Column(db.String, nullable=True)
    MiddleName = db.Column(db.String, nullable=True)
    LastName = db.Column(db.String, nullable=True)
    TypeOfAssistance = db.Column(db.String, nullable=True)
    Category = db.Column(db.String, nullable=True)
    SourceOfFund = db.Column(db.String, nullable=True)
    Amount  = db.Column(db.Float, nullable=True)
    ReceivedDate = db.Column(db.DateTime, nullable=True)
    Classtype = db.Column(db.String, nullable=True)
    Mode = db.Column(db.String, nullable=True)
    Released = db.Column(db.String, nullable=True)
    Balance = db.Column(db.Float, nullable=True)
    DateReceived = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'RecordPSWDO {self.ControlNumber}'
    

    
    
    
    
    
    
    
