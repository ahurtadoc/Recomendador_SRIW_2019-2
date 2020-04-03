# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:52:03 2020

@author: El-PC
"""
import pandas as pd
import sqlite3 as sql3


def conectBD():
    con = sql3.connect('recomen.db')
    return con

def crearBD(con):
    cur = con.cursor()
    
    juegos = pd.read_csv('juegos.csv')
    juegos.to_sql("juegos", con, if_exists="replace",index = False)
    
    TablaUsuario = '''CREATE TABLE IF NOT EXISTS usuarios (
                          correo TEXT PRIMARY KEY,
                          nombre TEXT,
                          contrase TEXT)'''
    cur.execute(TablaUsuario)
    
    TablaCalificacion = '''CREATE TABLE IF NOT EXISTS calificacion (
                          user_id TEXT,
                          juego_index INTEGER ,
                          calificacion INTEGER,
                          PRIMARY KEY(user_id,juego_index))'''
    cur.execute(TablaCalificacion)
    
    sentencia = ('SELECT Titulo FROM juegos')
    juegos = cur.execute(sentencia).fetchall()
    TablaContenido = 'CREATE TABLE IF NOT EXISTS contenido(user_id TEXT NOT NULL)'
    modificar_tabla1 = ('ALTER TABLE contenido ADD ')
    modificar_tabla2 = (' TEXT DEFAULT NULL')
    cur.execute(TablaContenido)
    for juego in juegos:
        sentencia = modificar_tabla1 + '"' + juego[0] +'"'+ modificar_tabla2
        cur.execute(sentencia)
    
    con.commit()
        
    

def registroU(con,correo,nombre,contrase):
    cur = con.cursor()

    try:
        sentencia = ("INSERT INTO usuarios VALUES (?,?,?)")
        cur.execute(sentencia,[correo,nombre,contrase])
        
        contenido = 'INSERT INTO contenido (user_id) VALUES (?)'
        cur.execute(contenido,[correo])
        
        con.commit()
        return('Usuario registrado correctamente')
    except:
        return('usuario ya existe')

    
def iniciar_sesion(con,correo,contrase):
    cur = con.cursor()
    sentencia = ('SELECT * FROM usuarios WHERE correo = ? AND contrase = ?')
    user = cur.execute(sentencia,[correo,contrase]).fetchone()
    if user == None:
        return False
    else:
        return user

def lista_juegos(con):
    sentencia = ('SELECT * FROM juegos')
    juegos = pd.read_sql_query(sentencia,con)
    return juegos
 
def contenido(con):
    sentencia = ('SELECT * FROM contenido')
    conten = pd.read_sql_query(sentencia,con)
    return conten


def recomend_to_sql(matriz, conten,con):
    usuarios = conten['user_id']
    
    final = pd.DataFrame(columns = list(conten))
    index = 0
    for i in matriz:
        final.loc[index] = [index] + i + [usuarios.loc[index]]
        index += 1
    
    final.to_sql("contenido_final",con,index = False)

def calificados(user,con):
    sentencia = 'SELECT * FROM contenido WHERE "user_id" = ?'
    return pd.read_sql_query(sentencia,con,params = [user])

def guardar_cambios(cambios,con,user):
    cur = con.cursor()
    for juego in cambios:
        sentencia = 'UPDATE contenido SET "'+ juego + '"= ? WHERE user_id = ?'
        calificacion = cambios[juego]
        cur.execute(sentencia,[calificacion,user])
    con.commit()
        
    return('Cambios guardados')


def guardar_tabla(cambios,con,user):
    cur = con.cursor()
    for juego in cambios:
        sentencia = 'SELECT "index" FROM juegos WHERE Titulo = "'+ juego + '"'
        index = cur.execute(sentencia).fetchone()
        index = int(index[0])
        
        try:
        
            sentencia = 'INSERT INTO calificacion (user_id,juego_index,calificacion) VALUES(?,?,?)' 
            cur.execute(sentencia,[user,index,cambios[juego]])
        except:
            sentencia = '''UPDATE calificacion SET calificacion = ? WHERE 
                                                    user_id = ? AND
                                                    juego_index = ?
                                                    ''' 
            cur.execute(sentencia,[cambios[juego],user,index])
    con.commit()
    return("correcto")

def is_cold_user(con,user):
    cur = con.cursor()
    sentencia = 'SELECT * FROM calificacion WHERE user_id = ?'
    if (cur.execute(sentencia,[user]).fetchall() == []):
        return True
    else:
        return False

def  cold_user(con):
    cur = con.cursor()
    sentencia = 'SELECT juego_index, calificacion FROM calificacion'
    juegos = cur.execute(sentencia).fetchall()
    lista_juegos = {}

    for i in juegos:
        try:
            lista_juegos[i[0]]
            c = lista_juegos[i[0]][0]
            n = lista_juegos[i[0]][1]
            lista_juegos[i[0]] = [(i[1]+c),(n+1)]
        except KeyError:
            lista_juegos[i[0]] = [i[1],1]

    juegoxcal = []
    for juego in lista_juegos:
        cal_pon = lista_juegos[juego][0]/lista_juegos[juego][1]
        sentencia = 'SELECT Titulo FROM juegos WHERE "index" = ? '
        juego = cur.execute(sentencia,[juego]).fetchall()[0][0]
        juegoxcal += [[juego,cal_pon]]
    
    return(sorted(juegoxcal, key=lambda x:x[1], reverse = True))

#con = sql3.connect('recomen.db')
#
#is_cold_user(con,'asd')
#
#print(cold_user(con))

