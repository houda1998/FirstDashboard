import dash

import dash_bootstrap_components as dbc




#DASH APP USING RECOMMENDED CSS AND Bootsrap
app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server
