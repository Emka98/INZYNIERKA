import os
import pandas as pd
from analiza_trendu.funkcja_potegowa import generate_plot
from ogolne.save_result import save_text_to_file
from analiza_trendu.wspolczyniki_A_C import calculate_indicator_A_C
from analiza_trendu.odleglosc_euklidesowa import odleglosc_euklidesowa

def make_prediction(df: pd.DataFrame, 
                    prediction_year,
                    dir_plots_path, 
                    path_result):
    
    text = f"Wyniki predykcji danych na rok {prediction_year}:\n"
    
    analize_trendu_result = os.path.join(path_result, "rezult_from_plots.txt")
    
    # Czas lotu w zależności od roku produkcji
    e_reg_endurance_year = generate_plot(
        df, 
        "Rok zawarcia pierszego kontraktu\n[rok]",
        "Czas lotu\n[h]",
        "Czas lotu w zależności od roku produkcji",
        dir_plots_path,
    )
    pred_endurance = e_reg_endurance_year(prediction_year)
    text += f"Czas lotu: {pred_endurance:0.3f} h\n"
    
    # Zasięg [km] w zależności od roku produkcji
    e_reg_range_year = generate_plot(
        df, 
        'Rok zawarcia pierszego kontraktu\n[rok]',
        'Zasięg SATA\n[km]',
        'Zasięg przy kominikacji SATA w zależności od roku produkcji', 
        dir_plots_path
    )
    pred_range = e_reg_range_year(prediction_year)
    text += f"Zasięg SATA: {pred_range:0.3f} km\n"
    
    # #Rozpiętosc skrzydeł zależnie od roku produkcji
    e_reg_wingSpan_year = generate_plot(
        df, 
        'Rok zawarcia pierszego kontraktu\n[rok]',
        'Rozpiętość skrzydeł\n[m]',
        'Rozpiętość skrzydeł w zależności od roku produkcji', 
        dir_plots_path
    )
    text += f"Rozpiętość skrzydeł: {e_reg_wingSpan_year(prediction_year):0.3f} m\n"

    # Masa własna w zależności od roku produkcji
    e_reg_empty_weight_year = generate_plot(
        df, 
        'Rok zawarcia pierszego kontraktu\n[rok]',
        'Masa własna\n[kg]',
        'Masa własna w zależności od roku produkcji', 
        dir_plots_path
    )
    text += f"Masa własna: {e_reg_empty_weight_year(prediction_year):0.3f} kg\n"
    
    # # Prędkość przelotowa w zależności od roku produkcji
    e_reg_crusingSpeed_year = generate_plot(
        df, 
        'Rok zawarcia pierszego kontraktu\n[rok]',
        'Prędkość przelotowa\n[km/h]',
        'Prędkość w zależności od roku produkcji', 
        dir_plots_path
    )
    text += f"Prędkość przelotowa: {e_reg_crusingSpeed_year(prediction_year):0.3f} km/h\n"

    # # Czas lotu w zależności od wydłużenia
    df['Wydłużenie płata\n[-]'] = (df['Rozpiętość skrzydeł\n[m]']**2) / df['Powierzchnia nośna\n[m^2]']
    e_reg_endurance_aspectRatio = generate_plot(
        df, 
        'Czas lotu\n[h]',
        'Wydłużenie płata\n[-]', 
        'Czas lotu w zależności od wydłużenia', 
        dir_plots_path
    )
    pred_ar = e_reg_endurance_aspectRatio(pred_endurance)
    text += f"Wydłużenie pałata: {pred_ar:0.3f}\n"

    # # Czas lotu w zależności od obciążenia powierzchni
    df['Obciązenie powierzchni\n[kg/m^2]'] = df['Masa stratowa\n[kg]'] / df['Powierzchnia nośna\n[m^2]']
    e_reg_endurance_wingLoading = generate_plot(
        df, 
        'Czas lotu\n[h]',
        'Obciązenie powierzchni\n[kg/m^2]',
        'Czas lotu w zależności od obciążenia powierzchni',
        dir_plots_path
    )
    pred_wl = e_reg_endurance_wingLoading(pred_endurance)
    text += f"Obciązenie powierzchni: {pred_wl:0.3f} kg/m^2\n"

    # # Czas lotu w zależności od obciążenia mocy
    # UWAGA: W poprawionej odległości euklidesowej masz kolumnę 'Moc silnika\n[KM]' * 0.7355, 
    # upewnij się, że nazwy kolumn w pliku Excel są spójne z poniższą (kW vs KM).
    df['Obciązenie mocy\n[kg/kW]'] = df['Masa stratowa\n[kg]'] / (df['Moc silnika\n[kW]'])
    e_reg_endurance_powerLoading = generate_plot(
        df,
        'Czas lotu\n[h]',
        'Obciązenie mocy\n[kg/kW]',
        'Czas lotu w zależności od obciążenia mocy',
        dir_plots_path
    )
    pred_pl = e_reg_endurance_powerLoading(pred_endurance)
    text += f"Obciązenie mocy: {pred_pl:0.3f} kg/kW\n"

    # # Masa własna/startowa w zależności od masy startowej
    df['Masa własna/Masa stratowa'] = df['Masa własna\n[kg]'] / df['Masa stratowa\n[kg]']
    e_reg_range_mass = generate_plot(
        df, 
        'Masa stratowa\n[kg]',
        'Masa własna/Masa stratowa',
        'Masa własna/startowa w zależności od masy startowej',
        dir_plots_path
    )
           
    # Zapis podstawowego raportu z trendów
    save_text_to_file(text, analize_trendu_result)
    
    # Obliczanie wskaźników A i C
    calculate_indicator_A_C(df, e_reg_range_mass, path_result)
    
    path_similarity_result = os.path.join(path_result, "najbardziej_zblizone_modele.txt")
    
    odleglosc_euklidesowa(
        df,
        pred_endurance,
        pred_range,
        pred_ar,
        pred_wl,
        pred_pl,
        prediction_year,
        5,
        path_similarity_result
    )
    
    excel_result_path = os.path.join(path_result, f"wyniki_analizy_{prediction_year}.xlsx")
    df.to_excel(excel_result_path, index=False)
    print(f"Dane z nowymi kolumnami zostały zapisane w: {excel_result_path}")
    
    return 0