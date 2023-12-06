# tpfinal-ProgII
Para compilar el programa en C:
> gcc functions.c main.c -Wall -gstabs -o main

Para correr el programa en conjunto, llamamos al ejecutable compilado en C:
> ./main Fito_Paez

Para correr los tests en C:

> gcc functions.c tests.c -Wall -gstabs -o tests
> ./tests

Para correr los tests en Python:
En caso de tener pytest, instalarlo:
> pip install pytest

Una vez teniendo pytest:
> python3 -m pytest tests.py