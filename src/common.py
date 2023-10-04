#============================================================================================
# Imports
#============================================================================================
import os
import urllib.parse
import boto3
from flask import request, abort
from functools import wraps

stack = os.getenv('STACK') or 'developer'

#============================================================================================
# Utility Functions
#============================================================================================
def columns(cursor):
    return {i:cd[0] for i,cd in enumerate(cursor.description)}

def getDBConnection(password):   
    # gotta define these
    driver = os.getenv('DB_DRIVER')
    server = os.getenv('DB_HOST')
    db = os.getenv('DB_INSTANCE')
    user = os.getenv('DB_USER')

    dbConnectionString = "driver={" + str(driver) + "};server=" + str(server) + ";database=" + str(db) + ";uid=" + str(user) + ";pwd=" + str(password)
    return dbConnectionString


#============================================================================================
# Decorator
#============================================================================================
def apikey_required(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        apikey = os.getenv('ECS_APIKEY')
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == apikey:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function



#============================================================================================
# Global variables
#============================================================================================
dbPassword = os.getenv('DB_PWD')
db_connection_string = getDBConnection(dbPassword)
apikey = os.getenv('ECS_APIKEY')



