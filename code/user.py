import fred_matt_merman as fmm
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

#CASE STUDY (Money, Banking, & Finance > Exchange Rates)
ID_CATEGORY = 94 #Daily Rates
ID_SERIES = ["DEXBZUS", "DEXCAUS", "DEXCHUS"]
DB = "./database.db"

#costante usata per selezionare il numero di valori da graficare.
#è importante che sia negativa! In quanto sono graficati gli ultimi dati
#è usato anche nel calcolo della varinza tra serie, nel case study
NUMBER_VALUE = -50

grid_color = "grey"
label_color = "white"
plot_color="green"
title_fontsize = 30
axes_fontsize = 20
text_pad = 20
context = {'axes.edgecolor':'grey',
           'axes.facecolor':'black',
           'font.family':'sans-serif', 
           'figure.facecolor':'black', 
           'figure.edgecolor':'black',
           'xtick.color':'white', 
           'ytick.color':'white', 
           'savefig.transparent':'True'}

def get_observations(list_series):

    if isinstance(list_series, list) and len(list_series) == 3:

        df = fmm.get_db(DB, "observations", list_series[0])
        observations_1 = df['date'].tolist()

        observations_2 = df['value'].tolist()
        observations_2 = fmm.convert_string_float(observations_2)

        df = fmm.get_db(DB, "observations", list_series[1])
        observations_3 = df['value'].tolist()
        observations_3 = fmm.convert_string_float(observations_3)

        df = fmm.get_db(DB, "observations", list_series[2])
        observations_4 = df['value'].tolist()
        observations_4 = fmm.convert_string_float(observations_4)

        return (observations_1, observations_2, observations_3, observations_4)
    
    else:
        
        df = fmm.get_db(DB, "observations", list_series)
        observations_1 = df['date'].tolist()
        observations_2 = df['value'].tolist()
        observations_2 = fmm.convert_string_float(observations_2)
        
        return (observations_1, observations_2)
        
def display_observations(list_series):
    
    observations = get_observations(list_series)

    with plt.rc_context(context):
  
        plt.figure(figsize=(21,9))
        
        plt.title("Observations", color=label_color, pad=text_pad, fontsize=title_fontsize)
        plt.grid(color=grid_color)
        
        plt.plot(observations[0][NUMBER_VALUE:], observations[1][NUMBER_VALUE:], color="blue", label="ID: " + list_series[0])
        plt.plot(observations[0][NUMBER_VALUE:], observations[2][NUMBER_VALUE:], color="green", label="ID: " + list_series[1])
        plt.plot(observations[0][NUMBER_VALUE:], observations[3][NUMBER_VALUE:], color="orange", label="ID: " + list_series[2])
    
        plt.ylabel("value", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        plt.xlabel("date", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        plt.xticks(rotation=45)
        
        #mp.savefig('chart_observation.png')
        
        legend = plt.legend(fontsize=text_pad)
        plt.setp(legend.get_texts(), color=label_color)
    
        return plt
    
#Calcolare la covarianza
def covariance(list_series):
    
    observations = get_observations(list_series)
    
    covariance = np.cov(observations[1][NUMBER_VALUE:], observations[2][NUMBER_VALUE:])[0][1]
    print("Cov(" + list_series[0] + "," + list_series[1] + ") = " + str(covariance))
    
    covariance = np.cov(observations[3][NUMBER_VALUE:], observations[2][NUMBER_VALUE:])[0][1]
    print("Cov(" + list_series[2] + "," + list_series[1] + ") = " + str(covariance))
    
    covariance = np.cov(observations[1][NUMBER_VALUE:], observations[3][NUMBER_VALUE:])[0][1]
    print("Cov(" + list_series[0] + "," + list_series[2] + ") = " + str(covariance))
    
#Calcolare e graficare su un solo grafico per ogni serie
#la serie delle differenze prime (𝑠𝑖+1 −𝑠𝑖) 
def display_first_diff(id):
    
    observations = get_observations(id)
    
    difference_array = []
    for index in range(len(observations[1]) - 1):
        
        difference = observations[1][index + 1] - observations[1][index]
        difference_array.append(difference)
    
    return fmm.display(observations[0], difference_array, "First differences", id, "date")

#Calcolare e graficare su un solo grafico per ogni serie la serie delle 
#differenze prime percentuali 𝑠𝑖+1−𝑠𝑖. (fate attenzione agli ∞)
def display_first_diff_perc(id):

    observations = get_observations(id)
    
    ratio_array = []
    for index in range(len(observations[1]) - 1):
        
        if observations[1][index] == 0: observations[1][index] = 0.1
        difference = (observations[1][index + 1] - observations[1][index])/observations[1][index]
        ratio_array.append(difference)
    
    return fmm.display(observations[0], ratio_array, "First differences percentages", id, "date")

def estimate_coef(x, y):
    
    # number of observations/points
    n = np.size(x)
 
    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)
 
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
 
    return (b_0, b_1)
    
#Per ogni serie calcolare la retta di regressione
def display_linear_regression(id):
        
    df = fmm.get_db(DB, "observations", id)
    
    #converte la sequenza di float in int
    for index in range(len(df)):
        value = df['value'][index]
        if value == ".": 
            df.iat[index, 2] = 0
 
    df['value'] = pd.to_numeric(df['value']).astype(int)
    df['day'] = range(1, len(df) + 1)
    
    b = estimate_coef(df['day'], df['value'])
            
    with plt.rc_context(context):
  
        plt.figure(figsize=(21,9))
        
        plt.title("Linear regression", color=label_color, pad=text_pad, fontsize=title_fontsize)
        plt.grid(color=grid_color)
        
        plt.scatter(df['day'].tolist()[NUMBER_VALUE:], df['value'].tolist()[NUMBER_VALUE:], color = "m", marker = "o", s = 30, label="ID: " + id)

        # predicted response vector
        y_pred = b[0] + b[1]*df['day']

        # plotting the regression line
        plt.plot(df['day'].tolist()[NUMBER_VALUE:], y_pred.tolist()[NUMBER_VALUE:], color = "b")

        plt.ylabel("value", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        plt.xlabel("day", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        plt.xticks(rotation=45)
        
        #mp.savefig('chart_observation.png')
        
        legend = plt.legend(fontsize=text_pad)
        plt.setp(legend.get_texts(), color=label_color)
    
        return plt
    
fmm.create_db(DB)

#Scaricare  tutte le serie  da  una  singola categoria (in realtà ne sono sufficienti 3)
#potrebbe essere necessario creare un db, con fmm.create_db(DB)
fmm.insert_db(DB, ID_CATEGORY, "series", True)

#Per vedere tutte le seriess scaricate, e quindi anche quelle relative a Daily Rates:
df = fmm.get_db(DB, "seriess", None)

#Scaricare tutte le osservabili per 3 seriess scelte
for index in range(len(ID_SERIES)):
    fmm.insert_db(DB, ID_SERIES[index], "observation", True)

#Graficare le 3 serie su un solo grafico 
plt = display_observations(ID_SERIES)
#plt.show()

#df = fmm.get_db(DB, "observations", None)
#print(df)

#df = fmm.get_db(DB, "seriess", None)
#print(df)

#a = fmm.download_insert_tree_category(DB, "11", "category_children", False, [])
#print(a)

#Calcolare la covarianza (attenzione ai nan!) 
covariance(ID_SERIES)

#Serie delle differenze prime, differenze prime percentuali e retta di regressione
for index in range(len(ID_SERIES)):
    plt = display_first_diff(ID_SERIES[index])
    #plt.show()
    plt = display_first_diff_perc(ID_SERIES[index])
    #plt.show()
    plt = display_linear_regression(ID_SERIES[index])
    #plt.show()