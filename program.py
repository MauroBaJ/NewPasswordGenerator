import mysql.connector
from cryptography.fernet import Fernet
import sys, random, os.path
from os import path


def genWordList():
    file = open("dictionary.txt", "r")
    arr= []
    lines = file.readlines()
    for line in lines:
        arr.append(line.rstrip())
    return arr

def pickRandomWords(number):
    pw = ""
    words = genWordList()
    n = 0
    while(n < number):
        pw = pw + random.choice(words)
        n += 1
    return pw

def genRandomPassword():
    print("Cuantas palabras desea? Eliga de 4 a 8")
    num = int(input())
    npw = pickRandomWords(num)
    return npw

db = mysql.connector.connect(
    host = 'localhost',
    user = 'admin',
    password = 'Mauricio2305',
    database = 'password_gen'
)

def generate_key():
    #Genera una llave y la guarda en un archivo
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    #Carga la llave
    return open("secret.key", "rb").read()

def encrypt_password(password):
    key = load_key()
    password = bytes(password, 'utf-8')
    f = Fernet(key)
    encrypted_password = f.encrypt(password)
    return encrypted_password

def decrypt_password(text):
    key = load_key()
    f = Fernet(key)
    decrypted_message= f.decrypt(text)
    password = decrypted_message.decode()
    return password

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

def insert(appName, username, password):
    query = "INSERT INTO passwords (appName, username, password) VALUES (%s, %s, %s)"
    values = (appName, username, password)
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    print("Registrado con exito")    
    


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
    
def opc2():
    print('A que aplicacion le cambiara el password?')
    app = input()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT idPassword FROM passwords WHERE LOWER(appName) LIKE LOWER('%" + app +"%')")
        result = cursor.fetchone()
    except:
        print("Ha ocurrido un error")
        print("Por motivos de seguridad, esta aplicacion se cerrara")
        sys.exit()
    if( result[0] ):
        cur2 = db.cursor()
        print("Ingrese el nombre de usuario: ")
        username = input()
        print("Desea crear una contraseña o añadir una existente? 1 / 2")
        opc = int(input())
        if(opc == 1):
            ##Crear Contraseña
            password = genRandomPassword()
        elif(opc == 2):
            print("Ingrese la contraseña: ")
            password = input()
        else: return
        print("Los datos son correctos? S/N\n")
        print('Usuario:' + username)
        print('Password:' + password)
        opcion = input()
        if(opcion == "s" or opcion == "S"):
            crp = encrypt_password(password)
            query = "UPDATE passwords SET username = '" + username + "', password = " + str(crp)[1:] + " WHERE idPassword = " + str(result[0])
            print(query)
            cur2.execute(query)
            db.commit()
            print('Se logro exitosamente')
        else: return
    else: print('No se encontro una cuenta que coincida')



def opc3():
    print('A que aplicacion le asignara este usuario? ')
    appName = input()
    print("Ingrese el nombre de usuario: ")
    username = input()
    print("Desea crear una contraseña o añadir una existente? 1 / 2")
    opc = int(input())
    if(opc == 1):
        ##Crear Contraseña
        password = genRandomPassword()
    elif(opc == 2):
        print("Ingrese la contraseña: ")
        password = input()
    else: return
    encrypted = encrypt_password(password)
    insert(appName, username, encrypted)

def opc4():
    print('Que aplicacion desea eliminar?')
    app = input()
    try:
        cursor = db.cursor(dictionary = True)
        cursor.execute("SELECT * FROM passwords WHERE LOWER(appName) LIKE LOWER('%" + app +"%')")
        results = cursor.fetchall()
    except:
        print("Ha ocurrido un error")
        print("Por motivos de seguridad, esta aplicacion se cerrara")
        sys.exit()
    finally:
        print("Se han encontrado ", len(results)," registros que concuerdan, desea visualizarlos? S/N")
        option = input()
        if( option == 'S' or option == 's'):
            for result in results:
                print("\n")
                print("#" + str(result["idPassword"]) + ": " + result["appName"] + " con username " + result["username"])
                print("Desea eliminar este registro? S/N")
                op = input()
                if(op == 's' or op == 'S'):
                    print("Seguro que desea eliminar este registro? S/N")
                    op2 = input()
                    if(op2 == 's' or op2 == 'S'):
                        print("Eliminando....")
                        cur2 = db.cursor()
                        print("DELETE FROM passwords WHERE idPassword = ", result["idPassword"])
                            # cur2.execute("DELETE FROM passwords WHERE idPassword = ", result["idPassword"])


if(path.exists("secret.key") == False):
    generate_key()
menu()