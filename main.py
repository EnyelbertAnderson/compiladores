import ply.lex as lex

# Definición de tokens
tokens = [
    'PRINCIPAL', 'SUMA', 'MENOS', 'IGUAL', 'MULTI', 'DIVIDIR',
    'CORCHEI', 'CORCHED', 'PARENI', 'PAREND', 'LLAVEI', 'LLAVED', 'DIFERENTE',
    'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL', 'INCREMENTAR', 'DECREMENTAR',
    'MIENTRAS', 'PARA', 'FUNCION', 'PARAR', 'DEVOLVER', 'SI', 'SINO', 'ENTERO',
    'DECIMAL', 'LETRA', 'SIONO', 'PALABRA', 'MOSTRAR', 'INGRESAR', 'COMENTARIO',
    'COMA', 'FIN', 'ID', 'NUM'
]

# Expresiones regulares para tokens simples
t_PRINCIPAL = r'Principal'
t_SUMA = r'\+'
t_MENOS = r'-'
t_IGUAL = r'=='
t_MULTI = r'\*'
t_DIVIDIR = r'/'
t_CORCHEI = r'\['
t_CORCHED = r'\]'
t_PARENI = r'\('
t_PAREND = r'\)'
t_LLAVEI = r'\{'
t_LLAVED = r'\}'
t_DIFERENTE = r'<>'
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_INCREMENTAR = r'\+\+[a-zA-Z]*'
t_DECREMENTAR = r'--[a-zA-Z]*'
t_FUNCION = r'parte'
t_MIENTRAS = r'mientras'
t_PARA = r'para'  
t_PARAR = r'parar'
t_DEVOLVER = r'devolver'
t_SI = r'si'
t_SINO = r'sino'
t_ENTERO = r'entero'
t_DECIMAL = r'decimal'
t_LETRA = r'letra'
t_SIONO = r'siono'
t_PALABRA = r'palabra'
t_MOSTRAR = r'mostrar\("[^"]*"\)'  
t_INGRESAR = r'ingresar'
t_COMENTARIO = r'//'
t_COMA = r','
t_FIN = r';'

# Ignorar caracteres como espacios y tabulaciones
t_ignore = ' \t'

# Regla para ignorar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Definición de funciones para manejar tokens con acciones adicionales
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    reserved_words = {
        'PRINCIPAL', 'PARAR', 'ENTERO', 'DECIMAL', 'LETRA', 'SIONO',
        'MIENTRAS', 'PARA', 'FUNCION', 'PARAR', 'DEVOLVER', 'SI', 'SINO', 'MOSTRAR', 'INGRESAR'
    }
    if t.value.upper() in reserved_words:
        t.type = t.value.upper()
    else:
        t.type = 'ID'  # Devolver el tipo de token como 'ID' en lugar de la palabra reservada
    return t

# Función para manejar errores
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para leer las pruebas desde un archivo de texto
def leer_pruebas(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        return archivo.read()

# Nombre del archivo que contiene las pruebas
nombres_archivos_pruebas = ['pruebas.txt','pruebas2.txt','pruebas3.txt']

# Iterar sobre los archivos de pruebas
for nombre_archivo_pruebas in nombres_archivos_pruebas:
    # Leer las pruebas desde el archivo
    pruebas = leer_pruebas(nombre_archivo_pruebas)

    print(f"Tokens encontrados en '{nombre_archivo_pruebas}':")
    # Ejecutar el lexer sobre las pruebas
    lexer.input(pruebas)

    # Tokenizar las pruebas e imprimir los tokens encontrados
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    print()  # Agregar una línea en blanco entre los tokens de cada archivo
