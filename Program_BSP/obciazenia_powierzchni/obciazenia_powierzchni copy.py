import math
import matplotlib.pyplot as plt
import numpy as np

# Stałe z poprzednichobliczen lub
Cxo = 0.009817477042468103
ar = 16
g = 9.81 
e = 0.8 
sigma = 1 
aktualna_powierzchnia_S = 0.0
# mass_TO = math.ceil(881 * g)
# mass_L = math.floor(624.99 * g)

mass_TO = 1000
mass_L = 1

#promien zkrętu
r = 50

Czmax = 1.35
Cz = Czmax / 1.1
kat_Wzn = 10

v_min = 42
v_crus = 50
v_max = 62

s_to = s_l = 500

cisnienie_dynamiczne = lambda v : 1.225 * v**2 / 2
gradient_wznoszenia = lambda kat: math.sin(math.radians(kat))

# Ladowanie
# ws < ladowanie [n/m^2]
ladowanie = (sigma * Czmax * (s_l - 122)) / 0.75
s = math.ceil(mass_L/ladowanie)

# Prędkosć minimalna [n/m^2] => WS
# Przepisy ASTM F3179/F3179M-24a 
licznik = 2 * mass_TO
mianownik = s * Cz * 1.255

# Start [N/N] <= T/W
def start(ws):
    licznik = 0.133 * ws * (1/Czmax) * (1 / sigma)
    mianownik = s_to - 3.834 * math.sqrt(ws * (1 / Czmax) * (1 / sigma))
    return licznik/mianownik

ws_range = [x/s for x in range(mass_L, mass_TO)]
start_dane = [start(x) for x in ws_range]

plt.plot(ws_range, start_dane, label='start' ,color = 'g')
plt.fill_between(ws_range, start_dane, 0, color='g', alpha=0.2)

# Wznoszenie [N/N] <= T/W
wznoszenie = gradient_wznoszenia(kat_Wzn) * 2 * math.sqrt(Cxo / (math.pi * ar * e))
plt.axhline(wznoszenie, xmin=0, xmax=10000, label='wznoszenie', color='r')

# inne warunki [n/m^2] <= WS
inne_warunki = lambda v : cisnienie_dynamiczne(v) * math.sqrt(math.pi * ar * e * Cxo)

# dowolny zakręt [n/m^2] = WS
def dowolny_zakret(v, r, Czmax):
    psi_dot = v / r  
    licznik = cisnienie_dynamiczne(v) * Czmax
    wyrazenie_w_nawiasie = (psi_dot * v) / g
    mianownik = math.sqrt((wyrazenie_w_nawiasie ** 2) + 1)
    ws = licznik / mianownik
    return ws

def prawidlowy_zakret(ws, v):
    psi_dot = v / r
    TW_max = (((psi_dot * v) / g) ** 2 + 1) * (ws / (cisnienie_dynamiczne(v) * math.pi * ar * e)) + (cisnienie_dynamiczne(v) * Cxo / ws)
    return TW_max

prawidlowy_zakret_dane_vmax = [prawidlowy_zakret(x,v_crus) for x in ws_range]
plt.plot(ws_range, prawidlowy_zakret_dane_vmax, label='prawidłowy zakręt' ,color = 'y')
plt.fill_between(ws_range, prawidlowy_zakret_dane_vmax, 0, color='y', alpha=0.2)

#Zasięg
zasieg = lambda v: cisnienie_dynamiczne(v) * math.sqrt(math.pi * ar * e * Cxo)
zasieg = zasieg(v_min)
plt.vlines(x=zasieg, ymin=1, ymax=wznoszenie, label='zasieg', color='r')

plt.ylim(0,1)
plt.xlabel('Obciążenie powierzchni W/S $[N/m^2]$', fontsize=11)
plt.ylabel('Stosunek ciągu do ciężaru T/W $[N/N]$', fontsize=11)
plt.title('Optymalne obciążenie powierzchni i obciążenia ciągu (mocy)', fontsize=12, fontweight='bold', pad=15)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', shadow=True)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()