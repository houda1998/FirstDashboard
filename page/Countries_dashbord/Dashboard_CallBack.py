from app import app
import dash
import plotly.express as px
import dash_table
import plotly.graph_objects as go
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Dashboard_data import mydata



#sql request

sql1="""SELECT * from ( select Concat(FirstName,' ',MiddleName,' ',LastName) as FULLName,
sum(salesAmount) as TotalProductCost, SalesTerritoryCountry, row_number() over (partition by SalesTerritoryCountry 
order by salesAmount desc) as rank_customer FROM factinternetSales fs join dimcustomer dc on fs.CustomerKey=dc.`CustomerKey` 
join dimSalesTerritory dt on fs.SalesTerritoryKey=dt.SalesTerritoryKey join dimproduct dp on dp.ProductKey=fs.ProductKey 
WHERE Concat(FirstName,' ',MiddleName,' ',LastName) is NOT null GROUP by Concat(FirstName,' ',MiddleName,' ',LastName) ) ranks
where rank_customer<=5 order by SalesTerritoryCountry,rank_customer"""
sql2="""SELECT YEAR(`DateFirstPurchase`) as yearFirstPurchase, EnglishCountryRegionName as Country,
    count( Concat(FirstName,' ',MiddleName,' ',LastName)) as Nbr_client from dimcustomer dc 
    join dimgeography dg on dc.GeographyKey=dg.GeographyKey group by Country,yearFirstPurchase"""
#global dataframe
global_df=mydata()
global_df2=mydata(sql1)
global_df3=mydata(sql2)


#callback to update charts by filtre and synch
@app.callback(
[Output('fig_bar_filtre', 'figure'),
Output('table_filtre','data'),
Output('fig_pie_filtre','figure'),
Output('fig_bar_ver_filtre','figure')],
 [ Input('dropdown_country', 'value'),
   Input('dropdown_model', 'value'),
   Input('dropdown_year', 'value'),
  Input('interval_data_filtre', 'n_intervals')])
def update_graph(country,model,year,n):
      #check if update 
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'].split('.')[0]=="interval_data":
              df=mydata()
              df2=mydata(sql1)
        else :
               df=global_df
               df2=global_df2  
      #filtre     
        if(model==[] and country==[]):
              dff=df
        elif model==[] and country!=[]:
              dff = df[df['SalesTerritoryCountry'].isin(country)]
        elif model!=[] and country==[]:
              dff=df['ModelName'].isin(model)
        elif model!=[] and country !=[]:
          dff = df[df['SalesTerritoryCountry'].isin(country) & df['ModelName'].isin(model)]
        #data for DataTable
        dff2=dff[dff['annee'].isin([year])]
        #plot charts
        fig_bar = px.histogram(dff, x='SalesTerritoryCountry', y='SalesAmount', title="Total des ventes de model par pays",color="ModelName", template="simple_white")
        fig_pie = px.pie(dff, values='SalesAmount', names='ModelName', title='Vente par model')
        dff2=df2[df2['SalesTerritoryCountry'].isin(country)]
        fig_bar_ver = px.bar(dff2, x="TotalProductCost", y="SalesTerritoryCountry", color="FULLName", title="Top 5 customer by country" ,barmode="group")
        return fig_bar,dff2.to_dict('records'),fig_pie,fig_bar_ver


#callback to update charts by filtre and synch
@app.callback(
    Output('fig_scatter_filtre', 'figure'),
    [Input('year-slider_filtre', 'value'),
    Input('dropdown_country', 'value'),
    Input('interval_data_filtre', 'n_intervals'),
    ])
def update_figure(selected_year,country,n):
      #check if update triggred
      ctx = dash.callback_context
      if ctx.triggered[0]['prop_id'].split('.')[0]=="interval_data":
            df3=mydata(sql2)
      else :
            df3=global_df3
      #filtres
      if country==[]:
            filtered_df = df3[df3.yearFirstPurchase == selected_year]
      else : 
            filtered_df = df3[df3['Country'].isin(country) & df3['yearFirstPurchase'].isin([selected_year])]
      #plot chart
      fig = px.scatter(filtered_df, x="Nbr_client", y="yearFirstPurchase",
                        color="Country", hover_name="Country",size="Nbr_client",
                        size_max=55)

      fig.update_layout(transition_duration=500)

      return fig


#callback to update slider by dropdown
@app.callback(
    Output('year-slider_filtre', 'value'),
    [Input('dropdown_year', 'value'),
    ])
def slider(selected_year):
      if selected_year!="": return selected_year
    
#callback for sunburst
@app.callback(
    Output('fig_sun_filtre', 'figure'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_country', 'value'),
    Input('dropdown_model', 'value'),
    Input('interval_data_filtre', 'n_intervals'),
    ])
def update_sunburst(selected_year,country,model,n):
      #check if update triggred
      ctx = dash.callback_context
      if ctx.triggered[0]['prop_id'].split('.')[0]=="interval_data":
            df=mydata()
            
      else :
            df=global_df
      #filtre
      if country==[] and model!=[] and [selected_year]!=[]:
            filtered_df = df[df['ModelName'].isin(model) & df['annee'].isin([selected_year])]
      elif country!=[] and [selected_year]!=[] and model==[]:
            filtered_df = df[df['SalesTerritoryCountry'].isin(country) & df['annee'].isin([selected_year])]
      elif [selected_year]==[] and country!=[] and model!=[]:
            filtered_df = df[df['SalesTerritoryCountry'].isin(country) & df['ModelName'].isin(model)]
      elif country!=[] and [selected_year]!=[] and model!=[]:
            filtered_df = df[df['SalesTerritoryCountry'].isin(country) & df['ModelName'].isin(model) & df['annee'].isin([selected_year])]
      #plot figure
      fig = px.sunburst(filtered_df, path=['annee', 'SalesTerritoryCountry','ModelName'], values='SalesAmount',
                        color='SalesAmount',
                        color_continuous_scale='RdBu',
                        )
      return fig



