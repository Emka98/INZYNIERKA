import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def generuj_wykres_napedow_dronow(df, kolumna_naped="Napęd", plot_title="Udział rodzajów napędu w bazie dronów", save_place=None):
    """
    Generuje i zapisuje wykres kołowy przedstawiający udział różnych rodzajów napędu.
    Wykres wyrenderowany jest w eleganckiej, zielonej palecie kolorów.
    
    :param df: DataFrame z danymi dronów
    :param kolumna_naped: Nazwa kolumny zawierającej typ napędu (domyślnie 'Napęd')
    :param plot_title: Tytuł wykresu
    :param save_place: Ścieżka do głównego folderu roboczego (Calculations). 
                       Jeśli podana, wykres zostanie zapisany w save_place/Wykresy/
    """
    # 1. Pobranie i wyczyszczenie danych o napędach
    if kolumna_naped not in df.columns:
        print(f"Błąd: Kolumna '{kolumna_naped}' nie istnieje w przesłanym DataFrame!")
        return

    # Usunięcie brakujących danych (NaN) i zliczenie wystąpień każdego napędu
    naped_counts = df[kolumna_naped].dropna().value_counts()

    if naped_counts.empty:
        print("Brak danych o napędach do wyświetlenia na wykresie.")
        return

    # 2. Tworzenie wykresu kołowego
    plt.figure(figsize=(8, 8))
    
    # --- ZIELONA PALETA KOLORÓW ---
    # Generujemy odcienie zieleni w zależności od liczby unikalnych kategorii
    num_categories = len(naped_counts)
    
    # Pobieramy próbki z palety 'Greens' od jasnego (0.3) do ciemnego (0.75) zielonego,
    # aby uniknąć skrajnie białego i całkowicie czarnego koloru.
    colors = plt.cm.Greens(np.linspace(0.35, 0.75, num_categories))

    # Wykres kołowy
    plt.pie(
        naped_counts, 
        labels=naped_counts.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors,
        textprops={'fontsize': 10, 'weight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5} # Białe linie oddzielające kawałki dla czytelności
    )

    plt.axis('equal')  # Gwarantuje, że wykres będzie idealnym kołem
    plt.title(plot_title, fontsize=14, weight='bold', pad=20)
    plt.tight_layout()

    # 3. Zapisywanie pliku
    if save_place:
        # Ustalamy folder docelowy: Calculations/Wykresy
        wykresy_dir = os.path.join(save_place, "Wykresy")
        
        # Jeśli folder Wykresy nie istnieje, program go automatycznie stworzy
        os.makedirs(wykresy_dir, exist_ok=True)
        
        save_path = os.path.join(wykresy_dir, "wykres_napedow.png")
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"-> Zielony wykres kołowy napędów został zapisany w: {save_path}")
    else:
        # Jeśli nie podano ścieżki zapisu, po prostu pokaż wykres na ekranie
        plt.show()
        
    plt.close() # Zamknięcie wykresu