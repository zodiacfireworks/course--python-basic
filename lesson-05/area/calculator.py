# -*- encoding:utf-8 -*-
import sys


def loaddata(filename):
    fileHandler = open(filename)

    data = []

    for n, line in enumerate(fileHandler):
        if n == 0:
            # Pasamos a la siguiente linea
            continue
            
        line = line.strip('\n')
        line = line.split()
        
        if line == []:
            continue
            
        line = [float(item) for item in line]
        
        data.append(line)

    return data


def semiperimeter(a, b, c):
    return (a + b + c) * 0.5


def area(a, b, c):
    """
    Given the sides of the triangle, calculates
    its area using Heron's Theorem
    
    Dados los lados del un triangulo, calcula su 
    area empleando el teorema de Herón.
    """
    p = semiperimeter(a, b, c)
    ar = (p * (p - a) * (p - b) * (p - c)) ** 0.5
    
    return ar


# Cuerpo principal del programa
# Alias 'main'
if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    
    triangles = loaddata(inputfile)
    
    headers = ["A", "B", "C", "Area Parcial", "Area Total"]
    
    fileHandler = open(outputfile, 'w')
    fileHandler.write(
        '{0:>8s}    {1:>8s}    {2:>8s}    {3:>14s}    {4:>14s}\n'.format(
            *headers
        )
    )
    
    area_total = 0
    
    for a, b, c in triangles:
        partial_area = area(a, b, c)
        area_total = area_total + partial_area
        fileHandler.write(
            '{0:8.2f}    {1:8.2f}    {2:8.2f}    {3:14.4f}    {4:14.4f}\n'.format(
                a,
                b,
                c,
                partial_area,
                area_total
            )
        )










