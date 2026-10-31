# Reto 3 · Del requisito a los casos de prueba (CafeFET)

**Requisito nuevo:** «Que el estudiante pueda repetir su último pedido con un solo clic.»
**Modelo:** `qwen-demo` con `--think=false`. Cada paso se ejecutó por separado: la salida de un paso se pegó dentro de la etiqueta del prompt siguiente.

## La cadena

| Paso | Técnica | Prompt | Salida |
|---|---|---|---|
| 1 · Requisito → historia | Few-shot con 2 ejemplos propios de CafeFET | [`prompt1_historia.txt`](prompt1_historia.txt) | [`salida1_historia.md`](salida1_historia.md) |
| 2 · Historia → criterios | Formato fijo Dado / Cuando / Entonces, con la historia en `<historia>` y las reglas en `<reglas>` | [`prompt2_criterios.txt`](prompt2_criterios.txt) | [`salida2_criterios.md`](salida2_criterios.md) |
| 3 · Criterios → tabla de casos | Tabla Markdown y autoverificación | [`prompt3_casos.txt`](prompt3_casos.txt) | [`salida3_casos.md`](salida3_casos.md) |
| 2 corregido | El mismo paso 2, con la plantilla y la cobertura explícitas | [`prompt2_criterios_v2.txt`](prompt2_criterios_v2.txt) | [`salida2_criterios_v2.md`](salida2_criterios_v2.md) |
| 3 repetido | El mismo prompt 3, con los criterios nuevos | [`prompt3_casos_v2.txt`](prompt3_casos_v2.txt) | [`salida3_casos_v2.md`](salida3_casos_v2.md) |
| 3 corregido | Paso 3 con contexto de moneda y horario | [`prompt3_casos_v3.txt`](prompt3_casos_v3.txt) | [`salida3_casos_v3.md`](salida3_casos_v3.md) |

## ¿En qué paso apareció el primer error?

**Paso 1 · sin errores.** La historia copió el formato de los ejemplos:

> Como estudiante, quiero poder repetir mi último pedido con un solo clic, para agilizar la finalización de mi compra y ahorrar tiempo en la cafetería.

**Paso 2 · aquí apareció el primer error.** Pedimos «entre 3 y 5 criterios… usando las reglas de negocio» y el modelo entregó **un solo criterio**, que además **no usa ninguna regla**:

> CA1. Repetir pedido anterior — Dado que es un estudiante… Cuando realiza clic… Entonces se cargan automáticamente los productos del pedido previo…

Creemos que hay dos causas:

1. **La plantilla de formato mostraba un solo bloque (`CA1.`).** El modelo copió la plantilla como si fuera un ejemplo few-shot, y eso incluye **cuántos** elementos tiene. La instrucción «entre 3 y 5» pesó menos que la forma de la plantilla. Es el mismo efecto que hace funcionar el paso 1, pero esta vez en contra nuestra.
2. **«Usando las reglas de negocio» era vago.** No decía cómo convertir las reglas en criterios, así que el modelo escribió el caso feliz, que es lo más obvio.

**Paso 3 · el error se propagó y aparecieron reglas inventadas.** Como solo había un criterio, los 3 casos de prueba cubren CA1. Al no ver ninguna regla, el modelo rellenó los huecos por su cuenta:

- **Inventó una regla:** «su último pedido fue hace 3 días (fuera del límite de retención de 24h)». CafeFET no tiene esa regla.
- **Inventó la moneda:** todos los montos en **euros** («Cappuccino 4.50€»).
- **Aceptó un pedido en domingo:** el CP1 es del 15/10/2023, que fue domingo, y espera que el pedido se cree. Viola la regla 1, pero el paso 3 no conoce las reglas.
- La autoverificación («cada criterio tiene al menos un caso») se cumplió trivialmente: con un solo criterio, no había nada que revisar.

## Qué corregimos y por qué

### Corrección 1 · paso 2 (donde apareció el primer error)

Cambios en [`prompt2_criterios_v2.txt`](prompt2_criterios_v2.txt):

- **Plantilla con dos bloques** (`CA1.` y `CA2.`) y la frase «repitiendo el bloque para cada criterio (CA1, CA2, CA3…)», para que la plantilla muestre que son varios.
- **Cobertura explícita:** CA1 es el caso feliz, y cada uno de los demás cubre una regla que puede impedir o afectar el pedido repetido, indicando el número de la regla.
- **Restricción contra lo inventado:** «usa solo las reglas de `<reglas>`: no inventes plazos, límites, montos ni pantallas», y los montos en pesos colombianos.

**Resultado:** 4 criterios que cubren el caso feliz y las reglas 3 (saldo insuficiente), 4 (producto agotado) y 5 (no recogido en 30 minutos). Al repetir el paso 3 con estos criterios, salió un caso por criterio y **desapareció la regla inventada de las 24 horas**.

**Lo que sigue imperfecto en el paso 2:**

- CA1 está marcado como «(regla 4)» aunque es el caso feliz de todas las reglas.
- No hay criterio para la regla 1, aunque repetir un pedido un domingo es justo el caso que debería probarse.
- CA2 inventa un detalle de interfaz («opción no seleccionable») a pesar de la restricción.

### Corrección 2 · paso 3 (supuestos que nacen en este paso)

Con los criterios corregidos, el paso 3 seguía usando **euros** y no ponía día ni hora. Ese supuesto no venía del paso 2: el prompt 3 solo recibe los criterios y nunca le dijimos en qué moneda trabaja CafeFET ni cuál es el horario. En [`prompt3_casos_v3.txt`](prompt3_casos_v3.txt) agregamos ese contexto (pesos sin decimales con ejemplos de precios, lunes a sábado de 7:00 a 18:00).

**Resultado:** montos en pesos (tinto $2.000, empanada $3.500), día y hora en cada caso, totales correctos ($5.500) y una nota final en la que el modelo afirma que verificó la cobertura de CA1 a CA4.

**Lo que la autoverificación no detectó:**

- El caso CA2-01 espera que el sistema «permita finalizar solo con el tinto», pero el criterio CA2 dice que el sistema **no permite** finalizar la compra. El caso contradice el criterio que dice cubrir.
- El caso CA4-01 tiene una línea de tiempo confusa («sábado 17:30 PM… hoy 8:00 AM»).

La autoverificación solo revisó lo que le pedimos: que cada criterio tuviera un caso. **No revisó que el resultado esperado fuera coherente con el criterio**. Para eso habría que pedirlo explícitamente o agregar un cuarto paso de revisión.

## Lo que aprendimos

- **Encadenar ayuda a encontrar el error**, porque cada paso se puede revisar por separado. Sin la cadena, en un solo prompt, habríamos visto una tabla con euros y una regla de 24 horas sin saber de dónde venían.
- **Los errores se propagan en silencio.** Un paso que entrega menos de lo pedido no falla de forma visible: el siguiente paso trabaja con lo que recibe y rellena el resto con supuestos.
- **Cada paso solo sabe lo que se le pasa.** Si el paso 3 necesita las reglas o la moneda, hay que dárselas en ese paso o asegurarse de que el paso anterior las incluya en su salida.
- **Las plantillas de formato funcionan como ejemplos.** El modelo copia su forma completa, incluido cuántos elementos tiene.
