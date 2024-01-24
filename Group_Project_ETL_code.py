# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:05:54 2023

@author: cdsouza
"""

# Importing Libraries
import pandas as pd
import os
import numpy as np
from datetime import date,time
import mysql.connector as sql
from abc import ABC, abstractmethod



# Defining a base class 'Data' which has abstract methods to build on. This class also incorporates the encapsulation pillar
# for the attribute 'database'
class Data(ABC):
    def __init__(self, database, password):
        self.__database = database
        self.__password = password

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database):
        self.__database = database

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    def create_database(self):
        pass

    def delete_database(self):
        pass

    @abstractmethod
    def csv_to_dataframe(self):
        pass

    @abstractmethod
    def data_cleaning_df(self):
        pass

    @abstractmethod
    def split_data_frames(self):
        pass

    @abstractmethod
    def create_sql_tables(self):
        pass

    @abstractmethod
    def load_database(self):
        pass
    
    
    
# This class inherits from the base class and also highlights the pillar of polymorphism where the methods in this class override 
# the methods in the base class
class Credit_Card_Data(Data):
    def __init__(self, database, password, file_path):
        super().__init__(database, password)
        self.file_path = file_path

    # Method to create a 'MySQL' Database
    def create_database(self):
        mydb = sql.connect(host='localhost', user='root', password=self.password, port=3306, use_pure=True)
        mycursor = mydb.cursor()
        mycursor.execute(f'create database {self.database}')
        mydb.commit()

    # Method to delete a 'MySQL' Database
    def delete_database(self):
        mydb = sql.connect(host='localhost', user='root', password=self.password, port=3306, use_pure=True)
        mycursor = mydb.cursor()
        mycursor.execute(f'DROP database {self.database}')
        mydb.commit()

    # Method to convert a csv to a Dataframe
    def csv_to_dataframe(self):
        path = self.file_path
        df = pd.read_csv(path)
        return df

    # Method to perform the DataCleaning in the Data which is now in the form of a Dataframe
    def data_cleaning_df(self):
        df = self.csv_to_dataframe()
        df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
        df[['Transaction_Date', 'Transaction_Time']] = df['trans_date_trans_time'].str.split(' ', expand=True)
        df.drop(columns=['trans_date_trans_time', 'unix_time'], inplace=True)
        rename_df_cols = {'cc_num': 'Credit_Card_Number',
                          'merchant': 'Merchant_Name',
                          'category': 'Category',
                          'amt': 'Amount-USD',
                          'first': 'First_Name',
                          'last': 'Last_Name',
                          'gender': 'Gender',
                          'street': 'Street',
                          'city': 'City',
                          'state': 'State',
                          'zip': 'Zip_Code',
                          'lat': 'Latitude',
                          'long': 'Longitude',
                          'city_pop': 'City_Population',
                          'job': 'Profession',
                          'dob': 'Date_Of_Birth',
                          'trans_num': 'Transaction_Number',
                          'merch_lat': 'Merchant_Latitude',
                          'merch_long': 'Merchant_Longitude',
                          'is_fraud': 'Fraud'}
        df.rename(columns=rename_df_cols, inplace=True)
        df['Fraud'] = df['Fraud'].map({0: 'No', 1: 'Yes'})
        df['Gender'] = df['Gender'].map({'M': 'Male', 'F': 'Female'})
        df['Merchant_Name'] = df['Merchant_Name'].map(lambda x: x.lstrip('fraud_'))
        df['Date_Of_Birth'] = df['Date_Of_Birth'].apply(
            lambda x: date(year=int(x[0:4]), month=int(x[5:7]), day=int(x[8:])))
        df['Transaction_Date'] = df['Transaction_Date'].apply(
            lambda x: date(year=int(x[0:4]), month=int(x[5:7]), day=int(x[8:])))
        df['Transaction_Time'] = df['Transaction_Time'].apply(
            lambda x: time(hour=int(x[0:2]), minute=int(x[3:5]), second=int(x[6:])))
        lst = [value for value in df['Profession'] if ',' in value]
        output_string = ''
        prof_dict = {}
        for profession in lst:
            words = profession.split(', ')
            if len(words) > 1:
                output_string = str(words[-1]) + ' ' + str(words[:-1][0])
                prof_dict[profession] = output_string
        df['Profession'] = df['Profession'].replace(prof_dict)
        state_data = {
            'AL': 'ALABAMA',
            'AK': 'ALASKA',
            'AS': 'AMERICAN SAMOA',
            'AZ': 'ARIZONA',
            'AR': 'ARKANSAS',
            'CA': 'CALIFORNIA',
            'CO': 'COLORADO',
            'CT': 'CONNECTICUT',
            'DE': 'DELAWARE',
            'DC': 'DISTRICT OF COLUMBIA',
            'FL': 'FLORIDA',
            'GA': 'GEORGIA',
            'GU': 'GUAM',
            'HI': 'HAWAII',
            'ID': 'IDAHO',
            'IL': 'ILLINOIS',
            'IN': 'INDIANA',
            'IA': 'IOWA',
            'KS': 'KANSAS',
            'KY': 'KENTUCKY',
            'LA': 'LOUISIANA',
            'ME': 'MAINE',
            'MD': 'MARYLAND',
            'MA': 'MASSACHUSETTS',
            'MI': 'MICHIGAN',
            'MN': 'MINNESOTA',
            'MS': 'MISSISSIPPI',
            'MO': 'MISSOURI',
            'MT': 'MONTANA',
            'NE': 'NEBRASKA',
            'NV': 'NEVADA',
            'NH': 'NEW HAMPSHIRE',
            'NJ': 'NEW JERSEY',
            'NM': 'NEW MEXICO',
            'NY': 'NEW YORK',
            'NC': 'NORTH CAROLINA',
            'ND': 'NORTH DAKOTA',
            'MP': 'NORTHERN MARIANA IS',
            'OH': 'OHIO',
            'OK': 'OKLAHOMA',
            'OR': 'OREGON',
            'PA': 'PENNSYLVANIA',
            'PR': 'PUERTO RICO',
            'RI': 'RHODE ISLAND',
            'SC': 'SOUTH CAROLINA',
            'SD': 'SOUTH DAKOTA',
            'TN': 'TENNESSEE',
            'TX': 'TEXAS',
            'UT': 'UTAH',
            'VT': 'VERMONT',
            'VA': 'VIRGINIA',
            'VI': 'VIRGIN ISLANDS',
            'WA': 'WASHINGTON',
            'WV': 'WEST VIRGINIA',
            'WI': 'WISCONSIN',
            'WY': 'WYOMING'}
        df['State'] = df['State'].replace(state_data)
        return df

    # Method to split the Main Dataframe into 3...This is to normalize the dataset.Such that before loading this into the dataset,
    # The dataset which is now divided into 3 are in the normalised form
    def split_data_frames(self):
        df = self.data_cleaning_df()

        df_cs = df[['Credit_Card_Number', 'First_Name',
                    'Last_Name', 'Gender', 'Date_Of_Birth',
                    'Profession', 'Street', 'City', 'State',
                    'Zip_Code', 'Latitude', 'Longitude',
                    'City_Population']]
        df_customer = df_cs.drop_duplicates(subset=['Credit_Card_Number', 'First_Name', 'Last_Name'])

        df_mr = df[['Merchant_Name', 'Category']]
        df_merchant = df_mr.drop_duplicates(subset=['Merchant_Name', 'Category'])

        df_transactions = df[['Merchant_Name', 'Transaction_Date',
                              'Transaction_Time', 'Credit_Card_Number',
                              'Amount-USD', 'Transaction_Number', 'Fraud']]

        return df_customer, df_merchant, df_transactions

    # Method to create blank tables in MYSQL to accomodate the data in the Dataframes
    def create_sql_tables(self):
        mydb = sql.connect(host='localhost', user='root', database=self.database, password=self.password, port=3306,
                           use_pure=True)
        mycursor = mydb.cursor()

        mycursor.execute('''CREATE TABLE Customers (
                            Credit_Card_Number VARCHAR(64) PRIMARY KEY,
                            First_Name VARCHAR(255),
                            Last_Name VARCHAR(255),
                            Gender CHAR(8),
                            Date_Of_Birth DATE,
                            Profession VARCHAR(255),
                            Street VARCHAR(255),
                            City VARCHAR(30),
                            State VARCHAR(30),
                            Zip_Code int,
                            Latitude DECIMAL(9, 6),
                            Longitude DECIMAL(9, 6),
                            City_Population int)''')

        mycursor.execute('''CREATE TABLE Merchant(
                            Merchant_Name VARCHAR(255),
                            Category VARCHAR(255),
                            PRIMARY KEY (Merchant_Name, Category)) ''')

        mycursor.execute('''CREATE TABLE Transactions (
                            Merchant_Name VARCHAR(255),
                            Transaction_Date DATE,
                            Transaction_Time TIME,
                            Credit_Card_Number VARCHAR(64),
                            Amount_in_USD VARCHAR(255),
                            Transaction_Number VARCHAR(32) PRIMARY KEY,
                            Fraud CHAR(8)) ''')

        mycursor.execute('''ALTER TABLE Transactions
                            ADD FOREIGN KEY (Merchant_Name)
                            REFERENCES Merchant(Merchant_Name)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE''')

        mycursor.execute('''ALTER TABLE Transactions
                            ADD FOREIGN KEY (Credit_Card_Number) REFERENCES 
                            Customers(Credit_Card_Number)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE''')
        mydb.commit()

    # Method to load all the 3 dataframes into their respectve Tables in MySQL
    def load_database(self):
        self.create_sql_tables()
        df_customers, df_merchant, df_transactions = self.split_data_frames()
        data_list = [df_customers, df_merchant, df_transactions]
        for key, dataframe in enumerate(data_list):
            data = [tuple(row) for row in dataframe.to_numpy()]
            data_iter = iter(data)
            for batch in range(round(len(dataframe) / 1000)):
                lst = []
                try:
                    for count in range(1000):
                        lst.append(next(data_iter))
                except StopIteration:
                    break
                finally:
                    mydb = sql.connect(host='localhost', user='root', password=self.password, database=self.database,
                                       port=3306, use_pure=True)
                    mycursor = mydb.cursor()
                    placeholders = ', '.join(['%s'] * len(dataframe.columns))
                    if key == 0:
                        table_name = 'customers'
                    elif key == 1:
                        table_name = 'merchant'
                    else:
                        table_name = 'transactions'
                    # Insert data into the table using executemany
                    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                    mycursor.executemany(insert_query, lst)
                    mydb.commit()
                    
                    
                    
                    
                    
                    
                    
# Main function which runs the ETL
def main():
    while True:
        try:
            db_name = input('Please enter the name of the MYSQL Database you would like to store the data in : ')
            p_word = input('Please enter the password of your MYSQL Server:')
            mydb = sql.connect(host ='localhost', user = 'root' ,password = p_word, port = 3306, use_pure = True)
            mycursor = mydb.cursor()
            mycursor.execute("show databases")
            db_list_of_tuples = mycursor.fetchall()
            db_list = [item for sublist in db_list_of_tuples for item in sublist]
            if db_name in db_list:
                print('Database already exists. Please retry entering another name for your database')
                continue
            else:
                 filepath = input('Please enter the filepath where your file is located :')
                 credit_card = Credit_Card_Data(db_name,p_word,filepath)
                 credit_card.create_database()
                 credit_card.load_database()
            break
        except:
            print('Incorrect Credentials')
            continue


if __name__ == '__main__': #keep this in main
   main()