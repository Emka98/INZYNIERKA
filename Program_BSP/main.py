import os
import pandas as pd
from analiza_trendu.analiza_trendu import make_prediction
from biegunowaAnallityczna.biegunowa import calbiegunowa
from obliczeniaMasy.masscalculator import masscal
#Set work dir
dir_work = os.getcwd()

#Get data
data_file = "Data/Lista dronów.xlsx"
data_file_path = os.path.join(dir_work,data_file)
df = pd.read_excel(data_file_path)

#Set dir for plots
dir_plots = "Wykresy"
dir_plots_path = os.path.join(dir_work,dir_plots)

#Place for results
dir_result = "Results"
dir_result = os.path.join(dir_work,dir_result)

#Place for results alizy trendów
analize_trendu_filename = "AnalizaTrendow.txt"
result = os.path.join(dir_result,analize_trendu_filename)

#Prediction of parameters
prediction_year = 2030

#Biegunowa analityczna
AR = 16
Kmax = 32

make_prediction(df, prediction_year, dir_plots_path, result)
calbiegunowa(AR, Kmax, result)
mass_filename = "mass.txt"
mass_filename_result = os.path.join(dir_result,mass_filename)
masscal(mass_filename_result)
