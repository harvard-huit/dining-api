#============================================================================================
# Imports
#============================================================================================
import os
import configparser
import urllib.parse
import boto3
from flask import request, abort
from functools import wraps

#6y72PMpT9wNKzgRp12

#============================================================================================
# Configuration files.
# Load application configuration from config.DEV.ini, config.STAGE.ini, config.PROD.ini using
# the STACK environment variable, or failing that, from config.DEVELOPER.ini.
# optionxform helps preserve the original case of the config options which are case-sensitive
#============================================================================================
config = configparser.ConfigParser()
config.optionxform = str
stack = os.getenv('STACK') or 'developer'
config.read(f'{os.path.dirname(__file__)}/config/config.{stack}.ini')

#============================================================================================
# Utility Functions
#============================================================================================
def columns(cursor):
    return {i:cd[0] for i,cd in enumerate(cursor.description)}

def getDbPassword(ssmClient, configSection, passwordConfigOption):
    password = getSSMParam(ssmClient, configSection, passwordConfigOption)
    return password

def getDBConnection(configSection, password):   
    dbConfig = dict(config[configSection])
    driver = dbConfig['driver']
    server = dbConfig['host']
    db = dbConfig['instance']
    user = dbConfig['user']
    dbConnectionString = "driver={" + driver + "};server=" + server + ";database=" + db + ";uid=" + user + ";pwd=" + password
    return dbConnectionString


""" def getDBConnectionForLocal(ssmClient, configSection, passwordConfigOption):   
    dbConfig = dict(config[configSection])
    driver = dbConfig['driver']
    server = dbConfig['host']
    db = dbConfig['instance']
    user = dbConfig['user']
    password = getSSMParam(ssmClient, configSection, passwordConfigOption)
    dbConnectionString = "driver={" + driver + "};server=" + server + ";database=" + db + ";uid=" + user + ";pwd=" + password
    return dbConnectionString

def getDBConnectionForAnsibleVars(configSection, nameForVar):   
    dbConfig = dict(config[configSection])
    driver = dbConfig['driver']
    server = dbConfig['host']
    db = dbConfig['instance']
    user = dbConfig['user']
    password = os.getenv('ECS_APIKEY')
    dbConnectionString = "driver={" + driver + "};server=" + server + ";database=" + db + ";uid=" + user + ";pwd=" + password
    return dbConnectionString """

#============================================================================================
# AWS Functions
#============================================================================================
def getSSMParam(ssmClient, configSection, configOption):
    parameter = ssmClient.get_parameter(
        Name=config.get(configSection,configOption), 
        WithDecryption=True)
    return parameter['Parameter']['Value']


#============================================================================================
# Decorator
#============================================================================================
def apikey_required(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == apikey:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function



#============================================================================================
# Global variables
#============================================================================================
ssm = boto3.client('ssm')
dbConfigSection = 'sqlserverDB'
#db_connection_string = getDBConnection(ssm, dbConfigSection, 'pass_parameter')

if stack.lower() == 'developer':
    dbPassword = getDbPassword(ssm, dbConfigSection, 'pass_parameter')
    db_connection_string = getDBConnection(dbConfigSection, dbPassword)
    apikey = getSSMParam(ssm, 'api', 'apikey_parameter')
else:    
    dbPassword = os.getenv('DB_PWD')
    db_connection_string = getDBConnection(dbConfigSection, dbPassword)
    apikey = os.getenv('ECS_APIKEY')



