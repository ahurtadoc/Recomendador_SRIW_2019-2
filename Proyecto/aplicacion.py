# -*- coding: utf-8 -*-


import wx
import wx.lib.mixins.listctrl  as  listmix
import sqlite3 as sql3
import pandas as pd
import Funciones as fun
import RecomendadorHibrido as rec_h
import webbrowser as wb
import WebScraping as scrapy
 

## Interfaz
################### Ventana principal #########################################

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (400,200))
        self.elementos()
        
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        text = '''Escoja la primera opcion para obtener los juegos disponibles
y la segunda para el sistema de recomendacion'''
        self.info = wx.StaticText(self.panel,label = text)
        self.boton_item = wx.Button(self.panel,-1,'Leer datos')
        self.boton_recom = wx.Button(self.panel,-1,'Sistema de recomendación')
        self.events()
        self.layout()
        
    def layout(self):
        #sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        aux_sizer = wx.BoxSizer(wx.HORIZONTAL)
        aux_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        aux_sizer.Add(self.info,0,wx.ALL|wx.EXPAND,5)

        main_sizer.AddMany([(aux_sizer,0,wx.EXPAND|wx.ALL,5 ),
                            (self.boton_item,0,wx.CENTER|wx.ALL,5 ),
                            (self.boton_recom,0,wx.CENTER|wx.ALL,5),
                            (aux_sizer2,1,wx.CENTER|wx.ALL,5 )
                            ])
#        #creacion layout
        
        self.panel.SetSizer(main_sizer)
        self.Layout()
        
    def events(self):
        self.boton_item.Bind(wx.EVT_BUTTON,self.item_scraping)
        self.boton_recom.Bind(wx.EVT_BUTTON,self.recomendador)
    
    def item_scraping(self,e):
        item = ItemFrame(None, 'Obtener Juegos')
        item.Center()
        item.Show()
        self.Hide()
            
    def recomendador(self,e):
        registro = LoginFrame(None,'Sistema de recomendacion')
        registro.Center()
        registro.Show()
        self.Hide()
        
        
#########################Ventana de WebScraping##############################
        
class ItemFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (500,250))
        self.elementos()
        
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        text = '''Ingrese la cantidad de paginas que desea consultar para cada una de las paginas web 
disponibles'''
        print(text)
        self.info = wx.StaticText(self.panel,label = text)
        self.best = wx.StaticText(self.panel, label = 'BestBuy.com')
        self.best_text = wx.TextCtrl(self.panel, style = wx.TE_PROCESS_ENTER)
        self.flip = wx.StaticText(self.panel, label = 'Flipkart.com')
        self.flip_text = wx.TextCtrl(self.panel, style = wx.TE_PROCESS_ENTER)
        self.boton_get = wx.Button(self.panel,-1,'Iniciar proceso')
        self.volver = wx.Button(self.panel,-1,'Volver')
        self.events()
        self.layout()
        
    def layout(self):
        #sizers principales
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        form_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=3, hgap=3)
        
        form_sizer.AddMany([(self.best,1,wx.CENTER|wx.ALL,5),
                            (self.best_text,1,wx.CENTER|wx.ALL,5),
                            (self.flip,1,wx.CENTER|wx.ALL,5 ),
                            (self.flip_text,1,wx.CENTER|wx.ALL,5)                            
                            ])

        main_sizer.AddMany([(self.info,0,wx.ALL,5 ),
                            (form_sizer,0,wx.ALL,5 ),
                            (self.boton_get,0,wx.CENTER|wx.ALL,5),
                            (self.volver,0,wx.ALL,5)
                            ])
        #creacion layout
        
        self.panel.SetSizer(main_sizer)
    
        
    def events(self):
        self.Bind(wx.EVT_CLOSE,self.home)
        self.boton_get.Bind(wx.EVT_BUTTON,self.scraping)
        self.volver.Bind(wx.EVT_BUTTON,self.home)

    
    def scraping(self,e):
        flipkart = self.flip_text.GetValue()
        bestbuy = self.best_text.GetValue()
        if flipkart.isdigit() and bestbuy.isdigit():
            flipkart = int(flipkart)
            bestbuy = int(bestbuy)
            
            if flipkart < 0 or bestbuy < 0:
                self.error()
            else:
                mensaje = scrapy.web_scrap(con,bestbuy,flipkart)
                wx.MessageBox(mensaje, "Atencion" ,wx.OK | wx.ICON_INFORMATION)
                juegos = fun.lista_juegos(con)
                fun.nuevos(con,list(juegos['Titulo']))
                
        else:
            self.error()
            
    def error(self):
        mensaje = 'El numero de paginas debe ser un entero mayor o igual a 0'
        wx.MessageBox(mensaje, "Atencion" ,wx.OK | wx.ICON_INFORMATION)

    def home(self,e):
        self.Destroy()
        main.Show()

###################### Ventana de inicio de sesión ##########################

class LoginFrame(wx.Frame):
    def __init__(self, parent, title,):
        wx.Frame.__init__(self, parent, title=title, size = (500,200))
        self.elementos()
        
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        self.correo_text = wx.StaticText(self.panel,label = 'Correo')
        self.pass_text = wx.StaticText(self.panel,label = 'Contraseña') 
        self.correo_ctrl = wx.TextCtrl(self.panel, style = wx.TE_PROCESS_ENTER)
        self.pass_ctrl = wx.TextCtrl(self.panel,style = wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.boton = wx.Button(self.panel,-1,'Iniciar sesión')
        self.boton_reg = wx.Button(self.panel,-1,'Registrar')
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
        
        self.panel.SetSizer(main_sizer)
        self.Layout()
        
    def events(self):
        self.correo_ctrl.Bind(wx.EVT_TEXT_ENTER,self.login)
        self.pass_ctrl.Bind(wx.EVT_TEXT_ENTER,self.login)
        self.boton.Bind(wx.EVT_BUTTON,self.login)
        self.boton_reg.Bind(wx.EVT_BUTTON,self.regis)
        self.Bind(wx.EVT_CLOSE,self.home)
    
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
            sesion = SesionFrame(None, 'Sesion de Usuario',usuario,self)
            sesion.Center()
            sesion.Show()
            self.Hide()
            
    
    def regis(self,e):
        registro = RegistroFrame(None,'Registrar Usuario',self)
        registro.Center()
        registro.Show()
        self.Hide()
 
    def home(self,e):
        self.Destroy()
        main.Show() 
######################## Ventana de registro #################################       
class RegistroFrame(wx.Frame):
    def __init__(self,parent,title,LoginFrame):
        wx.Frame.__init__(self,parent,title = title,size=(500,250))
        self.anterior = LoginFrame
        self.elementos()
    
    def elementos(self):
        self.panel = wx.Panel(self)
        self.name_text = wx.StaticText(self.panel,label = 'Nombre')
        self.correo_text = wx.StaticText(self.panel,label = 'Correo')
        self.pass_text = wx.StaticText(self.panel,label = 'Contraseña')
        self.name_ctrl = wx.TextCtrl(self.panel, style = wx.TE_PROCESS_ENTER)
        self.correo_ctrl = wx.TextCtrl(self.panel, style = wx.TE_PROCESS_ENTER)
        self.pass_ctrl = wx.TextCtrl(self.panel,style = wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.boton_reg = wx.Button(self.panel,-1,'Registrar')
        self.boton_can = wx.Button(self.panel,-1,'Cancelar')
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
        
        self.panel.SetSizer(main_sizer)
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
        self.anterior.Show()


################Ventana de sesion#############################################

class SesionFrame(wx.Frame):
    def __init__(self,parent,title,usuario,LoginFrame):
        wx.Frame.__init__(self,parent,title = title,size=(500,250))
        self.anterior = LoginFrame
        self.usuario = usuario
        self.elementos()
    
    def elementos(self):
        self.panel = wx.Panel(self)
        text = 'Escoja una de las siguientes tres opciones'
        self.info = wx.StaticText(self.panel,label = text)
        self.perfil = wx.Button(self.panel,-1,'Ver mi perfil')
        self.listarjuegos = wx.Button(self.panel,-1,'Listar juegos')
        self.recomendar = wx.Button(self.panel,-1,'Hacer recomendacion')
        self.efectividad = wx.Button(self.panel, label = 'Ver efectividad del Sistema')
        self.vernuevos =  wx.Button(self.panel, label = 'Ver juegos nuevos')
        self.cerrar_sesion = wx.Button(self.panel, label = 'Cerrar sesion')
        self.events()
        self.layout()
        
    def layout(self):
        #sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        #Sizer nombre
        menu_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer correo
#        correo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer pass
#        pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        #creacion layout
        menu_sizer.Add(self.perfil,0,wx.ALL, 5)
        menu_sizer.Add(self.listarjuegos,0,wx.ALL, 5)
        menu_sizer.Add(self.recomendar,0,wx.ALL, 5)
        
        main_sizer.AddMany([(self.info,0,wx.CENTER|wx.ALL,5),
                          (menu_sizer,1,wx.CENTER|wx.ALL,5),
                          (self.efectividad,0,wx.CENTER|wx.ALL,5),
                          (self.vernuevos,0,wx.ALL,5),
                          (self.cerrar_sesion,0,wx.ALL,5)
                          ])

        
        self.panel.SetSizer(main_sizer)
        self.Layout()
        
    def events(self):
        
        self.perfil.Bind(wx.EVT_BUTTON,self.mi_perfil)
        self.listarjuegos.Bind(wx.EVT_BUTTON,self.listar)
        self.recomendar.Bind(wx.EVT_BUTTON,self.recomendacion)
        self.efectividad.Bind(wx.EVT_BUTTON,self.efectivo)
        self.vernuevos.Bind(wx.EVT_BUTTON,self.nuevos)
        self.cerrar_sesion.Bind(wx.EVT_BUTTON,self.home)
        self.Bind(wx.EVT_CLOSE,self.home)
    
    
    def nuevos(self,e):
        usuario = self.usuario
#        print(usuario)
        rec = NuevosFrame(None,'Juegos Nuevos',usuario,self)
        rec.Center()
        rec.Show()
        self.Hide()
    
    def efectivo(self,e):
        mensaje = fun.eficiencia(con)
        wx.MessageBox(mensaje, "Efectividad" ,wx.OK | wx.ICON_INFORMATION)
        
    def mi_perfil(self,e):
        usuario = self.usuario
#        print(usuario)
        if fun.is_cold_user(con,self.usuario[0]):
            mensaje =  'Aun no registras ninguna preferencia'
            wx.MessageBox(mensaje, "Atencion" ,wx.OK | wx.ICON_INFORMATION)            
            
        else:
        
            per = PerfilFrame(None,'Mi perfil',usuario = usuario, ventana = self)
            per.Center()
            per.Show()
            self.Hide()
        
    def recomendacion(self,e):
        usuario = self.usuario
#        print(usuario)
        rec = RecomendacionesFrame(None,'Juegos Recomendados',usuario = usuario, ventana = self)
        rec.Center()
        rec.Show()
        self.Hide()
    
    def listar(self,e):
        usuario = self.usuario
        lista = ListaFrame(None, 'Lista de juegos',usuario,self)
        lista.Center()
        lista.Show()
        self.Hide()
    
    def home(self,e):
        self.Destroy()
        self.anterior.Show()    
        
    
###################### Ventana con la Lista de juegos##########################
class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    ''' TextEditMixin allows any column to be edited. '''
 
    #----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)
        
class ListaFrame(wx.Frame):
    def __init__(self,parent,title,user,LoginFrame):
        wx.Frame.__init__(self,parent,title = title,size=(1000,700))
        
        self.anterior = LoginFrame
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
Si desea ver el juego presione doble click en el enlace 
        '''
        self.info = wx.StaticText(self.panel,label = instruccion)
        self.guardar = wx.Button(self.panel, label = 'Guardar calificaciones')
        self.volver = wx.Button(self.panel, label = 'Volver')
        
        self.events()
        self.layout()
    
    def sesion(self,user):
        self.user = user
        self.cambios = {}
        juegos = fun.lista_juegos(con)
        calif = fun.calificados(self.user[0],con)
      

        for columna in list(juegos):
#            print(columna)
            self.list.AppendColumn(columna)

        self.list.AppendColumn('Calificacion')
        self.list.AppendColumn('Calificacion_Sistema')
#        print(len(columna))
        lista_calif = fun.cal_global(con)    
        for item in range(len(juegos)):
            aux = list(juegos.loc[item])
            
            row = []
            
            for i in aux:
                if i == None or i == 'None':
                    row += [""]
                else:
                    row += [i]
            
            try:
                puntaje = calif[aux[0]]
            except:
                puntaje = ""
            
            try:
                cal_g = lista_calif[aux[0]]
            except KeyError:
                    
                cal_g = ""
            
            row += [puntaje]
            row += [cal_g]
#            print(row,len(row))
#                puntaje = calif[juegos.loc[item][1]][0] 
#            if puntaje == None:
#                row += []
#            else:
#                row += [int(puntaje)]
            
#    
            self.list.Append(row)
   
    def layout(self):

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        lista_sizer = wx.BoxSizer(wx.HORIZONTAL)
        

        
        lista_sizer.Add(self.list,1,wx.ALL|wx.EXPAND,5)

        main_sizer.Add(self.info,0,wx.ALL,5)
        main_sizer.Add(lista_sizer,1,wx.ALL|wx.EXPAND)
        main_sizer.Add(self.guardar,0,wx.ALL|wx.CENTER,5)
        
        main_sizer.Add(self.volver,0,wx.ALL,5)

        self.panel.SetSizer(main_sizer)

    def events(self):
        self.list.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,self.edit_cal)
        self.list.Bind(wx.EVT_LIST_END_LABEL_EDIT,self.cambiar_cal)
        self.Bind(wx.EVT_CLOSE,self.home)
        self.guardar.Bind(wx.EVT_BUTTON,self.guardar_cal)
        self.volver.Bind(wx.EVT_BUTTON,self.home)
       
        
#    
    def edit_cal(self,e):
        col_id = e.GetColumn()
        index = e.GetIndex()
        
        if col_id == 7 or col_id == 8:
            self.openlink(index,col_id)
        
        if col_id != 10:
            e.Veto()
    
    def openlink(self,index,col_id):
        
        link = self.list.GetItemText(index,col_id)
        if link != "":
            wb.open(link, new=  2, autoraise=True)

        
        
            
    def cambiar_cal(self,e):
        
        try: 
            cambio = int(e.GetLabel())
            posibles = [1,2,3,4,5]
        
            juego = self.list.GetItemText(e.GetIndex(),0)

        
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
#            resul = fun.guardar_cambios(self.cambios,con,self.user[0])
            resul = fun.guardar_tabla(self.cambios,con,self.user[0])
            wx.MessageBox(resul, "Atencion" ,wx.OK | wx.ICON_INFORMATION)

        self.cambios = {}
        

    
    def home(self,e):
        self.Destroy()
        self.anterior.Show()
 
############################# Recomendaciones ################################ 

class RecomendacionesFrame(wx.Frame):
    def __init__(self,parent,title,usuario,ventana):
        wx.Frame.__init__(self,parent,title = title,size=(950,400))
        self.user = usuario
        
        self.sesion = ventana
        self.elementos()
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        texto = '''Estos son los 10 juegos más recomendados para ti
Si desea ver el juego presione doble click en el enlace '''
        self.info = wx.StaticText(self.panel,label = texto)
        self.list = EditableListCtrl(self.panel,style = wx.LC_REPORT)
        self.volver = wx.Button(self.panel, label = 'Volver') 
        self.tex = wx.StaticText(self.panel,label = 'Indique si le gustó la recomendacion')
        self.si = wx.Button(self.panel, label = 'Si')
        self.no = wx.Button(self.panel, label = 'No')
        self.listar()
        self.events()
        self.layout()
    
    def listar(self):
        column = list(fun.lista_juegos(con))
                
        if(fun.is_cold_user(con,self.user[0])):
            
            lista_calif = fun.cal_global(con)
            juegos = fun.listar_rec(con,fun.cold_user(con))
            
            for c in column:
                self.list.AppendColumn(c)
            self.list.AppendColumn('Calificacion_Sistema')
            
            for i in juegos:
               
                
                try:
                    cal_g = lista_calif[i[0]]
                except KeyError: 
                    cal_g = ""
                
                i += [cal_g]
                self.list.Append(i)
            

        else:
            
            lista_calif = fun.cal_global(con)
            juegos = rec_h.get_recomendations(con,self.user[0])
            juegos = fun.listar_rec(con,juegos)        
        
            for c in column:
                self.list.AppendColumn(c)
            self.list.AppendColumn('Calificacion_Sistema')   
            
            for i in juegos:
               
                try:
                    cal_g = lista_calif[i[0]]
                except KeyError:
                    
                    cal_g = ""
                
                i += [cal_g]
                self.list.Append(i)
            
    
   
    def layout(self):

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        lista_sizer = wx.BoxSizer(wx.HORIZONTAL)
        botones_sizer = wx.BoxSizer(wx.HORIZONTAL)

        
        botones_sizer.AddMany([(self.si,0,wx.ALL,5),
                               (self.no,0,wx.ALL,5)])
    
        lista_sizer.Add(self.list,1,wx.ALL|wx.EXPAND,5)

        main_sizer.Add(self.info,0,wx.ALL,5)
        main_sizer.Add(lista_sizer,1,wx.ALL|wx.EXPAND)
        main_sizer.Add(self.tex,0,wx.ALL,5)
        main_sizer.Add(botones_sizer,0,wx.ALL|wx.CENTER)
        main_sizer.Add(self.volver,0,wx.ALL,5)

        self.panel.SetSizer(main_sizer)

    def events(self):

        self.list.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,self.edit_cal)
        self.Bind(wx.EVT_CLOSE,self.home)
        self.volver.Bind(wx.EVT_BUTTON,self.home)
        self.si.Bind(wx.EVT_BUTTON,self.aciertos) 
        self.no.Bind(wx.EVT_BUTTON,self.aciertos) 
        
#    
    def aciertos(self,e):
        opcion = e.GetEventObject()
        self.si.Disable()
        self.no.Disable()
        opcion = opcion.GetLabel()
        fun.acierto(con,opcion)
        
    def edit_cal(self,e):
        col_id = e.GetColumn()
        index = e.GetIndex()
        
        if col_id == 7 or col_id == 8:
            self.openlink(index,col_id)
            e.Veto()
    
    def openlink(self,index,col_id):
        
        link = self.list.GetItemText(index,col_id)
        if link != "":
            wb.open(link, new=  2, autoraise=True)
    def home(self,e):
        self.Destroy()
        self.sesion.Show()

####################### Ventana de mi Perfil ################################
class PerfilFrame(wx.Frame):
    def __init__(self,parent,title,usuario,ventana):
        wx.Frame.__init__(self,parent,title = title,size=(800,300))
        self.user = usuario
        self.sesion = ventana
        self.elementos()
        
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        texto = 'Este es tu perfil de preferencias'
        self.info = wx.StaticText(self.panel,label = texto)
        self.list = wx.ListCtrl(self.panel,style = wx.LC_REPORT)
        self.volver = wx.Button(self.panel, label = 'Volver') 
        self.listar()
        self.events()
        self.layout()
    
    def listar(self):
        
        
        perfil = fun.perfil(con,self.user[0])    
        columnas = list(perfil)
        for c in columnas:
            self.list.AppendColumn(c)
        self.list.Append(perfil.iloc[0])
            
            
            
    
   
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

class NuevosFrame(wx.Frame):
    def __init__(self,parent,title,usuario,LoginFrame):
        wx.Frame.__init__(self,parent,title = title,size=(1000,700))
        
        self.anterior = LoginFrame
        self.elementos()
        self.sesion(usuario)
        
        
    def elementos(self):
        self.panel = wx.Panel(self)
        self.list = EditableListCtrl(self.panel,style= wx.LC_REPORT)
        instruccion = ''' Para asignar una calificación cambie el valor en en la columna 'Calificación' por un número entre 1 y 5 de la siguiente manera
        1 : Malo
        2 : Regular
        3 : Normal
        4 : Bueno
        5 : Muy bueno
Si desea ver el juego presione doble click en el enlace 
        '''
        self.info = wx.StaticText(self.panel,label = instruccion)
        self.guardar = wx.Button(self.panel, label = 'Guardar calificaciones')
        self.volver = wx.Button(self.panel, label = 'Volver')
        
        self.events()
        self.layout()
    
    def sesion(self,user):
        self.user = user
        self.cambios = {}
        columnas = list(fun.lista_juegos(con))
        juegos = fun.listar_nuevos(con,fun.traer_nuevos(con))
        
        calif = fun.calificados(self.user[0],con)
      

        for columna in columnas:
#            print(columna)
            self.list.AppendColumn(columna)

        self.list.AppendColumn('Calificacion')
        self.list.AppendColumn('Calificacion_Sistema')
#        print(len(columna))
        lista_calif = fun.cal_global(con)    
        for item in juegos:
            aux = item
            
            row = []
            
            for i in aux:
                if i == None or i == 'None':
                    row += [""]
                else:
                    row += [i]
            
            try:
                puntaje = calif[aux[0]]
            except:
                puntaje = ""
            
            try:
                cal_g = lista_calif[aux[0]]
            except KeyError:
                    
                cal_g = ""
            
            row += [puntaje]
            row += [cal_g]
#            print(row,len(row))
#                puntaje = calif[juegos.loc[item][1]][0] 
#            if puntaje == None:
#                row += []
#            else:
#                row += [int(puntaje)]
            
#    
            self.list.Append(row)
   
    def layout(self):

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        lista_sizer = wx.BoxSizer(wx.HORIZONTAL)
        

        
        lista_sizer.Add(self.list,1,wx.ALL|wx.EXPAND,5)

        main_sizer.Add(self.info,0,wx.ALL,5)
        main_sizer.Add(lista_sizer,1,wx.ALL|wx.EXPAND)
        main_sizer.Add(self.guardar,0,wx.ALL|wx.CENTER,5)
        
        main_sizer.Add(self.volver,0,wx.ALL,5)

        self.panel.SetSizer(main_sizer)

    def events(self):
        self.list.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,self.edit_cal)
        self.list.Bind(wx.EVT_LIST_END_LABEL_EDIT,self.cambiar_cal)
        self.Bind(wx.EVT_CLOSE,self.home)
        self.guardar.Bind(wx.EVT_BUTTON,self.guardar_cal)
        self.volver.Bind(wx.EVT_BUTTON,self.home)
       
        
#    
    def edit_cal(self,e):
        col_id = e.GetColumn()
        index = e.GetIndex()
        
        if col_id == 7 or col_id == 8:
            self.openlink(index,col_id)
        
        if col_id != 10:
            e.Veto()
    
    def openlink(self,index,col_id):
        
        link = self.list.GetItemText(index,col_id)
        if link != "":
            wb.open(link, new=  2, autoraise=True)

        
        
            
    def cambiar_cal(self,e):
        
        try: 
            cambio = int(e.GetLabel())
            posibles = [1,2,3,4,5]
        
            juego = self.list.GetItemText(e.GetIndex(),0)

        
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
#            resul = fun.guardar_cambios(self.cambios,con,self.user[0])
            resul = fun.guardar_tabla(self.cambios,con,self.user[0])
            wx.MessageBox(resul, "Atencion" ,wx.OK | wx.ICON_INFORMATION)

        self.cambios = {}
        

    
    def home(self,e):
        self.Destroy()
        self.anterior.Show()
try:
    if __name__ == '__main__':
        
        
        con = sql3.connect('recomen.db')
        fun.crearBD(con)
        
        
        
        app = wx.App()
        main = MainFrame(None, 'Ventana Principal')
        main.Center()
        main.Show()
        app.MainLoop()
        


    
finally:
    del app
    con.close()

