from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .shift import Shift
#from .staff import Staff

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role=db.Column(db.String(20),nullable=False,default='staff')

    staff=db.relationship('Staff',back_populates='user',uselist=False)

    def __init__(self, username, password, role='staff'):
        self.username = username
        self.set_password(password)
        self.role = role

    def __repr__(self):
        return f'<User {self.id} - {self.username} - {self.role}>'

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def schedule_shift(self,staff,shift): #function to schedule a shift for a staff member
        
        if not self.is_admin():
            raise PermissionError("Only admin users can schedule shifts.")
            
        new_shift=Shift(staff_id=staff.id,
                        scheduled_time_in=shift['scheduled_time_in'],
                        scheduled_time_out=shift['scheduled_time_out'],
                        date=shift['date']) #create a new Shift object
        db.session.add(new_shift) #add the new Shift object to the database session
        db.session.commit() #commit the changes to the database
        return new_shift
    
    def view_shift_report(self,staff,start_date=None, end_date=None): #function to view a shift report for the week
        
        if not self.is_admin():
            raise PermissionError("Only admin users can view shift reports.")
        else:
            query=Shift.query.filter_by(staff_id=staff.id) #query to get all shifts for the staff member

            if start_date and end_date:
                query=query.filter(Shift.date>=start_date,Shift.date<=end_date) #filter shifts by date range
            
            shifts=query.all()
            return [shift.get_json() for shift in shifts] #return the list of shifts
    