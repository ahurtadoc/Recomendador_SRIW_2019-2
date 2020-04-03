# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 01:33:49 2020

@author: Morales
"""

import pandas as pd
import sqlite3 as sql3
from surprise import Dataset
from surprise import Reader
import pandas as pd
import io
import Recomendador as recoco
import RecomendadorColaborativo as recocol

#listCon = [[145, 4.926921789638419], [7, 4.368009885080416], [186, 4.07767991120728], [275, 4.06981929693394], [50, 3.9624118121256116], [104, 3.957391716990625], [254, 3.9398516694491716], [43, 3.8487106478142037], [189, 3.8480831534332434], [2, 3.769553472374536]]
#listCol = [[69, 3.4213628659315254], [2, 3.2173275254893885], [64, 2.7163178528909597], [50, 2.66528062827859], [6, 2.6314335649360103], [14, 2.576203034584178], [5, 2.5699233808027997], [8, 2.4032137247813767], [16, 2.2434028699818533], [13, 2.005632830005536]]
#listaCon = " "
#listaCol = " "

def get_recomendations(con,usuario):
    pesoContenido = 0.6
    pesoColaborativo = 0.4
    hib = []
    
    listaCon = recoco.rec_cont(con,usuario)
    listaCol = recocol.rec_col(con,usuario)
    #print('colaborativo ', listCol)
#print(juegos[0])
    lista = []
    for i in range(len(listaCon)):
        lista.append((listaCon[i], listaCol[i][1]))
    #print(lista)
    #print(" ")
        # Sistema híbrido
    for i in range(len(lista)):
        lst1 = list(lista[i])
        lst2 = list(listaCol[i])
        lst1[1] = lst1[1] * pesoContenido
        lst2[1] = lst2[1] * pesoColaborativo
        lista[i] = lst1
        listaCol[i] = lst2
    #print(lista)
    #print(" ")
    #print(listCol)
    #print(" ")
    juegos = []
    for i in listaCon:
        juegos.append(i[0])
    #print(juegos)
    rec = []
    for i in lista:
        juego = i[0][0]
        otro = juegos.index(juego)
        suma = i[1] + list(listaCon[otro])[1]
        rec.append((juego, suma))

    recomendacion = sorted(rec, key=lambda tup: tup[1], reverse=True)
    if len(recomendacion) > 10:
        recomendacion = recomendacion[:10]
        
    hib = []
    for i in recomendacion:
        hib.append(i[0])

    return hib

con = sql3.connect('recomen.db')
get_recomendations(con,'asd')

