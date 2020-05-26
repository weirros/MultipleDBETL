# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:30:25 2020

@author: Weirroswei
"""


#import pymssql
import pandas as pd
import time,base64
import sqlalchemy
from EtGroupDB import DbS
from EtJobDefine import Jobs



#来源库，支持多个

db = base64.b64decode(DbS).decode()
db = eval('{'+db+'}')


def dblink(R):    ##返回链接字
    engine = sqlalchemy.create_engine(R)
    return engine

def rd(SQL):
    maindf=pd.DataFrame()
    for i in db:
        intime= time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn2=dblink(db[i])
            data_sql=pd.read_sql(SQL,conn2)
            print (i,data_sql.shape[0],'Rows')
            #maindf=maindf.reset_index(drop=True)
            maindf=maindf.append(data_sql) 
            print  (i,intime,time.strftime("%Y-%m-%d %H:%M:%S"))
            print('-'*100)
        except: 
            print (i,'DataBase Read Error!!')
            print('-'*100)
            pass
        finally:
            pass
    return maindf


def dwash(sql):
    
    mdf = rd(sql)
    cols = mdf.columns
    print (cols)
    print('-'*100)
    for i in cols:
        if mdf[i].dtype == 'datetime64[ns]' or ('日期' in str(i)):
           
            mdf[i] = mdf[i].reset_index(drop=True)
            mdf[i] = pd.to_datetime(mdf[i],  errors = 'coerce') #测试成功留null值
            #解决有效期字段大于2099的问题； 

    
    return mdf


def wd(R,k):

    tar0 = dwash(k)
    #tar0 = tar0.reset_index(drop=True) #避免index报错"Reindexing only valid with uniquely valued Index objects"； 

    tar0.to_excel(R+'.xlsx',sheet_name=R,index=None) #写到当前文件夹
    print(R+'.xlsx Was Wrote',time.strftime("%Y-%m-%d %H:%M:%S"))
    

def main():   
    
    for job in Jobs:
        sql,dbttable=job[0],job[1]
        print(dbttable)
        wd(dbttable,sql)
    
    print ('Done!')
    
if __name__ == '__main__':
    main()


    


