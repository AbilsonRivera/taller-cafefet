# Reto 4 · Razonar y manejar el contexto (CafeFET)

## Parte A · Cadena de pensamiento con `phi-demo`

`phi-demo` es phi4-mini con temperatura 0, semilla 42 y 700 tokens de salida. No tiene modo de razonamiento, por eso no lleva `--think=false`.

**El caso inválido** es un pedido que viola cuatro reglas a la vez y aun así fue aceptado: un domingo a las 18:40, con 6 productos, uno agotado, por $3.800 y con un saldo de $3.000. La función tiene **5 errores** (los mismos del reto 2):

| # | Error |
|---|---|
| E1 | `> 6` debería ser `> 5` |
| E2 | `< -1000` debería ser `< 0` |
| E3 | No valida el domingo |
| E4 | No valida los agotados |
| E5 | `hora <= 18` con hora entera acepta 18:40 |

| Versión | Prompt | Salida | Tiempo |
|---|---|---|---|
| Sin CoT · «Responde en una línea» | [`parte_a_cot_sin.txt`](parte_a_cot_sin.txt) | [`salida_parte_a_cot_sin.md`](salida_parte_a_cot_sin.md) | 13 s |
| Con CoT · «evalúa paso a paso cada if, su condición y su valor» | [`parte_a_cot_con.txt`](parte_a_cot_con.txt) | [`salida_parte_a_cot_con.md`](salida_parte_a_cot_con.md) | 153 s |
| Extra · CoT guiado, con un paso por línea del código | [`parte_a_cot_guiado.txt`](parte_a_cot_guiado.txt) | [`salida_parte_a_cot_guiado.md`](salida_parte_a_cot_guiado.md) | 200 s* |

\* Se ejecutó al mismo tiempo que otras pruebas, así que el tiempo está inflado.

### Resultados con datos

| | Sin CoT | Con CoT | CoT guiado |
|---|---|---|---|
| E1 · máximo 5 | ✓ («excedió el máximo de 5») | ✓ | ✗ (dice que la regla «se valida») |
| E2 · saldo negativo | ✗ | ✗ Afirma que el saldo «no queda negativo» | ✗ (calcula bien −800, pero dice que la regla «se valida») |
| E3 · domingo | ✗ | ✓ | ✗ |
| E4 · agotados | ✗ | ✗ Afirma que la función «valida bien» los agotados | ✓ Y propone el `if any(p.agotado …)` correcto |
| E5 · 18:40 | ✗ | ✗ | ✗ |
| **Errores reales encontrados** | **1 de 5** | **2 de 5** | **1 de 5** |
| Afirmaciones falsas | 0 | 3: el `if` de agotados no existe, el saldo «no queda negativo» y la regla 3 «se valida bien» | 2: las reglas 2 y 3 «se validan» |
| ¿Evaluó los `if` correctamente? | No se pidió | **No**: listó los *datos* como si fueran condiciones («len(productos) = 6 → True → retorna True») | **Sí**: 6 > 6 es False; 3000 − 3800 = −800 y −800 < −1000 es False; 7 ≤ 18 ≤ 18 es True → retorna True |

### Qué pasó y por qué

1. **Pedir el razonamiento sí cambió la respuesta, pero no siempre a mejor.** La versión con CoT encontró un error más (2 frente a 1), pero su «razonamiento» no era real. No evaluó los `if` del código, sino que enumeró los datos del enunciado. Se equivocó en una resta simple: dijo que con $3.000 y un pedido de $3.800 el saldo «no queda negativo». E inventó un `if` de agotados que la función no tiene. Un modelo pequeño puede producir texto con **forma** de razonamiento sin que el contenido sea fiel a lo que hace el código.
2. **Cuando le dimos los pasos exactos, el cálculo salió perfecto.** En la versión guiada, cada paso le decía qué línea evaluar y en qué orden (primero la resta, luego la comparación). Así obtuvo los tres valores correctos, y esa traza **explica exactamente por qué el pedido pasó**: 6 productos no activan `> 6`, −800 no activa `< −1000` y 18 está dentro de `<= 18`.
3. **Pero no conectó la traza con las reglas.** En el paso 4 le pedimos «busca la línea que verifica cada regla», y el modelo entendió que **si existe** una línea que habla de la regla, la regla está bien validada. Por eso dijo que las reglas 2 y 3 «se validan», aunque su propia traza muestra que dejan pasar el pedido. El error fue nuestro: el paso 4 debió preguntar «con los datos del caso, ¿la regla exige rechazar el pedido? ¿El código lo rechazó?».
4. **Comparación con la práctica 9 de la clase.** En la práctica 9 había **un solo** error (`> 3` en vez de `>= 3`) y la cadena de pensamiento lo encontraba. Nuestro caso tiene **cinco errores a la vez** y un modelo de 3.8B no logra sostener todo el análisis. El CoT ayuda cuando el problema cabe en pocos pasos. Con problemas más grandes, conviene dividirlos (un error o una regla por pregunta) o usar un modelo razonador.
5. **Lo más útil de la cadena de pensamiento fue la traza, no la conclusión.** Aunque la conclusión del CoT guiado estaba mal, cualquiera que lea «6 > 6 es False, la función no retorna aquí» ve el error E1 al instante. Escribir el razonamiento sirve sobre todo para que **un humano pueda verificarlo**.

## Parte B · La instrucción que se olvida

**Configuración:** `qwen-demo` con `--think=false` y `num_ctx 512`. La regla propia del caso es «empieza SIEMPRE tu respuesta con **«CafeFET responde:»**». Las dos preguntas piden al menos 400 palabras sobre CafeFET: cómo funciona un pedido anticipado y cómo manejar el saldo del carné.

| Archivo | Qué es |
|---|---|
| [`parte_b_comandos.txt`](parte_b_comandos.txt) | Los comandos para escribir en el chat de `ollama run qwen-demo --think=false`, con `/set parameter num_ctx 512`, `/clear` y `/set system` |
| [`parte_b_chat.py`](parte_b_chat.py) | La misma conversación enviada desde código, mensaje por mensaje |
| [`salida_parte_b.md`](salida_parte_b.md) | Las 5 respuestas completas y los tokens leídos en cada turno |

**Por qué hay un script:** el chat de `ollama run` reenvía en cada turno toda la conversación al servidor (`/api/chat`), con las opciones fijadas por `/set`. El script envía exactamente esos mensajes con `num_ctx 512`, así que el recorte que hace el servidor es el mismo. La ventaja es que también registra `prompt_eval_count`, la cantidad de tokens que el modelo **realmente leyó** en cada turno. Ese dato es la evidencia del recorte. Los comandos para repetirlo a mano en el chat están en `parte_b_comandos.txt`.

### Resultados

| Turno | Mensajes en el historial | Tokens que el modelo leyó | Tokens generados | ¿Empieza con «CafeFET responde:»? |
|---|---|---|---|---|
| **A0** · la regla como mensaje | 1 | 34 | 49 | ✓ SÍ |
| **A1** · pregunta 1 | 3 | 132 | 593 (475 palabras) | ✓ SÍ |
| **A2** · pregunta 2 | 5 | **39** | 700 (528 palabras) | ✗ **NO** |
| **B1** · pregunta 1 (regla en el system) | 2 | 73 | 696 (539 palabras) | ✓ SÍ |
| **B2** · pregunta 2 (regla en el system) | 4 | **60** | 639 (478 palabras) | ✓ SÍ |

| Versión | Dónde está la regla | Respuesta 1 | Respuesta 2 |
|---|---|---|---|
| A | Mensaje del chat | ✓ | ✗ |
| B | System prompt | ✓ | ✓ |

### Qué pasó, con nuestras palabras

1. **El modelo no recuerda nada entre turnos.** En cada turno se le vuelve a enviar todo el historial. Si el historial no cabe en la ventana de `num_ctx` tokens, Ollama descarta mensajes completos, empezando por el más antiguo. Siempre conserva el último mensaje y el system prompt.
2. **En A1 todo cabía.** El modelo leyó 132 tokens: la regla, el «Entendido» y la pregunta 1. Por eso empezó con «CafeFET responde:».
3. **En A2 ya no cabía.** El historial tenía 5 mensajes, pero la respuesta A1 sola ocupa 593 tokens, más que toda la ventana de 512. Ollama tuvo que botar la regla, el «Entendido», la pregunta 1 **y** la respuesta A1. El modelo leyó solo **39 tokens: únicamente la pregunta 2**. La regla no se «olvidó» por falta de atención: **ya no estaba en lo que el modelo leyó**.
4. **Que también se botara la respuesta A1 es importante.** Si A1 hubiera seguido en la ventana, el modelo habría visto que su respuesta anterior empezaba con «CafeFET responde:» y probablemente la habría imitado aunque la regla ya no estuviera. Como la ventana es tan pequeña, se fue todo y el efecto quedó limpio.
5. **Con el recorte se perdió el formato y también el contexto del caso.** La respuesta A2 interpreta «el saldo del carné de CafeFET» como las **finanzas de la empresa**: flujo de caja, cuentas bancarias, gastos operativos y un margen de «10 euros». Sin los mensajes anteriores, el modelo ya no sabía que el carné es la tarjeta del estudiante. El recorte borra cualquier cosa que se haya dicho antes en el chat, no solo las reglas.
6. **En la versión B la regla sobrevivió porque Ollama nunca descarta el system prompt.** En B2 el modelo leyó **60 tokens**, que son el system prompt (≈21) más la pregunta 2 (39). La pregunta 1 y su respuesta se botaron igual que en A, pero la regla seguía ahí. Por eso las dos respuestas empiezan con «CafeFET responde:». La respuesta B2 también entiende mejor el caso («el saldo del carné de un usuario… denegar la transacción si no alcanza»), aunque todavía inventa cosas como tasas de cambio y tarjetas de crédito.
7. **No fue deriva, fue recorte.** La regla se cumplió mientras estuvo dentro de la ventana (A0 y A1) y dejó de cumplirse exactamente en el turno en que salió. Los tokens leídos lo confirman: 132 → 39. Si se hubiera dejado de cumplir con la regla todavía adentro, sería deriva de atención.

**Conclusión práctica:** las reglas que siempre se deben cumplir van en el **system prompt**, que en un agente de código es el `AGENTS.md` o `CLAUDE.md`, nunca en un mensaje del chat. En conversaciones largas, además, hay que controlar qué ocupa la ventana: compactar o resumir el historial, guardar notas fuera del chat o separar el trabajo en sub-agentes con contexto propio. Si no, lo primero que se pierde es lo más antiguo, que suelen ser las instrucciones del principio.
