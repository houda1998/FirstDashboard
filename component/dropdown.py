import dash_bootstrap_components as dbc
from component.navbar import navbar
import dash_core_components as dcc
import dash_html_components as html


def dropdown(data,myid,label="",myvalues=[],disable=False):
   return html.Div([
   dcc.Dropdown(
    id=myid,
    options=[
       {'label': i, 'value': i} for i in data
           ],
    multi=True,
    searchable=True,
    clearable=True,
    value=myvalues,
    placeholder="Select a " + label,
    disabled=disable
) ])