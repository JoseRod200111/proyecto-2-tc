# Documentación - Proyecto No. 2

## Teoría de la Computación

## 1. Introducción

El objetivo del proyecto es implementar el algoritmo CYK (Cocke-Younger-Kasami) para determinar si una frase pertenece al lenguaje generado por una gramática libre de contexto.

Debido a que CYK requiere una gramática en Forma Normal de Chomsky, antes de ejecutar el algoritmo se realiza un proceso de simplificación y conversión de la gramática.

El proyecto fue implementado en Python y trabaja con gramáticas almacenadas en archivos de texto.

---

## 2. Objetivos

Los objetivos principales de la implementación son:

- leer una gramática CFG desde un archivo;
- simplificar la gramática;
- eliminar producciones epsilon;
- eliminar producciones unitarias;
- eliminar símbolos inútiles;
- convertir la gramática a Forma Normal de Chomsky;
- implementar CYK utilizando programación dinámica;
- determinar si una frase pertenece al lenguaje;
- medir el tiempo utilizado por CYK;
- construir un parse tree para las frases aceptadas.

---

## 3. Diseño de la aplicación

El programa fue dividido en varios archivos para separar las diferentes responsabilidades.

### main.py

Es el punto de entrada del programa.

Coordina las siguientes etapas:

```text
Lectura de gramática
        |
        v
Eliminar epsilon
        |
        v
Eliminar unitarias
        |
        v
Eliminar símbolos inútiles
        |
        v
Conversión a CNF
        |
        v
Entrada de frase
        |
        v
Algoritmo CYK
        |
        v
Resultado SÍ / NO
        |
        v
Parse tree
```

### gramatica.py

Este archivo se encarga de leer la gramática.

Las producciones se almacenan en un diccionario de Python.

Por ejemplo:

```text
S -> NP VP
```

se representa aproximadamente como:

```python
{
    "S": [
        ["NP", "VP"]
    ]
}
```

Una producción con distintas alternativas:

```text
NP -> Det N | he | she
```

se representa como:

```python
{
    "NP": [
        ["Det", "N"],
        ["he"],
        ["she"]
    ]
}
```

Esta representación permite recorrer y modificar las producciones durante la simplificación.

---

## 4. Simplificación de gramáticas

### 4.1 Eliminación de producciones epsilon

Una producción epsilon permite que un no terminal genere la cadena vacía.

El primer paso consiste en encontrar los símbolos anulables.

Posteriormente se generan las posibles variantes de las producciones donde estos símbolos aparecen.

Por ejemplo, si:

```text
A -> B C
```

y `C` es anulable, se consideran:

```text
A -> B C
A -> B
```

Finalmente se eliminan las producciones epsilon originales, manteniendo las alternativas necesarias.

---

### 4.2 Eliminación de producciones unitarias

Una producción unitaria tiene la forma:

```text
A -> B
```

donde `A` y `B` son no terminales.

El programa identifica los no terminales que pueden alcanzarse utilizando únicamente producciones unitarias.

Después copia sus producciones no unitarias al no terminal original.

Por ejemplo:

```text
A -> B
B -> C
C -> x
```

permite reemplazar las conexiones unitarias por:

```text
A -> x
B -> x
C -> x
```

cuando corresponde.

---

### 4.3 Eliminación de símbolos inútiles

Los símbolos inútiles se analizan en dos etapas.

Primero se buscan símbolos productores.

Un no terminal es productor si puede generar finalmente una cadena formada por terminales.

Posteriormente se buscan símbolos alcanzables.

Un símbolo es alcanzable si puede aparecer en alguna derivación comenzando desde el símbolo inicial.

Los símbolos que no cumplen estas propiedades se eliminan de la gramática.

---

## 5. Forma Normal de Chomsky

El algoritmo CYK requiere trabajar con una gramática en Forma Normal de Chomsky.

Las producciones utilizadas tienen las siguientes formas:

```text
A -> B C
```

o:

```text
A -> terminal
```

Cuando aparece un terminal dentro de una producción larga, se crea un no terminal auxiliar.

Por ejemplo:

```text
A -> + B
```

puede convertirse utilizando:

```text
T1 -> +
A -> T1 B
```

Cuando una producción tiene más de dos símbolos, también se crean variables auxiliares para dividirla.

Por ejemplo:

```text
A -> B C D
```

puede transformarse en:

```text
A -> B C1
C1 -> C D
```

Los nombres concretos de estas variables auxiliares no afectan el lenguaje generado por la gramática.

---

## 6. Algoritmo CYK

CYK utiliza programación dinámica para determinar si una cadena puede ser generada por una gramática en CNF.

La cadena primero se divide en tokens.

Por ejemplo:

```text
The cat drinks the beer
```

después de convertirla a minúsculas produce:

```text
the
cat
drinks
the
beer
```

### Primera etapa

Para cada palabra se buscan reglas de la forma:

```text
A -> palabra
```

y se colocan los posibles no terminales en la primera parte de la tabla.

Por ejemplo:

```text
the -> Det
cat -> N
drinks -> V, VP
beer -> N
```

### Segunda etapa

El algoritmo analiza fragmentos de longitud 2, después longitud 3, y así sucesivamente hasta cubrir la frase completa.

Para cada fragmento se prueban todas las formas de dividirlo en dos partes.

Si se encuentra una regla:

```text
A -> B C
```

donde `B` genera la parte izquierda y `C` genera la derecha, entonces `A` se agrega a esa celda.

### Criterio de aceptación

La frase pertenece al lenguaje cuando el símbolo inicial de la gramática aparece en la celda correspondiente a toda la frase.

En la gramática utilizada, el símbolo inicial es:

```text
S
```

Por lo tanto:

```text
S presente en la celda final
```

significa:

```text
SÍ pertenece al lenguaje
```

mientras que su ausencia produce:

```text
NO pertenece al lenguaje
```

---

## 7. Construcción del parse tree

Además del resultado de CYK, se almacenan las decisiones utilizadas para construir cada elemento de la tabla.

Para una producción:

```text
A -> B C
```

se guarda:

- el no terminal `A`;
- el punto donde se dividió la frase;
- el símbolo `B`;
- el símbolo `C`.

Utilizando esta información es posible reconstruir recursivamente el árbol.

Por ejemplo, para:

```text
The cat drinks the beer
```

se obtuvo:

```text
S
|-- NP
|   |-- Det
|   |   \-- the
|   \-- N
|       \-- cat
\-- VP
    |-- V
    |   \-- drinks
    \-- NP
        |-- Det
        |   \-- the
        \-- N
            \-- beer
```

El árbol también se guarda en:

```text
salida/parse_tree.txt
```

---

## 8. Medición de tiempo

Para medir exclusivamente el procesamiento realizado por CYK se utiliza:

```python
time.perf_counter()
```

Se registra el tiempo antes de comenzar el algoritmo y nuevamente al finalizar.

La diferencia representa el tiempo requerido para validar la frase.

Los tiempos obtenidos son muy pequeños debido al tamaño de las frases utilizadas, y pueden variar dependiendo del equipo y de cada ejecución.

---

## 9. Pruebas realizadas

### Caso 1 - Frase válida

Entrada:

```text
She eats a cake with a fork
```

Resultado:

```text
SÍ
```

Tiempo observado:

```text
0.00017350 segundos
```

La tabla CYK contiene `S` para la frase completa y se construye correctamente el parse tree.

---

### Caso 2 - Frase válida

Entrada:

```text
The cat drinks the beer
```

Resultado:

```text
SÍ
```

Tiempo observado:

```text
0.00011840 segundos
```

El parse tree obtenido fue:

```text
S
|-- NP
|   |-- Det
|   |   \-- the
|   \-- N
|       \-- cat
\-- VP
    |-- V
    |   \-- drinks
    \-- NP
        |-- Det
        |   \-- the
        \-- N
            \-- beer
```

---

### Caso 3 - Frase inválida

Entrada:

```text
The cat the beer
```

Resultado:

```text
NO
```

Tiempo observado:

```text
0.00013490 segundos
```

En la celda que representa la frase completa no aparece `S`.

Por esta razón la frase es rechazada y no se genera un parse tree.

---

## 10. Prueba adicional de simplificación

Antes de utilizar la gramática de frases en inglés también se probó el proceso de simplificación con una gramática de expresiones:

```text
E -> T X
X -> + T X | e
T -> F Y
Y -> * F Y | e
F -> ( E ) | id
```

En este ejemplo se verificaron:

- símbolos anulables;
- eliminación de epsilon;
- eliminación de producciones unitarias;
- símbolos productores y alcanzables;
- conversión a CNF.

La gramática CNF generada utiliza nombres auxiliares diferentes a la gramática de referencia, pero las producciones son equivalentes.

Por ejemplo:

```text
T1 -> (
T2 -> )
T3 -> +
T4 -> *
```

cumple la misma función que asignar otros nombres a estas variables auxiliares.

Esta prueba fue útil para verificar que la simplificación y conversión a CNF funcionan incluso cuando la gramática de entrada todavía no está en Forma Normal de Chomsky.

---

## 11. Obstáculos encontrados

Durante el desarrollo se encontraron principalmente los siguientes problemas.

### Conversión a CNF

Fue necesario distinguir entre:

- terminales aislados;
- terminales dentro de producciones largas;
- producciones de más de dos símbolos.

La solución consistió en realizar la conversión en dos etapas: primero reemplazar terminales cuando fuera necesario y posteriormente convertir las producciones largas a binarias.

### Reconstrucción del parse tree

Una implementación normal de CYK solamente necesita guardar si un no terminal puede producir un fragmento.

Sin embargo, esto no proporciona suficiente información para reconstruir el árbol.

La solución consistió en guardar también la división y los símbolos utilizados cuando CYK encuentra una producción válida.

### Representación del árbol

Inicialmente se utilizaron caracteres Unicode para representar las ramas del árbol.

Al mostrar el archivo mediante PowerShell se produjeron problemas de codificación.

La representación fue cambiada por caracteres ASCII:

```text
|--
\--
```

Esto evita depender de la configuración de codificación de la terminal.

### Resultado anterior del parse tree

Cuando se ejecutaba una frase inválida, el archivo generado por una ejecución válida anterior podía permanecer dentro de la carpeta de salida.

Para evitar confusiones, el programa elimina el archivo anterior antes de cada nueva ejecución y solamente genera uno nuevo si la frase pertenece al lenguaje.

---

## 12. Recomendaciones

Como mejoras futuras podrían agregarse:

- selección del archivo de gramática desde la consola;
- almacenamiento de múltiples parse trees cuando una gramática es ambigua;
- visualización gráfica del árbol;
- exportación de la tabla CYK;
- pruebas automatizadas para diferentes gramáticas.

Estas características no son necesarias para el funcionamiento actual del algoritmo.

---

## 13. Conclusiones

El proyecto permitió implementar el proceso completo necesario para utilizar CYK con gramáticas libres de contexto.

Se implementaron los algoritmos de simplificación y conversión a Forma Normal de Chomsky, y posteriormente CYK mediante programación dinámica.

Las pruebas realizadas demostraron que el programa puede aceptar frases válidas, rechazar frases que no pertenecen al lenguaje y reconstruir el parse tree correspondiente a una frase aceptada.

La separación del proyecto en módulos permite observar claramente cada etapa del proceso y facilita la comprensión del funcionamiento del algoritmo.