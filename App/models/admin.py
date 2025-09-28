from App.database import db
from .shift import Shift
#from .user import User

class Admin(db.Model):
    id=db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    name=db.Column(db.String(50),nullable=True)

    user=db.relationship('User', backref=db.backref('admin', uselist=False)) #one-to-one relationship with User

    def __init__(self, id, name): #constructor to initialize an Admin object
        self.id=id
        self.name=name

    def __repr__(self):
        return f'<Admin {self.id} - {self.name}>'
    
    def schedule_shift(self,staff,shift): #function to schedule a shift for a staff member
        new_shift=Shift(staff_id=staff.id,
                        scheduled_time_in=shift['scheduled_time_in'],
                        scheduled_time_out=shift['scheduled_time_out'],
                        date=shift['date']) #create a new Shift object
        db.session.add(new_shift) #add the new Shift object to the database session
        db.session.commit() #commit the changes to the database
        return new_shift
    
    def view_shift_report(self,staff,start_date=None,end_date=None): #function to view a shift report for the week
        query=Shift.query.filter_by(staff_id=staff.id) #query to get all shifts for the staff member

        if start_date and end_date:
            query=query.filter(Shift.date>=start_date,Shift.date<=end_date) #filter shifts by date range
            
        shifts=query.all()
        return [shift.get_json() for shift in shifts] #return the list of shifts
    