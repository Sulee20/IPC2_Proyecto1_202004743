import xml.etree.cElementTree as ET
import os

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
            desarrollar_experimento()
        elif opcion == "4":
            mostrar_datos_estudiante()
        elif opcion == "5":
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def inicializar_sistema():
    # Implementar la lógica para inicializar el sistema
    print("Sistema inicializado")

def crear_catalogo_experimentos():
    ruta=input("Ingrese la ruta del archivo xml: ")
    print("Catálogo de experimentos creado")
    if not os.path.exists(ruta):
        print(f"La ruta ' {ruta}' no existe")
    elif not os.path.isfile(ruta):
        print(f"'{ruta}' no es un archivo valido")
    else:
        try:
            tree=ET.parse(ruta)
            root= tree.getroot()

            print(f"Arcchivo XML cargado con exito")
            print(f"Elemento raiz: {root.tag}")

            for experimento in root.findall('experimento'):
                nombre=experimento.get('nombre')
                print(f"Experimento encontrado: {nombre}")
                tejido=experimento.find('tejido')
                if tejido is not None:
                    filas=tejido.get('filas')
                    columnas=tejido.get('columnas')
                    print(f"Matriz de {columnas} x {filas}")

                    rejilla=tejido.find('rejilla')
                    if rejilla is not None:
                        print("Contenido de la rejilla")
                        lineas=rejilla.text.strip().split('\n')
                        for linea in lineas:
                            print(linea.strip())

                proteinas=experimento.find('proteinas')
                if proteinas is not None:
                    print("\n parekja de proteinas:")
                    for pareja in proteinas.findall('pareja'):
                        print(pareja.text.strip())
        except ET.ParseError:
            print(f"El archivo '{ruta}' no es un xml valido")
        except Exception as e:
            print(f"Ocurrio un error al procesar el archivo: {e}")



def desarrollar_experimento():
    # Implementar la lógica para desarrollar un experimento
    print("Experimento desarrollado")

def mostrar_datos_estudiante():
    print("Datos del estudiante:\n Nombre: Mariana Sulecio\nCarne:202004743\nCurso: IPC2\nCarrera: Ingenieria en Sistemas\n4to Semestre")


menu_principal()