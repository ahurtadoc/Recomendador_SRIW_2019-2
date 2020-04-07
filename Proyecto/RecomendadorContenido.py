# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 18:13:57 2020

@author: Morales
"""

import numpy as np
import sqlite3 as sql3
import pandas as pd



def rec_cont(con,usuario):    
    
    juegos = pd.read_sql_query('select * from juegos', con)
    juegos_categ = pd.get_dummies(juegos, prefix_sep='', prefix='', columns=['Publicador'])
    juegos_categ = juegos_categ.drop(["Desarrollador", "Genero", "Link1", "Link2", "Comments","Estado"], axis=1)
    
    juegos_categ.to_sql("recomendador_contenido", con, if_exists="replace", index=False)
    query = 'SELECT Titulo, Nota FROM calificacion WHERE correo = "' + usuario + '"'
    calificacion = pd.read_sql_query(query, con)
    
    
    
    calificados = pd.DataFrame()
    for i in range(0, len(calificacion)):
        
        query = 'SELECT * FROM recomendador_contenido WHERE Titulo = "' + calificacion.loc[i][0] + '" '
        consulta = pd.read_sql_query(query, con)
        
        calificados = calificados.append(consulta)
    
    
    rango_calificados = [min(list(calificados['Precio'])),max(list(calificados['Precio']))]
    
    
    juegos2 = pd.merge(calificacion, calificados, on='Titulo', suffixes=('_x', '_y'))
    
    
    for i in range(len(juegos2)):
        for j in range(2, juegos2.loc[0].count()):
            juegos2.iat[i,j] = juegos2.iat[i,1]*juegos2.iat[i,j]
    
    perfil_sin_normalizar = juegos2.sum(axis=0)
    
    total_gamemode = perfil_sin_normalizar[2] + perfil_sin_normalizar[3]
    total_nota = perfil_sin_normalizar['Nota']
    
    
    
    total_publisher = 0
    
    for i in range(5, len(perfil_sin_normalizar)):
        total_publisher = total_publisher + perfil_sin_normalizar[i]
    
    perfil_normalizado = juegos2.astype('float64', errors='ignore')
    
    # Normalizacion de datos
    for i in range(1, len(juegos2)):
        perfil_normalizado = perfil_normalizado.drop(i)
    
    
    
    for i in range(2,perfil_normalizado.loc[0].count()):
        if i <= 3:
            perfil_normalizado.iat[0,i] = perfil_sin_normalizar[i]/total_gamemode
        elif i == 4:
            perfil_normalizado.iat[0,i] = perfil_sin_normalizar[i]/total_nota
        else:
            perfil_normalizado.iat[0,i] = perfil_sin_normalizar[i]/total_publisher
            
    perfil_normalizado = perfil_normalizado.drop(["Titulo", "Nota"], axis=1)
    
    ## Se normaliza el precio para el perfil
    prn = perfil_normalizado['Precio'][0]
    prn = (prn-rango_calificados[0])/(rango_calificados[1] - rango_calificados[0])
    perfil_normalizado['Precio'][0] = prn 
    
    ##
    juegos_categ2 = juegos_categ
    
    
    
    for i in range(len(juegos2)):
        juegos_categ2 = juegos_categ2.drop(juegos_categ[juegos_categ['Titulo']== juegos2.loc[i][0]].index)
        
    #Se normaliza el precio para los juegos
    rango_precios = [min(list(juegos_categ2['Precio'])),max(list(juegos_categ2['Precio']))]
    
    for i in range(len(juegos_categ2)):
        prn = juegos_categ2['Precio'].iat[i]
        prn = (prn-rango_precios[0])/(rango_precios[1] - rango_precios[0])
        juegos_categ2['Precio'].iat[i] = prn 
        
    
    #Se saca la similitud coseno de cada juego
    sim = []
    for i in range(len(juegos_categ2)):
        juego = list(juegos_categ2.iloc[i][1:])
        usuario = list(perfil_normalizado.iloc[0])
        sim += [np.dot(juego,usuario)/(np.linalg.norm(juego)*np.linalg.norm(usuario))] 
    
     
    juegos_categ2['Similitud'] = sim
    
    sim = np.array(sim)
    # Se lleva similitud coseno a calificacion
    sim = (sim*4) + 1
    
    nombres = list(juegos_categ2['Titulo'])
    
    listCon = []
    for n in range(len(nombres)):
        listCon += [[nombres[n],sim[n]]]
    return(sorted(listCon, key=lambda x:x[1], reverse = True))

#con = sql3.connect('recomen.db')
#print(rec_cont(con,'ola@'))