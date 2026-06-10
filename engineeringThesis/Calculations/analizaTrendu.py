import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#Generat plots and save
def generatePlot(step_regression: float, degree: float, X_data_name: str, Y_data_name :str, plot_title: str, save_place: str) -> float: # type: ignore
    
    df[X_data_name] = pd.to_numeric(df[X_data_name], errors='coerce')
    df[Y_data_name] = pd.to_numeric(df[Y_data_name], errors='coerce')
    df_clean_range = df.dropna(subset=[X_data_name, Y_data_name])
    
    X_data = df_clean_range[X_data_name]
    Y_data = df_clean_range[Y_data_name]
    
    x = X_data.astype(float).values
    y = Y_data.astype(float).values
    
    coeffs = np.polyfit(x, y, degree)
    
    trend_func = np.poly1d(coeffs)
    
    start = x.min()
    end = x.max() + step_regression
    X_trend = np.linspace(start, end, 100)
    Y_trend = trend_func(X_trend)
    
    plt.figure(figsize=(10, 6))
    
    plt.scatter(x, y, color='blue')
    
    plt.plot(X_trend, Y_trend, color='red', linestyle='--', linewidth=2, label=f'Linia trendu: {trend_func}')
        
    plt.title(plot_title, fontsize=14)
    plt.xlabel(X_data.name)
    plt.ylabel(Y_data.name)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    safe_title = plot_title.replace("/", "_").replace("\\", "_")
    plt.savefig(os.path.join(save_place, safe_title), dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()
    
    return  trend_func

#Get data
dir_work = os.getcwd()
data_file = "Lista dronów.xlsx"
data_file_path = os.path.join(dir_work,data_file)
df = pd.read_excel(data_file_path)

#Prediction of parameters
prediction_years = 5.0
prediction_step = 1.0
year_of_prediction = 2030
ApprKMTokW = 0.7355

# data cleaning
exclude = ['Nazwa', 
           'Kraj produkcji', 
           'Firma', 
           'Profil skrzydła', 
           'Notatka', 
           'Ref1', 
           'Ref2', 
           'Ref3', 
           'Ref4', 
           'Ref5']

for data in df:
    if not data in exclude:
        df[data] = pd.to_numeric(df[data], errors='coerce')

# List names of data
# print(df.columns.tolist())
# ['Nazwa', 
# 'Kraj produkcji', 
# 'Firma', 
# 'Zasięg SATA\n[km]', 
# 'Zasięg LOS\n[km]', 
# 'Moc silnika\n[KM]', 
# 'Typ silnika', 'Napęd', 
# 'Silnik', 
# 'Długość\n[m]', 
# 'Wysokość\n[m]', 
# 'Rozpiętość skrzydeł\n[m]', 
# 'Masa stratowa\n[kg]', 
# 'Masa własna\n[kg]', 
# 'Ładowność\n[kg]', 
# 'Powierzchnia nośna\n[m^2]', 
# 'Pierwszy pototyp\n[rok]', 
# 'Rok zawarcia pierszego kontraktu\n[rok]', 
# 'Prędkość przelotowa\n[km/h]', 
# 'Prędkość maxymalna\n[km/h]', 
# 'Czas lotu\n[h]', 
# 'Pułap\n[m]', 
# 'Profil skrzydła', 
# 'Notatka']

# Czas lotu w zależności od roku produkcji
e_reg_endurance_year = generatePlot(prediction_years, 
    prediction_step,
    'Rok zawarcia pierszego kontraktu\n[rok]',
    'Czas lotu\n[h]',
    'Czas lotu w zależności od roku produkcji', 
    dir_work
)

# Czas lotu w zależności od wydłużenia
df['Wydłużenie płata\n[-]'] = (df['Rozpiętość skrzydeł\n[m]']**2) / df['Powierzchnia nośna\n[m^2]']
e_reg_endurance_aspectRatio = generatePlot(prediction_years, 
    prediction_step,
    'Czas lotu\n[h]',
    'Wydłużenie płata\n[-]', 
    'Czas lotu w zależności od wydłużenia', 
    dir_work
)

# Czas lotu w zależności od obciążenia powierzchni
df['Obciązenie powierzchni\n[kg/m^2]'] = df['Masa stratowa\n[kg]'] / df['Powierzchnia nośna\n[m^2]']
e_reg_endurance_wingLoading = generatePlot(prediction_years,
    prediction_step,
    'Czas lotu\n[h]',
    'Obciązenie powierzchni\n[kg/m^2]',
    'Czas lotu w zależności od obciążenia powierzchni',
    dir_work
)

# Czas lotu w zależności od obciążenia mocy
df['Obciązenie mocy\n[kg/kW]'] = df['Masa stratowa\n[kg]'] / (df['Moc silnika\n[KM]']*ApprKMTokW)
e_reg_endurance_powerLoading = generatePlot(prediction_years,
    prediction_step,
    'Czas lotu\n[h]',
    'Obciązenie mocy\n[kg/kW]',
    'Czas lotu w zależności od obciążenia mocy',
    dir_work
)

# Zasięg [km] w zależności od roku produkcji
e_reg_range_year = generatePlot(prediction_years, 
    prediction_step,
    'Rok zawarcia pierszego kontraktu\n[rok]',
    'Zasięg SATA\n[km]',
    'Zasięg przy kominikacji SATA w zależności od roku produkcji', 
    dir_work
)

# Zasięg [km] w zależności od wydłużenia
e_reg_range_aspectRatio = generatePlot(prediction_years, 
    prediction_step,
    'Zasięg SATA\n[km]',
    'Wydłużenie płata\n[-]',
    'Zasięg przy kominikacji SATA w zależności od wydłuzenia', 
    dir_work
)

# Zasięg [km] w zależności od obciążenia powierzchni
e_reg_range_wingLoading = generatePlot(prediction_years, 
    prediction_step,
    'Zasięg SATA\n[km]',
    'Obciązenie powierzchni\n[kg/m^2]',
    'Zasięg przy kominikacji SATA w zależności od obciążenia powierzchni', 
    dir_work
)

# Zasięg [km] w zależności od obciążenia mocy
e_reg_range_powerLoading = generatePlot(prediction_years, 
    prediction_step,
    'Zasięg SATA\n[km]',
    'Obciązenie mocy\n[kg/kW]',
    'Zasięg przy kominikacji SATA w zależności od obciążenia mocy', 
    dir_work
)

# Masa własna/startowa w zależności od masy startowej
df['Masa własna/Masa stratowa'] = df['Masa własna\n[kg]'] / df['Masa stratowa\n[kg]']
e_reg_range_mass = generatePlot(prediction_years,
    prediction_step,
    'Masa stratowa\n[kg]',
    'Masa własna/Masa stratowa',
    'Masa własna/startowa w zależności od masy startowej',
    dir_work
)

# Get data from plots endurance
endudence = e_reg_endurance_year(year_of_prediction)
result_endurance_aspectRatio = e_reg_endurance_aspectRatio(endudence)
result_endurance_wingLoading = e_reg_endurance_wingLoading(endudence)
result_endurance_powerLoading = e_reg_endurance_powerLoading(endudence)

print("Wyniki z wykresów w zależności o czasu lotu")
print(f"Czas lotu: {endudence:.3f} h")
print(f"Wydłużenie płata: {result_endurance_aspectRatio:.3f}")
print(f"Obciążenie powierzchni: {result_endurance_wingLoading:.3f} kg/m^2")
print(f"Obciążenie mocy: {result_endurance_powerLoading:.3f} kg/kW")

print("#"*30)
print("#"*30)

range = e_reg_range_year(year_of_prediction)
result_range_aspectRatio = e_reg_range_aspectRatio(range)
result_range_wingLoading = e_reg_range_wingLoading(range)
result_range_powerLoading = e_reg_range_powerLoading(range)

print(f"Zasięg: {range:.3f}km")
print(f"Wydłużenie płata: {result_range_aspectRatio:.3f}")
print(f"Obciążenie powierzchni: {result_endurance_wingLoading:.3f}kg/m^2")
print(f"Obciążenie mocy: {result_endurance_powerLoading:.3f}kg/kW")

print("#"*30)
print("#"*30)

m1, m2 = pd.Series(df['Masa stratowa\n[kg]'].unique()).sample(n=2).sort_values().values
print(f"{m1} {e_reg_range_mass(m1)}")
print(f"{m2} {e_reg_range_mass(m2)}")
print(f"C = {np.log10(e_reg_range_mass(m1))/e_reg_range_mass(m2)/np.log10(m1/m2)}")



