#!pip install fuzzywuzzy
#!pip install python-Levenshtein

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from fuzzywuzzy import fuzz
import sqlite3 as sql3

##Nos conectamos a la base de datos
#con = sql3.connect('recomen.db')


def web_scrap(con,page_best,page_flip):
    ##Ingresamos las páginas máximas
    page1 = page_best
    page2 = page_flip
    
    ##Definimos una función que convertirá los títulos en solo caracteres para su comparación
    def comp(a_string):
      alphanumeric = ""
      for character in a_string:
        if character.isalnum():
          alphanumeric += character
      return alphanumeric
    
    ##Importamos los datos de la BD o creamos un Dataframe si no hay una
    try:
      games = pd.read_sql_query('SELECT * FROM juegos',con)
      games.loc[:,'Estado'] = False
    except:
      games = pd.DataFrame(columns=['Titulo','Publicador','Desarrollador','Genero','SinglePlayer','Multiplayer','Precio','Link1','Link2','Comments','Estado'])
    spec = ['Publicador','Desarrollador','Genero','Precio']
    
    ########################### BESTBUY #######################
    
    headers = {"User-agent":"Mozilla/5.0"}
    
    ##Creamos todas las paginas de Bestbuy indicadas
    bestbuys=[]
    for i in range(1,page1+1):
      page= 'https://www.bestbuy.com/site/playstation-4-ps4/playstation-4-ps4-video-games/pcmcat296300050018.c?cp='+str(i)+'&id=pcmcat296300050018&intl=nosplash'
      bestbuys.append(page)
    
    ##Buscamos los datos en las paginas de Bestbuy
    for page in bestbuys:
      pagex = requests.get(page, headers=headers)
      soupx = BeautifulSoup(pagex.content, 'html.parser')
      list_gamesx = soupx.find('ol', class_='sku-item-list')
      gamesx = list_gamesx.find_all('li', class_='sku-item')
      for game in gamesx:
        if (game.find(class_='product-image')):
          link = 'https://www.bestbuy.com'+game.find('a',class_='image-link')['href']+'&intl=nosplash'
        else:
          continue
        data = requests.get(link, headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        title = soup.find('div', class_='sku-title').text.replace(' - PlayStation 4','').replace('Standard Edition','').replace('PS4','').strip()
        ##Comprobamos que el juego no esté en la BD
        aux = -1
        for i in range(len(games)):
          t1 = comp(games.at[i,'Titulo']).lower()
          t2 = comp(title).lower()
          if fuzz.ratio(t1,t2)>99:
            aux = i
            break
        if (soup.find('div',class_='publisher product-data')):
          publisher = soup.find('div',class_='publisher product-data').findNext(class_='product-data-value body-copy').text
          publisher = publisher.split(sep=' ')[0].capitalize()
        else:
          publisher = ''
        if (soup.find('div',class_='specifications-accordion-wrapper').find(text=re.compile('Developer'))):
          developer = soup.find('div',class_='specifications-accordion-wrapper').find(text=re.compile('Developer')).findNext(class_='row-value col-xs-6 v-fw-regular').text
        else:
          developer = ''
        if (soup.find('div',class_='specifications-accordion-wrapper').find(text=re.compile('Genre'))):
          genre = soup.find('div',class_='specifications-accordion-wrapper').find(text=re.compile('Genre')).findNext(class_='row-value col-xs-6 v-fw-regular').text
        else:
          genre = ''
        if (soup.find('div',class_='specifications-accordion-wrapper').find(text=re.compile('Multiplayer'))):
          mode = soup.find('div',class_='specifications-accordion-wrapper').find(text=re.compile('Multiplayer')).findNext(class_='row-value col-xs-6 v-fw-regular').text
          if mode == 'Yes':
            multi = 1
            single = 0
          else:
            single = 1
            multi = 0
        else:
          single = 1
          multi = 0
        price = round(float(soup.find('div',class_='priceView-hero-price priceView-customer-price').find('span').text.replace('$','')),2)
        specx = [publisher,developer,genre,mode,price]
        ##Analizamos si el juego ya está, añadimos información faltante. Si no está, añadimos el juego.
        if aux==-1:
          games = games.append(pd.Series([title,publisher,developer,genre,single,multi,price,link,'','',True],index=games.columns),ignore_index=True)
        else:
          for i in range(4):
            if games.at[aux,spec[i]]=='':
              games.at[aux,spec[i]] = specx[i]
          games.at[aux,'Estado'] = True
    
    
    
    ########################### FLIPKART #######################
    
    ##Creamos todas las paginas de Flipkart indicadas
    flipkarts=[]
    for i in range(1,page2+1):
      page= 'https://www.flipkart.com/q/ps4-games?page='+str(i)
      flipkarts.append(page)
    
    ##Buscamos los datos en las paginas de Flipkart
    for page in flipkarts:
      pagex = requests.get(page).text
      soupx = BeautifulSoup(pagex, 'lxml')
      gamesx = soupx.find_all('a', class_='_2cLu-l')
      for game in gamesx:
        link = 'https://www.flipkart.com'+game['href']
        data = requests.get(link).text
        soup = BeautifulSoup(data, 'lxml')
        if (soup.find('td',class_='_3-wDH3 col col-3-12', text=('Title Name'))):
          title = soup.find('td',class_='_3-wDH3 col col-3-12', text=('Title Name')).findNext('li', class_='_3YhLQA').text.replace('Standard Edition','').replace('PS4','').strip()
        else:
          continue
        aux = -1
        for i in range(len(games)):
          t1 = comp(games.at[i,'Titulo']).lower()
          t2 = comp(title).lower()
          if fuzz.ratio(t1,t2)>99:
            aux = i
            break
        if (soup.find('table', class_='_3ENrHu').findNext(text=('Publisher'))):
          publisher = soup.find('table', class_='_3ENrHu').findNext(text=('Publisher')).findNext('li').text.strip()
          publisher = publisher.split(sep=' ')[0].capitalize()
        else:
          publisher = ''
        if (soup.find('table', class_='_3ENrHu').findNext(text=('Developer'))):
          developer = soup.find('table', class_='_3ENrHu').findNext(text=('Developer')).findNext('li').text.strip()
        else:
          developer = ''
        if (soup.find('table', class_='_3ENrHu').findNext(text=('Genre'))):
          genre = soup.find('table', class_='_3ENrHu').findNext(text=('Genre')).findNext('li').text.strip()
        else:
          genre = ''
        if (soup.find('table', class_='_3ENrHu').findNext(text=('Game Modes'))):
          mode = soup.find('table', class_='_3ENrHu').findNext(text=('Game Modes')).findNext('li').text.replace('-','').replace(' ','')
          if re.search('multiplayer',mode,re.I):
            multi = 1
            single = 0
          else:
            single = 1
            multi = 0
        else:
          single = 1
          multi = 0
        price = float(soup.find('div', class_='_1vC4OE _3qQ9m1').text.replace('₹','').replace(',',''))*(0.013)
        specx = [publisher,developer,genre,price]
        ##Analizamos si el juego ya está, añadimos información faltante y comentarios. Si no está, añadimos el juego.
        if aux==-1:
          games = games.append(pd.Series([title,publisher,developer,genre,single,multi,price,'',link,'',True],index=games.columns),ignore_index=True)
        else:
          for i in range(4):
            if games.at[aux,spec[i]]=='':
              games.at[aux,spec[i]] = specx[i]
              if games.at[aux,'Link1']!='':
                games.at[aux,'Comments'] = games.at[aux,'Comments']+'Único valor de característica para '+spec[i]+', valor faltante en bestbuy.com - '
            else:
              if specx[i] == '' and games.at[aux,'Link1']!='':
                games.at[aux,'Comments'] = games.at[aux,'Comments']+'Único valor de característica para '+spec[i]+', valor faltante en flipkart.com - '
              elif games.at[aux,spec[i]] != specx[i] and games.at[aux,'Link1']!='':
                games.at[aux,'Comments'].replace('Único valor de característica para '+spec[i]+', valor faltante en flipkart.com - ','')
                games.at[aux,'Comments'] = games.at[aux,'Comments']+'Diferencia de valor encontrado para Publicador. Se selecciona el valor '+str(games.at[aux,spec[i]])+'. Posibles valores: '+str(games.at[aux,spec[i]])+' en bestbuy.com y '+str(specx[i])+' en flipkart.com - '
          if games.at[aux,'Link2']=='':
            games.at[aux,'Link2'] = link
          games.at[aux,'Estado'] = True
    
    
    games.to_sql("juegos", con, if_exists="replace",index=False)
    con.commit()
    return 'Base de Datos de Juegos actualizada'
#    print (games.at[4,'Comments'])