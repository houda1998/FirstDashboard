import dash
from app import app
import plotly.express as px
import dash_table
import plotly.graph_objects as go
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from page.Countries_dashbord.Dashboard import display_page
import page.Countries_dashbord.Dashboard_CallBack
from page.root_page.Dashboard import layout
import page.root_page.Dashboard_CallBack
from Dashboard_data import mydata



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display(pathname):
    if pathname=="/":   return layout
    else :  return display_page(pathname)



if __name__ == "__main__":
    app.run_server(debug=True)
