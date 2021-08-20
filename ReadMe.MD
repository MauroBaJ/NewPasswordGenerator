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
Esta funcion le pide al usuario un dato para saber cuantas palabras debe concatenar, y es la que se llamara desde el menu. Se le pide al usuario de 4 a 8 palabras por los limites que puede llegar a tener el sistema de contraseñas de algunos sitios, sin embargo, pueden ser mas o menos.
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
____
La siguiente funcion solo carga la llave de encripcion para las siguientes.
```
def load_key():
    return open("secret.key", "rb").read()
```
___
### Encripcion y Desencripcion
___
La primera funcion es la de encriptar la contraseña que se le pase. Convierte el texto a formato de bytes, y luego utiliza las funciones de fermet para encriptarla.
```
def encrypt_password(password):
    key = load_key()
    password = bytes(password, 'utf-8')
    f = Fernet(key)
    encrypted_password = f.encrypt(password)
    return encrypted_password
```
La funcion de desencripcion es similar, pero en reversa. Cabe aclarar que la conversion de bytes a texto sucede al momento de hacer el fetch de la base de datos.
```
def decrypt_password(text):
    key = load_key()
    f = Fernet(key)
    decrypted_message= f.decrypt(text)
    password = decrypted_message.decode()
    return password

```
___
### Menu y Switch
Estas funciones son, como lo indica el titulo, el menu de opciones con las que cuenta el usuario, y la validacion de que opcion eligio el usuario.
```
def menu():
    opc = 0
    while( opc == 0):
        print('\n\n')
        print('________________________________________________________')
        print('1 - Ver Contraseñas\n')
        print('2 - Editar Contraseñas\n')
        print('3 - Crear nueva contraseña\n')
        print('4 - Eliminar Contraseñas\n')
        print('5 - Salir\n')
        print('\n\n')
        opc = int(input())
        val = checkForOption(opc)
    return
```
```
def checkForOption(opc):
    if( opc > 5): return 0
    elif(opc == 1):
        #READ
        opc1()
    elif(opc == 2):
        #UPDATE
        opc2()
    elif(opc == 3):
        #CREATE
        opc3()
    elif(opc == 4):
        #DELETE
        opc4()
    elif(opc == 5):
        return 1
    return 1
```
___

### Las opciones y el CRUD
____
En esta seccion se detallara el CRUD que realiza el programa sobre la base de datos. Por motivos desconocidos para mi, realize la operacion de insercio en una funcion a parte de su opcion.
___
#### Opcion 1 - Read
El programa realiza una consulta a la base de datos a partir de palabras similares a su busqueda. EN caso de contar con mas de un resultado obtenido se impimirán en el  for loop. Se convierte el resultado del query a un diccionario para tener la facilidad de imprimirlo mas tarde.
```
def opc1():
    print("De que servicio desea ver sus credenciales? ")
    service = input()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM passwords WHERE LOWER(appName) LIKE LOWER('%" + service +"%')")
    results = cursor.fetchall()
    for result in results:
        print("Usuario: " + result["username"])
        pw = bytes(result['password'], 'utf-8')
        print("Password: " + decrypt_password(pw))
    return 
```
___
#### Opcion 2   -   Update