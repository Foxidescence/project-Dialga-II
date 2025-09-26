import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
import datetime

from App.database import db, get_migrate
from App.models import (User,Shift,Staff,Admin)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    #initialize()
    db.drop_all()
    db.create_all()

    bob=User(username='bob', password='bobpass')
    sally=User(username='sally', password='sallypass')
    drake=User(username='drake', password='drakepass')

    db.session.add_all([bob, sally, drake])
    db.session.commit()

    bob_admin=Admin(id=bob.id,name='Bob')
    sally_staff=Staff(id=sally.id,name='Sally')
    drake_staff=Staff(id=drake.id,name='Drake')

    db.session.add_all([bob_admin,sally_staff,drake_staff])
    db.session.commit()

    print('database intialized!')

'''
User Commands
'''

@app.cli.command("create-shift", help="Create a shift for a staff member")
def create_shift():
    users=User.query.all() #fetch all the users
    print("Available users:")
    for u in users:
        role_status=""
        if Admin.query.get(u.id):
            role_status=" (Admin)"
        elif Staff.query.get(u.id):
            role_status=" (Staff)"
        print(f'ID: {u.id}, Username: {u.username}{role_status}') #print user details

    user_id = input("Enter your user ID: ") #get the user to enter the ID of their user

    admin_user=Admin.query.get(user_id) #fetch the Admin object
    if not admin_user: 
        print("The selected user is not an admin, or does not exist.") 
        return
    
    all_staff=Staff.query.all() #fetch all the staff members
    print("Staff members:")
    for staff in all_staff:
        print(f'ID: {staff.id}, Name: {staff.name}')
    
    staff_id=input("Enter the ID of the staff member to schedule a shift for: ")
    staff_obj = Staff.query.get(staff_id) # fetch the Staff object using the entered ID
    if not staff_obj:
        print("Staff member not found.")
        return
    
    scheduled_time_in=input("Enter the scheduled time in (HH:MM): ")
    scheduled_time_out=input("Enter the scheduled time out (HH:MM): ")
    date=input("Enter the date (YYYY-MM-DD): ") #enter shift information
    shift={
        'scheduled_time_in':scheduled_time_in,
        'scheduled_time_out':scheduled_time_out,
        'date':date
    } #create a dictionary to hold the shift information

    try:
        new_shift=admin_user.schedule_shift(staff_obj,shift) #schedule the shift/creat the shift object
        print(f'Shift created: {new_shift.get_json()}')
    except Exception as e:
        print(f'Error creating shift: {e}') #print any other error messages



@app.cli.command("view-shift-reports", help="View shift reports for a staff member for the week")
def view_shift_reports():
    today=datetime.date.today().strftime('%Y-%m-%d') #get today's date
    one_week_later=(datetime.date.today()+datetime.timedelta(days=7)).strftime('%Y-%m-%d') #get the date one week from today
    
    users=User.query.all() #fetch all the users, then show them
    print("Available users:")
    for u in users:
        role_status=""
        if Admin.query.get(u.id):
            role_status=" (Admin)"
        elif Staff.query.get(u.id):
            role_status=" (Staff)"
        print(f'ID: {u.id}, Username: {u.username}{role_status}') #print user details
    
    user_id=input("Enter your user ID: ")
    admin_user=Admin.query.get(user_id)
    if not admin_user: 
        print("The selected user is not an admin, or does not exist.") 
        return

    all_staff=Staff.query.all()
    print("Available Staff Members:")
    for s in all_staff:
        print(f'ID: {s.id}, Name: {s.name}') #print staff details

    staff_id=input("Enter the ID of the staff member to view shift reports for: ")
    staff=Staff.query.get(staff_id)
    if not staff:
        print("Staff member not found.")
        return
    
    try:
        reports=admin_user.view_shift_report(staff,today,one_week_later) #view the shift reports for the staff member
        if not reports:
            print("No shift reports found for {staff.name}.")
            return
        else:
            print(f'Shift reports for {staff.name} for the next week:')
            for report in reports: #iterate through and print each report
                print(report)
                print('---')
    except Exception as e:
        print(f'Error viewing shift reports: {e}')


@app.cli.command("view-roster", help="View the roster of shifts for all staff members")
def view_roster():
    today=datetime.date.today().strftime('%Y-%m-%d') #get today's date
    one_week_later=(datetime.date.today()+datetime.timedelta(days=7)).strftime('%Y-%m-%d') #get the date one week from today
    print(f'Roster for the next 7 days ({today} to {one_week_later}):\n')

    all_staff=Staff.query.all() #retreive all staff members
    for staff in all_staff: #iterate through each staff member
        print(f'Staff: {staff.name}') #print the staff member's name
        try:
            roster=staff.get_all_shifts(today,one_week_later) #view the roster of shifts for the staff member
            if not roster:
                print("No shifts scheduled.")
            for shift in roster: #iterate through each shift in the roster
                print(shift.get_json()) #print the shift
                print('---')
        except Exception as e:
            print(f'Error viewing roster for {staff.name}: {e}')
        print("\n")


@app.cli.command("log-time", help="Log time in or out for a shift")
def log_time():
    all_staff=Staff.query.all()
    print("Available Staff: ")
    for s in all_staff:
        print(f'ID: {s.id}, Name: {s.name}') #print staff details

    staff_id=input("Enter your staff ID: ")
    staff_member=Staff.query.get(staff_id) #get the staff member object
    if not staff_member:
        print("Staff member not found.")
        return
    
    shifts=staff_member.get_all_shifts(None,None)#get all the shifts for the staff member
    if not shifts: #if no shifts are found
            print(f'No shifts found for {staff_member.name}.') 
            return
    
    print(f'Shifts for {staff_member.name}:')
    for shift in shifts: #iterate through each shift
        print(shift.get_json()) #print the shift
        print('---')
    
    shift_id=input("Enter the ID of the shift to log time for: ")
    shift=Shift.query.get(shift_id) #get the shift object
    if not shift:
        print("Shift not found.")
        return
    
    action=input("Enter 'in' to log time in or 'out' to log time out: ").lower() #ensure input is lowercase
    try:
        if action=='in':
            time_in_str=input("Enter the time in (HH:MM): ")
            time_in=datetime.datetime.strptime(time_in_str, '%H:%M').time() #convert the time string to a time object
            updated_shift=staff_member.log_time_in(shift,time_in) #log the time in for the shift
            print(f'Time in logged: {updated_shift.get_json()}')
        elif action=='out':
            time_out_str=input("Enter the time out (HH:MM): ")
            time_out=datetime.datetime.strptime(time_out_str, '%H:%M').time() #convert the time string to a time object
            updated_shift=staff_member.log_time_out(shift,time_out) #log the time out for the shift
            print(f'Time out logged: {updated_shift.get_json()}')
        else:
            print("Invalid action. Please enter 'in' or 'out'.")
    except Exception as e:
        print(f'Error logging time: {e}')
        
# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("role", default="staff")
@click.argument("name", default=None, required=False)
def create_user_command(username, password,role):
    create_user(username, password,role)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)