# Import packages
from dash import Dash, html, callback, Output, Input, State, dcc
import math
import numpy as np
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import pickle

# Import csv file
df = pd.read_csv("Cars.csv")

# Split mileage, max_power into value and number
df[["mileage_value","mileage_unit"]] = df["mileage"].str.split(pat=' ', expand = True)
df[["max_power_value","max_power_unit"]] = df["max_power"].str.split(pat=' ', expand = True)
df.drop(["mileage","max_power"], axis=1, inplace=True)

# Filter dataframe not to include LPG and CNG in fuel column
df = df.loc[(df["fuel"] != 'LPG') & (df["fuel"] != 'CNG')]

# convert mileage, max_power from string to float64
df[["mileage" ,"max_power"]] = df[["mileage_value","max_power_value"]].astype('float64')
df.drop(["mileage_value","max_power_value",
        "mileage_unit","max_power_unit"], axis=1, inplace = True)

# Dicard dataframe containing test drive car in owner column
df = df[df["owner"] != 'Test Drive Car']

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.JOURNAL]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create app layout
app.layout = html.Div([
        html.H1("Car Price Prediction"),
        html.Br(),
        html.H3("Welcome to car prediction website!!!!"),
        html.Br(),
        html.H6("Put a number inside the box, fill one, two or everything doesn't matter. Click [Submit] to see result "),
        html.Br(),
        html.H4("Definition"),
        html.Br(),
        html.H6("Maximum power: Maximum power of a car in bhp"),
        html.H6("Mileage: The fuel efficieny of a car or ratio of distance which a car could move per unit of fuel consumption measuring in km/l"),
        html.H6("Engine: The engine power, measured in cubic centimetres (cc)"),
        html.Br(),
        html.Div(["Maximum power",dbc.Input(id = "max_power", type = 'number', min = 0, placeholder="Insert here"),
        dbc.FormText("Please do not put nagative numbers.",color="secondary"), html.Br()]),
        html.Div(["Mileage", dbc.Input(id = "mileage", min = 0, type = 'number', placeholder ="Insert here"),
        dbc.FormText("Please do not put nagative numbers.",color="secondary"), html.Br()]),
        html.Div(["Engine", dbc.Input(id = "engine", type = 'number', min = 0, placeholder="Insert here"),
        dbc.FormText("Please do not put nagative numbers.",color="secondary"), html.Br()]),
        dbc.Button(id="submit", children="submit", color="success", className="me-1"),
        html.Div(id="output", children = '')
])

# Callback input and output
@callback(
    Output(component_id = "output", component_property = "children"),
    State(component_id = "max_power", component_property = "value"),
    State(component_id = "mileage", component_property = "value"),
    State(component_id = "engine", component_property = "value"),
    Input(component_id = "submit", component_property = "n_clicks"),
    prevent_initial_call=True
)

# Function for finding estimated car price
def prediction (max_power, mileage, km_driven, submit):
    if max_power == None:
        max_power = df["max_power"].median() # Fill in maximum power if dosen't been inserted
    if mileage == None:
        mileage = df["mileage"].mean() # Fill in mileage if dosen't been inserted
    if engine == None:
        engine = df["engine"].median() # Fill in kilometers driven if doesn't been inserted
    model = pickle.load(open("/ml2023/code/Car_Predict.model", 'rb')) # Import model
    sample = np.array([[max_power, mileage, engine]]) 
    result = np.exp(model.predict(sample)) #Predict price
    return f"The predictive car price is {int(result[0])}"

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050') #I give up, tried everything still didn't work. I even switch my DNS 
    