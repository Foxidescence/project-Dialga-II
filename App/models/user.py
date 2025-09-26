from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    #staff=db.relationship('Staff',back_populates='user',uselist=False)
    #admin=db.relationship('Admin',backref=db.backref('user', uselist=False))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'

    def get_json(self):
        is_admin=hasattr(self, 'admin') and self.admin is not None
        is_staff=hasattr(self, 'staff') and self.staff is not None

        return{
            'id': self.id,
            'username': self.username,
            'is_admin': is_admin,
            'is_staff': is_staff
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)