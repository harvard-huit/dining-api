from flask import Flask, request, jsonify, make_response
from flask_restx import Resource, Api, fields, marshal
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

#--------------------------------------------------------------------------------------------
# Model Objects 
#--------------------------------------------------------------------------------------------
monitor_health_pass_model = api.model("monitor_health_pass",
	{
		"status": fields.String(
			description="PASS", 
            example="PASS",
			required=True
		)
	}
)

monitor_health_fail_model = api.model("monitor_health_fail",
	{
		"status": fields.String(
			description="FAIL", 
            example="FAIL",
			required=True
		),
        "error": fields.String(
			description="Error encountered", 
            example="The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.",
			required=True
		)
	}
)

location_model = api.model("location", 
	{       
        "location_name": fields.String(
			description="Location Name", 
			example="Barker Rotunda", 
			required=True
		),
         "location_number": fields.String(
			description="Location Number", 
			example="36", 
			required=True
		)
	}
)

failure_model = api.model("failure", 
	{
		"status": fields.String(
			description="FAIL", 
            example="FAIL",
			required=True
		),
        "error": fields.String(
			description="Failure encountered", 
            example="The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.",
			required=True
		)
	}
)

event_model = api.model("event", 
	{	       
        "meal_name": fields.String(
			description="Name of the meal, like Breakfast/Lunch/Dinner. The top level grouping for a given location.", 
			example="Breakfast", 
			required=True
		),
        "meal_number": fields.String(
			description="Meal Number", 
			example="1", 
			required=True
		),
        "menu_category_name": fields.String(
			description="The second level grouping for a given location. A breakfast or a lunch may have many menu categories.", 
			example="Bean/Grain", 
			required=True
		),
        "menu_category_number": fields.String(
			description="Category Number", 
			example="67", 
			required=True
		),
        "location_name": fields.String(
			description="Location name", 
			example="Barker Rotunda", 
			required=True
		),
        "location_number": fields.String(
			description="Location number", 
			example="36", 
			required=True
		),
        "serve_date": fields.String(
			description="Specific serve date. Formatted as mm/dd/yyyy", 
			example="09/15/2017", 
			required=True
		)
	}
)

recipe_model = api.model("recipe", 
	{	       
        "Sat_Fat_DV": fields.String(
			description="Sat Fat DV", 
			example="0", 
			required=True
		),
        "Trans_Fat_DV": fields.String(
			description="Trans Fat DV", 
			example="", 
			required=False
		),
        "Sugars_DV": fields.String(
			description="Sugars DV", 
			example="0", 
			required=True
		),
        "Dietary_Fiber_DV": fields.String(
			description="Dietary Fiber DV", 
			example="0", 
			required=True
		),
        "selling_price": fields.String(
			description="selling price", 
			example="0.00", 
			required=True
		),
        "ID": fields.String(
			description="recipt ID", 
			example="36297713", 
			required=True
		),
        "Menu_Category_Number": fields.String(
			description="Menu Category Number", 
			example="23", 
			required=True
		),
        "Recipe_Product_Information": fields.String(
			description="Recipe Product Information", 
			example="These less-processed oats retain more of their hull and therefore more of their nutritional value.", 
			required=True
		),
        "Cholesterol": fields.String(
			description="Cholesterol", 
			example="0mg", 
			required=True
		),
        "portion_cost": fields.String(
			description="portion cost", 
			example="0.00", 
			required=True
		),
        "Calories_From_Fat": fields.String(
			description="Calories From Fat", 
			example="27", 
			required=True
		),
        "Sodium": fields.String(
			description="Sodium", 
			example="14.8mg", 
			required=True
		),
        "Recipe_Web_Codes": fields.String(
			description="Recipe Web Codes", 
			example="VGN WGRN VGT", 
			required=True
		),
        "Total_Fat": fields.String(
			description="Total Fat", 
			example="3g", 
			required=True
		),
        "Recipe_Print_As_Name": fields.String(
			description="Recipe Print As Name", 
			example="Kashi Pilaf", 
			required=True
		),
        "Sat_Fat": fields.String(
			description="Sat Fat", 
			example="0g", 
			required=True
		),
        "Recipe_Print_As_Character": fields.String(
			description="Recipe Print As Character", 
			example="", 
			required=True
		),
        "Recipe_Print_As_Color": fields.String(
			description="Recipe Print As Color", 
			example="4194368", 
			required=True
		),
        "Total_Fat_DV": fields.String(
			description="Total Fat DV",
		    example="5", 
			required=True
		),
        "Serve_Date": fields.String(
			description="Serve Date", 
			example="09/11/2017", 
			required=True
		),
        "Total_Carb": fields.String(
			description="Total Carb", 
			example="29.6g", 
			required=True
		),
        "Cholesterol_DV": fields.String(
			description="Cholesterol DV", 
			example="0", 
			required=True
		),
        "Allergens": fields.String(
			description="Allergens", 
			example="Wheat ", 
			required=True
		),
        "Trans_Fat": fields.String(
			description="Trans Fat", 
			example="0g", 
			required=True
		),
        "Service_Department": fields.String(
			description="Service Department", 
			example="01", 
			required=True
		),
        "Catering_Department": fields.String(
			description="Catering Department", 
			example="01", 
			required=True
		),
        "Location_Number": fields.String(
			description="Location Number", 
			example="03", 
			required=True
		),
        "Sodium_DV": fields.String(
			description="Sodium DV", 
			example="1", 
			required=True
		),
        "Sugars": fields.String(
			description="Sugars", 
			example="0g", 
			required=True
		),
        "Serving_Size": fields.String(
			description="Serving Size", 
			example="5 OZL", 
			required=True
		),
         "Meal_Name": fields.String(
			description="Meal Name", 
			example="Breakfast", 
			required=True
		),
        "Total_Carb_DV": fields.String(
			description="Total Carb DV", 
			example="10", 
			required=True
		),
        "Ingredient_List": fields.String(
			description="Ingredient List", 
			example="7 Whole Grain Kashi Pilaf (Kashi Seven Whole Grains & Sesame® Pilaf (Whole: Oats Brown Rice Rye Hard Red Winter Wheat Triticale Buckwheat Barley Sesame Seeds).)", 
			required=True
		),
        "Update_Date": fields.String(
			description="Update Date", 
			example="", 
			required=True
		),
        "Location_Name": fields.String(
			description="Location Name", 
			example="Cronkhite Center", 
			required=True
		),
        "Recipe_Name": fields.String(
			description="Recipe Name", 
			example="CEREAL KASHI PILAF VGN", 
			required=True
		),
        "Protein": fields.String(
			description="Protein", 
			example="5.9g", 
			required=True
		),
        "Dietary_Fiber": fields.String(
			description="Dietary Fiber", 
			example="5.9g", 
			required=True
		),
        "Protein_DV": fields.String(
			description="Protein DV", 
			example="12", 
			required=True
		),
        "Meal_Number": fields.String(
			description="Meal Number", 
			example="1", 
			required=True
		),
        "Calories": fields.String(
			description="Calories", 
			example="167", 
			required=True
		),
        "Production_Department": fields.String(
			description="Production Department", 
			example="01", 
			required=True
		),
        "Menu_Category_Name": fields.String(
			description="Menu Category Name", 
			example="Make Your Own Bar", 
			required=True
		),
        "Recipe_Number": fields.String(
			description="Recipe Number", 
			example="031001", 
			required=True
		)
	}
)     

#--------------------------------------------------------------------------------------------
# /ats/dining/v1/monitor/health endpoint: Basic healthcheck
#--------------------------------------------------------------------------------------------
@api.route('/monitor/health')
class Health(Resource):
    @api.doc(description='''<p>
Health check endpoint which returns a status 200 and status: Pass if the API is up and responsive
''')
    @api.response(200, 'Success', monitor_health_pass_model)
    @api.response(500, 'Internal Server Error', monitor_health_fail_model)
    def get(self):
        try:
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

            if retStr != "":
                    return jsonify(
                        status = "PASS"
                    )
            else:
                    return make_response(jsonify(
                        status = "FAIL",
                        error = "Internal Server Error."
                    ), 500)
        except Exception as err:
            return make_response(jsonify(
                status = "FAIL",
                error = str(err)
            ), 500)


#--------------------------------------------------------------------------------------------
# /ats/dining/v1/locations endpoint:
# Get all the locations
#--------------------------------------------------------------------------------------------
@api.route('/locations')
class Locations(Resource):
    @api.doc(description='''<p>Get locations''')
    @api.response(200, 'Success', [location_model])
    @api.response(500, 'Internal Server Error', failure_model)
    def get(self):

        try:            
            conn = pyodbc.connect(common.db_connection_string)

            locations = []
            cursor = conn.cursor()
            cursor.execute("select l.location_number, l.location_name from locations as l")        

            for row in cursor:                
                #this creates a list of dictionaries
                locations.append({common.columns(cursor)[i]:row[i] for i in range(0, len(row))}) 

            conn.close()
            print(f"get locations")
            #return json.loads(json.dumps(locations, indent=4, sort_keys=True, default=str))       
            return make_response(jsonify(locations), 200)
        except Exception as err:
            print(f"Error occurred. {str(err)}")
            return make_response(jsonify(
                status = "FAIL",
                error = str(err)
            ), 500)
        

#--------------------------------------------------------------------------------------------
# /ats/dining/v1/events endpoint:
# Get the events based on the date and/or locationId
#--------------------------------------------------------------------------------------------
@api.route('/events')
@api.param("locationId", description="locationId", required=False, example='03')
@api.param("date", description="date", required=False, example='09/15/2017')
class Events(Resource):
    @api.doc(description='''<p>Get events''')
    @api.response(200, 'Success', [event_model])
    @api.response(500, 'Internal Server Error', failure_model)
    def get(self):

        try:            
            conn = pyodbc.connect(common.db_connection_string)        
   
            events = []
            cursor = conn.cursor()              
            
            #parameters
            locationIdVal = request.args.get('locationId', default = None)
            dateVal = request.args.get('date', default = None)

            #prepare query string
            queryStr = """select f.meal_name,l.location_number,l.location_name,
                f.serve_date,f.menu_category_name,f.menu_category_number,f.meal_number
                from forecastedrecipes as f
                join locations as l on f.location_number = l.location_number"""
            
            groupOrderSTr = """group by f.meal_name, l.location_number, l.location_name, f.serve_date, f.meal_number, f.menu_category_name, f.menu_category_number
            order by l.location_number"""

            if locationIdVal != None and dateVal != None:
                queryStr = queryStr + " where l.location_number ='" + locationIdVal + "' and f.serve_date = '" + dateVal + "'"
                queryStr = queryStr + groupOrderSTr            
            elif locationIdVal != None:
                queryStr = queryStr + " where l.location_number ='" + locationIdVal + "'"
                queryStr = queryStr + groupOrderSTr
            elif dateVal != None:
                queryStr = queryStr + " where f.serve_date = '" + dateVal + "'"
                queryStr = queryStr + groupOrderSTr
            else: 
                queryStr = queryStr + " where 1=1 " + groupOrderSTr            
            
            print(f"getting events location = {locationIdVal} date={dateVal}")
            cursor.execute(queryStr)

            for row in cursor:                
                #this creates a list of dictionaries
                events.append({common.columns(cursor)[i]:row[i] for i in range(0, len(row))})
            
            conn.close()            
            return make_response(jsonify(events), 200)
        except Exception as err:
            print(f"Error occurred. {str(err)}")
            return make_response(jsonify(
                status = "FAIL",
                error = str(err)
            ), 500)

#--------------------------------------------------------------------------------------------
# /ats/dining/v1/recipes endpoint:
# Get the events based on the date and/or locationId
#--------------------------------------------------------------------------------------------
@api.route('/recipes')
@api.param("locationId", description="locationId", required=False, example='03')
@api.param("date", description="date", required=False, example='09/15/2017')
class Recipes(Resource):
    @api.doc(description='''<p>Get recipes''')
    @api.response(200, 'Success', [recipe_model])
    @api.response(500, 'Internal Server Error', failure_model)
    def get(self):

        try:            
            conn = pyodbc.connect(common.db_connection_string)        

            locationIdVal = request.args.get('locationId', default = None)
            dateVal = request.args.get('date', default = None)

            recipes = []
            cursor = conn.cursor()            

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
            join Locations as l on l.location_number = f.location_number
            """
            if locationIdVal != None and dateVal != None:
                queryStr = queryStr + " where l.location_number ='" + locationIdVal + "' and f.serve_date = '" + dateVal + "'"
            elif locationIdVal != None:
                queryStr = queryStr + " where l.location_number ='" + locationIdVal + "'"
            elif dateVal != None:
                queryStr = queryStr + " where f.serve_date = '" + dateVal + "'"
            
            print(f"getting recipes location = {locationIdVal} date={dateVal}")
            cursor.execute(queryStr)

            for row in cursor:                
                #this creates a dict out of the array of values
                recipes.append({common.columns(cursor)[i]:row[i] for i in range(0, len(row))})
            
            conn.close()
            return make_response(jsonify(recipes), 200)
        except Exception as err:
            print(f"Error occurred. {str(err)}")
            return make_response(jsonify(
                status = "FAIL",
                error = str(err)
            ), 500)


@api.route('/recipe/<string:id>')
class Recipe(Resource):
    @api.doc(description='''<p>Get a single recipe by id''')
    @api.response(200, 'Success', recipe_model)
    @api.response(500, 'Internal Server Error', failure_model)    
    def get(self, id):        
        try:            
            conn = pyodbc.connect(common.db_connection_string)
        
            cursor = conn.cursor()

            recipe = {}

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
            
            print(f"getting recipe id = {id}")
            cursor.execute(queryStr)

            for row in cursor:
                recipe = {common.columns(cursor)[i]:row[i] for i in range(0, len(row))}
            
            conn.close()            
            return make_response(jsonify(recipe), 200)
        except Exception as err:
            print(f"Error occurred. {str(err)}")
            return make_response(jsonify(
                status = "FAIL",
                error = str(err)
            ), 500)


if __name__ == '__main__':
    app.run(debug=False)


