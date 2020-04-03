# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 00:12:47 2020

@author: Morales
"""

import sqlite3 as sql3
import pandas as pd
import numpy as np
import Funciones as fun
#import RecomendadorHibrido
from operator import itemgetter

def rec_cont(con,usuario):
    
    cur = con.cursor()
    contenido = pd.read_sql_query('select * from contenido', con)
    contenido2 = contenido
    
    contenido.to_csv("contenido.csv", index=False)
    
    #df1 = pd.read_csv('contenido.csv', sep=',')
    df1 = pd.read_csv('contenido.csv', sep=',', usecols= lambda column : column not in ["index", "user_id"])
    #df1.to_csv("contenidox.csv", index=False)
    
    #print(df1)
    
    df1 = np.array(df1)
    df1 = np.nan_to_num(df1)
    #print(df1)
    
    #maior = max(df1[3], key=int)
    #print(maior)
    
    ###############################################################################
       
    class MF():
    
        def __init__(self, R, K, alpha, beta, iterations):
            """
            Perform matrix factorization to predict empty
            entries in a matrix.
    
            Arguments
            - R (ndarray)   : user-item rating matrix
            - K (int)       : number of latent dimensions
            - alpha (float) : learning rate
            - beta (float)  : regularization parameter
            """
    
            self.R = R
            self.num_users, self.num_items = R.shape
            self.K = K
            self.alpha = alpha
            self.beta = beta
            self.iterations = iterations
    
        def train(self):
            # Initialize user and item latent feature matrice
            self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
            self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))
    
            # Initialize the biases
            self.b_u = np.zeros(self.num_users)
            self.b_i = np.zeros(self.num_items)
            self.b = np.mean(self.R[np.where(self.R != 0)])
    
            # Create a list of training samples
            self.samples = [
                (i, j, self.R[i, j])
                for i in range(self.num_users)
                for j in range(self.num_items)
                if self.R[i, j] > 0
            ]
    
            # Perform stochastic gradient descent for number of iterations
            training_process = []
            for i in range(self.iterations):
                np.random.shuffle(self.samples)
                self.sgd()
                mse = self.mse()
                training_process.append((i, mse))
                if (i+1) % 10 == 0:
                    print("Iteration: %d ; error = %.4f" % (i+1, mse))
    
            return training_process
    
        def mse(self):
            """
            A function to compute the total mean square error
            """
            xs, ys = self.R.nonzero()
            predicted = self.full_matrix()
            error = 0
            for x, y in zip(xs, ys):
                error += pow(self.R[x, y] - predicted[x, y], 2)
            return np.sqrt(error)
    
        def sgd(self):
            """
            Perform stochastic graident descent
            """
            for i, j, r in self.samples:
                # Computer prediction and error
                prediction = self.get_rating(i, j)
                e = (r - prediction)
    
                # Update biases
                self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
                self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])
    
                # Update user and item latent feature matrices
                self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
                self.Q[j, :] += self.alpha * (e * self.P[i, :] - self.beta * self.Q[j,:])
    
        def get_rating(self, i, j):
            """
            Get the predicted rating of user i and item j
            """
            prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
            return prediction
    
        def full_matrix(self):
            """
            Computer the full matrix using the resultant biases, P and Q
            """
            return self.b + self.b_u[:,np.newaxis] + self.b_i[np.newaxis:,] + self.P.dot(self.Q.T)
        
    # Perform training and obtain the user and item matrices 
    mf = MF(df1, K=2, alpha=0.1, beta=0.01, iterations=20)
    training_process = mf.train()
    #print(mf.P)
    #print(mf.Q)
    #print(mf.full_matrix())
    
    matris = mf.full_matrix()
    fun.recomend_to_sql(matris.tolist(),contenido2,con)
    

 
        
    #us(usu)
    #usu = str(1)
    query ='SELECT * FROM contenido_final WHERE user_id = "' + usuario + '"'
    print(query)
    df1 = pd.read_sql_query(query,con)
    #print(df1)
    #print(df1.max())
    df1 = df1.drop(['user_id'], axis=1)
    print(df1)
    df1 = np.array(df1)
    #print(df1)
    
    
    query = 'DROP TABLE contenido_final'
    cur.execute(query)
    reco = []
    print(df1)
    def recocontenido():
        max1 = sorted(enumerate(df1[0]), key=itemgetter(1),  reverse=True)
        for i in range(0, 10, 1):
            index, value = max1[i]
            reco.append([index, value])
        return reco
        
    listCon = recocontenido()
    
    
    return listCon 
#RecomendadorHibrido.listCon(listCon)
    #print(matris[0][1])
    
    
    #np.savetxt("contenido_final.csv", matris, delimiter=",")
    
    #import csv
    
    #con = sql3.connect('recomen.db')
    #cursor = con.cursor()
    #q = str(1)
    #query = "SELECT * FROM contenido_final WHERE user_id = " + q
    #contenido = pd.read_sql_query(query, con)
    #contenido.to_csv("contenido_final.csv", index=False)
    #df1 = pd.read_csv('contenido_final.csv', sep=',')
    #with open("contenido_final.csv", "r") as f:
    #    reader = csv.reader(f)
    #    i = next(reader)
    #    rest = [row for row in reader]
    #i.pop(len(i)-1)
    #i.pop(0)    
    #print(i)
    #print (contenido)
    #for jogo in i:
    #        df1.loc[df1['user_id'] == id][jogo].tolist()[0][0]
    #
    #results = {}
    #df1.head()
    #def item(id):
    #    return df1.loc[df1['asdasd'] == id]['Anthem'].tolist()[0][0]
    #
    # Just reads the results out of the dictionary.
    #def recommend(item_id, num):
    #    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")
    #    print("-------")
    #    recs = results[item_id][:num]
    #    for rec in recs:
    #        print("Recommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")
    #
    #recommend(item_id=1, num=2)
