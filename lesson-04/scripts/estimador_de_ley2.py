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

filehandler = open('result.csv', 'w')

for alpha in range(1, 10):
    num = 0.0
    den = 0.0

    for z, d in data:
        num = num + (z / (d**alpha))
        den = den + (1 / (d**alpha))

    z_estimated = num / den

    filehandler.write("{0:>2d},{1:.2f}\n".format(alpha, z_estimated))

    print("La ley estimada es de {0:.2f} para alpha igual a {1}".format(
        z_estimated, alpha))

filehandler.close()
