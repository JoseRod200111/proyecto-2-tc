# gramatica.py


def cargar_gramatica(ruta):
    """
    Lee una gramática desde un archivo de texto.

    Cada línea debe tener la forma:

    E -> T X | F Y | id

    Devuelve un diccionario como:

    {
        "E": [["T", "X"], ["F", "Y"], ["id"]],
        ...
    }
    """

    gramatica = {}

    with open(ruta, "r", encoding="utf-8") as archivo:

        for numero_linea, linea in enumerate(archivo, start=1):

            linea = linea.strip()

            # Ignorar líneas vacías
            if not linea:
                continue

            # Verificar que exista ->
            if "->" not in linea:
                raise ValueError(
                    f"Error en línea {numero_linea}: falta '->'"
                )

            izquierda, derecha = linea.split("->", 1)

            izquierda = izquierda.strip()
            derecha = derecha.strip()

            if not izquierda:
                raise ValueError(
                    f"Error en línea {numero_linea}: "
                    "falta el lado izquierdo"
                )

            if not derecha:
                raise ValueError(
                    f"Error en línea {numero_linea}: "
                    "falta el lado derecho"
                )

            # Separar las alternativas por |
            alternativas = derecha.split("|")

            producciones = []

            for alternativa in alternativas:

                alternativa = alternativa.strip()

                if not alternativa:
                    raise ValueError(
                        f"Error en línea {numero_linea}: "
                        "producción vacía"
                    )

                # Separar símbolos por espacios
                simbolos = alternativa.split()

                producciones.append(simbolos)

            if izquierda not in gramatica:
                gramatica[izquierda] = []

            gramatica[izquierda].extend(producciones)

    return gramatica


def mostrar_gramatica(gramatica):
    """
    Muestra una gramática de forma legible.
    """

    for izquierda, producciones in gramatica.items():

        cuerpos = []

        for produccion in producciones:
            cuerpos.append(" ".join(produccion))

        print(
            izquierda,
            "->",
            " | ".join(cuerpos)
        )