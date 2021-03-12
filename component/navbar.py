import dash_bootstrap_components as dbc
from Dashboard_data import mydata
df=mydata()
navbar = dbc.NavbarSimple(
children=[
    dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem(str(i), href="/"+str(i)) for i in df.SalesTerritoryCountry.unique()
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