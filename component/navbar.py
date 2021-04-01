import dash_bootstrap_components as dbc
from Dashboard_data import mydata
import dash_core_components as dcc

df=mydata()
#navbar from bootstrap
navbar = dbc.NavbarSimple(
children=[
        
    dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem(dcc.Link(str(i), href="/country="+str(i)))for i in df.SalesTerritoryCountry.unique()
        ],
        nav=True,
        in_navbar=True,
        label="Countries",
    ),
],
brand="MyDashBoard",
brand_href="/",
color="dark",
dark=True,
)