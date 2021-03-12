
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
import pandas as pd
import numpy as np
engine=create_engine('mysql+mysqldb://root:@localhost:3306/sales')
myquery="""select ModelName,SalesAmount,SalesTerritoryCountry
       from dimproduct dp 
       join factinternetsales fs 
       on dp.ProductKey=fs.Productkey
       join dimsalesTerritory St
       on St.SalesTerritoryKey=fs.SalesTerritoryKey
       ;"""
       
def mydata(query=myquery):
    df=pd.read_sql_query(query,engine)
    return df