# simplificacion.py


def encontrar_anulables(gramatica):
    """
    Encuentra los no terminales que pueden producir epsilon.

    Ejemplo:
    X -> e

    entonces X es anulable.
    """

    anulables = set()

    cambio = True

    while cambio:
        cambio = False

        for izquierda, producciones in gramatica.items():

            for produccion in producciones:

                # Caso directo:
                # X -> e
                if produccion == ["e"]:

                    if izquierda not in anulables:
                        anulables.add(izquierda)
                        cambio = True

                    continue

                # Caso indirecto:
                # A -> B C
                # si B y C son anulables,
                # entonces A también es anulable.

                todos_anulables = True

                for simbolo in produccion:

                    if simbolo not in anulables:
                        todos_anulables = False
                        break

                if todos_anulables:

                    if izquierda not in anulables:
                        anulables.add(izquierda)
                        cambio = True

    return anulables


def generar_variantes(produccion, anulables):
    """
    Genera las posibles producciones que aparecen
    al eliminar símbolos anulables.

    Ejemplo:

    T X

    si X es anulable:

    T X
    T
    """

    variantes = [[]]

    for simbolo in produccion:

        nuevas_variantes = []

        for variante in variantes:

            # Opción 1:
            # mantener el símbolo
            nueva = variante + [simbolo]

            if nueva not in nuevas_variantes:
                nuevas_variantes.append(nueva)

            # Opción 2:
            # eliminarlo si es anulable
            if simbolo in anulables:

                nueva = variante.copy()

                if nueva not in nuevas_variantes:
                    nuevas_variantes.append(nueva)

        variantes = nuevas_variantes

    return variantes


def eliminar_epsilon(gramatica):
    """
    Elimina las producciones epsilon de una gramática.
    """

    anulables = encontrar_anulables(gramatica)

    nueva_gramatica = {}

    # El primer no terminal del archivo
    # se toma como símbolo inicial.
    simbolo_inicial = next(iter(gramatica))

    for izquierda, producciones in gramatica.items():

        nuevas_producciones = []

        for produccion in producciones:

            # Ignorar directamente A -> e
            if produccion == ["e"]:
                continue

            variantes = generar_variantes(
                produccion,
                anulables
            )

            for variante in variantes:

                # No agregamos producción vacía,
                # excepto si el símbolo inicial
                # realmente puede producir epsilon.
                if len(variante) == 0:

                    if (
                        izquierda == simbolo_inicial
                        and simbolo_inicial in anulables
                    ):

                        if ["e"] not in nuevas_producciones:
                            nuevas_producciones.append(["e"])

                    continue

                if variante not in nuevas_producciones:
                    nuevas_producciones.append(variante)

        nueva_gramatica[izquierda] = nuevas_producciones

    return nueva_gramatica, anulables
def es_unitaria(produccion, gramatica):
    """
    Una producción es unitaria si tiene un solo símbolo
    y ese símbolo también es un no terminal.

    Ejemplo:
    E -> T
    """

    return (
        len(produccion) == 1
        and produccion[0] in gramatica
    )


def eliminar_unitarias(gramatica):
    """
    Elimina producciones unitarias como:

    E -> T
    T -> F

    copiando las producciones no unitarias
    de los no terminales alcanzables.
    """

    nueva_gramatica = {}

    for origen in gramatica:

        # No terminales alcanzables mediante
        # solamente producciones unitarias.
        alcanzables = [origen]

        cambio = True

        while cambio:
            cambio = False

            for actual in alcanzables.copy():

                for produccion in gramatica[actual]:

                    if es_unitaria(produccion, gramatica):

                        destino = produccion[0]

                        if destino not in alcanzables:
                            alcanzables.append(destino)
                            cambio = True

        # Ahora copiamos únicamente las producciones
        # que NO son unitarias.
        nuevas_producciones = []

        for no_terminal in alcanzables:

            for produccion in gramatica[no_terminal]:

                if not es_unitaria(produccion, gramatica):

                    if produccion not in nuevas_producciones:
                        nuevas_producciones.append(produccion)

        nueva_gramatica[origen] = nuevas_producciones

    return nueva_gramatica
def encontrar_productores(gramatica):
    """
    Encuentra los no terminales que pueden producir
    alguna cadena formada únicamente por terminales.
    """

    productores = set()
    cambio = True

    while cambio:
        cambio = False

        for izquierda, producciones in gramatica.items():

            for produccion in producciones:

                puede_producir = True

                for simbolo in produccion:

                    # Si es no terminal y todavía
                    # no sabemos que produce, falla.
                    if (
                        simbolo in gramatica
                        and simbolo not in productores
                    ):
                        puede_producir = False
                        break

                if puede_producir:

                    if izquierda not in productores:
                        productores.add(izquierda)
                        cambio = True

    return productores


def eliminar_no_productores(gramatica):
    """
    Elimina no terminales que nunca pueden producir
    una cadena de terminales.
    """

    productores = encontrar_productores(gramatica)

    nueva_gramatica = {}

    for izquierda, producciones in gramatica.items():

        if izquierda not in productores:
            continue

        nuevas_producciones = []

        for produccion in producciones:

            valida = True

            for simbolo in produccion:

                if (
                    simbolo in gramatica
                    and simbolo not in productores
                ):
                    valida = False
                    break

            if valida:
                nuevas_producciones.append(produccion)

        nueva_gramatica[izquierda] = nuevas_producciones

    return nueva_gramatica, productores


def encontrar_alcanzables(gramatica):
    """
    Encuentra los no terminales alcanzables
    desde el símbolo inicial.
    """

    simbolo_inicial = next(iter(gramatica))

    alcanzables = {simbolo_inicial}

    cambio = True

    while cambio:
        cambio = False

        for izquierda in list(alcanzables):

            if izquierda not in gramatica:
                continue

            for produccion in gramatica[izquierda]:

                for simbolo in produccion:

                    if (
                        simbolo in gramatica
                        and simbolo not in alcanzables
                    ):
                        alcanzables.add(simbolo)
                        cambio = True

    return alcanzables


def eliminar_no_alcanzables(gramatica):
    """
    Elimina no terminales a los que nunca se puede
    llegar desde el símbolo inicial.
    """

    alcanzables = encontrar_alcanzables(gramatica)

    nueva_gramatica = {}

    for izquierda, producciones in gramatica.items():

        if izquierda in alcanzables:
            nueva_gramatica[izquierda] = producciones

    return nueva_gramatica, alcanzables


def eliminar_inutiles(gramatica):
    """
    Elimina símbolos inútiles en el orden:

    1. No productores
    2. No alcanzables
    """

    sin_no_productores, productores = eliminar_no_productores(
        gramatica
    )

    resultado, alcanzables = eliminar_no_alcanzables(
        sin_no_productores
    )

    return resultado, productores, alcanzables