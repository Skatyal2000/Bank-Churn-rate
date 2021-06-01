# -*- coding: utf-8 -*-
"""Bank1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MjO5A0aHRomy1oAMTRcC7121MoiLVDmL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Churn_Modelling.csv')
df

df.info()

df.isnull().sum()

df1 = df.drop(['RowNumber','Surname','CustomerId'], axis=1)

df1

df1['Geography'].value_counts()

from sklearn.preprocessing import LabelEncoder
label = LabelEncoder()
df1.iloc[:,2] = label.fit_transform(df1.iloc[:,2])
df1

dfd = pd.get_dummies(df1['Geography'],drop_first=True)
dfd

df2 = pd.concat([df1,dfd],axis=1)
df2 = df2.drop(['Geography'],axis=1)
df2

x = df2.drop(['Exited'],axis=1)
y = df2['Exited']

y

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2 ,random_state = 0)

y_test

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

from sklearn import svm

from sklearn.model_selection import GridSearchCV
clf = GridSearchCV(svm.SVC(gamma='auto'), {
    'C': [1,5,10,20,30],
    'kernel': ['rbf','linear','poly']
}, cv=5, return_train_score=False)
clf.fit(x_train, y_train)
clf.cv_results_

dfn = pd.DataFrame(clf.cv_results_)
dfn

dfn[['param_C','param_kernel','mean_test_score']]

from sklearn.model_selection import RandomizedSearchCV
rs = RandomizedSearchCV(svm.SVC(gamma='auto'), {
        'C': [1,10,20],
        'kernel': ['rbf','linear']
    }, 
    cv=5, 
    return_train_score=False, 
    n_iter=2
)
rs.fit(x_train, y_train)
pd.DataFrame(rs.cv_results_)[['param_C','param_kernel','mean_test_score']]

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

model_params = {
    'svm': {
        'model': svm.SVC(gamma='auto'),
        'params' : {
            'C': [1,10,20],
            'kernel': ['rbf','linear']
        }  
    },
    'random_forest': {
        'model': RandomForestClassifier(),
        'params' : {
            'n_estimators': [1,5,10]
        }
    },
    'logistic_regression' : {
        'model': LogisticRegression(solver='liblinear',multi_class='auto'),
        'params': {
            'C': [1,5,10]
        }
    },
    'k-neighbour' : {
        'model': KNeighborsClassifier(),
        'params': {
            'n_neighbors': [1,5,10,15],
            'p': [1,2]
        }
    }
}

scores = []

for model_name, mp in model_params.items():
    clf =  GridSearchCV(mp['model'], mp['params'], cv=5, return_train_score=False)
    clf.fit(x_train, y_train)
    scores.append({
        'model': model_name,
        'best_score': clf.best_score_,
        'best_params': clf.best_params_
    })
    
dfa = pd.DataFrame(scores,columns=['model','best_score','best_params'])
dfa

cla = svm.SVC(kernel='rbf',C=10,gamma='auto')
cla.fit(x_train,y_train)

cla.score(x_test,y_test)