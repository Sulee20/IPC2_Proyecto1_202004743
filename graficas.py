from graphviz import Digraph

class Graficas:
    def __init__(self, nombre="grafico"):
        self.nombre = nombre
        self.pasos = []
        self.inicial = None
        self.final = None

    def agregar_paso(self, matriz, titulo):
        dot = Digraph(format='png')
        dot.attr(rankdir='TB') 
        
        dot.attr('node', 
                shape='circle',
                style='filled',
                fillcolor='#E6E6FA',  
                fontsize='10',
                height='0.4',
                width='0.4')
        dot.attr('edge', 
                color='#808080',  
                arrowsize='0.5') 
        
        nodos = {}
        for i in range(matriz.filas):
            with dot.subgraph() as s:
                s.attr(rank='same')  
                for j in range(matriz.columnas):
                    valor = matriz.obtener(i, j)
                    if valor and valor != "":
                        nombre_nodo = f"{titulo}_{i}_{j}"
                        nodos[(i, j)] = nombre_nodo
                        s.node(nombre_nodo, valor)

        for i in range(matriz.filas):
            for j in range(matriz.columnas - 1):
                if (i, j) in nodos and (i, j+1) in nodos:
                    dot.edge(nodos[(i, j)], nodos[(i, j+1)])

        for i in range(matriz.filas - 1):
            for j in range(matriz.columnas):
                if (i, j) in nodos and (i+1, j) in nodos:
                    dot.edge(nodos[(i, j)], nodos[(i+1, j)])

        self.pasos.append((dot, titulo))

    def generar_grafico_paso(self):
        if not self.pasos:
            print("No hay pasos para graficar")
            return

        final = Digraph(format='png')
        final.attr(rankdir='TB')
        final.attr('graph', 
                  splines='ortho',  
                  nodesep='0.5',    
                  ranksep='1.0')    
        
        final.attr('node',
                  shape='circle',
                  style='filled',
                  fillcolor='#E6E6FA',
                  fontsize='10',
                  height='0.4',
                  width='0.4')
        final.attr('edge',
                  color='#808080',
                  arrowsize='0.5')

        for idx, (paso, titulo) in enumerate(self.pasos):
            titulo_id = f"titulo_{idx}"
            final.node(titulo_id, titulo, shape='none', fontsize='14', fontweight='bold')
            
            with final.subgraph(name=f'cluster_{idx}') as c:
                c.attr(style='invis')  
                
                for line in paso.body:
                    if not line.strip().startswith('graph'):
                        c.body.append(line)
                
                if paso.body:
                    for line in paso.body:
                        if 'label=' in line and 'shape=' in line:
                            node_id = line.split('[')[0].strip()
                            final.edge(titulo_id, node_id, style='invis')
                            break

            if idx < len(self.pasos) - 1:
                final.attr(ranksep='1.5')

        final.render(f"{self.nombre}_completo", format='png', cleanup=True)
        print(f"Gráfico completo generado en: {self.nombre}_completo.png")

    def set_estado_inicial(self, matriz):
        dot = Digraph(format='png')
        dot.attr(rankdir='TB')  
    
        dot.attr('node', 
                shape='circle',
                style='filled',
                fillcolor='#E6E6FA',  
                fontsize='10',
                height='0.4',
                width='0.4')
        dot.attr('edge', 
                color='#808080',  
                arrowsize='0.5')
        
        nodos = {}
        for i in range(matriz.filas):
            with dot.subgraph() as s:
                s.attr(rank='same')
                for j in range(matriz.columnas):
                    valor = matriz.obtener(i, j)
                    if valor and valor != "":
                        nombre_nodo = f"inicio_{i}_{j}"
                        nodos[(i, j)] = nombre_nodo
                        s.node(nombre_nodo, valor)

        for i in range(matriz.filas):
            for j in range(matriz.columnas - 1):
                if (i, j) in nodos and (i, j+1) in nodos:
                    dot.edge(nodos[(i, j)], nodos[(i, j+1)])

        for i in range(matriz.filas - 1):
            for j in range(matriz.columnas):
                if (i, j) in nodos and (i+1, j) in nodos:
                    dot.edge(nodos[(i, j)], nodos[(i+1, j)])

        self.inicial = dot

    def set_estado_final(self, matriz):
        dot = Digraph(format='png')
        dot.attr(rankdir='TB')
        
        dot.attr('node', 
                shape='circle',
                style='filled',
                fillcolor='#E6E6FA',
                fontsize='10',
                height='0.4',
                width='0.4')
        dot.attr('edge', 
                color='#808080',
                arrowsize='0.5')
        
        nodos = {}
        for i in range(matriz.filas):
            with dot.subgraph() as s:
                s.attr(rank='same')
                for j in range(matriz.columnas):
                    valor = matriz.obtener(i, j)
                    if valor and valor != "":
                        nombre_nodo = f"final_{i}_{j}"
                        nodos[(i, j)] = nombre_nodo
                        s.node(nombre_nodo, valor)

        for i in range(matriz.filas):
            for j in range(matriz.columnas - 1):
                if (i, j) in nodos and (i, j+1) in nodos:
                    dot.edge(nodos[(i, j)], nodos[(i, j+1)])

        for i in range(matriz.filas - 1):
            for j in range(matriz.columnas):
                if (i, j) in nodos and (i+1, j) in nodos:
                    dot.edge(nodos[(i, j)], nodos[(i+1, j)])

        self.final = dot

    def generar_grafico_completo(self):
        final = Digraph(format='png')
        final.attr(rankdir='TB')
        final.attr('graph', 
                  splines='ortho',
                  nodesep='0.5',
                  ranksep='2.0')  
        
        final.attr('node',
                  shape='circle',
                  style='filled',
                  fillcolor='#E6E6FA',
                  fontsize='10',
                  height='0.4',
                  width='0.4')
        final.attr('edge',
                  color='#808080',
                  arrowsize='0.5')

        
        final.node('titulo_inicio', 'Inicio', shape='none', fontsize='14', fontweight='bold')

        with final.subgraph(name='cluster_0') as c1:
            c1.attr(style='invis')
            for line in self.inicial.body:
                if not line.strip().startswith('graph'):
                    c1.body.append(line)

        final.node('titulo_final', 'Final', shape='none', fontsize='14', fontweight='bold')
        with final.subgraph(name='cluster_1') as c2:
            c2.attr(style='invis')
            for line in self.final.body:
                if not line.strip().startswith('graph'):
                    c2.body.append(line)

        if self.inicial.body:
            for line in self.inicial.body:
                if 'label=' in line and 'shape=' in line:
                    node_id = line.split('[')[0].strip()
                    final.edge('titulo_inicio', node_id, style='invis')
                    break

        if self.final.body:
            for line in self.final.body:
                if 'label=' in line and 'shape=' in line:
                    node_id = line.split('[')[0].strip()
                    final.edge('titulo_final', node_id, style='invis')
                    break
        
        final.render(f"{self.nombre}_inicio_fin", format='png', cleanup=True)
        print(f"Gráfico de inicio y fin generado en: {self.nombre}_inicio_fin.png")

def generar_grafico_paso(graficas_obj):
    graficas_obj.generar_grafico_paso()

def generar_grafico_completo(graficas_obj):
    graficas_obj.generar_grafico_completo()





