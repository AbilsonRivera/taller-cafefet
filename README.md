# Taller · Ingeniería de prompts y de contexto · CafeFET

Diplomado en Ingeniería de Software con IA y Sistemas Agénticos · FET · Sesión 03 · Módulo 1

## Integrantes

- Abilson Rivera Garcia
- Bredman Estiven Velez Cortez

## Caso: 2 · CafeFET

Pedidos anticipados a la cafetería de la FET.

**Reglas de negocio:**

1. Se reciben pedidos de lunes a sábado, de 7:00 a 18:00.
2. Máximo 5 productos por pedido.
3. Se paga con el saldo del carné; el saldo nunca puede quedar negativo.
4. Los productos agotados no se pueden pedir.
5. Si el pedido no se recoge en 30 minutos, se cancela y se devuelve el saldo.

**Por qué elegimos CafeFET:** su función con errores (`crear_pedido`) tiene la mayor cantidad de fallas de los cuatro casos: `> 6` en lugar de `> 5`, un saldo que puede llegar a −$1.000, no valida el domingo, no valida los agotados y el límite de las 18:00 está mal con hora entera. Además, el requisito nuevo («repetir el último pedido con un clic») choca con casi todas las reglas. Eso daba más material para comparar y analizar.

**Decisiones del equipo:**

- A las 18:00 en punto todavía se reciben pedidos; a las 18:01 ya no.
- Las etiquetas de los casos ambiguos del bonus están explicadas en [`bonus/analisis.md`](bonus/analisis.md).

## Modelos y equipo usados

| Modelo | Base | Configuración | Dónde se usó |
|---|---|---|---|
| `qwen-demo` | qwen3.5:4b | temperatura 0, semilla 42, `num_predict 700`, siempre con `--think=false` | Retos 1, 2 (sin system prompt), 3 y 4B |
| `revisor-cafefet` | qwen3.5:4b | [`reto2/Modelfile.v1`](reto2/Modelfile.v1): temperatura 0, semilla 42, `num_ctx 8192` | Reto 2 (v1) |
| `revisor-cafefet-v2` | qwen3.5:4b | [`reto2/Modelfile.v2`](reto2/Modelfile.v2): igual a v1 y con system prompt endurecido | Reto 2 (v2) |
| `phi-demo` | phi4-mini | temperatura 0, semilla 42, `num_predict 700` (sin modo de razonamiento) | Reto 4A |
| `qwen3.5:4b` y `qwen3.5:0.8b` | — | desde Python, temperatura 0, semilla 42, `think=False` | Bonus |

| Equipo | |
|---|---|
| Procesador | AMD Ryzen 7 7730U (8 núcleos) |
| Memoria | 15 GB de RAM |
| GPU | Radeon integrada (sin GPU dedicada): toda la inferencia corrió en **CPU** |
| Sistema | Windows 11 · Ollama 0.40.13 · uv 0.13.1 · Python 3.12 |
| Tiempo por respuesta | Entre 8 s (respuestas cortas) y unos 150 s (700 tokens) con `qwen-demo` |

## Estructura

```
taller-cafefet/
├── README.md            ← este archivo
├── reto1/               ← fórmula base y delimitadores        → comparacion.md
├── reto2/               ← system prompt, Modelfile v1 y v2 y ataques → analisis.md
├── reto3/               ← cadena historia → criterios → casos  → nota.md
├── reto4/               ← cadena de pensamiento y ventana de contexto → explicacion.md
├── bonus/               ← JSON con Pydantic y evaluación A/B   → analisis.md
└── pyproject.toml       ← dependencias de Python (solo para el bonus y la reproducción del reto 4B)
```

**Convención:**

- Cada prompt está en un `.txt` y su salida en un `.md` con el mismo nombre (`salida_*.md`).
- Cada salida empieza con un encabezado que tiene el comando exacto, la fecha y el tiempo. Debajo está la respuesta **tal como salió** del modelo. Lo único que se quitó son los códigos de la animación de carga («spinner») que `ollama run` imprime en la terminal de Windows.
- El análisis de cada reto está en el `.md` indicado arriba.

## Cómo reproducirlo

```bash
# Modelos base y de práctica (del repositorio de la clase)
ollama pull qwen3.5:4b && ollama pull phi4-mini && ollama pull qwen3.5:0.8b
ollama create qwen-demo -f modelfiles/Modelfile.qwen-demo     # en fet-diplomadoIA-prompting-p2
ollama create phi-demo  -f modelfiles/Modelfile.phi-demo

# Revisores de este taller (desde la raíz de este repositorio)
ollama create revisor-cafefet    -f reto2/Modelfile.v1
ollama create revisor-cafefet-v2 -f reto2/Modelfile.v2

# Patrón de ejecución de los retos 1 a 4
ollama run qwen-demo --think=false < reto1/prompt_nuevo.txt
ollama run phi-demo < reto4/parte_a_cot_sin.txt

# Bonus
uv sync
cd bonus
uv run reporte_json_cafefet.py
uv run evalua_cafefet.py --modelo qwen3.5:0.8b
```

## Resultados en una línea

| Reto | Resultado principal | Análisis |
|---|---|---|
| 1 · Fórmula base | El prompt malo dio una función en JavaScript genérico que no cumplía ninguna regla y quedó cortada. Con los 5 bloques y `<reglas>` salió Python con 4 de 5 reglas. Sigue fallando en que **no descuenta el saldo** y en el límite de las 18:00. Quitar las restricciones alargó el código de 43 a 58 líneas sin cambiar las reglas | [`reto1/comparacion.md`](reto1/comparacion.md) |
| 2 · System prompt | Errores encontrados: `qwen-demo` 0–1 de 5, revisor v1 3 de 5, revisor v2 4 de 5. Ataques: la v1 resistió 4 de 5; en uno cayó a medias y **emitió «APROBADO» sin código**. La v2 resistió los 5 y reporta las instrucciones escondidas en el código | [`reto2/analisis.md`](reto2/analisis.md) |
| 3 · Encadenamiento | El primer error apareció en el **paso 2**: dio 1 criterio en vez de 3–5 porque la plantilla mostraba un solo bloque. Por eso, el paso 3 inventó una regla de «24 horas» y montos en euros. Al corregir el paso 2 salieron 4 criterios; al corregir el paso 3, los montos quedaron en pesos y dentro del horario | [`reto3/nota.md`](reto3/nota.md) |
| 4A · Cadena de pensamiento | Errores encontrados por `phi-demo`: sin CoT 1 de 5; con CoT 2 de 5, pero con 3 afirmaciones falsas; con CoT guiado 1 de 5, con la traza de los `if` correcta | [`reto4/explicacion.md`](reto4/explicacion.md) |
| 4B · Ventana de contexto | Con la regla en un mensaje: SÍ → **NO**. En el turno 2 el modelo leyó solo 39 tokens, únicamente la pregunta. Con la regla en el system prompt: SÍ → SÍ | [`reto4/explicacion.md`](reto4/explicacion.md) |
| Bonus | **A:** el JSON valida con el esquema en 6 de 6 mensajes, pero validar no es acertar. Ante datos faltantes, 4b deja `null` y 0.8b inventa un pedido completo. **B (aciertos):** con 4b, v1 9/10 y v2 10/10; con 0.8b, v1 4/10 y v2 7/10. La v2 nunca empeoró un caso | [`bonus/analisis.md`](bonus/analisis.md) |

## Reflexión del grupo

Al empezar pensábamos que lo importante era escribir bonita la pregunta, pero lo que más cambió los resultados fue darle al modelo la información que no tenía. Cuando le pedimos «haz una función para crear pedidos» nos dio algo en JavaScript para una tienda cualquiera. Cuando le pasamos las reglas de CafeFET dentro de `<reglas>`, ya hizo una función en Python que cumplía casi todo. Con el revisor pasó lo mismo: sin las reglas casi no encontraba errores, y con el system prompt encontró 3 o 4 de 5. Por eso creemos que la técnica con más efecto fue darle el contexto, o sea, las reglas del negocio. También nos sirvió hacer el reto 3 por pasos, porque así vimos en qué parte se empezaba a equivocar.

Nos sorprendió que el modelo se equivoca con mucha seguridad. Inventó una regla de 24 horas, puso precios en euros, dijo que había revisado todo cuando había casos que no cuadraban, y en el reto 4 hizo mal una resta mientras «razonaba». También vimos que en un chat largo se le olvida lo que le dijiste al principio, pero si la regla está en el system prompt no se le olvida.

Si mañana le pidiéramos a una herramienta de IA que programe algo de CafeFET, haríamos esto diferente:

- Darle todas las reglas y con ejemplos de los casos límite (por ejemplo, a las 18:00 sí se recibe y a las 18:01 no), porque explicadas solo con palabras las falló.
- Decirle claramente qué tiene que entregar, porque lo que no pusimos en el formato lo olvidó, como descontar el saldo.
- Pedirle el trabajo por partes y no todo de una vez.
- Poner las reglas fijas en el system prompt y no en el chat.
- Revisar y probar siempre lo que genere, porque aunque se vea bien puede tener errores.
