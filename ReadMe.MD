# New Password Generator
___
Un Gestor de Contraseñas en linea de comandos

## ¿Qué es?
___
Este es un pequeño script dedicado a la administración de contraseñas. Fue realizado en Python, utilizando una base de datos MySQl para el almacenamieto.
____

### Librerias necesarias
Este programa utiliza una serie de librerias que nos ayudaran a realizar tareas más complicadas. Entre ella están:
-   MySQL
    - Connector
- Cryptography
    - Fernet
- Sys
- Random
- OS
    - Path

___

### Complementos
Dentro del repositorio hay unos archivos complementarios. Entre ellos se encuentran:
-  diceware_list.sh
    -   Este es un shell script que con ayuda de la libreria diceware (``` pip install diceware ```)
- dictionary.txt
    - El resultado de ejecutar el archivo anterior, este contiene varias palabra random de las cuales el programa elegira para poder elegir en caso de que el usuario decida generar la contraseña de forma automática.
- script.sql
    - Este es el comando basico para generar la tabla donde se almacenaran los datos
- secret.key
    -   la llave de encripcion y desencripcion de las contraseñas, nos sirve para almacenar los datos de la contraseña encriptadas.

____

## Funciones explicadas
___
### Generacion de Contraseñas
Esta funcion retorna una lista con todas las palabras que se encuentran en el archivo de dictionary. Las procesa para remover el salto de linea  (\n)
```
def genWordList():
    file = open("dictionary.txt", "r")
    arr= []
    lines = file.readlines()
    for line in lines:
        arr.append(line.rstrip())
    return arr
```
________
Esta funcion toma como valor el numero de palabras que vamos a utilizar para generar la contraseña, y nos retorna un string.

```
def pickRandomWords(number):
    pw = ""
    words = genWordList()
    n = 0
    while(n < number):
        pw = pw + random.choice(words)
        n += 1
    return pw
```
___
Esta funcion le pide al usuario un dato para saber cuantas palabras debe concatenar, y es la que se llamara desde el menu
```
def genRandomPassword():
    print("Cuantas palabras desea? Eliga de 4 a 8")
    num = int(input())
    npw = pickRandomWords(num)
    return npw
```
____

### Funciones de llaves de encripcion
____
La primera funcion es la de generar una llave. Para esto utiliza Fernet, de la libreria cryptography. Inicialmente generamos una llave y la guardamos como teto en bytes en el archivo secret.key. Esta va de la mano con una validadcion al inicio del cuerpo del programa que verifica que el archivo exista, y en caso de que exista, se omite esta funcion.
```
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
```
```
if(path.exists("secret.key") == False):
    generate_key()
```