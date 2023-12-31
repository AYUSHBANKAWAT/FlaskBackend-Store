from user import User

users = [
    User(1,'Bob','123')
]

username_mapping = {u.username:u for u in users }
userId_mapping = { u.id:u for u in users }

def authenticate( username,password ):
    user =  username_mapping.get(username,None)
    if user and user.password==password:
        return user
    
def identify(payload):
    user_id = payload['identity']
    return userId_mapping.get(user_id,None)
    
