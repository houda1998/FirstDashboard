import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from component.dropdown import dropdown
from Dashboard_data import mydata
from component.navbar import navbar




#function to create layout by pathname
def display_page(pathname):
    #extract countryName
    country=pathname.split("=")
    country=country[1].replace("%20"," ")
    #Global Data
    df=mydata()
    df3=mydata("""SELECT YEAR(`DateFirstPurchase`) as yearFirstPurchase, EnglishCountryRegionName as Country,
count( Concat(FirstName,' ',MiddleName,' ',LastName)) as Nbr_client from dimcustomer dc 
join dimgeography dg on dc.GeographyKey=dg.GeographyKey group by Country,yearFirstPurchase""")
    #dataFrame of country from path
    df2=df[df['SalesTerritoryCountry'].isin([country])]
    #datatable
    datatable=dash_table.DataTable(
        id='table_filtre',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df2.to_dict('records'),page_size= 10
    )
    #filtres using component
    dropdown_country=dropdown(df.SalesTerritoryCountry.unique(),"dropdown_country","country",[country],True)
    default=[ i for i in df.ModelName.unique()]
    dropdown_product=dropdown(df.ModelName.unique(),"dropdown_model","ProductModel",[default[0]])
    dropdown_year = dropdown(df.annee.unique(
), "dropdown_year", "Année",[i for i in df.annee.unique()][0],False,False)
    #filtre layout
    filtres = [dbc.Col(dropdown_country),
           dbc.Col(dropdown_product),
           dbc.Col(dropdown_year)
           ]



    #page layout using bootstrap
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
             dbc.Row([
                    dbc.Col(dcc.Loading(id="loading-graph5",
                                        children=[html.Div([dcc.Graph(id='fig_scatter_filtre')]),
                                        dcc.Slider(
                                        id='year-slider_filtre',
                                        min=df3['yearFirstPurchase'].min(),
                                        max=df3['yearFirstPurchase'].max(),
                                        value=df3['yearFirstPurchase'].min(),
                                        marks={str(year): str(year) for year in df3['yearFirstPurchase'].unique()},
                                        step=None
                                    )], type="graph")),
                    dbc.Col(dcc.Loading(id="loading-graph6",
                                        children=[html.Div([dcc.Graph(id='fig_sun_filtre')])], type="graph")),
 ]),
        dcc.Interval(
            id="interval_data_filtre",
            interval=6*10000,
            n_intervals=0)


        ]
    )
    #layout using navbar component
    layout = dbc.Container([
        navbar,
        row
    ]
    )
    return layout
