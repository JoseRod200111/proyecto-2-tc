# cnf.py


def crear_nombre(usados, prefijo):
    """
    Crea nombres nuevos como:

    T1, T2, T3...
    C1, C2, C3...

    evitando repetir nombres existentes.
    """

    numero = 1

    while True:

        nombre = f"{prefijo}{numero}"

        if nombre not in usados:
            usados.add(nombre)
            return nombre

        numero += 1


def convertir_terminales(gramatica):
    """
    En producciones de longitud 2 o mayor,
    reemplaza terminales por nuevos no terminales.

    Ejemplo:

    E -> ( E )

    se convierte primero en algo como:

    E -> T1 E T2

    T1 -> (
    T2 -> )
    """

    nueva = {}

    usados = set(gramatica.keys())

    # Guarda qué variable representa cada terminal.
    reemplazos = {}

    # Producciones nuevas de terminales.
    producciones_terminales = {}

    for izquierda, producciones in gramatica.items():

        nueva[izquierda] = []

        for produccion in producciones:

            # Si solamente hay un símbolo:
            #
            # A -> terminal
            #
            # ya es válido en CNF.
            if len(produccion) == 1:

                nueva[izquierda].append(
                    produccion.copy()
                )

                continue

            nueva_produccion = []

            for simbolo in produccion:

                # Si el símbolo es un no terminal,
                # se deja igual.
                if simbolo in gramatica:

                    nueva_produccion.append(simbolo)

                else:

                    # Es un terminal dentro de una
                    # producción larga.

                    if simbolo not in reemplazos:

                        nombre = crear_nombre(
                            usados,
                            "T"
                        )

                        reemplazos[simbolo] = nombre

                        producciones_terminales[nombre] = [
                            [simbolo]
                        ]

                    nueva_produccion.append(
                        reemplazos[simbolo]
                    )

            if nueva_produccion not in nueva[izquierda]:
                nueva[izquierda].append(
                    nueva_produccion
                )

    # Agregar las nuevas reglas:
    #
    # T1 -> (
    # T2 -> )
    # etc.
    for nombre, producciones in producciones_terminales.items():

        nueva[nombre] = producciones

    return nueva, reemplazos


def convertir_a_binarias(gramatica):
    """
    Convierte producciones de más de 2 símbolos
    en producciones binarias.

    Ejemplo:

    A -> B C D

    pasa a:

    A  -> B C1
    C1 -> C D
    """

    nueva = {}

    usados = set(gramatica.keys())

    # Permite reutilizar una variable si la misma
    # combinación ya apareció.
    combinaciones = {}

    for izquierda, producciones in gramatica.items():

        nueva[izquierda] = []

        for produccion in producciones:

            # Longitud 1 o 2:
            # ya cumple esta parte de CNF.
            if len(produccion) <= 2:

                if produccion not in nueva[izquierda]:
                    nueva[izquierda].append(
                        produccion.copy()
                    )

                continue

            # Ejemplo:
            #
            # [T1, E, T2]
            #
            # queremos:
            #
            # izquierda -> T1 C1
            # C1 -> E T2

            simbolos = produccion.copy()

            actual_izquierda = izquierda

            while len(simbolos) > 2:

                primero = simbolos[0]

                resto = tuple(simbolos[1:])

                # Si este mismo resto ya apareció,
                # reutilizamos el no terminal.
                if resto in combinaciones:

                    nuevo = combinaciones[resto]

                else:

                    nuevo = crear_nombre(
                        usados,
                        "C"
                    )

                    combinaciones[resto] = nuevo

                regla = [primero, nuevo]

                if actual_izquierda not in nueva:
                    nueva[actual_izquierda] = []

                if regla not in nueva[actual_izquierda]:
                    nueva[actual_izquierda].append(
                        regla
                    )

                # Si el resto tiene exactamente
                # dos símbolos, ya podemos crear
                # la producción final.
                if len(resto) == 2:

                    if nuevo not in nueva:
                        nueva[nuevo] = []

                    regla_resto = list(resto)

                    if regla_resto not in nueva[nuevo]:
                        nueva[nuevo].append(
                            regla_resto
                        )

                    simbolos = []
                    break

                actual_izquierda = nuevo
                simbolos = list(resto)

    return nueva


def convertir_a_cnf(gramatica):
    """
    Convierte una gramática ya simplificada
    a Forma Normal de Chomsky.

    Paso 1:
    reemplazar terminales dentro de producciones largas.

    Paso 2:
    dividir producciones de más de dos símbolos.
    """

    con_terminales, reemplazos = convertir_terminales(
        gramatica
    )

    cnf = convertir_a_binarias(
        con_terminales
    )

    return cnf, reemplazos


def guardar_gramatica(gramatica, ruta):
    """
    Guarda la gramática resultante en un archivo.
    """

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        for izquierda, producciones in gramatica.items():

            cuerpos = []

            for produccion in producciones:
                cuerpos.append(
                    " ".join(produccion)
                )

            linea = (
                izquierda
                + " -> "
                + " | ".join(cuerpos)
            )

            archivo.write(linea + "\n")