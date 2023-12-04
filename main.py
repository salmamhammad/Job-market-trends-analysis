# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:42:05 2023

@author: Salma
"""
from elasticsearch import Elasticsearch



from elasticsearch.helpers import bulk

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#to ignore warnings
import warnings

df = (
    pd.read_csv("job_descriptions.csv")
    .dropna()
    .sample(20000, random_state=42)
    .reset_index()
)
print("\n\n\n Numerical and categorical variables  \n ")
cat_cols=df.select_dtypes(include=['object']).columns
num_cols = df.select_dtypes(include=np.number).columns.tolist()
print("Categorical Variables:")
print(cat_cols)
print("Numerical Variables:")
print(num_cols)


print(" unique values in each column   ")

print(df.nunique())


print("Missing Values Calculation  ")
print(df.isnull().sum())




print("\n\n\n dropping unessery column : \n ")
df = df.drop(['index'], axis = 1)
# Remove Job Id  column from data
df = df.drop(['Job Id'], axis = 1)
# Remove latitude  column from data
df = df.drop(['latitude'], axis = 1)
# Remove longitude  column from data
df = df.drop(['longitude'], axis = 1)
# Remove Company Size  column from data
df = df.drop(['Company Size'], axis = 1)
# Remove Job Posting Date  column from data
df = df.drop(['Job Posting Date'], axis = 1)
# Remove Contact Person  column from data
df = df.drop(['Contact Person'], axis = 1)
# Remove Contact  column from data
df = df.drop(['Contact'], axis = 1)
# Remove Company  column from data
df = df.drop(['Company'], axis = 1)
# Remove Company Profile  column from data
df = df.drop(['Company Profile'], axis = 1)
df = df.drop(['Job Description'], axis = 1)
# Remove Company Profile  column from data
df = df.drop(['skills'], axis = 1)
df = df.drop(['Responsibilities'], axis = 1)
df.info()

es = Elasticsearch("http://elastic:p6iWCc1RkAYQHhL9MB32@localhost:9200", api_key="V1NhZnNJc0JLTGZHT3JBOHA3RUw6SVZhZVU1bklRR0M1Y3NpaFdObzk2UQ==")
print(es.info().body)
warnings.filterwarnings('ignore')

mappings = {
        "properties": {
            "experience": {"type": "text", "analyzer": "english"},
            "qualifications": {"type": "text", "analyzer": "english"},
            "location": {"type": "text", "analyzer": "english"},
            "country": {"type": "text", "analyzer": "english"},
            "JobTitle": {"type": "text", "analyzer": "english"},
            "WorkType": {"type": "text", "analyzer": "english"},
            "Role": {"type": "text", "analyzer": "english"},
            "skills": {"type": "text", "analyzer": "english"},
            "Responsibilities": {"type": "text", "analyzer": "english"},
            "SalaryRange": {"type": "text", "analyzer": "english"},
            "Benefits": {"type": "text", "analyzer": "english"},
            "Preference": {"type": "text", "analyzer": "english"},
            "JobPortal": {"type": "text", "analyzer": "english"},
            "JobDescription": {"type": "text", "analyzer": "english"},
    }
}

es.indices.create(index="searchjob", mappings=mappings)

for i, row in df.iterrows():
    doc = {
        "experience": row["Experience"],
        "qualifications": row["Qualifications"],
        "location": row["location"],
        "country": row["Country"],
        "JobTitle": row["Job Title"],
        "WorkType": row["Work Type"],
        "Role": row["Role"],
        "skills": row["skills"],
        "Responsibilities": row["Responsibilities"],
        "SalaryRange": row["Salary Range"],
        "Benefits": row["Benefits"],
        "Preference": row["Preference"],
        "JobPortal": row["Job Portal"],
        "JobDescription": row["Job Description"],
    }
            
    es.index(index="searchjob", id=i, document=doc)

bulk_data = []
for i,row in df.iterrows():
    bulk_data.append(
        {
            "_index": "searchjob",
            "_id": i,
            "_source": {        
                "experience": row["Experience"],
                "qualifications": row["Qualifications"],
                "location": row["location"],
                "country": row["Country"],
                "JobTitle": row["Job Title"],
                "WorkType": row["Work Type"],
                "Role": row["Role"],
                "skills": row["skills"],
                "Responsibilities": row["Responsibilities"],
                "SalaryRange": row["Salary Range"],
                "Benefits": row["Benefits"],
                "Preference": row["Preference"],
                "JobPortal": row["Job Portal"],
                "JobDescription": row["Job Description"],
              
            }
        }
    )
bulk(es, bulk_data)
es.indices.refresh(index="searchjob")

print(es.cat.count(index="searchjob", format="json"))
es.search(index="searchjob", q="snow")
"""
resp = es.search(
    index="ddcfrrddfdddfd",
    query={
            "bool": {
                "must": {
                    "experience": {
                        "cast": "jack nicholson",
                    }
                },
                "filter": {"bool": {"must_not": {"match_phrase": {"qualifications": "roman polanski"}}}},
            },
        },            
)
resp.body
"""