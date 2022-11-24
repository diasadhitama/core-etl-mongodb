"""
    author : diasadhitama3@gmail.com
"""


import pandas as pd, os #type: ignore
from sqlalchemy import create_engine #type: ignore
import pymongo #type: ignore
from pymongo import MongoClient #type: ignore
from dotenv import load_dotenv #type: ignore


class ReadData:


    def insert(self):

        load_dotenv()


        URL         = os.environ['url']
        USR         = os.environ['usr']
        PASSWORD    = os.environ['pas']

        cluster     = MongoClient(
                                "mongodb+srv://{USER}:{PASSWORD}@{URL}/?retryWrites=true&w=majority".format(
                                    USER=USR, PASSWORD=PASSWORD, URL=URL   
                                )
        )

        # select database
        database        = cluster['sample_analytics']

        # select collection
        account_data    = database.accounts

        dataframe       = pd.DataFrame(account_data.find())

        # transform
        dataframe.columns = ["id", "accountid", "lmt", "prd"]

        dataframe_satu    = dataframe[["accountid", "lmt", "prd"]]

        try:

            engine_one = create_engine('postgresql://postgres:postgres@database-1.c9vm9shc1ua2.ap-northeast-1.rds.amazonaws.com:5432/postgres')

            print("success connect db")

        except:

            print("cannot connect db")

        dataframe_satu.to_sql("mongoetl", engine_one, if_exists="replace", index=False)

        print("success insert data")