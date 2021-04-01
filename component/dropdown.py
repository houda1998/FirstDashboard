import dash_bootstrap_components as dbc
from component.navbar import navbar
import dash_core_components as dcc
import dash_html_components as html

#dropdown component
def dropdown(data,myid,label="",myvalues=[],disable=False,multiple=True):
   return html.Div([
   dcc.Dropdown(
    id=myid,
    options=[
       {'label': i, 'value': i} for i in data
           ],
    multi=multiple,
    searchable=True,
    clearable=True,
    value=myvalues,
    placeholder="Select a " + label,
    disabled=disable,
     
) ])