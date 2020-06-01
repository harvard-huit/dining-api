#============================================================================================
# Imports
#============================================================================================
import os
import configparser
import urllib.parse
import boto3

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

def getDBConnection(ssmClient, configSection, passwordConfigOption):   
    dbConfig = dict(config[configSection])
    driver = dbConfig['driver']
    server = dbConfig['host']
    db = dbConfig['instance']
    user = dbConfig['user']
    password = getSSMParam(ssmClient, configSection, passwordConfigOption)
    dbConnectionString = "driver={" + driver + "};server=" + server + ";database=" + db + ";uid=" + user + ";pwd=" + password
    return dbConnectionString

#============================================================================================
# AWS Functions
#============================================================================================
def getSSMParam(ssmClient, configSection, configOption):
    parameter = ssmClient.get_parameter(
        Name=config.get(configSection,configOption), 
        WithDecryption=True)
    return parameter['Parameter']['Value']


#============================================================================================
# Global variables
#============================================================================================
ssm = boto3.client('ssm')
dbConfigSection = 'sqlserverDB'
db_connection_string = getDBConnection(ssm, dbConfigSection, 'pass_parameter')



