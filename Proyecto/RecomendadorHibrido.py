# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 01:33:49 2020

@author: Morales
"""


import sqlite3 as sql3
import RecomendadorContenido as recoco
import RecomendadorColaborativo as recocol
import pandas as pd
#listCon = [[145, 4.926921789638419], [7, 4.368009885080416], [186, 4.07767991120728], [275, 4.06981929693394], [50, 3.9624118121256116], [104, 3.957391716990625], [254, 3.9398516694491716], [43, 3.8487106478142037], [189, 3.8480831534332434], [2, 3.769553472374536]]
#listCol = [[69, 3.4213628659315254], [2, 3.2173275254893885], [64, 2.7163178528909597], [50, 2.66528062827859], [6, 2.6314335649360103], [14, 2.576203034584178], [5, 2.5699233808027997], [8, 2.4032137247813767], [16, 2.2434028699818533], [13, 2.005632830005536]]
#listaCon = " "
#listaCol = " "

def get_recomendations(con,usuario):
    pesoContenido = 0.4
    pesoColaborativo = 0.6
#    hib = []
    
    listaCon = recoco.rec_cont(con,usuario)
    listaCol = recocol.rec_col(con,usuario)
#    print(listaCol[:10])
#    print(listaCon[:10])
    rangolcl = len(listaCol)
    rangolcn = len(listaCon)
    items_peso = {}
    for i in range(rangolcl):
        try:
            nuevoCol= listaCol[i][1] * pesoColaborativo
            items_peso[listaCol[i][0]] = max(items_peso[listaCol[i][0]],nuevoCol)
        except KeyError:
            items_peso[listaCol[i][0]] = listaCol[i][1] * pesoColaborativo
       
    for i in range(rangolcn):
        try :
            nuevoCon = listaCon[i][1]* pesoContenido
            items_peso[listaCon[i][0]] = max(items_peso[listaCon[i][0]],nuevoCon)
        except KeyError:
            items_peso[listaCon[i][0]] = listaCon[i][1] * pesoContenido
        

    
#    sentencia = 'SELECT * FROM juegos WHERE Estado = 1'
#    pd.read_sql_query(sentencia,con)
    
    juegos_rec = sorted(items_peso.items(),  key=lambda x: x[1], reverse = True)
    
    return juegos_rec
#
#con = sql3.connect('recomen.db')
#x = get_recomendations(con,'ola@')
#print(x)


