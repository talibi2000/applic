#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy_financial as npf
def calcul_emprunt(profil, capital, taux_interet, date_maturite, VALUE_DATE, periodicite):
    dff=pd.read_excel('C:\\Users\\HP\\Desktop\\Output\\TCI.xlsx', sheet_name='DATA')
    if periodicite == 'annuel':
        increment = relativedelta(months=12)
        frequence_paiement = 1
    elif periodicite == 'semestriel':
        increment = relativedelta(months=6)
        frequence_paiement = 2
    elif periodicite == 'trimestriel':
        increment = relativedelta(months=3)
        frequence_paiement = 4
    else : 
        increment = relativedelta(months=1)
        frequence_paiement = 12
    periodes = []
    interets = []
    discount_factors = []

    date_actuelle = VALUE_DATE
    nombre_paiements = int(((date_maturite - VALUE_DATE).days / 365) * frequence_paiement)
    taux_interet_periodique = (taux_interet / 100) / frequence_paiement
    table_amortissement = np.zeros((nombre_paiements, 6), dtype=object)
    if profil == 'ECHCONST' or profil == "A":
        taux_interet_periodique = (taux_interet / frequence_paiement) / 100
        annuite = npf.pmt(taux_interet_periodique, nombre_paiements, -capital)
        capital_rest = capital
        for j in range(nombre_paiements):
            periodes.append((date_actuelle - VALUE_DATE).days / 365)
            discount_factor = 1 / ((1 + taux_interet_periodique) ** ((date_actuelle - VALUE_DATE).days / 365))
            discount_factors.append(discount_factor)
            date_actuelle += increment
            interetss = capital_rest * taux_interet_periodique
            interets.append(interetss)
            amortissement = npf.ppmt(taux_interet_periodique, j + 1, nombre_paiements, -capital, when='end')
            capital_rest -= amortissement
            table_amortissement[j] = j + 1, pd.to_datetime(date_actuelle, format='%Y-%m-%d'), annuite, interetss, amortissement, capital_rest
        duree_vie_ponderee = sum([periodes[i] * interets[i] * discount_factors[i] for i in range(len(periodes))])                              / sum([interets[i] * discount_factors[i] for i in range(len(periodes))])
        df_amortissement = pd.DataFrame(table_amortissement, columns=['id', "Date d'échéance", 'annuité', 'Intérêts', 'Amortissement', 'capital rest'])
    elif profil=='LINEAIRE'or profil == "L":  
        taux_interet_periodique = (taux_interet/100) / frequence_paiement
        amortissement = capital / nombre_paiements
        capital_rest = capital
        for j in range(nombre_paiements):
            periodes.append((date_actuelle - VALUE_DATE).days / 365)     
            discount_factor = 1 / ((1 + taux_interet_periodique) ** ((date_actuelle - VALUE_DATE).days / 365))
            discount_factors.append(discount_factor)
            date_actuelle += increment
            interetss = capital_rest * taux_interet_periodique
            annuite = amortissement + interetss
            interets.append(interetss)
            capital_rest -= amortissement
            table_amortissement[j] = i+1, pd.to_datetime(date_actuelle, format='%Y-%m-%d'), annuite, interetss, amortissement, capital_rest
        duree_vie_ponderee = sum([periodes[i] * interets[i] * discount_factors[i] for i in range(len(periodes))])                              / sum([interets[i] * discount_factors[i] for i in range(len(periodes))])        
        df_amortissement = pd.DataFrame(table_amortissement, columns=['id',"Date d'échéance", 'annuité', 'Intérêts', 'Amortissement', 'capital rest'])

    else :
        taux_interet_periodique = (taux_interet/100) / frequence_paiement
        annuite = capital * taux_interet_periodique
        capital_rest = capital
        for j in range(nombre_paiements):
            periodes.append((date_actuelle - VALUE_DATE).days / 365)     
            discount_factor = 1 / ((1 + taux_interet_periodique) ** ((date_actuelle - VALUE_DATE).days / 365))
            discount_factors.append(discount_factor)
            interetss = capital_rest * taux_interet_periodique
            interets.append(interetss)
            if j == nombre_paiements - 1:
                amortissement = capital
            else:
                amortissement = 0
            annuite = interetss + amortissement
            date_actuelle += increment
            capital_rest -= amortissement
            table_amortissement[j] = i+1, pd.to_datetime(date_actuelle, format='%Y-%m-%d'), annuite, interetss, amortissement, capital_rest

        duree_vie_ponderee = sum([periodes[i] * interets[i] * discount_factors[i] for i in range(len(periodes))])                              / sum([interets[i] * discount_factors[i] for i in range(len(periodes))])        
        df_amortissement = pd.DataFrame(table_amortissement, columns=['id',"Date d'échéance", 'annuité', 'Intérêts', 'Amortissement', 'capital rest'])

    duree=round(duree_vie_ponderee)
    valeur1 = dff.loc[dff['Date'].dt.strftime('%Y-%m') == VALUE_DATE.strftime('%Y-%m'), duree]
    valeur2 = dff.loc[dff['Date'].dt.strftime('%Y-%m') == VALUE_DATE.strftime('%Y-%m'), duree+1]
    TSR1 = valeur1.iloc[0]
    TCI1 = valeur1.iloc[1]
    TSR2 = valeur2.iloc[0]
    TCI2 = valeur2.iloc[1]
    resultats = pd.DataFrame({'TSR1': [TSR1], 'TCI1': [TCI1],'TSR2': [TSR2], 'TCI2': [TCI2]})
    def linear_interpolation(x1, y1, x2, y2, x):
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    TSR_interpole = linear_interpolation(duree, TSR1, duree+1, TSR2, duree_vie_ponderee)
    TCI_interpole = linear_interpolation(duree, TCI1, duree+1, TCI2, duree_vie_ponderee)
    message_TSR = f"Le TSR interpolé pour une échéance de {duree_vie_ponderee} ans est {TSR_interpole:.6f}"
    message_TCI = f"Le TCI interpolé pour une échéance de {duree_vie_ponderee} ans est {TCI_interpole:.6f}"
    dureee = f"duree_vie_ponderee est  {duree_vie_ponderee}ans"
    return dureee,message_TCI,message_TSR, df_amortissement


# In[ ]:





# In[ ]:




