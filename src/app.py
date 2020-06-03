from flask import Flask, request
from flask_restplus import Resource, Api
import common
import re
import json
import os
import base64
import boto3
import pyodbc
import configparser

app = Flask(__name__)
api = Api(app)

@api.route('/monitor/health')
class Health(Resource):
    def get(self):
        # environment var STACK, dev, test, stage, prod        
        conn = pyodbc.connect(common.db_connection_string)
       
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (10) Location_Number FROM Locations")        

        retStr = ""
        while True:
            row = cursor.fetchone()            
            if row == None:
                break
            else:
                retStr = retStr + row.Location_Number            

        conn.close()
        return retStr

@api.route('/monitor/driver')
class Driver(Resource):
    def get(self):
        return pyodbc.drivers()

@api.route('/locations')
class Locations(Resource):
    def get(self):

        try:            
            conn = pyodbc.connect(common.db_connection_string)
        except conn.DatabaseError as e:
            obj, = e.args
            print(("Context:", obj.context))
            print(("Message:", obj.message))
            return "Error Connecting to the DB", 500
   
        locations = []
        cursor = conn.cursor()
        cursor.execute("select l.location_number, l.location_name from locations as l")        

        for row in cursor:                
            #this creates a dict out of the array of values
            locations.append({common.columns(cursor)[i]:row[i] for i in range(0, len(row))})
        
        conn.close()
        return json.loads(json.dumps(locations, indent=4, sort_keys=True, default=str))

@api.route('/events')
class Events(Resource):
    def get(self):

        try:            
            conn = pyodbc.connect(common.db_connection_string)
        except conn.DatabaseError as e:
            obj, = e.args
            print(("Context:", obj.context))
            print(("Message:", obj.message))
            return "Error Connecting to the DB", 500
   
        events = []
        cursor = conn.cursor()
        cursor.execute("""select f.meal_name,l.location_number,l.location_name,
        f.serve_date,f.menu_category_name,f.menu_category_number,f.meal_number
        from forecastedrecipes as f
        join locations as l on f.location_number = l.location_number
        where 1=1
        group by f.meal_name, l.location_number, l.location_name, f.serve_date, f.meal_number, f.menu_category_name, f.menu_category_number
        order by l.location_number""")        

        for row in cursor:                
            #this creates a dict out of the array of values
            events.append({common.columns(cursor)[i]:row[i] for i in range(0, len(row))})
        
        conn.close()
        return json.loads(json.dumps(events, indent=4, sort_keys=True, default=str))


@api.route('/recipes')
class Recipes(Resource):
    def get(self):

        try:            
            conn = pyodbc.connect(common.db_connection_string)
        except conn.DatabaseError as e:
            obj, = e.args
            print(("Context:", obj.context))
            print(("Message:", obj.message))
            return "Error Connecting to the DB", 500
   
        recipes = []
        cursor = conn.cursor()
        cursor.execute("""
        select  f.ID,
        f.Serve_Date,
        f.Meal_Number,
        f.Meal_Name,
        l.Location_Number,
        l.Location_Name,
        f.Menu_Category_Number,
        f.Menu_Category_Name,
        f.Recipe_Number,
        f.Recipe_Name,
        f.Recipe_Print_As_Name,
        f.Ingredient_List,
        f.Allergens,
        f.Recipe_Print_As_Color,
        f.Recipe_Print_As_Character,
        f.Recipe_Product_Information,
        convert(varchar(30), f.Selling_Price, 1) as selling_price,
        convert(varchar(30), f.Portion_Cost, 1) as portion_cost,
        f.Production_Department,
        f.Service_Department,
        f.Catering_Department,
        f.Recipe_Web_Codes,
        f.Serving_Size,
        f.Calories,
        f.Calories_From_Fat,
        f.Total_Fat,
        f.Total_Fat_DV,
        f.Sat_Fat,
        f.Sat_Fat_DV,
        f.Trans_Fat,
        f.Trans_Fat_DV,
        f.Cholesterol,
        f.Cholesterol_DV,
        f.Sodium,
        f.Sodium_DV,
        f.Total_Carb,
        f.Total_Carb_DV,
        f.Dietary_Fiber,
        f.Dietary_Fiber_DV,
        f.Sugars,
        f.Sugars_DV,
        f.Protein,
        f.Protein_DV,
        f.Update_Date
        from ForecastedRecipes as f
        join Locations as l on l.location_number = f.location_number
        """)        

        for row in cursor:                
            #this creates a dict out of the array of values
            recipes.append({common.columns(cursor)[i]:row[i] for i in range(0, len(row))})
        
        conn.close()
        return json.loads(json.dumps(recipes, indent=4, sort_keys=True, default=str))


@api.route('/recipe/<string:id>')
class Recipe(Resource):
    def get(self, id):        
        try:            
            conn = pyodbc.connect(common.db_connection_string)
        except conn.DatabaseError as e:
            obj, = e.args
            print(("Context:", obj.context))
            print(("Message:", obj.message))
            return "Error Connecting to the DB", 500
   
        recipes = []
        cursor = conn.cursor()

        #connecting to sql Server database, execute() method takes no keyword arguments.
        #So put the database query in a string first.
        queryStr = """
        select  f.ID,
        f.Serve_Date,
        f.Meal_Number,
        f.Meal_Name,
        l.Location_Number,
        l.Location_Name,
        f.Menu_Category_Number,
        f.Menu_Category_Name,
        f.Recipe_Number,
        f.Recipe_Name,
        f.Recipe_Print_As_Name,
        f.Ingredient_List,
        f.Allergens,
        f.Recipe_Print_As_Color,
        f.Recipe_Print_As_Character,
        f.Recipe_Product_Information,
        convert(varchar(30), f.Selling_Price, 1) as selling_price,
        convert(varchar(30), f.Portion_Cost, 1) as portion_cost,
        f.Production_Department,
        f.Service_Department,
        f.Catering_Department,
        f.Recipe_Web_Codes,
        f.Serving_Size,
        f.Calories,
        f.Calories_From_Fat,
        f.Total_Fat,
        f.Total_Fat_DV,
        f.Sat_Fat,
        f.Sat_Fat_DV,
        f.Trans_Fat,
        f.Trans_Fat_DV,
        f.Cholesterol,
        f.Cholesterol_DV,
        f.Sodium,
        f.Sodium_DV,
        f.Total_Carb,
        f.Total_Carb_DV,
        f.Dietary_Fiber,
        f.Dietary_Fiber_DV,
        f.Sugars,
        f.Sugars_DV,
        f.Protein,
        f.Protein_DV,
        f.Update_Date
        from ForecastedRecipes as f
        join Locations as l on l.location_number = f.location_number where f.ID =  """ + id

        cursor.execute(queryStr)

        for row in cursor:                
            #this creates a dict out of the array of values
            recipes.append({common.columns(cursor)[i]:row[i] for i in range(0, len(row))})
        
        conn.close()
        return json.loads(json.dumps(recipes, indent=4, sort_keys=True, default=str))





