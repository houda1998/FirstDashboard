import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_table
from component.dropdown import dropdown
from Dashboard_data import mydata
from component.navbar import navbar



df = mydata()

datatable = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'), page_size=10

)

dropdown_country = dropdown(df.SalesTerritoryCountry.unique(
), "dropdown_country", "country", [i for i in df.SalesTerritoryCountry.unique()])
default = [i for i in df.ModelName.unique()]
dropdown_product = dropdown(df.ModelName.unique(
), "dropdown_model", "ProductModel", [default[0]])
filtres = [dbc.Col(dropdown_country),
           dbc.Col(dropdown_product)
           ]


row = html.Div(
    [
        dbc.Row(filtres),
        dbc.Row([
            dbc.Col(dcc.Loading(id="loading-graph3",
                                children=[html.Div(datatable)], type="graph")),
            dbc.Col(dcc.Loading(id="loading-graph1",
                                children=[html.Div([dcc.Graph(id='fig_bar')])], type="graph"))
        ]),
        dbc.Row([
                dbc.Col(dcc.Loading(id="loading-graph2",
                                    children=[html.Div([dcc.Graph(id='fig_pie')])], type="graph")),
                dbc.Col(dcc.Loading(id="loading-graph4",
                                    children=[html.Div([dcc.Graph(id='fig_bar_ver')])], type="graph")),

                ]),
        dcc.Interval(
            id="interval_data",
            interval=6*10000,
            n_intervals=0)


    ]
)

layout = dbc.Container([
    navbar,
    row
]
)
