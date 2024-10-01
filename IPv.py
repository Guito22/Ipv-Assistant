import os
import re
import signal
system = os.system
signal.signal(signal.SIGINT,lambda : 0)



system("title Programa de IPv4 e IPv6")
system("color 17")

input_ip="";mascara="";mascara_adaptada="";dir_inicio=""
cantidadRangos=0

def validarIntPositivo(mensaje,aux=1):
    while True:
        try:
            entrada = int(input(mensaje))
            if entrada<=0 and aux==1:
                raise ValueError
            if entrada<0 and aux==0:
                raise ValueError
            
            break
        except ValueError:
            system("cls")
            if aux==1:
                print("Debe ingresar un numero mayor a 0 válido")
            else:
                print("Debe ingresar un numero mayor o igual a 0 válido")


    return entrada

'''retorna el valor si es un float, el segundo parametro es opcional
0 para todos o 1 para solo positivos'''
def validarFloat(mensaje,op=0):
    while True:
        try:
            entrada = float(input(mensaje))
            if entrada<=0 and op==1:
                raise ValueError
            
            break
        except ValueError:
            system("cls")
            if op==1:
                print("Debe ingresar un numero mayor a 0 válido")
            else:
                print("Debe ingresar un numero válido")


    return entrada


def validarIPv4(mensaje):
    input_ip = input(mensaje)
    flag = 0

    pattern = r"^(\d{1,3}.){3}\d{1,3}$"
    match = re.match(pattern, input_ip)
    if (match):
        field = input_ip.split(".")
        for i in range(0, len(field)):
            if (int(field[i]) < 256):
                flag += 1
            else:
                flag = 0
    if (flag == 4):
        return input_ip
    else:
        return False

def claseRed():

    octetos = input_ip.split(".")
    primer_oct = int(octetos[0])
    if primer_oct<127:
        return "A"
    elif primer_oct<192:
        return "B"

    elif primer_oct<224:
        return "C"

def infoRed():
    print("Informacion de la red")
    print(f"Red Base: {input_ip}")
    print(f"Tipo de direccion base: Clase "+claseRed())
    match claseRed():
        case ("A"):
            print("Mascara: 255.0.0.0")
        case ("B"):
            print("Mascara: 255.255.0.0")
        case ("C"):
            print("Mascara: 255.255.255.0")
        

def validarMascaraAdaptada(mascara):
    
    octetosAdaptada = mascara.split(".")
    for i in range(0,4):
        octetosAdaptada[i]=int(octetosAdaptada[i])

    valoresValidos = [0,128,192,224,240,248,252,254,255]

    match claseRed():
        case ("A"):
            if octetosAdaptada[0]!=255:
                return False
            for i in range(1,4):
                if octetosAdaptada[i] in valoresValidos:
                    if octetosAdaptada[i]<255 and i<3:
                        for j in range(i+1,4):
                            if octetosAdaptada[j]>0:
                                return False
                else:
                    return False
        case ("B"):
            if octetosAdaptada[0]!=255:
                return False
            if octetosAdaptada[1]!=255:
                return False
            if octetosAdaptada[2] in valoresValidos:
                if octetosAdaptada[2]<255:
                    if octetosAdaptada[3]>0:
                        return False
                else:
                    if octetosAdaptada[3] not in valoresValidos:
                        return False
        case ("C"):
            for i in range(0,3):
                if octetosAdaptada[i]!=255:
                    return False
            if octetosAdaptada[3] not in valoresValidos:
                return False
            

    return True
                
def calcularBitsMascaraAdaptada(mascara):
    nuevos_bit_red = 0
    inicio=0
    octetosAdaptada = mascara.split(".")
    for i in range(0,4):
        octetosAdaptada[i]=int(octetosAdaptada[i])
    match claseRed():
        case ("A"):
            inicio=1
        case ("B"):
            inicio=2
        case ("C"):
            inicio=3

    for i in range(inicio,4):
        aux = octetosAdaptada[i]
        for j in range(7,-1,-1):
            aux = aux - 2**j
            if aux>=0:
                nuevos_bit_red+=1
            else:
                break
    
    return nuevos_bit_red

def calcularMascaraAdaptada(nuevosBitsRed):
    octetos = [255,0,0,0]
    if claseRed()=="B":
        octetos[1]=255
    if claseRed()=="C":
        octetos[1]=255
        octetos[2]=255

    for i in range(1,4):
        if octetos[i]==0:
            for j in range(7,-1,-1):
                if octetos[i]<255 and nuevosBitsRed>0:
                    octetos[i]+=2**j
                    nuevosBitsRed-=1
                else:
                    break


    return f"{octetos[0]}.{octetos[1]}.{octetos[2]}.{octetos[3]}"

def imprimirRangosIniciales(bitsLibres,nuevosBitsRed,cantidadRangos,vendidas):
    octetosDireccion = input_ip.split(".")
    for i in range(0,4):
        octetosDireccion[i]=int(octetosDireccion[i])
    
    print(f"{octetosDireccion[0]}.",end="")

    if claseRed()=="B" or claseRed=="C":
        print(f"{octetosDireccion[1]}.",end="")

    if claseRed()=="C":
        print(f"{octetosDireccion[2]}.",end="")

    for i in range(1,nuevosBitsRed+1):
        print(f" R",end="")
        if i%8==0:
            print(" .",end="")
    for i in range(1,bitsLibres+1):
        print(f" H",end="")
        if (i+nuevosBitsRed)%8==0 and i<bitsLibres:
            print(" .",end="")

    print("\n\n")

    for i in range(0,cantidadRangos):
        for j in range(0,3):
            print(f"{octetosDireccion[j]}.",end="")
        print(f"{octetosDireccion[3]}",end="") 

        for j in range(0,4):
            if bitsLibres>=8*(j+1):
                octetosDireccion[3-j]+=255
            else:
                octetosDireccion[3-j] += (2**(bitsLibres-(8*j)))-1
                break

        print("  -  ",end="")
        for j in range(0,3):
            print(f"{octetosDireccion[j]}.",end="")
        print(f"{octetosDireccion[3]}   ({i+1})",end="")
            
        if i==0 or i==(2**nuevosBitsRed)-1:
            print("   RESERVADA",end="")
        if vendidas>=i and i>0:
            print("   VENDIDA",end="")

        print("\n")

        for j in range(0,3):
            if octetosDireccion[3-j]==255:
                octetosDireccion[3-j]=0
            else:
                octetosDireccion[3-j]+=1
                break

    system("pause")                    

def avanzarDirecciones(inicio,cantidad):
    octetosDireccion = inicio.split(".")
    for i in range(0,4):
        octetosDireccion[i]=int(octetosDireccion[i])   

    print(f'Inicio: {inicio}')
    for i in range(0,cantidad):
        if octetosDireccion[3]<255:
            octetosDireccion[3]+=1
        else:
            octetosDireccion[3]=0
            if octetosDireccion[2]<255:
                octetosDireccion[2]+=1
            else:
                octetosDireccion[2]=0
                octetosDireccion[1]+=1


    print(f'{cantidad} adelante: {octetosDireccion[0]}.{octetosDireccion[1]}.{octetosDireccion[2]}.{octetosDireccion[3]}')
    system("pause")

def validarIPv6(direccion):
    pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'

    match = re.match(pattern,direccion)

    return True if match else False

def mostrarRangosInicialesIPv6(direccion,cantidad,bitsHost,bitsRed,vendidas):
    hextetos = direccion.split(":")
    nuevosBitsRed = 128-bitsRed-bitsHost
    hextetosRed = 0; aux=0;contadorNibbles=0
    for i in range(1,9):
        if bitsRed>=i*16:
            print(f"{hextetos[i-1]}:",end="")
            hextetosRed+=1


    print(" 0"*(int(bitsRed/4)-(hextetosRed*4))+" ",end="")
    contadorNibbles+=int(bitsRed/4)-(hextetosRed*4)

    if (bitsRed-(int(bitsRed/4)*4))>0:
        print("o"*(bitsRed-(int(bitsRed/4)*4)),end="")
        print("r"*(4-(bitsRed-(int(bitsRed/4)*4))),end="")
        aux+=4-(bitsRed-(int(bitsRed/4)*4))
        contadorNibbles+=1
        if contadorNibbles==4:
            print(" : ",end="")
        print(" ",end="")

    for i in range(1,nuevosBitsRed-aux+1):
        print("r",end="")
        if i%4==0:
            print(" ",end="")
            contadorNibbles+=1
            if contadorNibbles%4==0:
                print(": ",end="")

     
    if (128-bitsHost)%4!=0:
        print("h"*(bitsHost-(int(bitsHost/4)*4)),end="")
        contadorNibbles+=1
        if contadorNibbles%4==0:
                print(" : ",end="")      

    for i in range(1,int(bitsHost/4)+1):
        print(" H",end="")
        contadorNibbles+=1
        if contadorNibbles%4==0 and i!=int(bitsHost/4):
            print(" : ",end="")  
            
    print("\n")



    for i in range(0,8):
        hextetos[i] = hexToDec(hextetos[i])

    for i in range(0,cantidad):
        for j in range(0,7):
            print(f"{format(hextetos[j],"X")}:",end="")
        print(f"{format(hextetos[7],"X")}",end="")

        for j in range(0,8):
            if bitsHost>=16*(j+1):
                hextetos[7-j] += (2**16)-1
            else:
                hextetos[7-j] += (2**(bitsHost-(16*j)))-1
                break

        print(" - ",end="")
        for j in range(0,7):
            print(f"{format(hextetos[j],"X")}:",end="")
        print(f"{format(hextetos[7],"X")}",end="") 

        print(f"   ({i+1})",end="")
        if i==0 or i==(2**nuevosBitsRed)-1:
            print("   RESERVADA",end="")
        if vendidas>=i and i>0:
            print("   VENDIDA",end="")

        print("\n")

        for j in range(0,8):
            if hextetos[7-j]==2**(16)-1:
                hextetos[7-j] = 0
            else:
                hextetos[7-j] += 1
                break       
        
    system("pause")
    system("cls")   

def hexToDec(hexNum):
    if hexNum=='0000':
        hexNum='0'
    for i in range(0,2**16):
        if hexNum.upper()==format(i,"X"):
            return i
        

def avanzarDireccionesIPv6(direccion,cantidad):
    cadena_completa = ""
    nueva_direccion = []
    hextetos = direccion.split(":")
    for i in range(0,8):
        hextetos[i] = ('0'*(4-len(hextetos[i])))+hextetos[i]
        cadena_completa+=hextetos[i]

    hex_final = format((int(cadena_completa,16)+cantidad),"X")
    hex_final = '0'*(32-len(hex_final)) + hex_final
    print(f"{direccion}  -  ",end="")
    for i in range(0,8):
        nueva_direccion.append(hex_final[(4*i):((4*i)+4)])

    
    for i in range(0,7):
        print(f"{nueva_direccion[i]}:",end="")
    print(f"{nueva_direccion[7]}")

    system("pause")
    system("cls")




while True:
    print("Bienvenido al auxiliar de IPv4 e IPv6!!")
    print("1.- Ipv6")
    print("2.- Ipv4")
    print("3.- Salir")
    opcion = input("Respuesta: ")

    match opcion:
        case("1"):
            nuevos_bits_red_IPv6 = 0
            system("cls")
            print("IPv6")
            while True:
                dir_IPv6 = input("Ingrese la red base: ")
                system("cls")
                if validarIPv6(dir_IPv6):
                    break
                else:
                    print("DIRECCIÓN BASE INVÁLIDA!!")


            while True:
                bits_red_Ipv6 = validarIntPositivo("Ingrese cuantos bits de red tiene la red: ")
                system("cls")
                if bits_red_Ipv6>0 and bits_red_Ipv6<128:
                    break
                else:
                    print("No se pueden asignar tantos bits a red")


            while True:
                print("Ingrese una de las siguientes opciones: ")
                print("1.- Segmentar por cantidad de subredes minimas necesarias")
                print("2.- Segmentar por cantidad de direcciones por subred minimas necesarias")
                op_segmentacion_IPv6 = input("Respuesta: ")
                system("cls")
                if op_segmentacion_IPv6=="1" or op_segmentacion_IPv6=="2":
                    break
                else:
                    print("OPCIÓN INCORRECTA!!")

            if op_segmentacion_IPv6=="1":
                while True:
                    subredes_necesarias = validarIntPositivo("Cantidad de subredes minimas necesarias: ")
                    system("cls")
                    if subredes_necesarias<=2**(128-bits_red_Ipv6-2)-2:
                        break
                    else:
                        print("No se pueden crear esa cantidad de subredes")
                
                for i in range(1,128):
                    if (2**i)-2>=subredes_necesarias:
                        nuevos_bits_red_IPv6 = i
                        break
                 	 
                  
            else:
                while True:
                    dir_necesarias = validarIntPositivo("Cantidad de direcciones minimas necesarias por subred: ")
                    system("cls")
                    if dir_necesarias<=2**(128-bits_red_Ipv6-2)-2:
                        break
                    else:
                        print("No se pueden crear subredes con tantas direcciones")

                for i in range(1,128):
                    if (2**i)-2>=dir_necesarias:
                        nuevos_bits_red_IPv6 = 128-bits_red_Ipv6-i
                        break
            bitsHost = 128-(bits_red_Ipv6+nuevos_bits_red_IPv6)
            

            while True:
                print(f'Direccion Base: {dir_IPv6}')
                print(f'Bits de red para subred: {nuevos_bits_red_IPv6}')
                print(f'Bits de host para subred: {bitsHost}')
                print(f"Cantidad subredes utiles: {(2**nuevos_bits_red_IPv6)-2}")
                print(f"Cantidad de direcciones utiles por subred: {(2**bitsHost)-2}\n")

                print("Ingrese una de las siguientes opciones: ")
                print("1.- Mostrar rangos desde el inicio")
                print("2.- Calcular rango desde direccion especifica")
                print("3.- Calcular PV de red base, subred y direccion")
                print("4.- Salir")

                op_IPv6 = input("Respuesta: ")

                system("cls")

                match op_IPv6:
                    case ("1"):
                        while True:
                            cantidad = validarIntPositivo("Ingrese la cantidad de rangos que quiere ver: ")
                            system("cls")
                            
                            if cantidad<=2**(nuevos_bits_red_IPv6):
                                break
                            else:
                                print("No hay tantas subredes")
                        while True:
                            vendidas = validarIntPositivo("Ingrese cuantas redes han sido vendidas: ",0)
                            system("cls")

                            if vendidas<=2**(nuevos_bits_red_IPv6):
                                break
                            else:
                                print("No hay tantas subredes")
                        mostrarRangosInicialesIPv6(dir_IPv6,cantidad,bitsHost,bits_red_Ipv6,vendidas)

                    case ("2"):
                        while True:
                            cantidad = validarIntPositivo("Ingrese la cantidad de direcciones que quiere avanzar: ")
                            system("cls")
                            if cantidad<=2**(128-bits_red_Ipv6)-1:
                                break
                            else:
                                print("No puede avanzar tantas direcciones")
                        while True:
                            dir_inicio = input("Ingrese la direccion de inicio: ")
                            system("cls")
                            if validarIPv6(dir_inicio):
                                break
                            else:
                                print("Ingrese una direccion valida")

                        avanzarDireccionesIPv6(dir_inicio,cantidad)


                    case ("3"):
                        while True:
                            system("cls")
                            print(f'Direccion Base: {dir_IPv6}')
                            print(f'Bits de red para subred: {nuevos_bits_red_IPv6}')
                            print(f'Bits de host para subred: {bitsHost}')
                            print(f"Cantidad subredes utiles: {(2**nuevos_bits_red_IPv6)-2}")
                            print(f"Cantidad de direcciones utiles por subred: {(2**bitsHost)-2}\n")
                            print("Ingrese uno de los siguientes precios de compra: ")
                            print("1.- Red base")
                            print("2.- Subred")
                            print("3.- Direccion")
                            op_monto = input("Respuesta: ")
                            system("cls")
                            if op_monto>="1" and op_monto<="3":
                                break
                        

                        monto = validarFloat("Ingrese el monto ($): ",1)
                        system("cls")
                        margen = validarFloat("Ingrese el margen de ganancia: ")
                        system("cls")

                        subredes_vendibles = (2**nuevos_bits_red_IPv6)-2
                        dir_vendibles = subredes_vendibles*(2**(bitsHost)-2)
                        print("Precios de Venta:")
    
                        match op_monto:
                            case ("1"):
                                pvDirBase = monto/((100-margen)/100)
                                pvSubred = pvDirBase/subredes_vendibles
                                print("Se toma en cuenta que el costo de la red fue sin subnetear")
                                print(f"Direccion base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")

                            case ("2"):
                                print("SE TOMA EN CUENTA QUE YA ESTABA SUBNETEADA A LA HORA DE COMPRA")
                                pvSubred = monto/(((100-margen)/100))
                                pvDirBase = pvSubred*subredes_vendibles
                                print(f"Direccion Base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")
                            case ("3"):
                                print("Caso de que el costo de la direccion ya era con la red subneteada")

                                pvDir = monto/((100-margen)/100)
                                pvDirBase = pvDir*dir_vendibles
                                pvSubred = pvDir*(2**(bitsHost)-2)
                                print(f"Direccion Base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")
                                print(f"Direccion: {pvDir}$")

                                print("Caso de que el precio era por direccion util antes de subnetear")
                                nroDireccionesIniciales = (2**(128-bits_red_Ipv6))-2
                                pvDirBase = (monto*nroDireccionesIniciales)/((100-margen)/100)
                                pvSubred = pvDirBase/subredes_vendibles
                                pvDir = pvSubred/(2**(bitsHost)-2)
                                print(f"Direccion base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")
                                print(f"Direccion: {pvDir}$")

                            

                        system('pause')
                        system('cls')
                    case ("4"):
                        break
                    case _:
                        print("OPCIÓN INCORRECTA!!")
            
            


        case("2"):
            system("cls")
            print("IPv4")
            while True:
                input_ip = validarIPv4("Ingrese la direccion base: ")
                if input_ip:
                    break

                system("cls")
                print("Dirección IPv4 incorrecta")

            system("cls")
            
            while True:
                infoRed()

                bits_libres = 0
                nuevos_bit_red = 0
                if claseRed()=="A":
                    bits_libres=24
                elif claseRed()=="B":
                    bits_libres=16
                else:
                    bits_libres=8
                print(f"Bits de red: {32-bits_libres}, Bits de Host: {bits_libres}")
    
                print("\nIngrese una de las siguientes opciones de segmentacion: ")
                print("1.- Segmentar por cantidad de subredes necesarias")
                print("2.- Segmentar por cantidad de direcciones por subred necesarias")
                print("3.- Ingresar mascara adaptada")
                op_segmentacion = input("Respuesta: ")

                system("cls")

                if op_segmentacion>="1" and op_segmentacion<="3":
                    break


            match op_segmentacion:
                case ("1"):
                    cantidad = validarIntPositivo("Cantidad de subredes minima: ")

                    while cantidad>2**bits_libres:
                        system("cls")
                        print("No se pueden hacer tantas redes")
                        cantidad = validarIntPositivo("Cantidad de subredes utiles minima: ")

                    for i in range(1,bits_libres+1):
                        if cantidad<=(2**i)-2:
                            nuevos_bit_red=i
                            break

                    

                case ("2"):
                    cantidad = validarIntPositivo("Cantidad de direcciones utiles por subred minima: ")
                    for i in range(1,bits_libres+1):
                        if (2**i)-2>=cantidad:
                            nuevos_bit_red=bits_libres-i
                            break    


                case ("3"):
                    while True:
                        mascara_adaptada = input("Mascara adaptada: ")
                        system("cls")
                        if validarMascaraAdaptada(mascara_adaptada):
                            break
                        print("Ingrese una mascara adaptada valida")

                    nuevos_bit_red = calcularBitsMascaraAdaptada(mascara_adaptada)    





            while True:
                system("cls")
                infoRed()
                print(f"Mascara adaptada: {calcularMascaraAdaptada(nuevos_bit_red)}")
                print("\nIngrese una de las siguientes opciones:")
                print("1.- Calcular rangos desde el inicio")
                print("2.- Calcular rango desde direccion especifica")
                print("3.- Calcular PV de direccion base, subred y direccion")
                print("4.- Salir")
                opcion2 = input("Respuesta: ")
                system("cls")
                match opcion2:
                    case ("1"):
                        while True:
                            cantidad = validarIntPositivo("Ingrese la cantidad de rangos que quiere ver: ")
                            system("cls")
                            if cantidad<2**nuevos_bit_red:
                                break
                            else:
                                print(f"Solo hay {2**nuevos_bit_red} rangos")
                        while True:
                            vendidas = validarIntPositivo("Ingrese cuantas redes han sido vendidas: ",0)
                            system("cls")

                            if vendidas<=2**(nuevos_bit_red):
                                break
                            else:
                                print("No hay tantas subredes")


                        imprimirRangosIniciales(bits_libres-nuevos_bit_red,nuevos_bit_red,cantidad,vendidas)

                    case ("2"):
                        dir_inicio = validarIPv4("Ingrese la direccion desde la que se va a empezar a contar: ")
                        cantidad = validarIntPositivo("Ingrese la cantidad de direcciones que quiere avanzar: ")
                        avanzarDirecciones(dir_inicio,cantidad)

                    case ("3"):
                        while True:
                            system("cls")
                            print("Ingrese uno de los siguientes precios de compra: ")
                            print("1.- Red base")
                            print("2.- Subred")
                            print("3.- Direccion")
                            op_monto = input("Respuesta: ")
                            system("cls")
                            if op_monto>="1" and op_monto<="3":
                                break


                        monto = validarFloat("Ingrese el monto ($): ",1)
                        system("cls")
                        margen = validarFloat("Ingrese el margen de ganancia: ")
                        system("cls")

                        subredes_vendibles = (2**nuevos_bit_red)-2
                        dir_vendibles = subredes_vendibles*(2**(bits_libres-nuevos_bit_red)-2)
                        print(dir_vendibles)
                        print("Precios de Venta:")
                        match op_monto:
                            case ("1"):
                                pvDirBase = monto/((100-margen)/100)
                                pvSubred = pvDirBase/subredes_vendibles
                                pvDir = pvSubred/(2**(bits_libres-nuevos_bit_red)-2)
                                print(f"Direccion base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")
                                print(f"Direccion: {pvDir}$")

                            case ("2"):
                                print("SE TOMA EN CUENTA QUE YA ESTABA SUBNETEADA A LA HORA DE COMPRA")
                                pvSubred = monto/(((100-margen)/100))
                                pvDir = pvSubred/dir_vendibles
                                pvDirBase = pvSubred*subredes_vendibles
                                print(f"Direccion Base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")
                                print(f"Direccion: {pvDir}$")
                            case ("3"):
                                print("Caso de que el costo de la direccion ya era con la red subneteada")

                                pvDir = monto/((100-margen)/100)
                                pvDirBase = pvDir*dir_vendibles
                                pvSubred = pvDir*(2**(nuevos_bit_red)-2)
                                print(f"Direccion Base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")
                                print(f"Direccion: {pvDir}$")

                                print("Caso de que el precio era por direccion util antes de subnetear")
                                nroDireccionesIniciales = (2**bits_libres)-2
                                pvDirBase = (monto*nroDireccionesIniciales)/((100-margen)/100)
                                pvSubred = pvDirBase/subredes_vendibles
                                pvDir = pvSubred/(2**(bits_libres-nuevos_bit_red)-2)
                                print(f"Direccion base: {pvDirBase}$")
                                print(f"Subred: {pvSubred}$")
                                print(f"Direccion: {pvDir}$")
                                
                        system("pause")

                    case ("4"):
                        break

            system("pause")

        case("3"):
            break
        case _:
            print("OPCIÓN INCORRECTA!!")
    system("pause")
    system("cls")

print("Fin del programa")