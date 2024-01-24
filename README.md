# Credit Card Fraud Analysis

The primary objective is to derive comprehensive insights from the credit card fraud dataset that was downloaded from Kaggle
The Credit Card Transactions Fraud Detection Dataset (kaggle.com) Dataset was available in the ‘.csv’ format and therefore would require some transformations before we could use it for any analysis. Our intention was to leverage most of the learning outcomes at the Albany Beck Pioneer Program. The major tools that we utilized are : 

👉 Python

👉 MYSQL

👉 PowerBI

👉 MS-Excel

## Roadmap

![image](https://github.com/piperalpha7/Credit-Card-Fraud-Analysis/assets/94968239/b866bb99-93df-4693-83a3-369373eea139)

Above is a picture of out ETL pipeline. The way we went about our project was to first ingest the ‘.csv’ file in a Python Pandas dataframe. The reason to do this was the ease and flexibility to manipulate tabular data. Moreover pandas proved to be an efficient tool while handling a large dataset with 555719 rows without any lag. 

We then carried out a variety of transformations.
The ‘Clean Data’ was now in the form of DataFrame itself. We now created a trifurcation in order to carry out further Data Analysis.This is as follows:

👉 Path 1 - 'Clean Data' was normalized and divided into 3 Dataframes which would then be loaded as MYSQL tables. The MYSQL Database could then easily be 
   loaded onto PowerBI to carry out any analysis and create a Dashboard.
👉 Path 2 - Use the ‘Clean Data’ directly in creating some plots in python. 
👉 Path 3 -  Use the ‘Clean Data’ in MS-Excel to create a ‘fraud-customer’ dashboard.

As part of the cleaning process, the dataset was normalised using pandas and then loaded onto a MYSQL Database.
Following is the ERD Diagram of the MYSQL Database
 
![image](https://github.com/piperalpha7/Credit-Card-Fraud-Analysis/assets/94968239/5577049e-2de6-4581-985b-abc17f5d11ea)



## Analysis


### PowerBI Dashboard
Following are some of the screenshots from the Dashboard created on PowerBI. The analysis was divided into Transactions, Regions, Merchants and Customers.

![image](https://github.com/piperalpha7/Credit-Card-Fraud-Analysis/assets/94968239/e209b408-7730-4077-b882-70d20277c45f)


![image](https://github.com/piperalpha7/Credit-Card-Fraud-Analysis/assets/94968239/67c208fd-173f-4a53-9f3a-b4cc73c36998)


### Excel Dashboard

Besides this, a customer profile for fraudulent customers was created using MS-Excel as follows:-

![image](https://github.com/piperalpha7/Credit-Card-Fraud-Analysis/assets/94968239/dd1b667b-d168-4f6a-ae91-faf430668fb8)



## Key Insights

Some of the insights discovered are as follows: -

👉 Fraudulent customers comprised of a mere 0.04% of all the customers.
👉 Fraudulent customers seem to be over cautious in the way they spende, always spending between $1 and $1320.
👉 More than 30% of Fraudulent Transactions were done by customers belonging to the age groups of ‘31-40’ and ‘51-60’.
👉 Most fraudulent transactions took place between the hours of 22:00- 04:00.


Doing this group project ensured that I learnt a lot about a variety of tools, and how an effective ETL pipeline could bring about so many tools together.







LINK TO CONFLUENCE SPACE : https://albanybeck-kvoges.atlassian.net/wiki/spaces/AGA/overview


 

