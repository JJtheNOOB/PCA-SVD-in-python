
# coding: utf-8

# __A (Original Matrix) =   u * S * v__

# - A = Input data matrix (m * n)
# - v = Right singular vectors, holds important, non redundant information on features (r * n)
# - S (or sigma) = diagnal matrix; contains all of the information about the decomposition processes performed during the compression
# (r * r)
# - u = Left singular vectors (m * r)

# In[2]:


import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA, TruncatedSVD


# In[3]:


#Load the boston dataset
from sklearn.datasets import load_boston
boston = load_boston()
X = pd.DataFrame(boston.data, columns = boston.feature_names)
y = pd.DataFrame(boston.target)


# In[4]:


X.describe()


# In[5]:


X.info()


# In[7]:


reg = linear_model.LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25,
                                                   random_state = 2019)


# In[8]:


reg.fit(X_train, y_train)
reg.score(X_test, y_test)


# In[23]:


#Using pca
pca = PCA(n_components = 10, whiten = 'True')
x = pca.fit(X).transform(X)


# In[24]:


pca.explained_variance_


# In[25]:


pca_reg = linear_model.LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.25,
                                                   random_state = 2019)
pca_reg.fit(X_train, y_train)


# In[26]:


pca_reg.score(X_test, y_test)


# In[29]:


#Truncated SVD
svd = TruncatedSVD(n_components = 10)
x = svd.fit(X).transform(X)
svd_reg = linear_model.LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.25,
                                                   random_state = 2019)
svd_reg.fit(X_train, y_train)


# In[30]:


svd_reg.score(X_test, y_test)

