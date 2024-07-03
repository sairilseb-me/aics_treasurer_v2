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