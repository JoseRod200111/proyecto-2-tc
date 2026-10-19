import os

from gramatica import (
    cargar_gramatica,
    mostrar_gramatica
)

from simplificacion import (
    eliminar_epsilon,
    eliminar_unitarias,
    eliminar_inutiles
)

from cnf import (
    convertir_a_cnf,
    guardar_gramatica
)

from cyk import (
    ejecutar_cyk,
    mostrar_tabla_cyk
)

from arbol import (
    construir_arbol,
    mostrar_arbol,
    guardar_arbol
)


def main():

    print("=" * 60)
    print("PROYECTO No. 2 - SIMPLIFICACIÓN DE CFG Y CYK")
    print("=" * 60)

    # --------------------------------------------------
    # ARCHIVO DE GRAMÁTICA
    # --------------------------------------------------

    ruta = "entrada/ingles.txt"

    print(f"\nArchivo de gramática: {ruta}")

    try:

        gramatica = cargar_gramatica(
            ruta
        )

    except FileNotFoundError:

        print("\nERROR:")
        print("No se encontró el archivo de gramática.")

        return

    except ValueError as error:

        print("\nERROR EN LA GRAMÁTICA:")
        print(error)

        return

    # --------------------------------------------------
    # GRAMÁTICA ORIGINAL
    # --------------------------------------------------

    print("\nGRAMÁTICA ORIGINAL")
    print("-" * 60)

    mostrar_gramatica(
        gramatica
    )

    # --------------------------------------------------
    # ELIMINACIÓN DE EPSILON
    # --------------------------------------------------

    print("\nELIMINACIÓN DE PRODUCCIONES EPSILON")
    print("-" * 60)

    (
        gramatica_sin_epsilon,
        anulables
    ) = eliminar_epsilon(
        gramatica
    )

    if anulables:

        print(
            "\nSímbolos anulables:",
            ", ".join(
                sorted(anulables)
            )
        )

    else:

        print(
            "\nNo existen símbolos anulables."
        )

    print(
        "\nGramática sin producciones epsilon:\n"
    )

    mostrar_gramatica(
        gramatica_sin_epsilon
    )

    # --------------------------------------------------
    # ELIMINACIÓN DE UNITARIAS
    # --------------------------------------------------

    print("\nELIMINACIÓN DE PRODUCCIONES UNITARIAS")
    print("-" * 60)

    gramatica_sin_unitarias = eliminar_unitarias(
        gramatica_sin_epsilon
    )

    print(
        "\nGramática sin producciones unitarias:\n"
    )

    mostrar_gramatica(
        gramatica_sin_unitarias
    )

    # --------------------------------------------------
    # ELIMINACIÓN DE SÍMBOLOS INÚTILES
    # --------------------------------------------------

    print("\nELIMINACIÓN DE SÍMBOLOS INÚTILES")
    print("-" * 60)

    (
        gramatica_simplificada,
        productores,
        alcanzables
    ) = eliminar_inutiles(
        gramatica_sin_unitarias
    )

    print(
        "\nSímbolos productores:",
        ", ".join(
            sorted(productores)
        )
    )

    print(
        "Símbolos alcanzables:",
        ", ".join(
            sorted(alcanzables)
        )
    )

    print(
        "\nGramática simplificada:\n"
    )

    mostrar_gramatica(
        gramatica_simplificada
    )

    # --------------------------------------------------
    # FORMA NORMAL DE CHOMSKY
    # --------------------------------------------------

    print("\nFORMA NORMAL DE CHOMSKY")
    print("-" * 60)

    (
        gramatica_cnf,
        reemplazos
    ) = convertir_a_cnf(
        gramatica_simplificada
    )

    print(
        "\nGramática en CNF:\n"
    )

    mostrar_gramatica(
        gramatica_cnf
    )

    guardar_gramatica(
        gramatica_cnf,
        "salida/gramatica_cnf.txt"
    )

    print(
        "\nGramática CNF guardada en:"
    )

    print(
        "salida/gramatica_cnf.txt"
    )

    # --------------------------------------------------
    # LIMPIAR PARSE TREE ANTERIOR
    # --------------------------------------------------

    ruta_arbol = "salida/parse_tree.txt"

    if os.path.exists(ruta_arbol):

        os.remove(
            ruta_arbol
        )

    # --------------------------------------------------
    # ENTRADA DE FRASE
    # --------------------------------------------------

    print("\nALGORITMO CYK")
    print("-" * 60)

    print(
        "\nIngrese una frase simple en inglés."
    )

    print(
        "Ejemplo: She eats a cake with a fork"
    )

    cadena_original = input(
        "\nw = "
    ).strip()

    # La gramática utiliza terminales en minúscula.
    cadena = cadena_original.lower()

    tokens = cadena.split()

    if not tokens:

        print(
            "\nLa frase está vacía."
        )

        return

    # --------------------------------------------------
    # EJECUTAR CYK
    # --------------------------------------------------

    (
        aceptada,
        tabla,
        caminos,
        tiempo
    ) = ejecutar_cyk(
        gramatica_cnf,
        tokens
    )

    # --------------------------------------------------
    # TABLA CYK
    # --------------------------------------------------

    mostrar_tabla_cyk(
        tabla,
        tokens
    )

    # --------------------------------------------------
    # RESULTADO
    # --------------------------------------------------

    print("\nRESULTADO")
    print("-" * 60)

    print(
        f"\nw = {cadena_original}"
    )

    if aceptada:

        print(
            "Pertenece al lenguaje: SÍ"
        )

    else:

        print(
            "Pertenece al lenguaje: NO"
        )

    print(
        f"Tiempo CYK: "
        f"{tiempo:.8f} segundos"
    )

    # --------------------------------------------------
    # PARSE TREE
    # --------------------------------------------------

    if aceptada:

        simbolo_inicial = next(
            iter(gramatica_cnf)
        )

        arbol = construir_arbol(
            caminos,
            0,
            len(tokens) - 1,
            simbolo_inicial
        )

        print("\nPARSE TREE")
        print("-" * 60)

        mostrar_arbol(
            arbol
        )

        guardar_arbol(
            arbol,
            ruta_arbol
        )

        print(
            "\nParse tree guardado en:"
        )

        print(
            ruta_arbol
        )

    else:

        print(
            "\nNo se genera parse tree "
            "porque la frase no pertenece "
            "al lenguaje."
        )

    print(
        "\nProceso terminado."
    )


if __name__ == "__main__":
    main()