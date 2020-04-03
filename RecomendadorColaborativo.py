# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 01:09:44 2020

@author: Morales
"""

import pandas as pd
import sqlite3 as sql3
from surprise import Dataset
from surprise import Reader
from surprise import SVD, NormalPredictor
from surprise.model_selection import GridSearchCV
#import pandas as pd
import io
from collections import defaultdict
#from surprise import SVD
#from surprise import Dataset
#from surprise.model_selection import GridSearchCV

con = sql3.connect('recomen.db')
def rec_col(con,usuario):

    df1 = pd.read_sql_query('select * from calificacion', con)
    df1.to_csv("calificacion.csv", index=False)
    #df1
    df2 = pd.read_csv('calificacion.csv')
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df2, reader)
    #df2
    
    

    param_grid = {'n_factors':[50,100,150],'n_epochs':[20,30],  'lr_all':[0.005,0.01],'reg_all':[0.02,0.1]}
    gs = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3)
    gs.fit(data)
    params = gs.best_params['rmse']
    svdtuned = SVD(n_factors=params['n_factors'],
                   n_epochs=params['n_epochs'], lr_all=params['lr_all'],
                   reg_all=params['reg_all'])
    
    
    
    
    def get_top_n(predictions, n=10):
        '''Return the top-N recommendation for each user from a set of predictions.
    
        Args:
            predictions(list of Prediction objects): The list of predictions, as
                returned by the test method of an algorithm.
            n(int): The number of recommendation to output for each user. Default
                is 10.
    
        Returns:
        A dict where keys are user (raw) ids and values are lists of tuples:
            [(raw item id, rating estimation), ...] of size n.
        '''
    
        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))
    
        # Then sort the predictions for each user and retrieve the n highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]
    
        return top_n
    
    # First train an SVD algorithm on the movies dataset.
    trainset = data.build_full_trainset()
    untuned = SVD()
    untuned.fit(trainset)
    
    # Then predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = untuned.test(testset)
    #print(type(predictions))
    top_n = get_top_n(predictions, n=3)
    # Print the "n" recommended items for each user
    #for pelicula, calificacion in top_n["Alexander Hurtado Cardona"]:
    #    print(pelicula, calificacion)
    
    
    param_grid = { 'n_factors': [50,100,150],
        "n_epochs": [20, 30, 40, 50, 90],
        "lr_all": [0.002, 0.005, 0.01, 0.02, 0.04],
        "reg_all": [0.02, 0.005, 0.1]
    }
    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)
    
    gs.fit(data)
    
    tunedParams = gs.best_params['rmse']
    
    #print(gs.best_score["rmse"])
    #print(gs.best_params["rmse"])
    #print(gs.best_score["mae"])
    #print(gs.best_params["mae"])
    
    trainset = data.build_full_trainset()
    svdtuned = SVD(n_factors=tunedParams['n_factors'], n_epochs=tunedParams['n_epochs'],lr_all=tunedParams['lr_all'], reg_all=tunedParams['reg_all'])
    svdtuned.fit(trainset)
    
    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = svdtuned.test(testset)
    
    top_n = get_top_n(predictions, n=3)
    # Print the recommended items for each user
    #for pelicula, calificacion in top_n["Alexander Hurtado Cardona"]:
    #    print(pelicula, calificacion)
    
    #print("Matriz Pu \n" ,svdtuned.pu)
    
    #print("Matriz Qi \n",svdtuned.qi)
    
    trainset = data.build_full_trainset()
    algo = SVD(n_factors=tunedParams['n_factors'], n_epochs=tunedParams['n_epochs'],lr_all=tunedParams['lr_all'], reg_all=tunedParams['reg_all'])
    algo.fit(trainset)
    
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    top_n = get_top_n(predictions, n=10)
    

    recoco = []
    def recocolaborativa(usuario):
        for pelicula, calificacion in top_n[usuario]:
            recoco.append([pelicula, calificacion])
        return recoco
    #print(usu)
    listCol = recocolaborativa(usuario)
    return listCol

con = sql3.connect('recomen.db')
print(rec_col(con,'asd'))