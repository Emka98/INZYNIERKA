import pandas as pd
import numpy as np
import os
from analiza_trendu.funkcja_potegowa import generatePlot
from analiza_trendu.odleglosc_euklidesowa import znajdz_najblizsze_drony
from Reszta.napedy import generuj_wykres_napedow_dronow
from Reszta.silniki import wykres_procentowy_producentow

#Set work dir
dir_work = os.getcwd()

#Get data
data_file = "Data/Lista dronów.xlsx"
data_file_path = os.path.join(dir_work,data_file)
df = pd.read_excel(data_file_path)

#Set dir for plots
dir_plots = "Wykresy"
dir_plots_path = os.path.join(dir_work,dir_plots)

#Prediction of parameters
prediction_years = 5.0
prediction_step = 1.0
year_of_prediction = 2030
ApprKMTokW = 0.7355

#Set Swet/Sref stosunek powierzchni omywanej Swet do powierzchni odniesienia Sw
Swet_Sref_ratio  =  2.5
Kmax = 17
oswalda = 0.8

# List names of data
# print(df.columns.tolist())

# Czas lotu w zależności od roku produkcji
e_reg_endurance_year = generatePlot(prediction_years, 
    prediction_step,
    'Rok zawarcia pierszego kontraktu\n[rok]',
    'Czas lotu\n[h]',
    'Czas lotu w zależności od roku produkcji', 
    dir_plots_path
)


# Czas lotu w zależności od wydłużenia
df['Wydłużenie płata\n[-]'] = (df['Rozpiętość skrzydeł\n[m]']**2) / df['Powierzchnia nośna\n[m^2]']
e_reg_endurance_aspectRatio = generatePlot(prediction_years, 
    prediction_step,
    'Czas lotu\n[h]',
    'Wydłużenie płata\n[-]', 
    'Czas lotu w zależności od wydłużenia', 
    dir_plots_path
)

# Czas lotu w zależności od obciążenia powierzchni
df['Obciązenie powierzchni\n[kg/m^2]'] = df['Masa stratowa\n[kg]'] / df['Powierzchnia nośna\n[m^2]']
e_reg_endurance_wingLoading = generatePlot(prediction_years,
    prediction_step,
    'Czas lotu\n[h]',
    'Obciązenie powierzchni\n[kg/m^2]',
    'Czas lotu w zależności od obciążenia powierzchni',
    dir_plots_path
)

# Czas lotu w zależności od obciążenia mocy
df['Obciązenie mocy\n[kg/kW]'] = df['Masa stratowa\n[kg]'] / (df['Moc silnika\n[KM]']*ApprKMTokW)
e_reg_endurance_powerLoading = generatePlot(prediction_years,
    prediction_step,
    'Czas lotu\n[h]',
    'Obciązenie mocy\n[kg/kW]',
    'Czas lotu w zależności od obciążenia mocy',
    dir_plots_path
)

# Zasięg [km] w zależności od roku produkcji
e_reg_range_year = generatePlot(prediction_years, 
    prediction_step,
    'Rok zawarcia pierszego kontraktu\n[rok]',
    'Zasięg SATA\n[km]',
    'Zasięg przy kominikacji SATA w zależności od roku produkcji', 
    dir_plots_path
)

# Zasięg [km] w zależności od wydłużenia
e_reg_range_aspectRatio = generatePlot(prediction_years, 
    prediction_step,
    'Zasięg SATA\n[km]',
    'Wydłużenie płata\n[-]',
    'Zasięg przy kominikacji SATA w zależności od wydłuzenia', 
    dir_plots_path
)

# Zasięg [km] w zależności od obciążenia powierzchni
e_reg_range_wingLoading = generatePlot(prediction_years, 
    prediction_step,
    'Zasięg SATA\n[km]',
    'Obciązenie powierzchni\n[kg/m^2]',
    'Zasięg przy kominikacji SATA w zależności od obciążenia powierzchni', 
    dir_plots_path
)

# Zasięg [km] w zależności od obciążenia mocy
e_reg_range_powerLoading = generatePlot(prediction_years, 
    prediction_step,
    'Zasięg SATA\n[km]',
    'Obciązenie mocy\n[kg/kW]',
    'Zasięg przy kominikacji SATA w zależności od obciążenia mocy', 
    dir_plots_path
)

# Masa własna/startowa w zależności od masy startowej
df['Masa własna/Masa stratowa'] = df['Masa własna\n[kg]'] / df['Masa stratowa\n[kg]']
e_reg_range_mass = generatePlot(prediction_years,
    prediction_step,
    'Masa stratowa\n[kg]',
    'Masa własna/Masa stratowa',
    'Masa własna/startowa w zależności od masy startowej',
    dir_plots_path
)

#Rozpiętosc skrzydeł zależnie od roku produkcji
e_reg_year_wingSpan = generatePlot(prediction_years, 
    prediction_step,
    'Rok zawarcia pierszego kontraktu\n[rok]',
    'Rozpiętość skrzydeł\n[m]',
    'Rozpiętość skrzydeł w zależności od roku produkcji', 
    dir_plots_path
)

# Masa własna w zależności od roku produkcji
e_reg_empty_weight_year = generatePlot(prediction_years, 
    prediction_step,
    'Rok zawarcia pierszego kontraktu\n[rok]',
    'Masa własna\n[kg]',
    'Czas lotu w zależności od roku produkcji', 
    dir_plots_path
)

# Prędkość przelotowa w zależności od roku produkcji
e_reg_crusingSpeed_year = generatePlot(prediction_years, 
    prediction_step,
    'Rok zawarcia pierszego kontraktu\n[rok]',
    'Prędkość przelotowa\n[km/h]',
    'Czas lotu w zależności od roku produkcji', 
    dir_plots_path
)

# Get data from plots endurance
endudence = e_reg_endurance_year(year_of_prediction)
wingSpan = e_reg_year_wingSpan(year_of_prediction)
empty_weight = e_reg_empty_weight_year(year_of_prediction)
crusingSpeed = e_reg_crusingSpeed_year(year_of_prediction)
result_endurance_aspectRatio = e_reg_endurance_aspectRatio(endudence)
result_endurance_wingLoading = e_reg_endurance_wingLoading(endudence)
result_endurance_powerLoading = e_reg_endurance_powerLoading(endudence)
range = e_reg_range_year(year_of_prediction)
result_range_aspectRatio = e_reg_range_aspectRatio(range)
result_range_wingLoading = e_reg_range_wingLoading(range)
result_range_powerLoading = e_reg_range_powerLoading(range)
avg_aspect_ratio = (result_endurance_aspectRatio + result_range_aspectRatio) / 2
avg_wing_loading = (result_endurance_wingLoading + result_range_wingLoading) / 2
avg_power_loading = (result_endurance_powerLoading + result_range_powerLoading) / 2

print()
print("#"*30)
print()

print("Wyniki z wykresów:")
print(f"Czas lotu: {endudence:.3f} h")
print(f"Rozpiętość skrzydeł: {wingSpan:.3f} m")
print(f"Zasięg: {range:.3f}km")
print(f"predkosc przelotowa: {crusingSpeed:.3f}km/h")
print(f"Masa własna: {empty_weight:.3f}kg")
print(f"Wydłużenie płata wykres z czasu lotu: {result_endurance_aspectRatio:.3f}")
print(f"Wydłużenie płata wykres z zasięgu: {result_range_aspectRatio:.3f}")
print(f"Obciążenie powierzchni wykres z czasu lotu: {result_endurance_wingLoading:.3f} kg/m^2")
print(f"Obciążenie powierzchni wykres z zasięgu: {result_range_wingLoading:.3f}kg/m^2")
print(f"Obciążenie mocy z czasu lotu: {result_endurance_powerLoading:.3f} kg/kW")
print(f"Obciążenie mocy z zasięgu: {result_range_powerLoading:.3f} kg/kW")
 
print()
print("#"*30)
print()

m1 = df['Masa stratowa\n[kg]'].min()
m2 = df['Masa stratowa\n[kg]'].max()
C = np.log10((e_reg_range_mass(m1)/e_reg_range_mass(m2)))/np.log10((m1/m2))
A = e_reg_range_mass(m1)/(m1**C)

print(f"{"Obliczenie współczynmików A i C"}")
print(f"x1 = {m1} y1 = {e_reg_range_mass(m1)}")
print(f"x2 = {m2} y2 = {e_reg_range_mass(m2)}")
print(f"C = {C}")
print(f"A = {A}")

print("Wyniki z wykresów:")
print(f"Czas lotu: {endudence:.0f} h")
print(f"Zasięg: {range:.3f}km")
print(f"Wydłużenie płata wykres z czasu lotu: {avg_aspect_ratio:.3f}")
print(f"Obciążenie powierzchni wykres z czasu lotu: {avg_wing_loading:.3f} kg/m^2")
print(f"Obciążenie mocy z czasu lotu: {avg_power_loading:.3f} kg/kW")

print()
print("#"*30)
print()

# Wywołanie zaimportowanej funkcji z osobnego pliku
najblizsze = znajdz_najblizsze_drony(
    df_drones=df,
    t_endurance=endudence,
    t_range=range,
    t_ar=avg_aspect_ratio,
    t_wl=avg_wing_loading,
    t_pl=avg_power_loading,
    year_of_prediction=year_of_prediction,
    top_n=5
)

print()
print("#"*30)
print()

# Generowanie wykresu kołowego dla napędów z Twojej tabeli 'df'
generuj_wykres_napedow_dronow(
    df=df,
    kolumna_naped="Napęd",
    plot_title="Udział rodzajów napędu w bazie dronów",
    save_place=dir_work,  # To automatycznie zapisze wykres w Calculations/Wykresy/wykres_napedow.png
)

print()
print("#"*30)
print()

#Biegunowa 
biegunowa = (np.pi * avg_aspect_ratio * oswalda) / (4* Kmax**2)
print(f"Cx0 = {biegunowa}")

#Masa startowa
wykres_procentowy_producentow(df,dir_plots_path)