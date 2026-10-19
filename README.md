# Proyecto No. 2 - Teoría de la Computación

Universidad del Valle de Guatemala  
Curso: Teoría de la Computación

## Descripción

Este proyecto implementa en Python un proceso completo para trabajar con gramáticas libres de contexto (CFG) y determinar si una cadena pertenece al lenguaje generado por una gramática mediante el algoritmo CYK (Cocke-Younger-Kasami).

El programa realiza las siguientes etapas:

1. Lectura de una gramática desde un archivo de texto.
2. Eliminación de producciones epsilon.
3. Eliminación de producciones unitarias.
4. Eliminación de símbolos inútiles.
5. Conversión de la gramática a Forma Normal de Chomsky (CNF).
6. Ejecución del algoritmo CYK.
7. Medición del tiempo de ejecución.
8. Construcción del parse tree cuando la frase pertenece al lenguaje.

La implementación utiliza una tabla de programación dinámica para el algoritmo CYK.

---

## Estructura del proyecto

```text
proyecto-2/
│
├── main.py
├── gramatica.py
├── simplificacion.py
├── cnf.py
├── cyk.py
├── arbol.py
├── README.md
├── DOCUMENTACION.md
│
├── entrada/
│   ├── 1.txt
│   ├── 1-cnf.txt
│   └── ingles.txt
│
└── salida/
    ├── gramatica_cnf.txt
    └── parse_tree.txt
```

### Archivos principales

`main.py`  
Coordina todo el programa: lectura, simplificación, conversión a CNF, ejecución de CYK y generación del parse tree.

`gramatica.py`  
Lee una gramática desde un archivo de texto y la representa mediante estructuras de Python.

`simplificacion.py`  
Implementa:
- eliminación de producciones epsilon;
- eliminación de producciones unitarias;
- eliminación de símbolos no productores;
- eliminación de símbolos no alcanzables.

`cnf.py`  
Convierte una gramática simplificada a Forma Normal de Chomsky.

`cyk.py`  
Implementa el algoritmo CYK mediante programación dinámica y mide su tiempo de ejecución.

`arbol.py`  
Reconstruye y muestra el parse tree de una frase aceptada.

---

## Gramática utilizada

La gramática principal utilizada para las pruebas con frases en inglés se encuentra en:

```text
entrada/ingles.txt
```

La gramática permite construir frases simples utilizando sustantivos, determinantes, verbos y frases preposicionales.

Ejemplos:

```text
She eats a cake with a fork
The cat drinks the beer
```

El programa convierte automáticamente la entrada a minúsculas antes de ejecutar CYK.

---

## Ejecución

No se requieren librerías externas.

Se necesita Python 3.

Desde la carpeta raíz del proyecto ejecutar:

```powershell
python .\main.py
```

El programa mostrará primero las diferentes etapas de simplificación de la gramática y posteriormente solicitará una frase.

Ejemplo:

```text
w = She eats a cake with a fork
```

---

## Forma Normal de Chomsky

Antes de ejecutar CYK, el programa convierte la gramática a Forma Normal de Chomsky.

Las producciones utilizadas por CYK tienen las formas:

```text
A -> B C
```

o:

```text
A -> terminal
```

Para producciones que originalmente contienen terminales junto con otros símbolos o más de dos símbolos, el programa genera no terminales auxiliares.

---

## Algoritmo CYK

CYK utiliza programación dinámica.

Primero se determinan los no terminales capaces de producir individualmente cada palabra de la frase.

Posteriormente se analizan fragmentos cada vez mayores de la entrada combinando resultados previamente calculados.

Una frase pertenece al lenguaje si el símbolo inicial de la gramática aparece en la celda que representa la frase completa.

El programa muestra:

- tabla CYK;
- frase analizada;
- resultado SÍ o NO;
- tiempo de ejecución;
- parse tree, si la frase es aceptada.

---

## Parse tree

Cuando una frase pertenece al lenguaje, el programa reconstruye el árbol sintáctico utilizando las decisiones almacenadas durante CYK.

También se guarda una copia en:

```text
salida/parse_tree.txt
```

Si una frase no pertenece al lenguaje, no se genera un parse tree anterior o inválido.

---

## Pruebas realizadas

### Prueba 1

Entrada:

```text
She eats a cake with a fork
```

Resultado:

```text
Pertenece al lenguaje: SÍ
```

Tiempo observado en una ejecución:

```text
0.00017350 segundos
```

Se generó correctamente el parse tree.

### Prueba 2

Entrada:

```text
The cat drinks the beer
```

Resultado:

```text
Pertenece al lenguaje: SÍ
```

Tiempo observado en una ejecución:

```text
0.00011840 segundos
```

Se generó correctamente el parse tree.

### Prueba 3

Entrada:

```text
The cat the beer
```

Resultado:

```text
Pertenece al lenguaje: NO
```

Tiempo observado en una ejecución:

```text
0.00013490 segundos
```

No se genera parse tree para una frase rechazada.

Los tiempos pueden variar ligeramente entre ejecuciones y equipos.

---

## Prueba adicional de simplificación y CNF

También se utilizaron:

```text
entrada/1.txt
entrada/1-cnf.txt
```

para comprobar la implementación de simplificación y conversión a Forma Normal de Chomsky.

La gramática original contiene producciones epsilon y producciones que todavía no cumplen CNF.

El programa realiza las transformaciones y obtiene una gramática equivalente a la gramática CNF proporcionada como referencia, aunque los nombres de los no terminales auxiliares generados pueden ser diferentes.

---

## Video

https://youtu.be/3UQtOxobXrw

---

## Autor

José Roberto Rodríguez Reyes