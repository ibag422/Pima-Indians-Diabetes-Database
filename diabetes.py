# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:03:09 2019

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

df = pd.read_csv('diabetes.csv')

X = df.iloc[:, :-1].values
Y = df.iloc[:, -1].values 

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size = 0.2)

D = 8
M = 4
K =2

N = len(Ytrain)
T = np.zeros((N, K))
for i in range(N):
    T[i, Ytrain[i]] = 1

# ============================================================================

# different activation functions
    
def sigmoid(a):
    return 1/(1 + np.exp(-a))

def tanh(a):
    return (np.exp(a) - np.exp(-a)/(np.exp(a) + np.exp(-a)))

def relu(a):
    return np.maximum(0.01, a)

def mult_meth(a):
    return a * (a>0)

def abs_meth(a):
    return (abs(a) + a / 2)

def fancy(a):
    a[a<0] = 0
    return a

def feed_forward(X, W1, b1, W2, b2):
    # this is a binary classification so output layer (Y) needs to use sigmoid
    a = X.dot(W1) + b1
    Z = sigmoid(a)
    A = Z.dot(W2) + b2
    Y = sigmoid(A)
    return Z, Y

def classification_rate(Y, P):
    n_correct = 0
    n_total = 0
    for i in range(len(Y)):
        n_total += 1
        if Y[i] == P[i]:
            n_correct += 1
    return float(n_correct) / n_total

def cost(T, Y):
    tot = T * np.log(Y)
    return tot.sum()

def derivative_w2(Z, T, Y):
    N, K = T.shape
    ret2 = Z.T.dot(T-Y) # "Z transpose dot T -Y" Z.T = MxN, T-Y = NxK, result = MxK
    return ret2

def derivative_b2(T, Y):
    return (T-Y).sum(axis=0)

def derivative_w1(X, Z, T, Y, W2):
    N, D = X.shape
    M, K = W2.shape
    dZ = (T-Y).dot(W2.T) * Z * (1-Z)
    return X.T.dot(dZ)

def derivative_b1(T, Y, W2, Z):
    return ((T - Y).dot(W2.T) * Z * (1-Z)).sum(axis=0)  

# =============================================================================
    
W1 = np.random.randn(D, M)
b1 = np.random.randn(M)
W2 = np.random.randn(M, K)
b2 = np.random.randn(K)

learning_rate = 0.001
costs = []

for epoch in range(1000):
    Z, output = feed_forward(Xtrain, W1, b1, W2, b2)
    if epoch % 100 == 0:
        c = cost(T, output)
        costs.append(c)
        pred = np.argmax(output, axis = 1)
        c_r = classification_rate(Ytrain, pred)
        print('cost: {}, classificaiton rate: {}'.format(c, c_r))
    W2 += learning_rate * derivative_w2(Z, T, output)
    b2 += learning_rate * derivative_b2(T, output)    
    W1 += learning_rate * derivative_w1(Xtrain, Z, T, output, W2)
    b1 += learning_rate * derivative_b1(T, output, W2, Z)
    
plt.plot(costs)
plt.show()


# test set classification:

test_N = len(Ytest)
test_T = np.zeros((test_N, K))
for i in range(test_N):
    test_T[i, Ytest[i]] = 1
    
test_Z, test_output = feed_forward(Xtest, W1, b1, W2, b2)
test_cost = cost(test_T, test_output)
test_pred = np.argmax(test_output, axis = 1)
test_cr = classification_rate(Ytest, test_pred)

print("Test Set:")
print('cost: {}, classification rate: {}'.format(test_cost, test_cr))
































