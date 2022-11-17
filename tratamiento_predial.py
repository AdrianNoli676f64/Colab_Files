#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import datetime as dt
import numpy as np
import warnings
warnings.filterwarnings("ignore")


# In[1]:


def definir_temporalidad():
    global df
    global year
    df = uwu[['fcobro', 'ctapredial', 'impuesto', 'total', 'perini', 'pcancl', 'perfin', 'mes', 'year']]  ### Indicar columnas
    print("Escribe 'By_Year' para tratar el año completo o 'By_Month' para analizar solo un mes")
    pregunta = input("Elige una opción: ")
    #### Elegir y filtrar opciones
    if pregunta == 'By_Year':
        print("Escribe el año con numero entero")
        year = int((input("Año para analizar: ")))
        df = df.loc[(df['year'] == (year)) & (df['pcancl'] != 'C') & (df['pcancl'] != '0')].reset_index(drop=True)
        print('El nombre del DataFrame es df')
        return df
    elif pregunta == 'By_Month':
        print("Escribe el año y mes con numero entero")
        year = int((input("Año para analizar: ")))
        month = int((input("Mes para analizar: ")))
        df = df.loc[(df['year'] == (year)) & (df['mes'] == (month)) & (df['pcancl'] != 'C') & (df['pcancl'] != '0')].reset_index(drop=True)
        print('El nombre del DataFrame es df')
        return df
    else:
        print(f""+pregunta+" no es una respuesta válida, escribe (By_Year/By_Month)")
        return definir_temporalidad()


# In[2]:


def add_bimestres(df):
    print("################################################################")
    global pregunta2
    pregunta2 = input("Añadir bimestres y pagos bimestrales? (Si/No): ")
    if pregunta2 == 'Si':
        inicio = list()
        for periodo in df['perini']:
            i = str(periodo)[4:]
            if i == '':
                i = 1
            inicio.append(int(i))
        final = list()
        for periodo in df['perfin']:
            f = str(periodo)[4:]
            if f == '':
                f = 1
            final.append(int(f))
        bimestres = list()
        for i in range(0,len(inicio)):
            bimestre = 0
            if inicio[i] == final[i]:
                bimestre = 1
            else:
                bimestre = (final[i] - inicio[i]) + 1
        bimestres.append(bimestre)
        df['bimestres'] = bimestres
        df['pagos'] = 1
        df['imp'] = (df['impuesto']/df['bimestres'])
        df=df.loc[(df['bimestres'] > 0)]
        print('Añadido, los casos donde el perfin sea menor al perini fueron eliminados')
    elif pregunta2 == 'No':
        print("Weno UwU")
        pass
    else:
        print(f""+pregunta2+" no es una opción válida")
        add_bimestres(df)
    return df


# In[3]:


def add_rangos(df):
    print("################################################################")
    pregunta3 = input("Añadir rangos de pago? (Si/No): ")
    if pregunta3 == 'Si' and pregunta2 == 'Si':
        rg = pd.read_excel("/content/drive/MyDrive/Predial/Entrada/rangos_predial.xlsx")
        rg = rg.loc[(rg['year']==year)]
        range_ = rg['Rango'].to_list()
        tarifa = rg['Tarifa'].to_list()
        conditionlist = [
            (df['imp'] <= tarifa[0]),
            (df['imp'] > tarifa[0]) & (df['imp'] <= tarifa[1]), (df['imp'] > tarifa[1]) & (df['imp'] <= tarifa[2]),
            (df['imp'] > tarifa[2]) & (df['imp'] <= tarifa[3]), (df['imp'] > tarifa[3]) & (df['imp'] <= tarifa[4]),
            (df['imp'] > tarifa[4]) & (df['imp'] <= tarifa[5]), (df['imp'] > tarifa[5]) & (df['imp'] <= tarifa[6]),
            (df['imp'] > tarifa[6]) & (df['imp'] <= tarifa[7]), (df['imp'] > tarifa[7]) & (df['imp'] <= tarifa[8]),
            (df['imp'] > tarifa[8]) & (df['imp'] <= tarifa[9]), (df['imp'] > tarifa[9]) & (df['imp'] <= tarifa[10]),
            (df['imp'] > tarifa[10]) & (df['imp'] <= tarifa[11]), (df['imp'] > tarifa[11]) & (df['imp'] <= tarifa[12]),
            (df['imp'] > tarifa[12]) & (df['imp'] <= tarifa[13]), (df['imp'] > tarifa[13]) & (df['imp'] <= tarifa[14]),
            (df['imp'] > tarifa[14])
        ]
        df['rango'] = np.select(conditionlist, range_, default='')
        print("Rangos añadidos basándose en el pago bimestral por cuenta")
    elif pregunta3 == 'Si' and pregunta2 == 'No':
        print('No se añadieron bimestres e impuestos bimestrales')
        pass
    elif pregunta3 == 'No':
        print("Weno UwU")
        pass
    else:
        print(f""+pregunta3+" no es una opción válida")
        add_rangos(df)
    return df


# In[4]:


def agrupar(df):
    global df_group
    global pregunta4
    print("################################################################")
    pregunta4 = input("Agrupar por cuentas prediales? (Si/No): ")
    find_column = 'rango' in df.columns
    if pregunta4 == 'Si'and find_column == True:
        df_group = df.groupby(['ctapredial', 'rango'], as_index = False).sum()
        df_group['imp'] = df_group['imp']/df_group['bimestres']
    elif pregunta4 == 'Si'and find_column == False:
        df_group = df.groupby(['ctapredial'], as_index = False).sum()
        df_group['imp'] = df_group['imp']/df_group['bimestres']
    elif pregunta4 == 'No':
        print('Weno UnU')
        pass
    else:
        print(f""+pregunta4+" no es una opción válida")
        agrupar(df)
    return df_group


# In[ ]:




