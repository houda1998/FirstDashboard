import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from component.dropdown import dropdown
from Dashboard_data import mydata
from component.navbar import navbar

def display_page(pathname):
    country=pathname.replace("/","")
    country=country.replace("%20"," ")
    df=mydata()
    df2=df[df['SalesTerritoryCountry'].isin([country])]
    datatable=dash_table.DataTable(
        id='table_filtre',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df2.to_dict('records'),page_size= 10
    )
    dropdown_country=dropdown(df.SalesTerritoryCountry.unique(),"dropdown_country","country",[country],True)
    default=[ i for i in df.ModelName.unique()]
    dropdown_product=dropdown(df.ModelName.unique(),"dropdown_model","ProductModel",[default[0]])
    filtres=[dbc.Col(dropdown_country),
    dbc.Col(dropdown_product)
    ]
    row = html.Div(
        [   
            dbc.Row(filtres),
            dbc.Row([
                dbc.Col( dcc.Loading(id = "loading-graph3", children=[html.Div(datatable)], type="graph")),
                dbc.Col(dcc.Loading(id = "loading-graph1", children=[html.Div([dcc.Graph(id='fig_bar_filtre')])], type="graph"))
                ]),
            dbc.Row([
                    dbc.Col(dcc.Loading(id = "loading-graph2", children=[html.Div([dcc.Graph(id='fig_pie_filtre')])], type="graph")),
                    dbc.Col(dcc.Loading(id = "loading-graph4", children=[html.Div([dcc.Graph(id='fig_bar_ver_filtre')])], type="graph")),

                ]),
        dcc.Interval(
            id="interval_data_filtre",
            interval=6*10000,
            n_intervals=0)


        ]
    )

    layout = dbc.Container([
        navbar,
        row
    ]
    )
    return layout
