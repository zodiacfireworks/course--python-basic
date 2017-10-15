# -*- encoding: utf-8 -*-
table = input('¿Qué tabla deseas? : ')

error = False
try:
    table = int(table)
except Exception:
    print('El valor ingresado no se puede convertir a entero')
    error = True

if error:
    print('Lo sentimos, no podemos general la tabla :(')
else:
    filename = 'table{0}.txt'.format(table)

    filehandler = open(filename, 'w')

    for i in range(0,13):
        filehandler.write('{0} x {1} = {2}\n'.format(i, table, i*table))

    filehandler.close()
    print('¡Tu tabla ha sido generada exitosamente!')