import math
from ogolne.save_result import save_text_to_file

def masscal(path):
    
    text = ""
    
    # znane masy
    mass = 75
    
    # Wczesnie policzone wspolczyniki A i C
    c = -0.13441672738453134
    a = 1.5098473319833845
    
    #0,5 [kg/kWh] jednostkowe zużycie paliwa dla silników śmigłowych [kg/Ws]
    fuel_consumption = 0.5/3600000
    
    # [m/s^2] przyspieszenie ziemskie
    g = 9.81 
    
    # sprawność śmigła
    n_prop = 0.8
    
    # współczynnik wynikający z faktu iż samolot nie leci z maksymalną doskonałością 
    kz = 0.8
    
    # maksymalna doskonałość
    Kmax = 32
        
    # zakładam ze predkośc patrolowa to  predkosci przzelotowej
    cruise_speed = 42
    speed_climb = 0.7*cruise_speed
    speed_loiter = 0.5*cruise_speed
    
    # współczynnik lekkości
    K_vs = 1
    
    odleglosc_do_miejsca_patrolowego = 300000
    czas_patrolu = 180000
    czas_oczekiwania = 900
    
    # [o] kat wznoszenia1 
    katWz1 = 12
    wysokosc_przelotowa = 3000
    odleglosc_wznoszenie1 = wysokosc_przelotowa/math.sin(math.radians(katWz1))
    odleglosc_wznoszenie11 = wysokosc_przelotowa/math.tan(math.radians(katWz1))

    katWz2 = 5
    wysokosc_patrolowa = 12000 - wysokosc_przelotowa
    odleglosc_wznoszenie2 = wysokosc_patrolowa/math.sin(math.radians(katWz2))
    odleglosc_wznoszenie22 = wysokosc_patrolowa/math.tan(math.radians(katWz2))
    
    katOp1 = 5
    odleglosc_opadania1 = wysokosc_patrolowa/math.sin(math.radians(katOp1))
    odleglosc_opadania11 = wysokosc_patrolowa/math.tan(math.radians(katOp1))
    
    katOp2 = 2
    odleglosc_opadania2 = wysokosc_przelotowa/math.sin(math.radians(katOp2))
    odleglosc_opadania22 = wysokosc_przelotowa/math.tan(math.radians(katOp2))

    # #Obliczenia iloczynu
    Start = 0.97
    text += f"Start: {Start}\n"
    Rozbieg = 0.985
    text += f"Rozbieg: {Rozbieg}\n"
    Wznosznie1 = math.e**(-((fuel_consumption*odleglosc_wznoszenie1*g)/(kz*n_prop*Kmax)))
    text += f"Wznosznie1: {Wznosznie1}\n"
    Dolot = math.e**(-((fuel_consumption*(odleglosc_do_miejsca_patrolowego-odleglosc_wznoszenie11-odleglosc_wznoszenie22)*g/(kz*n_prop*Kmax))))
    text += f"Dolot: {Dolot}\n"
    Wznosznie2 = math.e**(-((fuel_consumption*odleglosc_wznoszenie2*g)/(kz*n_prop*Kmax)))
    text += f"Wznosznie2: {Wznosznie2}\n"
    Patrolowanie = math.e**(-((fuel_consumption*czas_patrolu*speed_loiter*g)/(kz*n_prop*Kmax)))
    text += f"Patrolowanie: {Patrolowanie}\n"
    Opadanie1 = math.e**(-((fuel_consumption*odleglosc_opadania1*g)/(kz*n_prop*Kmax)))
    text += f"Opadanie1: {Opadanie1}\n"
    Powrot = math.e**(-((fuel_consumption*(odleglosc_do_miejsca_patrolowego-odleglosc_opadania11-odleglosc_opadania22)*g/(kz*n_prop*Kmax))))
    text += f"Powrot: {Powrot}\n"
    Opadanie2 = math.e**(-((fuel_consumption*odleglosc_opadania2*g)/(kz*n_prop*Kmax)))
    text += f"Opadanie2: {Opadanie2}\n"
    Oczekiwanie = math.e**(-((fuel_consumption*czas_oczekiwania*speed_loiter*g)/(kz*n_prop*Kmax)))
    text += f"Oczekiwanie: {Oczekiwanie}\n"
    Ladowanie = 0.995
    text += f"Ladowanie: {Ladowanie}\n"

    # Iloczyn wyznaczonych powyżej proporcji
    proportions_determined = Start * Rozbieg * Wznosznie1 * Dolot * Wznosznie2 * Patrolowanie * Opadanie1 * Powrot * Opadanie2 * Oczekiwanie * Ladowanie
    
    
    for zakladana_masa in range(1, 100000, 1):
        weight_ratio = 1.06 * (1 - proportions_determined)
        weight_ratio_emp_start = a * zakladana_masa**c * K_vs
        
        mianownik = 1 - weight_ratio - weight_ratio_emp_start
        W_obl = mass / mianownik
        
        if (abs(W_obl-zakladana_masa)) < 1:
            text += f"Masa obliczona {W_obl} \nMasa założona: {zakladana_masa}  {W_obl-zakladana_masa}\n"
            text += f"weight_ratio: {weight_ratio}\n"
            text += f"Masa do lądowania: {zakladana_masa * proportions_determined}"

    save_text_to_file(text,path)
    return
    