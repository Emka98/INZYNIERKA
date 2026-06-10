import os
import matplotlib.pyplot as plt
import pandas as pd

def wykres_procentowy_producentow(df, save_path, kolumna_silnika='Silnik'):
    save_path = os.path.join(save_path,"wykres_procentowy_producentow")
    """
    Funkcja zlicza wystąpienia każdego producenta silników (częstość użycia)
    i generuje procentowy wykres kołowy.
    
    Parametry:
    df (pd.DataFrame): Tabela z danymi samolotów.
    save_path (str): Ścieżka do zapisu wykresu.
    kolumna_silnika (str): Kolumna zawierająca nazwy silników (domyślnie 'Silnik').
    """
    # 1. Czyszczenie danych: usuwamy puste wiersze w kolumnie z silnikami
    df_clean = df.dropna(subset=[kolumna_silnika]).copy()
    
    # 2. Wyciąganie producenta (bierzemy pierwsze słowo z nazwy silnika, np. "Pratt" z "Pratt & Whitney")
    #    Jeśli masz osobną kolumnę z samym producentem, możesz pominąć ten krok.
    df_clean['Producent'] = df_clean[kolumna_silnika].astype(str).apply(lambda x: x.split()[0])
    
    # 3. Zliczanie, ile razy dany producent występuje w tabeli
    czestosc_producentow = df_clean['Producent'].value_counts().reset_index()
    czestosc_producentow.columns = ['Producent', 'Liczba_wystapien']
    
    # 4. Grupowanie niszowych producentów (poniżej 3% udziału) do kategorii "Inni"
    if len(czestosc_producentow) > 6:
        suma_wszystkich = czestosc_producentow['Liczba_wystapien'].sum()
        prog = suma_wszystkich * 0.03  # 3% udziału
        
        glowne = czestosc_producentow[czestosc_producentow['Liczba_wystapien'] >= prog]
        inne = czestosc_producentow[czestosc_producentow['Liczba_wystapien'] < prog]
        
        if not inne.empty:
            suma_inne = pd.DataFrame([{
                'Producent': 'Inni producenci', 
                'Liczba_wystapien': inne['Liczba_wystapien'].sum()
            }])
            czestosc_producentow = pd.concat([glowne, suma_inne], ignore_index=True)

    # 5. Generowanie wykresu kołowego
    plt.figure(figsize=(10, 8))
    
    # Profesjonalna paleta barw
    kolory = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    plt.pie(
        czestosc_producentow['Liczba_wystapien'],
        labels=czestosc_producentow['Producent'],
        autopct='%1.1f%%',
        startangle=140,
        colors=kolory[:len(czestosc_producentow)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )
    
    plt.title('Udział procentowy producentów silników\n(na podstawie liczby zastosowań w modelach)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # Upewniamy się, że folder istnieje i zapisujemy
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f" Sukces! Wykres producentów zapisany w: {save_path}")