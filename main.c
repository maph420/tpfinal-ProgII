//librerias
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
#include<assert.h>

//macros
#define RUTA_A_LEER "Textos/"
#define RUTA_A_ESCRIBIR "Entradas/"
#define RUTA_ARCHIVOS "archivos.txt"
#define CANT_CARACTERES_MAX 2000
#define LONGITUD_MAX_LINEA 255
#define LONGITUD_MAX_COMANDO 100


char* armar_cadena(char* palabras[], int cantPalabras) {
    
     if (cantPalabras == 0) {
        char* comando = malloc(1);  // Allocate space for an empty string
        comando[0] = '\0';          // Ensure the string is properly terminated
        return comando;
    }
    char* comando = malloc(sizeof(char)*100);
    // inicializar la cadena comando
    comando[0] = '\0';
    for (int i=0; i<cantPalabras; i++) {
        strcat(comando, palabras[i]);
    }
    return comando;
}

char** obtener_textos(char* rutaArtista) {
    char linea[LONGITUD_MAX_LINEA];
    char** textos = malloc(sizeof(char *)*30);
    int i=0;
    FILE* archivoNombres;

    char* cadenasComando[] = {"ls ", rutaArtista, "> archivos.txt"};
    char* comandoVolcarNombres = armar_cadena(cadenasComando, 3);

    // system retorna algo distinto de 0 si falla el comando
    if (system(comandoVolcarNombres) != 0) {
        printf("Error: Directorio no encontrado. Revisar argumento pasado. \n");
        free(textos);
        free(comandoVolcarNombres);
        return NULL;
    }

    archivoNombres = fopen(RUTA_ARCHIVOS, "r");
    
    if (archivoNombres == NULL) {
        free(textos);
        free(comandoVolcarNombres);
        fclose(archivoNombres);
        printf("Error: no se pudo abrir el archivo de nombres. Revisar argumento pasado.\n");
        return NULL;
    }
    
    while( fgets(linea, LONGITUD_MAX_LINEA, archivoNombres)) {
        textos[i] = malloc(sizeof(char)*50);
        strcpy(textos[i], linea);
        i++;
    }
    if (i==0) {
        printf("Error: archivos.txt esta vacio\n");
        free(textos);
        free(comandoVolcarNombres);
        fclose(archivoNombres);
        return NULL;
    }
    // aseguramos de colocar una marca que indique el fin de la lista
    textos[i] = NULL;
    free(comandoVolcarNombres);
    fclose(archivoNombres);
    return textos;
}   

char* limpiar_texto(char* nomTexto) {
    char c, resultado[CANT_CARACTERES_MAX];
    int i = 0, puntoEncontrado = 0, espacioEncontrado = 0, enterEncontrado = 0;

    FILE* archivoEntrada;
    archivoEntrada = fopen(nomTexto, "r");

    if (archivoEntrada == NULL) {
        printf("Hubo un problema al abrir el archivo %s\n", nomTexto);
        return NULL;
    }
    while ( (c = fgetc(archivoEntrada)) != EOF) {

        if (c >= 'A' && c <= 'Z') {
            resultado[i++] = tolower(c);
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }
        
        else if ((c >= 'a' && c <= 'z') || (c>= '0' && c<= '9')) {
            resultado[i++] = c;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        } 
        else if (c == ' ' && !espacioEncontrado && !puntoEncontrado && !enterEncontrado) {
            resultado[i++] = c;
            espacioEncontrado = 1;
            enterEncontrado = 0;
            puntoEncontrado=0;
        }

        else if (c == '.') {
            resultado[i++] = '\n';
            puntoEncontrado = 1;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }

        else if (c == '\n' && !puntoEncontrado && !enterEncontrado && !espacioEncontrado) {
            resultado[i++] = ' ';
            enterEncontrado = 1;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
        }
    }
    // nos aseguramos de agregar terminador al final de la cadena
    if (i>1) {
        resultado[i]='\0';
    }
    
    // copiamos el resultado en un puntero a char, para retornarlo al scope del main
    char* resultadoCopia = malloc((sizeof(char)*i)+1);
    strcpy(resultadoCopia, resultado);

    fclose(archivoEntrada);
    return resultadoCopia;
}

int recorrer_y_limpiar(char** textos, char* rutaArtista, char* nomArchivoDestino) {
    char *textoLimpio;
    int i=0;
    FILE* archivoDestino = fopen(nomArchivoDestino, "w");
    
    if (archivoDestino == NULL) {
        printf("Error: No se pudo abrir el archivo de destino\n");
        return -1;
    }
    while (textos[i] != NULL) {
        char* cadenasRutaTexto[] = {rutaArtista, "/", textos[i]};
        char* rutaTexto = armar_cadena(cadenasRutaTexto, 3);
        // reemplazamos el "enter" al final de cada oracion por un terminador
        rutaTexto[strlen(rutaTexto)-1] = '\0';

        textoLimpio = limpiar_texto(rutaTexto);
        if (textoLimpio == NULL) {
            return -1;
        }
        fputs(textoLimpio, archivoDestino);
        fputc('\n', archivoDestino);

        free(rutaTexto);
        free(textoLimpio);
        free(textos[i]);
        i++;
    }
    fclose(archivoDestino);
    return 0;
}

int llamar_python(char* args) {
    char* cadenasComando[] = {"python3 main.py ", args};
    char* comandoLlamadaPython = armar_cadena(cadenasComando, 2);
    if (system(comandoLlamadaPython) != 0) {
        printf("Error: no se pudo llamar al script en python.\n");
        return -1;
    }
    free(comandoLlamadaPython);
    return 0;
}
void test_armar_cadena() {
    char* palabras1[] = {"Esto", " ", "es", " UNA ", "prueba!"};
    char* palabras2[] = {"SoloUnaPalabra"};
    //?
    char* palabras3[] = {NULL};
    char *test1, *test2, *test3;

    test1 = armar_cadena(palabras1, 5);
    assert(strcmp(test1, "Esto es UNA prueba!") == 0);
    
    test2 = armar_cadena(palabras2, 1);
    assert(strcmp(test2, "SoloUnaPalabra") == 0);
    
    test3 = armar_cadena(palabras3, 0);
    assert(strcmp(test3, "") == 0);

    free(test1);
    free(test2);
    free(test3);
    printf("-Los test de armar_cadena pasaron exitosamente.\n");
}

void liberar_textos(char** textos) {
    
    if (textos != NULL) {
        for (int i = 0; textos[i] != NULL; i++) {
                free(textos[i]);
        }
    }
    free(textos);
}

void test_obtener_textos() {
    // Test case 1: Provide a valid directory
    char** textos1 = obtener_textos("Tests/Textos/Andres_Calamaro");
    assert(textos1 != NULL);
    assert(strcmp(textos1[0],"flaca.txt\n") == 0);
    assert(strcmp(textos1[1],"mienfermedad.txt\n") == 0);
    assert(strcmp(textos1[2],"tequieroigual.txt\n") == 0);
    
    char** textos2 = obtener_textos("Tests/Textos#Andres_Calamaro.txt");
    assert(textos2 == NULL);
   
    char** textos3 = obtener_textos("Tests/Textos/Gustavo_Cerati");
    assert(textos3 != NULL);
    assert(strcmp(textos3[0],"crimen.txt\n") == 0);
    assert(strcmp(textos3[1],"jugodeluna.txt\n") == 0);
    assert(strcmp(textos3[2],"karaoke.txt\n") == 0);

    char** textos4 = obtener_textos("Tests/Textos/Cantante1");
    assert(textos4 == NULL);

    liberar_textos(textos1);
    liberar_textos(textos2);
    liberar_textos(textos3);
    liberar_textos(textos4);
    
    printf("-Los test de obtener_textos pasaron\n");
}
void test_limpiar_texto() {
    char* result1 = limpiar_texto("Tests/archivo_a_limpiar.txt");
    assert(result1 != NULL);
    assert(strcmp(result1, "este texto va a ser limpiado menos mal") == 0);
    char* result2 = limpiar_texto("nonexistent_file.txt");
    assert(result2 == NULL);
    
    free(result1);
    free(result2);
    printf("-Los test de limpiar_texto pasaron\n");
}
void test_recorrer_y_limpiar() {
    char** textos1 = malloc(sizeof(char*) * 4);
    textos1[0] = strdup("texto1.txt\n");
    textos1[1] = strdup("texto2.txt\n");
    textos1[2] = strdup("texto3.txt\n");
    textos1[3] = NULL;

    char *rutaArtista = malloc(sizeof(char)*50);
    char *nomArchDestino = malloc(sizeof(char)*50);
    strcpy(rutaArtista, "Tests/Textos/Cantante2");
    strcpy(nomArchDestino, "Tests/salida.txt");
    int result1 = recorrer_y_limpiar(textos1, rutaArtista, nomArchDestino);
    //abrir arch, fijarse si tiene lo que deberia
    FILE* archSalida = fopen("Tests/salida.txt", "r");
    char linea[LONGITUD_MAX_LINEA];
    char** contenidoLinea = malloc(sizeof(char *)*30);
    int i=0;
    while( fgets(linea, LONGITUD_MAX_LINEA, archSalida)) {
        //printf("linea: %s\n", linea);
        contenidoLinea[i] = malloc(sizeof(char)*50);
        strcpy(contenidoLinea[i], linea);
        i++;
    }
    contenidoLinea[i] = NULL;
    assert(strcmp(contenidoLinea[0], "este es el primer texto\n") == 0);
    assert(strcmp(contenidoLinea[1], "el que le sigue al primero es el segundo\n") == 0);
    assert(strcmp(contenidoLinea[2], "este archivo de texto es el segundo\n") == 0);
    assert(strcmp(contenidoLinea[3], "por ultimo este es el tercero\n") == 0);
    assert(strcmp(contenidoLinea[4], "este es el ultimo texto\n") == 0);
    assert(strcmp(contenidoLinea[5], "\n") == 0);

    printf("los test de recorrer_y_limpiar pasaron\n");
    liberar_textos(contenidoLinea);
    fclose(archSalida);
    free(textos1);
    free(rutaArtista);
    free(nomArchDestino);
}


int main(int argc, char** argv) {

    int verif, llamadaPython;
    char* rutaArtista, **textos, *nomArchivoDestino;
    
    if (argc != 2) {
        printf("Numero de argumentos incorrecta.\nUso: ./main nombre_de_artista\n");
        return 0;
    }
    char* cadenasRutaArtista[] = {RUTA_A_LEER, argv[1]};
    rutaArtista = armar_cadena(cadenasRutaArtista, 2);

    textos = obtener_textos(rutaArtista);
    if (textos == NULL) {
        free(rutaArtista);
        return -1;
    }

    char* cadenasArchDest[] = {RUTA_A_ESCRIBIR, argv[1], ".txt"};
    nomArchivoDestino = armar_cadena(cadenasArchDest, 3);

    verif = recorrer_y_limpiar(textos, rutaArtista, nomArchivoDestino);
    if (verif != 0) {
        return -1;
    }

    free(textos);
    free(rutaArtista);
    free(nomArchivoDestino);

    llamadaPython = llamar_python(argv[1]);
    if (llamadaPython != 0) {
        return -1;
    }
    
    test_armar_cadena();
    test_obtener_textos();
    test_limpiar_texto();
    test_recorrer_y_limpiar();
    return 0;
}