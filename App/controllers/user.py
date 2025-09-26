from App.models import User,Staff,Admin
from App.database import db

def create_user(username, password, role, name=None):
    if (role.lower() not in ['admin', 'staff']): #make sure the user entered a valid role
        raise ValueError("Role must be either 'admin' or 'staff'")
        return None
    
    newuser=User(username=username, password=password)
    db.session.add(newuser)

    db.session.flush()  # Flush to get the new user's ID

    if role.lower()=='admin':
        admin_name=name if name else username.capitalize() #make name username capitalized if no name is provided
        new_role = Admin(id=newuser.id, name=admin_name)
    elif role.lower()=='staff':
        staff_name=name if name else username.capitalize()
        new_role = Staff(id=newuser.id, name=staff_name)

    db.session.add(new_role)
    db.session.commit()
    print(f"New {role.capitalize()} created for user '{username}'!")
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
