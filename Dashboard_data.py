
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
import pandas as pd
import numpy as np


#CREATE ENGINE USING SQLALCHEMY
engine=create_engine('mysql+mysqldb://root:@localhost:3306/sales')
#defaul query
myquery="""select ModelName,SalesAmount,SalesTerritoryCountry,Year(orderDate) as annee
       from dimproduct dp 
       join factinternetsales fs 
       on dp.ProductKey=fs.Productkey
       join dimsalesTerritory St
       on St.SalesTerritoryKey=fs.SalesTerritoryKey
       ;"""
#CREATE PANDAS DATAFRAME FROM SQL
def mydata(query=myquery):
    df=pd.read_sql_query(query,engine)
    return df