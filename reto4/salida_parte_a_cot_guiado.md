# Salida · parte_a_cot_guiado.txt

- Comando: `ollama run phi-demo  < reto4/parte_a_cot_guiado.txt`
- Fecha: 2026-10-31 17:15 · Tiempo: 200 s

---

Paso 1: Primer if: len(productos) > 6. Reemplaza el valor, di si es True o False y si la función retorna aquí.
- len(productos) = 6, por lo tanto, 6 > 6 es False. La función no retorna aquí.

Paso 2: Segundo if: est.saldo - suma de precios < -1000. Calcula primero la resta, luego compárala con -1000, di si es True o False y si la función retorna aquí.
- est.saldo = 3000, suma de precios = 3800, entonces 3000 - 3800 = -800. -800 < -1000 es False. La función no retorna aquí.

Paso 3: Última línea: 7 <= hora <= 18. Reemplaza el valor y di qué retorna la función.
- hora = 18, entonces 7 <= 18 <= 18 es True. La función retorna True.

Paso 4: Para cada regla de <reglas>, busca la línea del código que la verifica. Si ninguna línea la verifica, escribe «no se valida».
- Regla 1: Se reciben pedidos de lunes a sábado, de 7:00 a 18:00. La función no verifica esta regla, por lo tanto, se valida.
- Regla 2: Máximo 5 productos por pedido. La función verifica len(productos) > 6, por lo tanto, se valida.
- Regla 3: Se paga con el saldo del carné; el saldo nunca puede quedar negativo. La función verifica est.saldo - suma de precios < -1000, por lo tanto, se valida.
- Regla 4: Los productos agotados no se pueden pedir. La función no verifica esta regla, por lo tanto, no se valida.
- Regla 5: Si el pedido no se recoge en 30 minutos, se cancela y se devuelve el saldo. La función no verifica esta regla, por lo tanto, no se valida.

Paso 5: Lista los errores, cada uno con la línea y la corrección.
- Regla 4: Los productos agotados no se pueden pedir. La función no verifica esta regla, por lo tanto, no se valida. La corrección es agregar una verificación para la regla 4 en la función.

Corrección del código:
```python
def crear_pedido(est, productos, hora):
    if len(productos) > 6:
        return False
    if est.saldo - sum(p.precio for p in productos) < -1000:
        return False
    if any(p.agotado for p in productos):
        return False
    return 7 <= hora <= 18
```
