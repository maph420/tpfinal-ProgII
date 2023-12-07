# tpfinal-ProgII
Para compilar el programa en C:
> gcc funciones.c main.c -Wall -gstabs -o main

Para correr el programa en conjunto, llamamos al ejecutable compilado en C:
> ./main Fito_Paez

Para correr los tests en C:

> cd Tests

> gcc ../funciones.c tests.c -Wall -gstabs -o tests

> ./tests

Para correr los tests en Python:

En caso de no tener pytest, instalarlo:
> pip install pytest

Una vez teniendo pytest:
> python3 -m pytest Tests/tests.py

TODO:

.Arreglar test en C (test_recorrer_y_limpiar)

.Informe con explicacion

.Pensar mejor solucion a los casos especificos de python