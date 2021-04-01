import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_table
from component.dropdown import dropdown
from Dashboard_data import mydata
from component.navbar import navbar


#global data
df = mydata()
df2=mydata("""SELECT YEAR(`DateFirstPurchase`) as yearFirstPurchase, EnglishCountryRegionName as Country,
count( Concat(FirstName,' ',MiddleName,' ',LastName)) as Nbr_client from dimcustomer dc 
join dimgeography dg on dc.GeographyKey=dg.GeographyKey group by Country,yearFirstPurchase""")
df3=mydata("""select sum(`AutomaticResponses`) as TotalReponseAutomatic ,shift,EnglishDayNameofWeek as day
from FactCallCenter fc join dimdate dd
on dd.DateKey=fc.DateKey
group by day,shift""")


#create dataTable
datatable = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'), page_size=10

)


#create filters using component
dropdown_country = dropdown(df.SalesTerritoryCountry.unique(
), "dropdown_country", "country", [i for i in df.SalesTerritoryCountry.unique()])
default = [i for i in df.ModelName.unique()]
dropdown_product = dropdown(df.ModelName.unique(
), "dropdown_model", "ProductModel", [default[0]])

dropdown_year = dropdown(df.annee.unique(
), "dropdown_year", "Année",[i for i in df.annee.unique()][0],False,False)




#layout for filters
filtres = [dbc.Col(dropdown_country),
           dbc.Col(dropdown_product),
           dbc.Col(dropdown_year)
           ]

#layout for our charts and filters (using bootstrap)
row = html.Div(
    [
        dbc.Row(filtres),
        
        dbc.Row([
            html.Br(),
            html.Br(),
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
                    dbc.Row([
                    dbc.Col(dcc.Loading(id="loading-graph5",
                                        children=[html.Div([dcc.Graph(id='fig_scatter')]),
                                        dcc.Slider(
                                        id='year-slider',
                                        min=df2['yearFirstPurchase'].min(),
                                        max=df2['yearFirstPurchase'].max(),
                                        value=df2['yearFirstPurchase'].min(),
                                        marks={str(year): str(year) for year in df2['yearFirstPurchase'].unique()},
                                        step=None
                                    )], type="graph")),
                    dbc.Col(dcc.Loading(id="loading-graph6",
                                        children=[html.Div([dcc.Graph(id='fig_sun')])], type="graph")),

                    
                 
          
        ]),
        dcc.Interval(
            id="interval_data",
            interval=6*10000,
            n_intervals=0)


    ]
)
#layout of our page
layout = dbc.Container([
    navbar,
    row
]
)
