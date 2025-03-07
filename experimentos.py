from estructuras import Matriz, ListaParejas
from graficas import Graficas, generar_grafico_paso, generar_grafico_completo

experimentos = []

class Experimento:
    def __init__(self,nombre,filas,columnas):
        self.nombre = nombre
        self.filas = int(filas)
        self.columnas = int(columnas)
        self.rejilla = Matriz(self.filas, self.columnas)
        self.reactivas = ListaParejas()
        # Contador para llevar el registro de células que se volvieron X
        self.celulas_inertes_total = 0
    
    def establecer_proteina(self, fila, columna, proteina):
        return self.rejilla.establecer(fila, columna, proteina)

    def agregar_pareja(self, prot1, prot2):
        self.reactivas.agregar(prot1, prot2)

    def __str__(self):
        matriz_str = ""
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                valor = self.rejilla.obtener(i, j) or ""
                fila.append(str(valor))
            matriz_str += " ".join(fila) + "\n"

        parejas_str = ""
        for i in range(self.reactivas.parejas.tamano):
            pareja = self.reactivas.parejas.obtener(i)
            if i > 0:
                parejas_str += ", "
            parejas_str += f"{pareja.prot1} {pareja.prot2}"
        
        if not parejas_str:
            parejas_str = "Ninguna"

        return (
            f"Experimento: {self.nombre}\n"
            f"Dimensión: {self.filas}x{self.columnas}\n"
            f"Rejilla:\n{matriz_str}"
            f"Parejas: {parejas_str}"
        )

def show_rejilla(rejilla):
    for i in range(rejilla.filas):
        fila = []
        for j in range(rejilla.columnas):
            valor = rejilla.obtener(i, j)
            if valor is None or valor == "":
                fila.append("     ") 
            else:
                fila.append(f"{valor:^5}")  
        print(" ".join(fila))
    

def show_resultado(rejilla, celulas_inertes_total):
    
    total_celulas_actuales = 0
    
    for i in range(rejilla.filas):
        for j in range(rejilla.columnas):
            valor = rejilla.obtener(i, j)
            if valor and valor != "":
                total_celulas_actuales += 1
    
   
    total_celulas_original = total_celulas_actuales + celulas_inertes_total
    
    if total_celulas_original == 0:
        porcentaje = 0
    else:
        porcentaje = (celulas_inertes_total / total_celulas_original) * 100

    print("\nResultado del experimento")
    print(f"Células inertes: {celulas_inertes_total}")
    print(f"Total de células original: {total_celulas_original}")
    print(f"Porcentaje de células inertes: {porcentaje:.2f}%")

    if 30 <= porcentaje <= 60:
        print("Medicamento exitoso")
    elif porcentaje < 30:
        print("Medicamento no efectivo")
    else:
        print("Medicamento fatal")

def marcar_parejas_reactivas(rejilla, parejas):
    
    hubo_cambio = False
    
    for i in range(rejilla.filas):
        for j in range(rejilla.columnas - 1):
            prot1 = rejilla.obtener(i, j)
            prot2 = rejilla.obtener(i, j+1)
            
            if not prot1 or prot1 == "" or not prot2 or prot2 == "" or prot1 == 'X' or prot2 == 'X':
                continue
                
            if parejas.pareja_reactiva(prot1, prot2):
                rejilla.establecer(i, j, 'X')
                rejilla.establecer(i, j+1, 'X')
                hubo_cambio = True
    
    for i in range(rejilla.filas - 1):
        for j in range(rejilla.columnas):
            prot1 = rejilla.obtener(i, j)
            prot2 = rejilla.obtener(i+1, j)
            
            if not prot1 or prot1 == "" or not prot2 or prot2 == "" or prot1 == 'X' or prot2 == 'X':
                continue
                
            if parejas.pareja_reactiva(prot1, prot2):
                rejilla.establecer(i, j, 'X')
                rejilla.establecer(i+1, j, 'X')
                hubo_cambio = True
    
    return hubo_cambio

def colapsar_filas(rejilla):
    x_eliminadas = 0
    
    for i in range(rejilla.filas):
        nueva_fila = []
        for j in range(rejilla.columnas):
            valor = rejilla.obtener(i, j)
            if valor == 'X':
                x_eliminadas += 1
            elif valor and valor != "":
                nueva_fila.append(valor)

        while len(nueva_fila) < rejilla.columnas:
            nueva_fila.append("")
        
        for j in range(rejilla.columnas):
            rejilla.establecer(i, j, nueva_fila[j])
    
    return x_eliminadas

def colapsar_columnas(rejilla):
    x_eliminadas = 0
    
    for j in range(rejilla.columnas):
        nueva_columna = []
        for i in range(rejilla.filas):
            valor = rejilla.obtener(i, j)
            if valor == 'X':
                x_eliminadas += 1
            elif valor and valor != "":
                nueva_columna.append(valor)
        
        while len(nueva_columna) < rejilla.filas:
            nueva_columna.append("")
        for i in range(rejilla.filas):
            rejilla.establecer(i, j, nueva_columna[i])
    
    filas_no_vacias = []
    for i in range(rejilla.filas):
        fila_vacia = True
        for j in range(rejilla.columnas):
            if rejilla.obtener(i, j) != "":
                fila_vacia = False
                break
        if not fila_vacia:
            filas_no_vacias.append(i)
    
    nueva_rejilla = Matriz(len(filas_no_vacias), rejilla.columnas)
    for nuevo_i, i in enumerate(filas_no_vacias):
        for j in range(rejilla.columnas):
            nueva_rejilla.establecer(nuevo_i, j, rejilla.obtener(i, j))
    
    rejilla.filas = nueva_rejilla.filas
    rejilla.datos = nueva_rejilla.datos
    
    return x_eliminadas

def aplicar_accion(rejilla, parejas, celulas_inertes_total):

    hubo_cambio = marcar_parejas_reactivas(rejilla, parejas)
    
    if hubo_cambio:
        print("\nRejilla con células reactivas marcadas como X:")
        show_rejilla(rejilla)

        x_eliminadas_filas = colapsar_filas(rejilla)
        print("\nRejilla después de colapsar filas:")
        show_rejilla(rejilla)
        
        x_eliminadas_columnas = colapsar_columnas(rejilla)
        print("\nRejilla después de colapsar columnas:")
        show_rejilla(rejilla)
        
        celulas_inertes_total += max(x_eliminadas_filas, x_eliminadas_columnas)
        
        return True, celulas_inertes_total
    
    return False, celulas_inertes_total

def ejecutar_paso_paso(rejilla, parejas):
    paso = 0
    celulas_inertes_total = 0

    graficas = Graficas("experimento_paso_a_paso")
    
    graficas.agregar_paso(rejilla, f"Paso {paso}")
    
    print(f"\nPaso {paso}: ")
    show_rejilla(rejilla)
    
    while True:
        paso += 1
        print(f"\nPaso {paso}: ")

        accion, celulas_inertes_total = aplicar_accion(rejilla, parejas, celulas_inertes_total)
        graficas.agregar_paso(rejilla, f"Paso {paso}")
        generar_grafico_paso(graficas)

        if not accion:
            print("Experimento terminado")
            break
    
    show_resultado(rejilla, celulas_inertes_total)
   

def ejecutar_completo(rejilla, parejas):
    paso = 0
    celulas_inertes_total = 0

    graficas = Graficas("experimento_completo")
    graficas.set_estado_inicial(rejilla)
    
    print("\nEstado Inicial:")
    show_rejilla(rejilla)
    
    while True:
        paso += 1
        accion, celulas_inertes_total = aplicar_accion(rejilla, parejas, celulas_inertes_total)
        if not accion:
            break
    graficas.set_estado_final(rejilla)
    
  
    generar_grafico_completo(graficas)

    print(f"El experimento se completó en {paso-1} pasos")
    show_rejilla(rejilla)
    show_resultado(rejilla, celulas_inertes_total)
    print("Si")


def desarrollar_experimento(experimento):
    
    copia_rejilla = Matriz(experimento.filas, experimento.columnas)
    for i in range(experimento.filas):
        for j in range(experimento.columnas):
            valor = experimento.rejilla.obtener(i, j)
            copia_rejilla.establecer(i, j, valor)

    print("1. Paso a paso\n2. Completo")
    modo = int(input("Ingresa el modo en que quieres desarrollar el experimento: "))
    if modo == 1:
        ejecutar_paso_paso(copia_rejilla, experimento.reactivas)
    elif modo == 2:
        ejecutar_completo(copia_rejilla, experimento.reactivas)
    else:
        print("Opción no válida")


