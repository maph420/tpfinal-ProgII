//librerias
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
#include<dirent.h>

//macros
#define RUTA_A_LEER "Textos/"
#define RUTA_A_ESCRIBIR "Entradas/"
#define CANT_CARACTERES_MAX 2000

//funciones
char* procesar_texto(char* nomTexto) {
    FILE* archivoEntrada;
    archivoEntrada = fopen(nomTexto, "r");

    //?
    if (archivoEntrada == NULL) {
        exit(1);
    }
    char c;
    int i = 0;
    int puntoEncontrado = 0;
    int espacioEncontrado = 0;
    int enterEncontrado = 0;
    char resultado[CANT_CARACTERES_MAX];
    while ( (c = fgetc(archivoEntrada)) != EOF) {

        if (c >= 'A' && c <= 'Z') {
            resultado[i] = tolower(c);
            i++;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }
        
        else if ((c >= 'a' && c <= 'z')) {
            resultado[i] = c;
            i++;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }

        else if (c == ' ' && !espacioEncontrado && !puntoEncontrado) {
            espacioEncontrado = 1;
            resultado[i] = c;
            i++;
            enterEncontrado = 0;
        }

        else if (c == '.') {
            puntoEncontrado = 1;
            resultado[i] = '\n';
            i++;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }
        // reemplaza salto de linea por espacio (codigos ascii)
        else if (c == '\n' && !puntoEncontrado && !enterEncontrado) {
            resultado[i] = ' ';
            i++;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 1;
        }
    }
    if (i>0 && resultado[i-1] == '\n') {
        resultado[i-1]='\0';
    }
    
    char* resultadoCopia = malloc((sizeof(char)*i)+1);
    strcpy(resultadoCopia, resultado);
    //printf("resultado: %s\n", resultadoCopia);
    fclose(archivoEntrada);
    return resultadoCopia;
}

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("Numero de argumentos incorrecta.\nUso: ./main nombre_de_artista\n");
        return 0;
    }
  
    char rutaArtista[100];
    strcpy(rutaArtista, RUTA_A_LEER);
    strcat(rutaArtista, argv[1]);

    struct dirent *pDirent;
    DIR *controladorDir;
    controladorDir = opendir(rutaArtista);

    if (controladorDir == NULL) {
        printf("Error al abrir el archivo. Revisar argumento pasado.\n");
        return -1;
    }
    char nomArchivoDestino[100];
    FILE* archivoDestino;
    strcpy(nomArchivoDestino, RUTA_A_ESCRIBIR);
    strcat(nomArchivoDestino, argv[1]);
    strcat(nomArchivoDestino, ".txt");
    archivoDestino = fopen(nomArchivoDestino, "w");

    char rutaTexto[100];
    char* textoProcesado;

    // recorrer directorio
    while ((pDirent = readdir(controladorDir)) != NULL) {
        // ignorar directorios ocultos
        if (pDirent->d_name[0] != '.') {
            strcpy(rutaTexto, rutaArtista);
            strcat(rutaTexto, "/");
            strcat(rutaTexto, pDirent->d_name);
            textoProcesado = procesar_texto(rutaTexto);
            fputs(textoProcesado, archivoDestino);
            fputc('\n', archivoDestino);
            free(textoProcesado);
        }
    }
    closedir(controladorDir);
    fclose(archivoDestino);
    return 0;
}