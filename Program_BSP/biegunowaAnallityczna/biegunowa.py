import math
import os
from ogolne.save_result import save_text_to_file
def calbiegunowa(AR, Kmax, path_dir_save):
    
    file_name = "biedunowa analityczna"
    text = ""
    path_to_save = os.path.join(path_dir_save,file_name)
    
    #oswald for regular rectagel wing cal AR > 3
    # e = 1.78*(1 - 0.045*AR**0.68)-0.64
    
    # oswald galinski book:
    e = 0.8
    
    cxo = (math.pi * AR * e) / (4 * Kmax ** 2)
    
    text += f"Biedunowa analityczna: {cxo}"
    save_text_to_file(text, path_to_save)

    return cxo