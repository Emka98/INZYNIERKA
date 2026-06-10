import math

# 737-300 data
mass = 32_800
M_max = We = mass * 2.20462262
np = 12_409
v_max_ms = 243.333
v_max = v_max_ms * 1.944
T_max_kN = 86700
T_max = T_max_kN * 224.8089431
Tem_Prz_Tur_stC = 1450
Tem_Prz_Tur = (Tem_Prz_Tur_stC * (9/5)) + 491.67
Rp = 20

# Moje dane
# mass = 881
# M_max = We = mass * 2.20462262
# np = 1000
# v_max_ms = 62
# v_max = v_max_ms * 1.944
# T_max_kN = 2_756.99
# T_max = T_max_kN * 224.8089431
# Tem_Prz_Tur_stC = 900
# Tem_Prz_Tur = (Tem_Prz_Tur_stC * (9/5)) + 491.67
# Rp = 2

sum_1970 = []
sum_1986 = []

text_1986 = ""
text_1970 = ""

# rozwoj konstrukcji w 1986 [h]
c1_1970 = 0.027
c2_1970= 0.791
c3_1970 = 1.526
c4_1970 = 0.183

c1_1986 = 4.86
c2_1986= 0.777
c3_1986 = 0.894
c4_1986 = 0.163

He_1986 = math.ceil(c1_1986 * We**c2_1986 * v_max**c3_1986 * np**c4_1986)
He_1970 = math.ceil(c1_1970 * We**c2_1970 * v_max**c3_1970 * np**c4_1970)

wspolny_text = "Czas na rozwój konstrukcji: "
text_1986 += wspolny_text + str(He_1986) + " h" + "\n"
text_1970 += wspolny_text + str(He_1970) + " h" + "\n"

# Wsparcie prac badawczo rozwojowych [USD]
c1_1970 = 0.00549
c2_1970 = 0.873
c3_1970 = 1.890
c4_1970 = 0.346

c1_1986 = 45.42
c2_1986 = 0.63
c3_1986 = 1.3
c4_1986 = 0

Cd_1986 = math.ceil(c1_1986 * We**c2_1986 * v_max**c3_1986 * np**c4_1986)
Cd_1970 = math.ceil(c1_1970 * We**c2_1970 * v_max**c3_1970 * np**c4_1970)

sum_1986.append(Cd_1986)
sum_1970.append(Cd_1970)

wspolny_text = "Wsparcie prac badawczo rozwojowych: "
text_1970 += wspolny_text + str(Cd_1970) + " USD" + "\n"
text_1986 += wspolny_text + str(Cd_1986) + " USD" + "\n"

# Cena silnika i awioniki [USD]
c1_1970 = 130
c2_1970 = 0.836

c1_1986 = 1548.0
c2_1986 = 0.04324
c3_1986 = 3.25
c4_1986 = 0.969
c5_1986 = 2228.0

Cen_1970 = math.ceil(c1_1970 * T_max**c2_1970)
Cen_1986 = math.ceil(c1_1986 * (c2_1986 * T_max + c3_1986 * M_max + c4_1986 * Tem_Prz_Tur - c5_1986))

# sum_1986.append(Cen_1986)
# sum_1970.append(Cen_1970)

wspolny_text = "Cena silnika i awioniki: "
text_1970 += wspolny_text + str(Cen_1970) + " USD" + "\n"
text_1986 += wspolny_text + str(Cen_1986) + " USD" + "\n"

# Robocizna [h]
c1_1970 = 20.348
c2_1970 = 0.740
c3_1970 = 0.543
c4_1970 = 0.524

c1_1986 = 7.370
c2_1986 = 0.820
c3_1986 = 0.484
c4_1986 = 0.641

Hml_1970 = math.ceil(c1_1970 * We**c2_1970 * v_max**c3_1970 * np**c4_1970)
Hml_1986 = math.ceil(c1_1986 * We**c2_1986 * v_max**c3_1986 * np**c4_1986)

wspolny_text = "Robocizna: "
text_1970 += wspolny_text + str(Hml_1970) + " h" + "\n"
text_1986 += wspolny_text + str(Hml_1986) + " h" + "\n"

# Materiały [USD]
c1_1970 = 18.47
c2_1970 = 0.689
c3_1970 = 0.624
c4_1970 = 0.792

c1_1986 = 11.00
c2_1986 = 0.921
c3_1986 = 0.621
c4_1986 = 0.799

Cmm_1970 = math.ceil(c1_1970 * We**c2_1970 * v_max**c3_1970 * np**c4_1970)
Cmm_1986 = math.ceil(c1_1986 * We**c2_1986 * v_max**c3_1986 * np**c4_1986)

sum_1986.append(Cmm_1986)
sum_1970.append(Cmm_1970)

wspolny_text = "Materiały: "
text_1970 += wspolny_text + str(Cmm_1970) + " USD" + "\n"
text_1986 += wspolny_text + str(Cmm_1986) + " USD" + "\n"

# Oprzyrządowanie i narzędzia [h]
c1_1970 = 2.79
c2_1970 = 0.764
c3_1970 = 0.899
c4_1970 = 0.178
c5_1970 = 0.066

c1_1986 = 5.99
c2_1986 = 0.777
c3_1986 = 0.696
c4_1986 = 0.263
c5_1986 = 0

Ht_1970 = c1_1970 * We**c2_1970 * v_max**c3_1970 * np**c4_1970 * Rp**c5_1970
Ht_1986 = c1_1986 * We**c2_1986 * v_max**c3_1986 * np**c4_1986

wspolny_text = "Oprzyrządowanie i narzędzia: "
text_1970 += wspolny_text + str(Hml_1970) + " h" + "\n"
text_1986 += wspolny_text + str(Hml_1986) + " h" + "\n"

# System zapewnienia jakości [h]
c1_1986 = c1_1970 = 0.13

Hqc_1970 = math.ceil(c1_1970 * Hml_1970)
Hqc_1986 = math.ceil(c1_1986 * Hml_1986)

wspolny_text = "System zapewnienia jakości: "
text_1970 += wspolny_text + str(Hqc_1970) + " h" + "\n"
text_1986 += wspolny_text + str(Hqc_1986) + " h" + "\n"

# Próby w locie (zaniedbywane w fazie produkcji) [USD]
c1_1970 = 0.000714
c2_1970 = 1.160
c3_1970 = 1.371
c4_1970 = 1.281

c1_1986 = 243.03
c2_1986 = 0.325
c3_1986 = 0.822
c4_1986 = 1.210

Cft_1970 = math.ceil(c1_1970 * We**c2_1970 * v_max**c3_1970 * np**c4_1970)
Cft_1986 = math.ceil(c1_1986 * We**c2_1986 * v_max**c3_1986 * np**c4_1986)

sum_1986.append(Cft_1986)
sum_1970.append(Cft_1970)

wspolny_text = "Próby w locie: "
text_1970 += wspolny_text + str(Cft_1970) + " USD" + "\n"
text_1986 += wspolny_text + str(Cft_1986) + " USD" + "\n"

# Stawki godzinowe [USD]
c1_1970 = 16.0
c2_1970 = 11.50
c3_1970 = 10.0
c4_1970 = 10.0

c1_1986 = 59.10
c2_1986 = 61.70
c3_1986 = 55.40
c4_1986 = 50.10

Ce_1970 = math.ceil(He_1970 * c1_1970)
text_1970 += f"Koszt inzynierów po przliczeniu stawek za roboczo godziny: {Ce_1970} USD\n"
sum_1970.append(Ce_1970)
Cml_1970 = math.ceil(Hml_1970 * c2_1970)
text_1970 += f"Koszt narzędzi po przliczeniu stawek za roboczo godziny: {Cml_1970} USD\n"
sum_1970.append(Cml_1970)
Ct_1970 = math.ceil(Ht_1970 * c3_1970)
text_1970 += f"Koszt wytworzenia po przliczeniu stawek za roboczo godziny: {Ct_1970} USD\n"
sum_1970.append(Ct_1970)
Coc_1970 = math.ceil(Hqc_1970 * c4_1970)
text_1970 += f"Koszt kontroli jakości po przliczeniu stawek za roboczo godziny: {Coc_1970} USD\n"
sum_1970.append(Coc_1970)

Ce_1986 = math.ceil(He_1986 * c1_1986)
text_1986 += f"Koszt inzynierów po przliczeniu stawek za roboczo godziny: {Ce_1986} USD\n"
sum_1986.append(Ce_1986)
Cml_1986 = math.ceil(Hml_1986 * c2_1986)
text_1986 += f"Koszt narzędzi po przliczeniu stawek za roboczo godziny: {Cml_1986} USD\n"
sum_1986.append(Cml_1986)
Ct_1986 = math.ceil(Ht_1986 * c3_1986)
text_1986 += f"Koszt wytworzenia po przliczeniu stawek za roboczo godziny: {Ct_1986} USD\n"
sum_1986.append(Ct_1986)
Coc_1986 = math.ceil(Hqc_1986 * c4_1986)
text_1986 += f"Koszt kontroli jakości po przliczeniu stawek za roboczo godziny: {Coc_1986} USD\n"
sum_1986.append(Coc_1986)

# Obliczenie kosztów jednostkowych [USD]
cost_1970 = math.ceil(sum(sum_1970)/np)
cost_1986 = math.ceil(sum(sum_1986)/np)

wspolny_text = "Szacowany koszt jednostkowy: "
text_1970 += wspolny_text + str(cost_1970) + " USD" + "\n"
text_1986 += wspolny_text + str(cost_1986) + " USD" + "\n"

a = math.ceil((cost_1986 - cost_1970) / (1986 - 1970))
b = math.ceil(cost_1970 - a*1970)

# esty_cost = lambda year: a*year + b

# print(f"y = {a}x + {b}")
# print(f"{esty_cost(2030)} = {a}*2030 + {b}")

print(f"Rok 1970: \n{text_1970}")
print(f"Rok 1986:\n{text_1986}")

CPI_1970_to_2030 = 9.35
CPI_1986_to_2030 = 3.25

real_cost_70_in_2030 = math.ceil((cost_1970 * CPI_1970_to_2030))
real_cost_86_in_2030 = math.ceil((cost_1986 * CPI_1986_to_2030))

print(f"Koszt proj. 1970 w cenach 2030: {real_cost_70_in_2030} USD")
print(f"Koszt proj. 1986 w cenach 2030: {real_cost_86_in_2030} USD")
