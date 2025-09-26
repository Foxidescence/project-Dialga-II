from App.database import db
#from .user import User
from .shift import Shift

class Staff(db.Model):
    id=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    name=db.Column(db.String(50),nullable=True)

    #user=db.relationship('User',back_populates='staff',uselist=False)#one-to-one relationship with User
    #shifts=db.relationship('Shift',backref=db.backref('staff',lazy=True)) #one-to-many relationship with Shift

    def __init__(self,id,name): #constructor to initialize a Staff object
        self.id=id
        self.name=name

    def __repr__(self):
        return f'<Staff {self.id} - {self.name}>'

    def get_all_shifts(self,start_date=None,end_date=None): #view the roster of shifts for the week
        query=Shift.query.filter_by(staff_id=self.id) #query to get all shifts for the staff member
        if start_date and end_date:
            query=query.filter(Shift.date>=start_date,Shift.date<=end_date) #filter shifts by date range
        return query.order_by(Shift.date).all() #return a list of dictionaries
                                                    #where each dictionary represents a shift

    def log_time_in(self,shift,time_in): #log the time in for a shift
        shift.logged_time_in=time_in.strftime('%H:%M') #converts time to string
        db.session.commit() #commit changes
        return shift
    
    def log_time_out(self,shift,time_out): #log the time out for a shift
        shift.logged_time_out=time_out.strftime('%H:%M') 
        db.session.commit() #commit changes
        return shift
    

    