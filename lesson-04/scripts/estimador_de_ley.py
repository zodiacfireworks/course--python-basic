# -*- encoding: utf-8 -*-
# Abrimos el archivo para leerlo
filehandler = open('data.txt', 'r')

data = []

for line in filehandler:
    line = line.strip('\n')
    line = line.split()
    line = [float(item) for item in line]
    data.append(line)

filehandler.close()

num = 0.0
den = 0.0
alpha = 1

for z, d in data:
    num = num + (z / (d**alpha))
    den = den + (1 / (d**alpha))

z_estimated = num / den

print("La ley estimada es de {0:.2f}".format(z_estimated))
