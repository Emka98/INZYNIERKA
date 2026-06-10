import pandas as pd
import numpy as np
# Import zewnętrznej funkcji do zapisu zgodnie z Twoim wymaganiem
from ogolne.save_result import save_text_to_file

def odleglosc_euklidesowa(df: pd.DataFrame,
                         t_endurance,
                         t_range,
                         t_ar, 
                         t_wl, 
                         t_pl, 
                         year_of_prediction, 
                         top_n,
                         output_filename="wynik_prognozy.txt"): # Dodano parametr z domyślną nazwą pliku

    # Praca na kopii ze względów bezpieczeństwa
    working_df = df.copy()
    
    # Definiujemy dokładne nazwy kolumn z pliku Excel
    col_endurance = 'Czas lotu\n[h]'
    col_range = 'Zasięg SATA\n[km]'
    col_ar = 'Wydłużenie płata\n[-]'
    col_wl = 'Obciązenie powierzchni\n[kg/m^2]'
    col_pl = 'Obciązenie mocy\n[kg/kW]'
    
    # KROK 1: Wyliczamy kolumny na podstawie innych danych (naprawiona kolejność)
    working_df[col_ar] = (working_df['Rozpiętość skrzydeł\n[m]']**2) / working_df['Powierzchnia nośna\n[m^2]']
    working_df[col_wl] = working_df['Masa stratowa\n[kg]'] / working_df['Powierzchnia nośna\n[m^2]']
    working_df[col_pl] = working_df['Masa stratowa\n[kg]'] / (working_df['Moc silnika\n[kW]'])
    
    # Definiujemy mapowanie naszych cech (kolumny w DF vs. wartości docelowe)
    feature_mapping = {
        col_endurance: t_endurance,
        col_range: t_range,
        col_ar: t_ar,
        col_wl: t_wl,
        col_pl: t_pl
    }
    
    # KROK 2: Usuwamy wiersze z brakami danych (NaN) w kluczowych kolumnach
    working_df = working_df.dropna(subset=list(feature_mapping.keys()))
    
    if working_df.empty:
        error_msg = "Błąd: Brak wystarczających danych w bazie (wszystkie wiersze zawierają wartości NaN w kluczowych kolumnach)."
        print(error_msg)
        save_text_to_file(error_msg, output_filename)
        return None
    
    # Słownik do przechowywania znormalizowanych wartości
    normalized_data = {}
    normalized_targets = {}
    
    # Normalizacja Min-Max dla każdej cechy
    for col, target_val in feature_mapping.items():
        min_val = min(working_df[col].min(), target_val)
        max_val = max(working_df[col].max(), target_val)
        diff = max_val - min_val
        
        if diff == 0:
            normalized_data[col] = np.zeros(len(working_df))
            normalized_targets[col] = 0.0
        else:
            normalized_data[col] = (working_df[col] - min_val) / diff
            normalized_targets[col] = (target_val - min_val) / diff
            
    # Obliczanie odległości euklidesowej dla każdego wiersza
    squared_distances = np.zeros(len(working_df))
    for col in feature_mapping.keys():
        squared_distances += (normalized_data[col] - normalized_targets[col]) ** 2
        
    working_df['Odległość'] = np.sqrt(squared_distances)
    
    # Maksymalna możliwa odległość euklidesowa w przestrzeni 5-wymiarowej [0, 1]^5 wynosi sqrt(5)
    max_possible_dist = np.sqrt(len(feature_mapping))
    working_df['Podobieństwo [%]'] = (1.0 - (working_df['Odległość'] / max_possible_dist)) * 100
    
    # Sortowanie wyników rosnąco po odległości i pobranie top_n
    closest_drones = working_df.sort_values(by='Odległość').head(top_n)
    
    # Pomocnicza funkcja do eliminacji brzydkich 'nan' na wydruku (teksty)
    def f_val(val, default="brak danych"):
        if pd.isna(val) or str(val).strip().lower() == 'nan':
            return default
        return val

    # Pomocnicza funkcja do bezpiecznego formatowania liczb zmiennoprzecinkowych (zapobiega crashom przy NaN)
    def f_num(val, format_str=":.2f", default="brak danych"):
        if pd.isna(val) or str(val).strip().lower() == 'nan':
            return default
        return f"{val:{format_str}}"

    # Zamiast bezpośrednich printów, zbieramy linie tekstu do listy
    output_lines = []
    
    # DYNAMICZNY NAGŁÓWEK
    output_lines.append(f"=== {len(closest_drones)} MODELI NAJBARDZIEJ ZBLIŻONYCH DO PROGNOZY NA ROK {year_of_prediction} ===")
    
    for idx, (df_idx, row) in enumerate(closest_drones.iterrows(), 1):
        nazwa = f_val(row.get('Nazwa'), "Nieznany model")
        firma = f_val(row.get('Firma'))
        kraj = f_val(row.get('Kraj produkcji'))
        naped = f_val(row.get('Napęd'))
        silnik = f_val(row.get('Silnik'))
        typ_silnika = f_val(row.get('Typ silnika'))
        
        # Bezpieczne wyciąganie cech numerycznych
        moc_str = f_num(row.get('Moc silnika\n[KM]'), ".0f", "brak danych")
        if moc_str != "brak danych":
            moc_str += " KM"
            
        val_endurance = row[col_endurance]
        val_range = row[col_range]
        val_ar = row[col_ar]
        val_wl = row[col_wl]
        val_pl = row[col_pl]
        
        # Budowanie sformatowanego rekordu tekstu
        output_lines.append(f"{idx}. {nazwa} (Firma: {firma})")
        output_lines.append(f"   Dopasowanie: {row['Podobieństwo [%]']:.2f}% (Odległość euklidesowa: {row['Odległość']:.4f})")
        output_lines.append(f"   Kraj produkcji: {kraj}")
        output_lines.append(f"   Typ napędu: {naped} | Silnik: {silnik} (Typ: {typ_silnika}, Moc: {moc_str})")
        output_lines.append(f"   - Czas lotu: {val_endurance:.1f} h (prognoza: {t_endurance:.1f} h)")
        output_lines.append(f"   - Zasięg: {val_range:.1f} km (prognoza: {t_range:.1f} km)")
        output_lines.append(f"   - Wydłużenie płata: {val_ar:.2f} (prognoza: {t_ar:.2f})")
        output_lines.append(f"   - Obciążenie powierzchni: {val_wl:.2f} kg/m^2 (prognoza: {t_wl:.2f} kg/m^2)")
        output_lines.append(f"   - Obciążenie mocy: {val_pl:.2f} kg/kW (prognoza: {t_pl:.2f} kg/kW)")
        output_lines.append(f"   - Profil skrzydła (root): {f_val(row.get('Profil skrzydła\n[root]'))}")
        output_lines.append(f"   - Profil skrzydła (tip): {f_val(row.get('Profil skrzydła\n[tip]'))}")
        
        # Bezpieczne formatowanie wymiarów gabarytowych i reszty parametrów (odporne na NaN)
        dlugosc = f_num(row.get('Długość\n[m]'), ".2f")
        wysokosc = f_num(row.get('Wysokość\n[m]'), ".2f")
        rozpietosc = f_num(row.get('Rozpiętość skrzydeł\n[m]'), ".2f")
        
        output_lines.append(f"   - Wymiary: dł. {dlugosc} m | wys. {wysokosc} m | rozpiętość {rozpietosc} m")
        output_lines.append(f"   - Zasięgi operacyjne: SATA: {f_val(row.get('Zasięg SATA\n[km]'))} km | LOS: {f_val(row.get('Zasięg LOS\n[km]'))} km")
        output_lines.append(f"   - Prędkości: przelotowa {f_val(row.get('Prędkość przelotowa\n[km/h]'))} km/h | max {f_val(row.get('Prędkość maxymalna\n[km/h]'))} km/h")
        output_lines.append(f"   - Pułap operacyjny: {f_val(row.get('Pułap\n[m]'))} m")
        
        # Bezpieczne formatowanie mas
        m_wlasna = f_num(row.get('Masa własna\n[kg]'), ".1f")
        m_startowa = f_num(row.get('Masa stratowa\n[kg]'), ".1f") 
        ladownosc = f_num(row.get('Ładowność\n[kg]'), ".1f")
        
        output_lines.append(f"   - Masowe: własna {m_wlasna} kg | startowa {m_startowa} kg | ładowność {ladownosc} kg")
        output_lines.append("-" * 50)
        
    # Łączymy wszystkie linie znakiem nowej linii, tworząc jeden blok tekstu
    full_text_report = "\n".join(output_lines)
    
    # WYWOŁANIE TWOJEJ FUNKCJI: Zapisujemy pełny raport tekstowy do wskazanego pliku
    save_text_to_file(full_text_report, output_filename)
        
    return