from flask import Flask

def login_required(func):
    def wrapper(*args, **kwargs):
        if not Flask.user_id:
            return {'message': 'Admin must be authorized.'}, 401
        else :
            return func(*args, **kwargs)
    return wrapper
