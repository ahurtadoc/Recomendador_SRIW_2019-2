# -*- coding: utf-8 -*-
"""Aplicacion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mz3Yk9QYsXLezr0_3hsHSKeH-rD-wA0H
"""

import wx
#import wx.dataview
import wx.lib.mixins.listctrl  as  listmix
import sqlite3 as sql3
import pandas as pd
import Funciones as fun
import RecomendadorHibrido as rech
#import RecomendadorColaborativo
#import Recomendador 
#from ItemScrapy import connectBD

## Interfaz

###################### Ventana de inicio de sesión ##########################
class LoginFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (500,300))
        self.elementos()
        
        
        
    def elementos(self):
        
        self.correo_text = wx.StaticText(self,label = 'Correo')
        self.pass_text = wx.StaticText(self,label = 'Contraseña') 
        self.correo_ctrl = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER)
        self.pass_ctrl = wx.TextCtrl(self,style = wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.boton = wx.Button(self,-1,'Iniciar sesión')
        self.boton_reg = wx.Button(self,-1,'Registrar')
        self.events()
        self.layout()
        
    def layout(self):
        #sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        form_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5, hgap=5)
#        #Sizer nombre
#        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
#        #sizer pass
#        pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
#        
        form_sizer.AddMany([(self.correo_text,1),
                            (self.correo_ctrl,1,wx.EXPAND),
                            (self.pass_text,1),
                            (self.pass_ctrl,1,wx.EXPAND)])
#        #creacion layout

        
        main_sizer.Add(self.boton_reg,0,wx.LEFT|wx.ALL,5)
        main_sizer.Add(form_sizer,0,wx.CENTER|wx.ALL,5)

        main_sizer.Add(self.boton,0,wx.CENTER|wx.ALL,5)
        
        self.SetSizer(main_sizer)
        self.Layout()
        
    def events(self):
        self.correo_ctrl.Bind(wx.EVT_TEXT_ENTER,self.login)
        self.pass_ctrl.Bind(wx.EVT_TEXT_ENTER,self.login)
        self.boton.Bind(wx.EVT_BUTTON,self.login)
        self.boton_reg.Bind(wx.EVT_BUTTON,self.regis)
    
    def login(self,e):
        correo = self.correo_ctrl.GetValue()
        password = self.pass_ctrl.GetValue()
        
        usuario = fun.iniciar_sesion(con,correo,password)
        if usuario == False:
            mensaje = 'usuario o contraseña incorrecto'
            wx.MessageBox(mensaje, "Atencion" ,wx.OK | wx.ICON_INFORMATION)
#            print('usuario o contraseña incorrecto')
        else:
#            RecomendadorColaborativo.us(usuario[0])
#            Recomendador.us(usuario[0])
            sesion = ListaFrame(None, 'Lista de juegos',usuario)
            sesion.Center()
            sesion.Show()
            self.Hide()
            
    
    def regis(self,e):
        registro = RegistroFrame(None,'Registrar Usuario')
        registro.Center()
        registro.Show()
        self.Hide()
 
######################## Ventana de sesion #################################       
class RegistroFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title = title,size=(500,300))
        self.elementos()
    
    def elementos(self):
        
        self.name_text = wx.StaticText(self,label = 'Nombre')
        self.correo_text = wx.StaticText(self,label = 'Correo')
        self.pass_text = wx.StaticText(self,label = 'Contraseña')
        self.name_ctrl = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER)
        self.correo_ctrl = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER)
        self.pass_ctrl = wx.TextCtrl(self,style = wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.boton_reg = wx.Button(self,-1,'Registrar')
        self.boton_can = wx.Button(self,-1,'Cancelar')
        self.events()
        self.layout()
        
    def layout(self):
        #sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        #Sizer nombre
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer correo
        correo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer pass
        pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        #creacion layout
        name_sizer.Add(self.name_text,1,wx.ALL, 5)
        name_sizer.Add(self.name_ctrl,1,wx.ALL|wx.ALIGN_CENTER, 5)
        correo_sizer.Add(self.correo_text,1,wx.ALL, 5)
        correo_sizer.Add(self.correo_ctrl,1,wx.ALL|wx.ALIGN_CENTER, 5)
        pass_sizer.Add(self.pass_text,1,wx.ALL, 5)
        pass_sizer.Add(self.pass_ctrl,1,wx.ALL|wx.ALIGN_CENTER, 5)
        
        main_sizer.Add(name_sizer,0,wx.CENTER|wx.ALL,5)
        main_sizer.Add(correo_sizer,0,wx.CENTER|wx.ALL,5)
        main_sizer.Add(pass_sizer,0,wx.CENTER|wx.ALL,5)
        main_sizer.Add(self.boton_reg,0,wx.CENTER|wx.ALL,5)
        main_sizer.Add(self.boton_can,0,wx.CENTER|wx.ALL,5)
        
        self.SetSizer(main_sizer)
        self.Layout()
        
    def events(self):
        self.name_ctrl.Bind(wx.EVT_TEXT_ENTER,self.regis)
        self.correo_ctrl.Bind(wx.EVT_TEXT_ENTER,self.regis)
        self.pass_ctrl.Bind(wx.EVT_TEXT_ENTER,self.regis)
        self.boton_reg.Bind(wx.EVT_BUTTON,self.regis)
        self.boton_can.Bind(wx.EVT_BUTTON,self.home)
        self.Bind(wx.EVT_CLOSE,self.home)
    
    def regis(self,e):
        nombre = self.name_ctrl.GetValue()
        correo = self.correo_ctrl.GetValue()
        password = self.pass_ctrl.GetValue()
        
        r = fun.registroU(con,correo,nombre,password)
        wx.MessageBox(r, "Atencion" ,wx.OK | wx.ICON_INFORMATION)
        
    
    def home(self,e):
        self.Destroy()
        frame.Show()
    

class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    ''' TextEditMixin allows any column to be edited. '''
 
    #----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)
        
class ListaFrame(wx.Frame):
    def __init__(self,parent,title,user):
        wx.Frame.__init__(self,parent,title = title,size=(1000,700))
        
        self.elementos()
        self.sesion(user)
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        self.list = EditableListCtrl(self.panel,style= wx.LC_REPORT)
        instruccion = ''' Para asignar una calificación cambie el valor en en la columna 'Calificación' por un número entre 1 y 5 de la siguiente manera
        1 : Malo
        2 : Regular
        3 : Normal
        4 : Bueno
        5 : Muy bueno
        '''
        self.info = wx.StaticText(self.panel,label = instruccion)
        self.guardar = wx.Button(self.panel, label = 'Guardar calificaciones')
        self.cerrar_sesion = wx.Button(self.panel, label = 'Cerrar sesion') 
        self.recomendar = wx.Button(self.panel, label = 'Hacer recomendación')
        self.events()
        self.layout()
    
    def sesion(self,user):
        self.user = user
        self.cambios = {}
        juegos = fun.lista_juegos(con)
        calif = fun.calificados(self.user[0],con)
      

        for columna in list(juegos):
            self.list.AppendColumn(columna)

        self.list.AppendColumn('Calificacion')
            
        for item in range(len(juegos)):
            row = list(juegos.loc[item])
            
            
            puntaje = calif[juegos.loc[item][1]][0] 
            if puntaje == None:
                row += []
            else:
                row += [int(puntaje)]
    
            self.list.Append(row)
   
    def layout(self):

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        lista_sizer = wx.BoxSizer(wx.HORIZONTAL)
        

        
        lista_sizer.Add(self.list,1,wx.ALL|wx.EXPAND,5)

        main_sizer.Add(self.info,0,wx.ALL,5)
        main_sizer.Add(lista_sizer,1,wx.ALL|wx.EXPAND)
        main_sizer.Add(self.guardar,0,wx.ALL|wx.CENTER,5)
        main_sizer.Add(self.recomendar,0,wx.ALL,5)
        main_sizer.Add(self.cerrar_sesion,0,wx.ALL,5)

        self.panel.SetSizer(main_sizer)

    def events(self):
        self.list.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,self.edit_cal)
        self.list.Bind(wx.EVT_LIST_END_LABEL_EDIT,self.cambiar_cal)
        self.Bind(wx.EVT_CLOSE,self.home)
        self.guardar.Bind(wx.EVT_BUTTON,self.guardar_cal)
        self.recomendar.Bind(wx.EVT_BUTTON,self.recomendacion)
        self.cerrar_sesion.Bind(wx.EVT_BUTTON,self.home)
#    
    def edit_cal(self,e):
        col_id = e.GetColumn()
        if col_id != 9:
            e.Veto()
            
    def cambiar_cal(self,e):
        
        try: 
            cambio = int(e.GetLabel())
            posibles = [1,2,3,4,5]
        
            juego = self.list.GetItemText(e.GetIndex(),1)

        
            if cambio in posibles:
                self.cambios[juego] = cambio 
                
                
            else:
                raise(ValueError)
        except ValueError:
            mensaje = 'El valor ingresado no es válido'
            wx.MessageBox(mensaje, "Atencion" ,wx.OK | wx.ICON_INFORMATION)
#            print('formato no valido')
            e.Veto()
        
    def guardar_cal(self,e):
        if len(self.cambios) == 0 :
            mensaje =  'Debe realizar cambios en la calificacion'
            wx.MessageBox(mensaje, "Atencion" ,wx.OK | wx.ICON_INFORMATION)
#            print('Debe hacer cambios')
        else:
            resul = fun.guardar_cambios(self.cambios,con,self.user[0])
            fun.guardar_tabla(self.cambios,con,self.user[0])
            wx.MessageBox(resul, "Atencion" ,wx.OK | wx.ICON_INFORMATION)

        self.cambios = {}
        
    def recomendacion(self,e):
        usuario = self.user
        print(usuario)
        rec = RecomendacionesFrame(None,'Juegos Recomendados',usuario = usuario, ventana = self)
        rec.Center()
        rec.Show()
        self.Hide()
    
    def home(self,e):
        self.Destroy()
        frame.Show()
 
############################# Recomendaciones ################################ 

class RecomendacionesFrame(wx.Frame):
    def __init__(self,parent,title,usuario,ventana):
        wx.Frame.__init__(self,parent,title = title,size=(800,700))
        self.user = usuario
        
        self.sesion = ventana
        self.elementos()
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        texto = 'Estos son los 10 juegos más recomendados para ti'
        self.info = wx.StaticText(self.panel,label = texto)
        self.list = wx.ListCtrl(self.panel,style = wx.LC_REPORT)
        self.volver = wx.Button(self.panel, label = 'Volver') 
        self.listar()
        self.events()
        self.layout()
    
    def listar(self):
        
        
        self.list.AppendColumn('Juego',width=-2)

        
        if(fun.is_cold_user(con,self.user[0])):
            juegos = fun.cold_user(con)
            print(juegos)
            if len(juegos) > 10:
                for i in range(10):
                    row = [juegos[i][0]]
#                    print(row)
                    self.list.Append(row)
            else:
                for j in juegos:
                    row = [j[0]]
#                    print(row)
                    self.list.Append(row)
        
        else:
        
        
            row = ['Aca va el recomendador']
            self.list.Append(row)
#            rech.get_recomendations(con,self.user)
            
    
   
    def layout(self):

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        lista_sizer = wx.BoxSizer(wx.HORIZONTAL)

        
        lista_sizer.Add(self.list,1,wx.ALL|wx.EXPAND,5)

        main_sizer.Add(self.info,0,wx.ALL,5)
        main_sizer.Add(lista_sizer,1,wx.ALL|wx.EXPAND)
        main_sizer.Add(self.volver,0,wx.ALL|wx.CENTER,5)

        self.panel.SetSizer(main_sizer)

    def events(self):

        self.Bind(wx.EVT_CLOSE,self.home)
        self.volver.Bind(wx.EVT_BUTTON,self.home)
    
    def home(self,e):
        self.Destroy()
        self.sesion.Show()
try:
    if __name__ == '__main__':
        
        con = sql3.connect('recomen.db')
#        fun.crearBD(con)
        juegos = fun.lista_juegos(con)
    
        
        
        app = wx.App()
        frame = LoginFrame(None, 'Iniciar sesion')
        frame.Center()
        frame.Show()
        app.MainLoop()
        


    
finally:
    del app
    con.close()

