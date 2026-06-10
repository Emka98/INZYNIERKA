import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_plot(df: pd.DataFrame, X_data_name: str, Y_data_name: str, plot_title: str, save_place: str):
    # 1. Kopiowanie i bezpieczna konwersja
    df_local = df.copy()
    df_local[X_data_name] = pd.to_numeric(df_local[X_data_name], errors="coerce")
    df_local[Y_data_name] = pd.to_numeric(df_local[Y_data_name], errors="coerce")

    # 2. Filtrowanie (logarytm wymaga wartości > 0)
    df_clean = df_local[
        (df_local[X_data_name] > 0) & (df_local[Y_data_name] > 0)
    ].dropna(subset=[X_data_name, Y_data_name])

    if df_clean.empty:
        print(f"Brak poprawnych danych dla: {plot_title}")
        return None

    x = df_clean[X_data_name].values
    y = df_clean[Y_data_name].values

    # 3. Obliczanie trendu potęgowego metodą regresji liniowej na logarytmach
    coeffs = np.polyfit(np.log(x), np.log(y), 1)
    A = coeffs[0]  # Wykładnik potęgowy
    C = np.exp(coeffs[1])  # Współczynnik proporcjonalności

    def trend_func(t):
        return C * np.power(t, A)

    # 4. Przygotowanie linii trendu (dokładnie od min do max z danych)
    start = x.min()
    end = x.max()
    X_trend = np.linspace(start, end, 100)
    Y_trend = trend_func(X_trend)

    # 5. Rysowanie wykresu
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color="blue", alpha=0.6, label="Dane rzeczywiste")

    # Formatowanie legendy
    label_text = rf"Trend potęgowy: $y = {C:.2e} \cdot x^{{{A:.2f}}}$"

    plt.plot(
        X_trend,
        Y_trend,
        color="red",
        linestyle="--",
        linewidth=2,
        label=label_text,
    )

    # 6. Opis osi i estetyka
    plt.title(plot_title, fontsize=14)
    plt.xlabel(X_data_name, fontsize=12)
    plt.ylabel(Y_data_name, fontsize=12)
    plt.legend(loc="best", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)

    # 7. Zapisywanie pliku
    if not os.path.exists(save_place):
        os.makedirs(save_place)

    # Czyszczenie nazwy pliku ze znaków specjalnych (w tym \n)
    invalid_chars = ['/', '\\', ' ', ':', '?', '*', '<', '>', '|', '"', '\n']
    safe_title = plot_title
    for char in invalid_chars:
        safe_title = safe_title.replace(char, "_")
        
    save_path = os.path.join(save_place, f"{safe_title}.png")

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Wykres zapisany: {save_path}")

    return trend_func