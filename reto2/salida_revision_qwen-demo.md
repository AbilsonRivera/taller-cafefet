# Salida · revision_funcion.txt

- Comando: `ollama run qwen-demo --think=false < reto2/revision_funcion.txt`
- Fecha: 2026-10-31 17:01 · Tiempo: 95 s

---

El código que has compartido para la función `crear_pedido` en CafeFET tiene una lógica funcional básica, pero presenta **dos errores críticos** y un problema de estilo que podrían causar fallos en pruebas o comportamientos inesperados:

### 1. Errores Críticos (Lógica)

*   **Condición de saldo invertida:**
    La línea `if est.saldo - sum(p.precio for p in productos) < -1000:` es incorrecta.
    *   Si el saldo del estudiante es positivo y se le restan precios, el resultado será un número menor que el saldo original.
    *   El operador `< -1000` significa "si el resultado es menor que -1000". Esto solo sería verdadero si el saldo inicial fuera extremadamente negativo (ej. -2000) o si la resta resultara en un valor muy bajo.
    *   **Lo correcto:** Debes verificar si el saldo restante es **menor o igual a cero** (o menor que 1000, dependiendo de si se permite endeudarse ligeramente). La lógica debería ser: `if est.saldo - sum(...) < 0:` (sin deuda) o `if est.saldo - sum(...) <= 1000:` (siendo estricto con el límite de 1000).

*   **Falta de validación de precios:**
    No se verifica si los precios individuales son negativos. Si un producto tiene precio `-50`, la suma podría ser menor que el saldo, haciendo que el pedido sea válido aunque no tenga sentido lógico. Se recomienda validar `p.precio >= 0`.

### 2. Problema de Estilo (Retorno)

*   **Retorno explícito vs. Devolución implícita:**
    La función tiene dos líneas de `return False` y una línea final que devuelve un valor booleano (`True`) implícitamente. En Python, es mejor tener una estructura clara donde el éxito se devuelva al final o usar la lógica de "devolver True por defecto".

### Código Corregido y Mejorado

Aquí tienes la versión optimizada con comentarios explicativos:

```python
def crear_pedido(est, productos, hora):
    # 1. Validar cantidad de productos (máximo 6)
    if len(productos) > 6:
        return False
    
    # 2. Calcular el costo total
    costo_total = sum(p.precio for p in productos)
    
    # 3. Validar precios individuales (opcional pero recomendado)
    if any(p.precio < 0 for p in productos):
        return False

    # 4. Validar saldo del estudiante
    # El saldo restante debe ser mayor o igual a 0 (o permitir deuda de hasta 1000 según reglas específicas)
    saldo_restante = est.saldo - costo_total
    
    # Asumiendo que la regla es: No se puede endeudar más de 1000 unidades.
    # Si el saldo restante es menor a -1000, significa que se debe más de 1000.
    if saldo_restante < -1000:
        return False

    # 5
