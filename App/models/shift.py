from App.database import db

class Shift(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    staff_id=db.Column((db.String(10)),db.ForeignKey('staff.id'),nullable=False)
    scheduled_time_in=db.Column(db.String(20),nullable=False)
    scheduled_time_out=db.Column(db.String(20),nullable=False)
    date=db.Column(db.String(20),nullable=False)
    logged_time_in=db.Column(db.String(20),nullable=True)
    logged_time_out=db.Column(db.String(20),nullable=True)

    def __init__(self,staff_id,scheduled_time_in,scheduled_time_out,date): #constructor to initialize a Shift object
        self.staff_id=staff_id
        self.scheduled_time_in=scheduled_time_in
        self.scheduled_time_out=scheduled_time_out
        self.date=date
        self.logged_time_in=None
        self.logged_time_out=None

    def get_json(self): #return a dictionary representation of the Shift object
        return{
            'id':self.id,
            'staffID':self.staff_id,
            'scheduled_time_in':self.scheduled_time_in,
            'scheduled_time_out':self.scheduled_time_out,
            'logged_time_in':self.logged_time_in,
            'logged_time_out':self.logged_time_out,
            'date':self.date
        }