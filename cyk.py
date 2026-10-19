# cyk.py

import time


def separar_reglas(gramatica):
    """
    Separa las producciones CNF en dos grupos.

    Terminales:
        A -> a

    Binarias:
        A -> B C
    """

    reglas_terminales = {}
    reglas_binarias = {}

    no_terminales = set(gramatica.keys())

    for izquierda, producciones in gramatica.items():

        for produccion in producciones:

            # ------------------------------------------
            # A -> terminal
            # ------------------------------------------

            if (
                len(produccion) == 1
                and produccion[0] not in no_terminales
            ):

                terminal = produccion[0]

                if terminal not in reglas_terminales:
                    reglas_terminales[terminal] = []

                if izquierda not in reglas_terminales[terminal]:
                    reglas_terminales[terminal].append(izquierda)

            # ------------------------------------------
            # A -> B C
            # ------------------------------------------

            elif (
                len(produccion) == 2
                and produccion[0] in no_terminales
                and produccion[1] in no_terminales
            ):

                pareja = (
                    produccion[0],
                    produccion[1]
                )

                if pareja not in reglas_binarias:
                    reglas_binarias[pareja] = []

                if izquierda not in reglas_binarias[pareja]:
                    reglas_binarias[pareja].append(
                        izquierda
                    )

    return reglas_terminales, reglas_binarias


def ejecutar_cyk(gramatica, tokens):
    """
    Ejecuta el algoritmo CYK.

    Devuelve:

    aceptada
    tabla
    caminos
    tiempo
    """

    inicio_tiempo = time.perf_counter()

    n = len(tokens)

    if n == 0:
        return False, [], {}, 0.0

    reglas_terminales, reglas_binarias = separar_reglas(
        gramatica
    )

    # --------------------------------------------------
    # Tabla CYK
    #
    # tabla[i][j] contiene los no terminales capaces
    # de generar los tokens desde i hasta j.
    # --------------------------------------------------

    tabla = []

    for i in range(n):

        fila = []

        for j in range(n):
            fila.append(set())

        tabla.append(fila)

    # --------------------------------------------------
    # Caminos para reconstruir el parse tree.
    #
    # clave:
    # (inicio, fin, no_terminal)
    # --------------------------------------------------

    caminos = {}

    # --------------------------------------------------
    # Primera diagonal:
    # producciones A -> terminal
    # --------------------------------------------------

    for i in range(n):

        token = tokens[i]

        if token in reglas_terminales:

            for no_terminal in reglas_terminales[token]:

                tabla[i][i].add(
                    no_terminal
                )

                caminos[
                    (i, i, no_terminal)
                ] = (
                    "terminal",
                    token
                )

    # --------------------------------------------------
    # Longitudes 2 ... n
    # --------------------------------------------------

    longitud = 2

    while longitud <= n:

        inicio = 0

        while inicio <= n - longitud:

            fin = inicio + longitud - 1

            # Probar todas las divisiones posibles.
            corte = inicio

            while corte < fin:

                izquierda = tabla[inicio][corte]
                derecha = tabla[corte + 1][fin]

                for B in izquierda:

                    for C in derecha:

                        pareja = (B, C)

                        if pareja in reglas_binarias:

                            for A in reglas_binarias[pareja]:

                                if A not in tabla[inicio][fin]:

                                    tabla[inicio][fin].add(A)

                                    caminos[
                                        (inicio, fin, A)
                                    ] = (
                                        "binaria",
                                        corte,
                                        B,
                                        C
                                    )

                corte += 1

            inicio += 1

        longitud += 1

    simbolo_inicial = next(iter(gramatica))

    aceptada = (
        simbolo_inicial
        in tabla[0][n - 1]
    )

    fin_tiempo = time.perf_counter()

    tiempo = fin_tiempo - inicio_tiempo

    return (
        aceptada,
        tabla,
        caminos,
        tiempo
    )


def mostrar_tabla_cyk(tabla, tokens):
    """
    Muestra solamente las celdas utilizadas
    de la tabla CYK.
    """

    print("\nTABLA CYK")
    print("-" * 60)

    n = len(tokens)

    for longitud in range(1, n + 1):

        print(
            f"\nLongitud {longitud}:"
        )

        for inicio in range(
            0,
            n - longitud + 1
        ):

            fin = inicio + longitud - 1

            contenido = tabla[inicio][fin]

            texto = ", ".join(
                sorted(contenido)
            )

            if not texto:
                texto = "∅"

            fragmento = " ".join(
                tokens[inicio:fin + 1]
            )

            print(
                f"[{inicio},{fin}] "
                f"{fragmento:<25} "
                f"{{{texto}}}"
            )