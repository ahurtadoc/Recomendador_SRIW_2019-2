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
    
    
    TablaUsuario = '''CREATE TABLE IF NOT EXISTS usuarios (
                          correo TEXT PRIMARY KEY,
                          nombre TEXT,
                          contrase TEXT)'''
    cur.execute(TablaUsuario)
    
    TablaCalificacion = '''CREATE TABLE IF NOT EXISTS calificacion (
                          correo TEXT,
                          Titulo TEXT ,
                          Nota INTEGER,
                          PRIMARY KEY(correo,Titulo))'''
    cur.execute(TablaCalificacion)
        
    
    Tabla_aciertos = 'CREATE TABLE IF NOT EXISTS aciertos(valor INTEGER) '
    cur.execute(Tabla_aciertos)
    
    juegos_nuevos = 'CREATE TABLE IF NOT EXISTS nuevos(juego TEXT PRIMARY KEY, valor INTEGER) '
    cur.execute(juegos_nuevos)

    con.commit()
        
    

def registroU(con,correo,nombre,contrase):
    cur = con.cursor()

    try:
        sentencia = ("INSERT INTO usuarios VALUES (?,?,?)")
        cur.execute(sentencia,[correo,nombre,contrase])
        
        #contenido = 'INSERT INTO contenido (user_id) VALUES (?)'
        #cur.execute(contenido,[correo])
        
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
    sentencia = ('SELECT * FROM juegos WHERE estado == 1')
    juegos = pd.read_sql_query(sentencia,con)
    return juegos.drop(['Estado'],axis = 1)
 
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
    cur = con.cursor()
    sentencia = 'SELECT * FROM calificacion WHERE "correo" = ?'
    lista = cur.execute(sentencia,[user]).fetchall()
    calificaciones = {}
    for i in lista:
        calificaciones[i[1]] = i[2]
    return calificaciones


def listar_rec(con,lista_nombres):
    sentencia = 'SELECT * FROM juegos WHERE Estado = 1'
    juegos_disponibles = pd.read_sql_query(sentencia,con)
    juegos_disponibles = juegos_disponibles.drop('Estado', axis = 1)
    aux = 0
    juegos_finales = []
    for i in lista_nombres:
        juego = juegos_disponibles[juegos_disponibles.Titulo == i[0]]
        if len(juego) > 0:
            juegos_finales += [list(juego.iloc[0])]
            aux += 1
        if aux == 10:
            break
        
    return juegos_finales




def guardar_tabla(cambios,con,user):
    cur = con.cursor()
    for juego in cambios:

        
        try:
        
            sentencia = 'INSERT INTO calificacion (correo,Titulo,Nota) VALUES(?,?,?)' 
            cur.execute(sentencia,[user,juego,cambios[juego]])
        except:
            sentencia = '''UPDATE calificacion SET Nota = ? WHERE 
                                                    correo = ? AND
                                                    Titulo = ?
                                                    ''' 
            cur.execute(sentencia,[cambios[juego],user,juego])
    con.commit()
    return("Cambios guardados")

def is_cold_user(con,user):
    cur = con.cursor()
    sentencia = 'SELECT * FROM calificacion WHERE correo = ?'
    if (cur.execute(sentencia,[user]).fetchall() == []):
        return True
    else:
        return False

def  cold_user(con):
    cur = con.cursor()
    sentencia = 'SELECT Titulo, Nota FROM calificacion'
    juegos = cur.execute(sentencia).fetchall()
    lista_juegos = {}
    if len(juegos) == 0:
        return(traer_nuevos(con))  

    else:
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
    
            juegoxcal += [[juego,cal_pon]]
        
        return(sorted(juegoxcal, key=lambda x:x[1], reverse = True))


def perfil(con,usuario):
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
            perfil_normalizado.iat[0,i] = round(perfil_sin_normalizar[i]/total_gamemode,2)
        elif i == 4:
            perfil_normalizado.iat[0,i] = round(perfil_sin_normalizar[i]/total_nota,2)
        else:
            perfil_normalizado.iat[0,i] = round(perfil_sin_normalizar[i]/total_publisher,2)
            
    perfil_normalizado = perfil_normalizado.drop(["Titulo", "Nota"], axis=1)
    

    return(perfil_normalizado)


def cal_global(con):
    cur = con.cursor()
    sentencia = 'SELECT Titulo, Nota FROM calificacion'
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

    juegoxcal = {}
    for juego in lista_juegos:
        cal_pon = lista_juegos[juego][0]/lista_juegos[juego][1]

        juegoxcal[juego] = round(cal_pon,2)
    return juegoxcal

def promedio(con):
    cur = con.cursor()
    sentencia = 'SELECT Nota FROM calificacion'
    notas = cur.execute(sentencia).fetchall()
    s = 0
    for i in notas:
        s += i[0]
        
    
    promedio = s/len(notas)
    return round(promedio,2)


def acierto(con,opcion):
    cur = con.cursor()
    sentencia = 'INSERT INTO aciertos (valor) VALUES (?)'
    if opcion == 'Si':
        cur.execute(sentencia,[1])
    else:
        cur.execute(sentencia,[0])
    con.commit()


def eficiencia(con):
    cur = con.cursor()
    sentencia = 'SELECT * FROM aciertos'
    aciertos = cur.execute(sentencia).fetchall()
    if len(aciertos) == 0:
        return('Aun no hay reseñas del sistema de recomendacion')
    else:
        s = 0
        for i in aciertos:
            if i[0] == 1:
                s +=1
        porcentaje = s/len(aciertos)
        porcentaje = round(porcentaje*100,2) 
        return 'El sistema tiene una efectividad del ' + str(porcentaje) + '%'
        
    

def nuevos(con,lista_juegos):
    cur = con.cursor()
    for j in lista_juegos:
        try:
            
            sentencia = 'INSERT INTO nuevos (juego,valor) VALUES(?,1)' 
            cur.execute(sentencia,[j])
        except:
            sentencia = 'UPDATE nuevos SET valor = 0 WHERE juego = ? '
            cur.execute(sentencia,[j])                         
                                        
    con.commit()

#

def traer_nuevos(con):
    cur = con.cursor()
    sentencia = 'SELECT * FROM nuevos WHERE valor = 1'
    
    return(cur.execute(sentencia).fetchall())

def listar_nuevos(con,lista_nombres):
    sentencia = 'SELECT * FROM juegos WHERE Estado = 1'
    juegos_disponibles = pd.read_sql_query(sentencia,con)
    juegos_disponibles = juegos_disponibles.drop('Estado', axis = 1)
    juegos_finales = []
    for i in lista_nombres:
        juego = juegos_disponibles[juegos_disponibles.Titulo == i[0]]
        if len(juego) > 0:
            juegos_finales += [list(juego.iloc[0])]
        
    return juegos_finales
