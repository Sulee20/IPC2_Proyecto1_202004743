class Nodo:
    def __init__(self, dato=None) :
        self.dato= dato
        self.siguiente = None
class Lista:
    def __init__(self):
        self.cabeza=None
        self.cola=None 
        self.tamano= 0

    def vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevoNodo = Nodo(dato)
        if self.vacia():
            self.cabeza = nuevoNodo
            self.cola = nuevoNodo
        else:
            self.cola.siguiente = nuevoNodo
            self.cola = nuevoNodo
        self.tamano += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self.tamano:
            return None
        
        actual = self.cabeza
        for i in range(indice):
            actual = actual.siguiente
        return actual.dato

    def modificar(self, indice, nuevoDato):
        if indice <0 or indice>=self.tamano:
            return False
        
        actual=self.cabeza
        for i in range(indice):
            actual=actual.siguiente
        actual.dato=nuevoDato
        return True

class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.datos = Lista()  

        for i in range(filas):
            fila = Lista()
            for j in range(columnas):
                fila.agregar("")  
            self.datos.agregar(fila)  

    def establecer(self, fila, columna, valor):
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            return False
        
        fila_actual = self.datos.obtener(fila)
        if not isinstance(fila_actual, Lista):  
            print(f"Error: No se pudo obtener la fila {fila}")
            return False
    
        resultado = fila_actual.modificar(columna, valor)

        if not resultado:
            print(f"Error: No se pudo modificar la columna {columna} en la fila {fila}")
        
        return resultado
    
    def obtener(self, fila, columna):
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            return None

        fila_actual = self.datos.obtener(fila)
        if not isinstance(fila_actual, Lista):
            return None
        
        # Línea agregada para devolver el valor de la celda
        return fila_actual.obtener(columna)


class Pareja:
    def __init__(self, prot1, prot2):
        self.prot1=prot1
        self.prot2=prot2
    
    def coincide(self, prot1,prot2):
        return(self.prot1==prot1 and self.prot2==prot2) or \
            (self.prot1==prot2 and self.prot2==prot1)

class ListaParejas:
    def __init__(self):
        self.parejas=Lista()
    
    def agregar (self, prot1, prot2):
        nueva_pareja=Pareja(prot1,prot2)
        self.parejas.agregar(nueva_pareja)
        
    def obtener(self, indice):
        if indice < 0 or indice >= self.parejas.tamano:
            return None
        return self.parejas.obtener(indice)

    def pareja_reactiva(self, prot1, prot2):
        for i in range(self.parejas.tamano):
            pareja=self.parejas.obtener(i)
            if  pareja.coincide(prot1,prot2):
                return True
        return False

