import csv

def parsear_gramatica(archivo_gramatica):
    gramatica = {}
    with open(archivo_gramatica, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                no_terminal, producciones = linea.split('->')
                no_terminal = no_terminal.strip()
                producciones = [
                    produccion.strip().split()
                    for produccion in producciones.strip().split('|')
                ]
                gramatica[no_terminal] = producciones
    return gramatica

def calcular_conjuntos_primero(gramatica):
    conjuntos_primero = {}

    def calcular_primero(simbolo):
        if simbolo in conjuntos_primero:
            return conjuntos_primero[simbolo]
        conjunto_primero = set()
        if simbolo not in gramatica:
            conjunto_primero.add(simbolo)
        else:
            for produccion in gramatica[simbolo]:
                if not produccion:
                    conjunto_primero.add('')
                else:
                    conjunto_primero_primer_simbolo = calcular_primero(produccion[0])
                    conjunto_primero.update(conjunto_primero_primer_simbolo)
                    if '' in conjunto_primero_primer_simbolo and len(produccion) > 1:
                        for token in produccion[1:]:
                            conjunto_primero_token = calcular_primero(token)
                            conjunto_primero.update(conjunto_primero_token - {''})
                            if '' not in conjunto_primero_token:
                                break
        conjuntos_primero[simbolo] = conjunto_primero
        return conjunto_primero

    for no_terminal in gramatica:
        calcular_primero(no_terminal)
    return conjuntos_primero

def calcular_conjuntos_siguiente(gramatica, conjuntos_primero):
    conjuntos_siguiente = {no_terminal: set() for no_terminal in gramatica}
    simbolo_inicial = next(iter(gramatica))
    conjuntos_siguiente[simbolo_inicial].add('$')

    cambio = True
    while cambio:
        cambio = False
        for no_terminal in gramatica:
            for produccion in gramatica[no_terminal]:
                siguiente_final = conjuntos_siguiente[no_terminal]
                for i in range(len(produccion) - 1, -1, -1):
                    simbolo = produccion[i]
                    if simbolo in gramatica:
                        if siguiente_final.difference(conjuntos_siguiente[simbolo]):
                            conjuntos_siguiente[simbolo].update(siguiente_final)
                            cambio = True
                        if '' in conjuntos_primero[simbolo]:
                            siguiente_final = siguiente_final.union(conjuntos_primero[simbolo] - {''})
                        else:
                            siguiente_final = conjuntos_primero[simbolo]
    return conjuntos_siguiente

def construir_tabla_analisis(gramatica, conjuntos_primero, conjuntos_siguiente):
    tabla_analisis = {}
    for no_terminal, producciones in gramatica.items():
        for produccion in producciones:
            conjunto_primero = calcular_conjunto_primero_produccion(conjuntos_primero, produccion)
            for terminal in conjunto_primero:
                if terminal != '':
                    tabla_analisis.setdefault(no_terminal, {})[terminal] = produccion
            if '' in conjunto_primero:
                for terminal in conjuntos_siguiente[no_terminal]:
                    tabla_analisis.setdefault(no_terminal, {})[terminal] = produccion
    return tabla_analisis

def calcular_conjunto_primero_produccion(conjuntos_primero, produccion):
    conjunto_primero = set()
    for simbolo in produccion:
        conjunto_primero.update(conjuntos_primero[simbolo])
        if '' not in conjuntos_primero[simbolo]:
            break
    return conjunto_primero

def guardar_tabla_analisis_en_csv(tabla_analisis, archivo_csv):
    with open(archivo_csv, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        terminales = sorted({
            terminal for producciones in tabla_analisis.values() for terminal in producciones
        })
        escritor.writerow([''] + terminales)
        for no_terminal, producciones in sorted(tabla_analisis.items()):
            fila = [no_terminal] + [
                ' '.join(producciones.get(terminal, [])) for terminal in terminales
            ]
            escritor.writerow(fila)

if __name__ == "__main__":
    archivo_gramatica = "gramatica.txt"
    archivo_csv = "tabla_analisis.csv"
    gramatica = parsear_gramatica(archivo_gramatica)
    conjuntos_primero = calcular_conjuntos_primero(gramatica)
    conjuntos_siguiente = calcular_conjuntos_siguiente(gramatica, conjuntos_primero)
    print("Conjuntos de PRIMEROS (FIRST):")
    for no_terminal, primero in conjuntos_primero.items():
        print(f"{no_terminal}: {primero}")
    print("\nConjuntos de SIGUIENTES (FOLLOW):")
    for no_terminal, siguiente in conjuntos_siguiente.items():
        print(f"{no_terminal}: {siguiente}")
    tabla_analisis = construir_tabla_analisis(gramatica, conjuntos_primero, conjuntos_siguiente)
    guardar_tabla_analisis_en_csv(tabla_analisis, archivo_csv)
