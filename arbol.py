# arbol.py


class NodoArbol:

    def __init__(
        self,
        valor,
        izquierdo=None,
        derecho=None
    ):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho


def construir_arbol(
    caminos,
    inicio,
    fin,
    simbolo
):
    """
    Reconstruye el parse tree usando
    la información guardada por CYK.
    """

    clave = (
        inicio,
        fin,
        simbolo
    )

    if clave not in caminos:
        return None

    informacion = caminos[clave]

    # ------------------------------------------
    # A -> terminal
    # ------------------------------------------

    if informacion[0] == "terminal":

        terminal = informacion[1]

        hijo = NodoArbol(
            terminal
        )

        return NodoArbol(
            simbolo,
            izquierdo=hijo
        )

    # ------------------------------------------
    # A -> B C
    # ------------------------------------------

    if informacion[0] == "binaria":

        corte = informacion[1]
        simbolo_izquierdo = informacion[2]
        simbolo_derecho = informacion[3]

        izquierdo = construir_arbol(
            caminos,
            inicio,
            corte,
            simbolo_izquierdo
        )

        derecho = construir_arbol(
            caminos,
            corte + 1,
            fin,
            simbolo_derecho
        )

        return NodoArbol(
            simbolo,
            izquierdo,
            derecho
        )

    return None


def obtener_lineas_arbol(nodo):
    """
    Convierte el árbol en líneas de texto
    usando solamente caracteres ASCII.
    """

    lineas = []

    def recorrer(
        actual,
        prefijo="",
        es_ultimo=True,
        es_raiz=False
    ):

        if actual is None:
            return

        if es_raiz:
            lineas.append(actual.valor)
            nuevo_prefijo = ""

        else:

            if es_ultimo:
                conector = "\\-- "
                nuevo_prefijo = prefijo + "    "
            else:
                conector = "|-- "
                nuevo_prefijo = prefijo + "|   "

            lineas.append(
                prefijo
                + conector
                + actual.valor
            )

        hijos = []

        if actual.izquierdo is not None:
            hijos.append(actual.izquierdo)

        if actual.derecho is not None:
            hijos.append(actual.derecho)

        for indice, hijo in enumerate(hijos):

            ultimo = (
                indice == len(hijos) - 1
            )

            recorrer(
                hijo,
                nuevo_prefijo,
                ultimo,
                False
            )

    recorrer(
        nodo,
        es_raiz=True
    )

    return lineas


def mostrar_arbol(nodo):
    """
    Muestra el parse tree en pantalla.
    """

    lineas = obtener_lineas_arbol(
        nodo
    )

    for linea in lineas:
        print(linea)


def guardar_arbol(
    nodo,
    ruta
):
    """
    Guarda el parse tree en un archivo de texto.
    """

    lineas = obtener_lineas_arbol(
        nodo
    )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        for linea in lineas:

            archivo.write(
                linea + "\n"
            )