from app import app
import plotly.express as px
import dash_table
import plotly.graph_objects as go
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Dashboard_data import mydata


@app.callback(
[Output('fig_bar_filtre', 'figure'),
Output('table_filtre','data'),
Output('fig_pie_filtre','figure'),
Output('fig_bar_ver_filtre','figure')],
 [ Input('dropdown_country', 'value'),
   Input('dropdown_model', 'value'),
  Input('interval_data_filtre', 'n_intervals')])
def update_graph(country,model,n):
        df=mydata()
        df2=mydata("""SELECT * from ( select Concat(FirstName,' ',MiddleName,' ',LastName) as FULLName,sum(salesAmount) as TotalProductCost, SalesTerritoryCountry, row_number() over (partition by SalesTerritoryCountry order by salesAmount desc) as rank_customer FROM factinternetSales fs join dimcustomer dc on fs.CustomerKey=dc.`CustomerKey` join dimSalesTerritory dt on fs.SalesTerritoryKey=dt.SalesTerritoryKey join dimproduct dp on dp.ProductKey=fs.ProductKey WHERE Concat(FirstName,' ',MiddleName,' ',LastName) is NOT null GROUP by Concat(FirstName,' ',MiddleName,' ',LastName) ) ranks where rank_customer<=5 order by SalesTerritoryCountry,rank_customer""")
        dff = df[df['SalesTerritoryCountry'].isin(country) & df['ModelName'].isin(model)]
        fig_bar = px.histogram(dff, x='SalesTerritoryCountry', y='SalesAmount', title="bar_chart",color="ModelName", template="simple_white")
        fig_pie = px.pie(dff, values='SalesAmount', names='ModelName', title='Vente par model')
        dff2=df2[df2['SalesTerritoryCountry'].isin(country)]
        fig_bar_ver = px.bar(dff2, x="TotalProductCost", y="SalesTerritoryCountry", color="FULLName", title="Top 5 customer by country" ,barmode="group")
        return fig_bar,dff.to_dict('records'),fig_pie,fig_bar_ver
