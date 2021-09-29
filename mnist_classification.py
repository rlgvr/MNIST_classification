# -*- coding: utf-8 -*-
"""MNIST_classes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LvZJ1W7s9aLFTpEPZJMWg8NDSqtIgg9s
"""

##Import libraries
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.stats import multivariate_normal as mvn
import seaborn as sns

class GaussNB():

    def fit(self, X, y, epsilon = 0.5e-1):  ### higher accuracy with this epsilon 
        self.likelihoods = dict()
        self.priors = dict()

        self.K = set(y.astype(int))

        for k in self.K:
    
            X_k =X[y==k,:]


            self.likelihoods[k] = {"mean":X_k.mean(axis=0), "cov":X_k.var(axis=0) + epsilon }
            self.priors[k]=len(X_k)/len(X)

    def predict(self, X):

        N, D = X.shape

        P_hat = np.zeros((N,len(self.K)))

        for k, l in self.likelihoods.items():
            P_hat[:,k] = mvn.logpdf(X, l["mean"], l["cov"])+ np.log(self.priors[k]) 
  
        return P_hat.argmax(axis=1)

### Multiclasses classifier, works with any number of classes(categories)
class GaussBayes():
    
    def fit(self, X,y, epsilon=0.5e-1):
        self.likelihoods = dict()
        self.priors = dict()
        ###for categorical values use onehtencoder
        self.K = set(y.astype(int))
        
        for k in self.K:
            X_k = X[y==k,:]
            N_k,D = X_k.shape   ## N_k=total number of observations of that class
            mu_k = X_k.mean(axis=0)
            self.likelihoods[k] = {"mean":X_k.mean(axis=0), "cov": (1/(N_k-1))*np.matmul((X_k-mu_k).T,X_k-mu_k)+ epsilon*np.identity(D)}
            self.priors[k] = len(X_k)/len(X)
    
    
    def predict(self, X):
        N,D = X.shape
        P_hat = np.zeros((N,len(self.K)))
        
        for k,l in self.likelihoods.items():
            P_hat[:,k] = mvn.logpdf(X,l["mean"], l["cov"])+np.log(self.priors[k])
        
        return P_hat.argmax(axis=1)

class KNNClassifier():
    
    def fit(self, X, y):
        self.X=X
        self.y=y
    
    def predict(self, X, K, epsilon=1e-3):
        N=len(X)
        y_hat = np.zeros(N)
        
        for i in range(N):
            dist2 = np.sum((self.X-X[i])**2, axis=1)
            idxt = np.argsort(dist2)[:K] ##gives indexes of sorted df
            gamma_k = 1/(np.sqrt(dist2[idxt]+epsilon))  ##weights 
            y_hat[i] = np.bincount(self.y[idxt], weights=gamma_k).argmax()  ### what happen if subtract epsilon?
            
        return y_hat

def show_me(X):
    plt.imshow(X.reshape(28,28))
    
def show_me_allmean(X,y,k):
    show_me(sum(X[y==k,:]/len(X[y==k,:])))

def accuracy(y,y_hat):
    return np.mean(y==y_hat)

## import train data
df = pd.read_csv('/content/MNIST_train.csv', index_col=1)
d = dict.fromkeys(df.select_dtypes(np.int64).columns, np.int32)
df = df.astype(d)

## import test data 
test = pd.read_csv('/content/MNIST_test.csv')
y_test = test['labels']
test = test.drop(columns=['Unnamed: 0', 'index', 'labels'])

X_test = test.to_numpy()
y_test = y_test.to_numpy()

## Define X and y 
y = df['labels']
X = df.drop(columns=['Unnamed: 0', 'labels'])

### check 
X.describe()

## Normalize
X = X/255

## X and y as numpy arrays to fit the model
X = X.to_numpy()
y = y.to_numpy()

X

y

"""## GaussNB"""

gsn = GaussNB()

gsn.fit(X,y)

y_hat_gsn = gsn.predict(X)

y_test_gsn = gsn.predict(X_test)

#accuracy train
accuracy(y, y_hat_gsn)

accuracy test
accuracy(y_test, y_test_gsn)

plt.figure(figsize=(10,7))
y_actu = pd.Series(y_test, name='Actual')
y_pred = pd.Series(y_test_gsn, name='Predicted')
cm = pd.crosstab(y_actu, y_pred)
ax = sns.heatmap(cm, annot=True, fmt="d")
plt.ylabel('True label')
plt.xlabel('Predicted label')

plt.figure(figsize=(10,7))
y_actu = pd.Series(y, name='Actual')
y_pred = pd.Series(y_hat_gsn, name='Predicted')
cm = pd.crosstab(y_actu, y_pred)
ax = sns.heatmap(cm, annot=True, fmt="d")
plt.ylabel('True label')
plt.xlabel('Predicted label')

"""## GaussBayes"""

GB = GaussBayes()

GB.fit(X,y)

y_hat_GB = GB.predict(X)

y_test_GB_hat = GB.predict(X_test)

#accuracy train
accuracy(y, y_hat_GB)

# accuracy test
accuracy(y_test, y_test_GB_hat)

plt.figure(figsize=(10,7))
y_actu = pd.Series(y, name='Actual')
y_pred = pd.Series(y_hat_GB, name='Predicted')
cm = pd.crosstab(y_actu, y_pred)
ax = sns.heatmap(cm, annot=True, fmt="d")
plt.ylabel('True label')
plt.xlabel('Predicted label')

plt.figure(figsize=(10,7))
y_actu = pd.Series(y_test, name='Actual')
y_pred = pd.Series(y_test_GB_hat, name='Predicted')
cm = pd.crosstab(y_actu, y_pred)
ax = sns.heatmap(cm, annot=True, fmt="d")
plt.ylabel('True label')
plt.xlabel('Predicted label')

show_me_allmean

show_me(X[8313])

y[100]

"""## KNN Classifier"""

knn = KNNClassifier()

knn.fit(X,y)

y_hat_knn = knn.predict(X,1)





