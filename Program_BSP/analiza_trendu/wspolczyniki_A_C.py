import os
import pandas as pd
import numpy as np
from ogolne.save_result import save_text_to_file

def calculate_indicator_A_C(df: pd.DataFrame,e_reg_range_mass, path_result):
    
    text = ""
    indicator_A_C_result = os.path.join(path_result,"indicator_A_C.txt")
    
    m1 = df['Masa stratowa\n[kg]'].min()
    m2 = df['Masa stratowa\n[kg]'].max()
    
    C = np.log10((e_reg_range_mass(m1)/e_reg_range_mass(m2)))/np.log10((m1/m2))
    A = e_reg_range_mass(m1)/(m1**C)
    
    text += "Obliczenie współczynmików A i C\n"
    text += f"x1 = {m1} y1 = {e_reg_range_mass(m1)}\n"
    text += f"x2 = {m2} y2 = {e_reg_range_mass(m2)}\n"
    text += f"C = {C}\n"
    text += f"A = {A}\n"
    
    save_text_to_file(text, indicator_A_C_result)
    
    return 0
   
    

