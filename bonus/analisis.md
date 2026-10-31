# Bonus · Del texto libre a datos, y prompts medidos con casos de prueba (CafeFET)

Los scripts se adaptaron de `scripts/reporte_json.py` y `scripts/evalua.py` del repositorio de la clase. `comun.py` es una copia del de la clase.

```bash
uv sync                 # en la raíz del repositorio
cd bonus
uv run reporte_json_cafefet.py                       # parte A con qwen3.5:4b
uv run reporte_json_cafefet.py --modelo qwen3.5:0.8b
uv run evalua_cafefet.py                             # parte B con qwen3.5:4b
uv run evalua_cafefet.py --modelo qwen3.5:0.8b
```

| Script | Salidas |
|---|---|
| [`reporte_json_cafefet.py`](reporte_json_cafefet.py) | [`salida_reporte_json_4b.md`](salida_reporte_json_4b.md) · [`salida_reporte_json_0.8b.md`](salida_reporte_json_0.8b.md) |
| [`evalua_cafefet.py`](evalua_cafefet.py) | [`salida_evalua_4b.md`](salida_evalua_4b.md) · [`salida_evalua_0.8b.md`](salida_evalua_0.8b.md) |

## Parte A · Mensaje de chat → JSON validado

El esquema `PedidoChat` (Pydantic) se le pasa a Ollama con `format=`, así que el modelo solo puede generar JSON con esa forma:

| Campo | Tipo |
|---|---|
| `accion` | `Literal["crear", "modificar", "cancelar", "consultar"]` |
| `productos` | Lista de `{nombre, cantidad ≥ 1}` |
| `hora_recogida` | `"HH:MM"` o `null` |
| `observaciones` | Texto o `null` |
| `faltantes` | `list[Literal["productos", "hora_recogida"]]` |

Después de validar, el script revisa en código dos reglas de negocio: que no haya más de 5 productos y que la hora esté entre 7:00 y 18:00.

| # | Mensaje | qwen3.5:4b | qwen3.5:0.8b |
|---|---|---|---|
| 1 | «2 empanadas y un tinto para las 10:30. La empanada sin ají» | ✓ Todo correcto, con «sin ají» en las observaciones | ✗ **Perdió el tinto** y metió la observación en el nombre («Empanada sin ají») |
| 2 | «¿Me apartan un almuerzo ejecutivo y una limonada de coco? Paso a las 12 y media» | ✓ Convirtió «12 y media» en `12:30` | ⚠ Datos bien, pero `faltantes: ["productos"]` aunque sí hay productos |
| 3 | «Cancelen mi pedido de las 3 de la tarde» | ✓ `cancelar` ⚠ La referencia «de las 3» se perdió: el esquema no tiene dónde ponerla | ✓ `cancelar`, con faltantes que no aplican a una cancelación |
| 4 | «En el pedido de las 4 pm cámbienme el jugo de mora por uno de lulo» | ✓ `modificar` ⚠ Perdió «jugo de mora», y en faltantes pone productos aunque hay uno | ✗ `crear`. Puso **16:00 como hora de recogida**, cuando es la hora del pedido existente |
| 5 *(incompleto)* | «Quiero lo de siempre.» | ✓ No inventó productos ni hora y marca ambos como faltantes ✗ Pero `accion: consultar` | ✗ **Inventó** «Café especial», «Chocolate» y `09:00`, y al mismo tiempo los marca como faltantes |
| 6 *(ambiguo)* | «Dos pandebonos y… no sé, algo de tomar. Paso más tarde.» | ✓ Hora `null` («más tarde» no es una hora) ✗ **Inventó un producto llamado «tomar»** | ✗ Dos entradas «Pandeboón» de 1, sin bebida y con faltantes contradictorios |

**JSON válido según el esquema:** 6 de 6 con los dos modelos. **Extracciones completamente correctas:** 4b → 2 de 6 sin ningún reparo (1 y 2) y 4 de 6 aceptables; 0.8b → 0 de 6. Las alertas de negocio no se activaron con ninguno: ningún mensaje pedía más de 5 productos ni una hora fuera del horario.

### ¿Qué hace el modelo cuando falta un dato?

- **4b, en general, deja el hueco vacío.** En «lo de siempre» y «más tarde» puso `null` o una lista vacía y anotó el dato en `faltantes`, que es lo que pedía el prompt («no inventes productos ni horas»).
- **Pero cuando el esquema lo obliga a elegir, elige.** `accion` es un `Literal` sin opción «no sé», así que para «Quiero lo de siempre» tuvo que escoger y eligió `consultar`. El esquema no le dejó expresar la duda. Con «algo de tomar» pasó algo parecido: el campo `nombre` tenía que ser texto y convirtió lo vago en algo concreto: un producto llamado «tomar».
- **0.8b inventa.** En el mensaje 5 se inventó un pedido completo (café especial, chocolate, 9:00) y a la vez dijo que faltaban productos y hora. El modelo pequeño no sostiene la coherencia entre campos.
- **El esquema garantiza la forma, no la verdad.** Las 12 respuestas pasaron la validación de Pydantic y aun así varias están mal. `format=` evita que el código falle al leer el JSON, pero no evita datos falsos.

**Qué mejoraríamos:**

- Agregar `"desconocida"` al `Literal` de `accion`.
- Agregar campos para la hora del pedido al que se refiere el mensaje y para los productos que se quitan en una modificación.
- Agregar un `model_validator` de Pydantic que rechace contradicciones, como `productos` con elementos y `"productos"` dentro de `faltantes`. Así el código detectaría solo los casos que hay que preguntarle al estudiante.

## Parte B · Evaluación A/B de dos prompts

**La tarea:** clasificar mensajes del chat en `PEDIDO`, `CANCELACION`, `RECLAMO` o `CONSULTA`, con 10 casos etiquetados a mano. 4 de ellos son ambiguos y su etiqueta es una **decisión del equipo**:

| # | Mensaje ambiguo | Etiqueta | Por qué la decidimos así |
|---|---|---|---|
| 7 | «¿Todavía hay buñuelos? Si hay, apártenme dos.» | PEDIDO | Aunque es una pregunta, la intención es pedir |
| 8 | «Me descontaron el saldo dos veces…, ¿es normal?» | RECLAMO | Es una pregunta, pero hay una falla de por medio |
| 9 | «Pedí hace 40 minutos y no alcancé a pasar, ¿me devuelven la plata?» | CANCELACION | Por la regla 5, un pedido no recogido se cancela y se devuelve el saldo |
| 10 | «Ya no voy a ir por el almuerzo, ¿lo pueden anular?» | CANCELACION | Está escrito como pregunta, pero pide anular |

**Las dos versiones del prompt:**

- **v1 (zero-shot):** solo la lista de categorías.
- **v2:** una definición por categoría, con «aunque lo escriba como pregunta», la regla de los 30 minutos y tres ejemplos.

| Modelo | v1 | v2 | Fallan en v1 y no en v2 | Fallan en v2 y no en v1 |
|---|---|---|---|---|
| qwen3.5:4b | **9/10** (ambiguos 3/4) | **10/10** (ambiguos 4/4) | #9 | ninguno |
| qwen3.5:0.8b | **4/10** (ambiguos 2/4) | **7/10** (ambiguos 3/4) | #3, #4, #10 | ninguno |

### Análisis

- **Con 4b, la v1 solo falla en el caso que depende de una regla del negocio.** El #9 lo clasificó como RECLAMO, y desde el texto es razonable: alguien que pide su plata suena a reclamo. Pero nuestro equipo decidió que es CANCELACION por la regla de los 30 minutos, y el modelo no tiene cómo saberlo. Con la definición de la v2, que menciona esa regla, acierta. Es el mismo caso de «Renovar es lentísimo» de la clase: **cuando la etiqueta es una decisión del equipo, hay que escribirla en el prompt**.
- **Con 0.8b, la v1 casi siempre responde PEDIDO.** Lo hizo con 6 de los 10 mensajes, incluidos un reclamo («el sándwich estaba frío») y una consulta («¿hasta qué hora reciben pedidos?»). Parece que el modelo pequeño se guía por palabras sueltas del dominio (producto o pedido → PEDIDO).
- **La v2 corrigió 3 casos con 0.8b**, pero los 3 que siguen fallando (#5 «¿cuántos productos puedo **pedir**?», #6 «la app me dejó **pedir**…» y #9 «**Pedí** hace 40 minutos…») contienen la palabra *pedir*. Las definiciones ayudan, pero no superan esa asociación por palabras en un modelo de 0.8B.
- **La v2 nunca empeoró un caso** en ninguno de los dos modelos. Con estos datos, la v2 es mejor sin discusión.
- **Precaución con nuestra propia evaluación:**
  - El tercer ejemplo de la v2 («No pude recoger mi almuerzo a tiempo, ¿qué pasa con mi plata?») se parece mucho al caso #9, así que parte de la mejora puede venir de que el ejemplo es casi la respuesta. Para medir mejor habría que usar casos de prueba que no se parezcan a los ejemplos del prompt.
  - Con 10 casos, cada caso vale 10 puntos: la diferencia 9 → 10 en 4b es un solo caso.
  - Lo correcto es seguir agregando a `CASOS` cada error que aparezca, como pruebas de regresión.
- **El modelo importa tanto como el prompt.** El mismo prompt v2 da 10/10 con 4b y 7/10 con 0.8b. El modelo pequeño es más rápido (24 s contra 67 s para las 20 clasificaciones), pero para esta tarea no alcanza ni con el mejor prompt.
