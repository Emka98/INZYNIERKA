import math as m

ws = 671
tw = 0.319
v = 42
n = 0.8
g = 9.81
mass = 881

moc = mass * g * tw
moc = moc * v
moc_w_watach = moc / n
moc_w_kwatach = m.ceil(moc_w_watach / 1000)

print(f"Silnik {moc_w_kwatach} kW")

#Lycoming IO-390
s = m.ceil(mass * g / ws)
print(f"Optymalna powierchnia nośna: {s}")


print(f"Ciag silnika {(n * moc_w_watach) / v} N")