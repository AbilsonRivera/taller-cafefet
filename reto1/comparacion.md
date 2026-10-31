# Reto 1 · Rescatar un prompt malo (CafeFET)

Modelo: `qwen-demo` (qwen3.5:4b, temperatura 0, semilla 42, máximo 700 tokens), siempre con `--think=false`.

| Archivo | Qué es |
|---|---|
| [`prompt_malo.txt`](prompt_malo.txt) → [`salida_malo.md`](salida_malo.md) | El prompt original del caso: «Haz una función para crear pedidos.» |
| [`prompt_nuevo.txt`](prompt_nuevo.txt) → [`salida_nuevo.md`](salida_nuevo.md) | Fórmula base (5 bloques) y reglas dentro de `<reglas>…</reglas>` |
| [`prompt_variante_sin_restricciones.txt`](prompt_variante_sin_restricciones.txt) → [`salida_variante_sin_restricciones.md`](salida_variante_sin_restricciones.md) | El prompt nuevo **sin el bloque `[RESTRICCIONES]`** (lo único que cambia) |

## 1. Lo que el modelo tuvo que adivinar con el prompt malo

La salida del prompt malo es una función `crearPedido` en **JavaScript** para una tienda genérica. Estas son las decisiones que el modelo tomó solo, porque el prompt no decía nada:

| # | Decisión que tuvo que adivinar | Lo que eligió | Lo que necesitaba CafeFET |
|---|---|---|---|
| 1 | Lenguaje | JavaScript | Python 3.12 |
| 2 | Dominio del sistema | Tienda genérica («Laptop Gamer», «Mouse Inalámbrico») | Cafetería de la FET con pedidos anticipados |
| 3 | Forma del pedido | Un solo producto con `cantidad` y `precioUnitario` | Una lista de productos, cada uno con precio y estado de agotado |
| 4 | Cómo se paga | No hay pago: solo calcula `total = cantidad * precio` | Se descuenta del saldo del carné, que nunca puede quedar negativo |
| 5 | Reglas de negocio | Solo valida campos vacíos, cantidad > 0 y precio ≥ 0 | Las 5 reglas: horario, máximo 5 productos, saldo, agotados y 30 minutos para recoger |
| 6 | Persistencia | Un arreglo global `pedidos = []` que simula la base de datos | Nada: la función recibe los datos y retorna un resultado |
| 7 | Qué retorna | Un objeto `{ exito, mensaje, pedido }` | Un resultado claro de aceptado o rechazado, con motivo |
| 8 | Moneda | `total.toFixed(2)` (con centavos) | Pesos colombianos enteros |
| 9 | Alcance de la respuesta | Explicación, función y pruebas con `console.log` | Solo la función |

La décima consecuencia muestra el costo de no fijar el alcance: la respuesta **se cortó a mitad de línea** (`Total $`) porque gastó los 700 tokens del límite en pruebas y explicaciones que nadie pidió.

## 2. Qué cambió con la fórmula base

El prompt nuevo tiene los cinco bloques:

| Bloque | Contenido |
|---|---|
| **Qué quiero** | Nombre y firma de la función, lenguaje y qué debe hacer |
| **Para quién** | Backend FastAPI de CafeFET, mantenido por desarrolladores junior |
| **Contexto** | Qué atributos traen `estudiante`, `productos` y `ahora`, más las 5 reglas dentro de `<reglas>…</reglas>` |
| **Formato** | Solo código, con type hints y docstring, que retorna la tupla `(aceptado, motivo, recoger_antes_de)` |
| **Restricciones** | Solo librería estándar, sin base de datos, sin `print`, validar en orden y descontar el saldo al final, máximo 40 líneas |

Comparación regla por regla de las tres salidas:

| Regla o requisito | Prompt malo | Prompt nuevo | Variante sin restricciones |
|---|---|---|---|
| Python 3.12 con type hints y docstring | ✗ (JavaScript) | ✓ | ✓ |
| Retorna la tupla pedida | ✗ | ✓ (pero anota `Tuple[bool, str, datetime]` aunque retorna `None`) | ✓ (anotación correcta `datetime \| None`) |
| R1 · No recibe pedidos el domingo | ✗ | ✓ `weekday() == 6` | ✓ |
| R1 · Horario 7:00–18:00, y a las 18:01 ya no | ✗ | ⚠ `ahora.hour > 18` **acepta de 18:01 a 18:59** | ⚠ el mismo error |
| R2 · Máximo 5 productos y no vacío | ✗ | ✓ | ✓ |
| R3 · Rechaza si el saldo no alcanza | ✗ | ✓ `saldo < total` | ✓ `total > saldo` |
| R3 · **Descuenta el total del saldo** | ✗ | ✗ **no lo hace** | ✗ **no lo hace** |
| R4 · Rechaza productos agotados | ✗ | ✓ | ✓ |
| R5 · Hora límite = ahora + 30 min | ✗ | ✓ | ✓ |
| Lee los datos como objetos (`estudiante.saldo`) | — | ✗ usa diccionarios (`estudiante['saldo']`) | ✗ diccionarios y además `.get('saldo', 0)` |
| Valida en el orden de la lista | — | ✗ valida R4 antes que R3 | (no se pidió) |
| Longitud | 70 líneas y cortada | 43 líneas (pidió máximo 40) | 58 líneas |

**Lo que mejoró:** de 0 reglas pasó a cumplir 4 de 5 casi por completo. Con delimitar las reglas y fijar la firma y el retorno, el modelo dejó de inventar el dominio, el lenguaje y la estructura.

**Lo que sigue fallando, y por qué creemos que pasa:**

1. **No descuenta el saldo.** La orden aparece dos veces: en «qué quiero» y en «restricciones». Pero el bloque **formato**, que describe en detalle qué retorna la función, no la menciona. El modelo se guió por lo que tenía que retornar y no por el efecto secundario. Para corregirlo, la orden debería ir en el formato o como paso numerado (por ejemplo, «antes de retornar True, resta el total de `estudiante.saldo`»).
2. **El límite de las 18:00 quedó mal**, aunque el prompt decía explícitamente «a las 18:01 ya no». El modelo tradujo «de 7 a 18» como `hour > 18`, que es el mismo tipo de error de límite que tiene la función original del caso. Para un modelo pequeño, una aclaración en prosa no basta. Habría que dar casos concretos («18:00 → acepta; 18:01 → rechaza») o pedirle que se autoverifique con esos casos.
3. **Ignoró que los datos son objetos.** El contexto decía «objeto con el atributo saldo», pero el modelo usó diccionarios, que es el patrón más común en sus datos de entrenamiento. Con objetos reales, el código fallaría con `TypeError`. Eso solo se detecta probando o revisando el código, no leyéndolo por encima.
4. **Las restricciones cuantitativas se cumplen a medias:** pedimos máximo 40 líneas y dio 43, y no respetó el orden de validación.

## 3. La variante: quitar el bloque de restricciones

Solo se borró `[RESTRICCIONES]`. Las diferencias:

- **Creció de 43 a 58 líneas.** El docstring es más largo y separa cada validación en su propio `if`, con un mensaje distinto por regla. El límite de líneas era lo único que lo mantenía corto.
- **Los mensajes de error salieron más específicos** («Solo se reciben pedidos de lunes a sábado» en lugar de «Horario inválido»). Al quitar el límite de líneas, el modelo tuvo espacio para ser más claro. La restricción de longitud tenía un costo en calidad de los mensajes.
- **Agregó un valor por defecto silencioso** (`estudiante.get('saldo', 0)`). Si falta el saldo, lo trata como 0 en lugar de fallar. Es una decisión que nadie pidió.
- **No usó base de datos, red ni `print`**, aunque ya no estaba prohibido. Esas restricciones eran redundantes: el **contexto** ya decía que todo llegaba por parámetros y el **formato** pedía «solo el código».
- Los errores de fondo (no descuenta el saldo, límite de las 18:00, diccionarios) **siguen iguales**. No dependían del bloque de restricciones.

**Conclusión:** en nuestro caso, el bloque con más efecto fue el **contexto con las reglas delimitadas**: es lo que convirtió una función genérica en una función de CafeFET. Las restricciones solo controlaron la longitud y el estilo. Un dato más: el modelo tiende a ignorar lo que el **formato** no menciona. Si algo es obligatorio, como descontar el saldo, tiene que estar donde el modelo mira para armar la salida.
