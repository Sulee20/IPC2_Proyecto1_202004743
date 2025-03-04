import os
import xml.etree.ElementTree as ET
from experimentos import Experimento, experimentos, desarrollar_experimento


def inicializar_sistema():
    global experimentos
    experimentos.clear()
    print("Sistema inicializado. Se han eliminado todos los experimentos.")

def crear_catalogo_experimentos():
    ruta = input("Ingrese la ruta del archivo xml: ")
    if not os.path.exists(ruta):
        print(f"La ruta '{ruta}' no existe")
    elif not os.path.isfile(ruta):
        print(f"'{ruta}' no es un archivo válido")
    else:
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            print(f"Archivo XML cargado con éxito")
            print(f"Elemento raíz: {root.tag}")

            for experimento_xml in root.findall('experimento'):
                nombre = experimento_xml.get('nombre')
                print(f"Experimento encontrado: {nombre}")

                tejido = experimento_xml.find('tejido')
                if tejido is not None:
                    filas = tejido.get('filas')
                    columnas = tejido.get('columnas')
                    print(f"Matriz de {filas} x {columnas}")

                    experimento_obj=Experimento(nombre, filas, columnas)

                    rejilla = tejido.find('rejilla')
                    if rejilla is not None:
                        print("Contenido de la rejilla:")
                        lineas = rejilla.text.strip().split('\n')
                        for i, linea in enumerate(lineas):
                            proteinas = linea.strip().split()
                            print(" ".join(proteinas))
                            for j, proteina in enumerate(proteinas):
                                experimento_obj.establecer_proteina(i, j, proteina)

                    proteinas = experimento_xml.find('proteinas')
                    if proteinas is not None:
                        print("\nParejas de proteínas:")
                        for pareja in proteinas.findall('pareja'):
                            par = pareja.text.strip().split()
                            if len(par) == 2:
                                prot1, prot2 = par
                                experimento_obj.agregar_pareja(prot1, prot2)
                                print(f"{prot1} {prot2}")
                    experimentos.append(experimento_obj)
            return experimentos
        except FileNotFoundError:
            print(f"El archivo '{ruta}' no fue encontrado.")
        except ET.ParseError:
            print(f"El archivo '{ruta}' no es un XML válido.")
        except Exception as e:
            print(f"Ocurrió un error al procesar el archivo: {e}")

def experimento_manual():
    nombre = input("Ingresa el nombre del experimento: ")
    try:
        filas = int(input("Ingresa el número de filas: "))
        columnas = int(input("Ingresa el número de columnas: "))
        if filas <= 0 or columnas <= 0:
            raise ValueError("Las filas y columnas deben ser mayores a 0")
    except ValueError as e:
        print(f"Error: {e}")
        return None
    
    experimento=Experimento(nombre, filas, columnas)
    
    print(f"Ingresa la matriz de {filas} x {columnas}")
    for i in range(filas):
        for j in range(columnas):
            proteina = input(f"Valor ({i+1}, {j+1}): ")
            experimento.establecer_proteina(i,j, proteina)
    
    print("\nLas rejillas son:")
    print(experimento)
    
    cant=int(input("Ingresa la cantidad de parejas en el experimento: "))
    while cant < 1:
        cant = int(input("Ingresa al menos una pareja: "))
    
    for i in range(cant):
        pareja = input(f"Ingresa la pareja {i+1} (formato: 'prot1 prot2'): ")
        par = pareja.split()
        if len(par) == 2:
            prot1, prot2 = par
            experimento.agregar_pareja(prot1, prot2)
    
    experimentos.append(experimento)
    return experimento  

def experimento_catalogo():
    if not experimentos:
        print("No hay experimentos en el catálogo.")
        return None
    
    for i, experimento in enumerate(experimentos):
        print(f"{i+1}. {experimento.nombre}")
    
    try:
        indice = int(input("\nSelecciona el número del experimento: ")) - 1
        if 0 <= indice < len(experimentos):
            print(experimentos[indice])
            return experimentos[indice]
        else:
            print("Índice no válido.")
            return None
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return None

def mostrar_datos_estudiante():
    print("Datos del estudiante:\nNombre: Mariana Sulecio\nCarne: 202004743\nCurso: IPC2\nCarrera: Ingeniería en Sistemas\n4to Semestre")

def menu_principal():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Inicializar sistema")
        print("2. Crear catálogo de experimentos")
        print("3. Desarrollar un experimento")
        print("4. Mostrar datos del estudiante")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            inicializar_sistema()
        elif opcion == "2":
            crear_catalogo_experimentos()
        elif opcion == "3":
            print("\n--- Menú Secundario ---")
            print("1. Crear experimento manualmente")
            print("2. Seleccionar experimento del catálogo")
            eleccion = input("Selecciona una opción: ")

            experimento_seleccionado = None
            if eleccion == "1":
                experimento_seleccionado = experimento_manual()
            elif eleccion == "2":
                experimento_seleccionado = experimento_catalogo()
            else:
                print("Elige una opción válida")
            
            if experimento_seleccionado:
                desarrollar_experimento(experimento_seleccionado)  
        elif opcion == "4":
            mostrar_datos_estudiante()
        elif opcion == "5":
            print("Hasta luego! :D")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

