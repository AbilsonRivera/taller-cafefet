# Salida · prompt_variante_sin_restricciones.txt

- Comando: `ollama run qwen-demo --think=false < reto1/prompt_variante_sin_restricciones.txt`
- Fecha: 2026-10-31 16:59 · Tiempo: 93 s

---

```python
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any

def crear_pedido(
    estudiante: Dict[str, Any], 
    productos: List[Dict[str, Any]], 
    ahora: datetime
) -> Tuple[bool, str, datetime | None]:
    """
    Valida un pedido anticipado de CafeFET y calcula la hora límite de recogida.

    Si el pedido es válido, devuelve True y la hora límite (ahora + 30 minutos).
    Si no es válido, devuelve False, una descripción del motivo de rechazo y None.

    Args:
        estudiante: Diccionario con al menos la clave 'saldo' (int).
        productos: Lista de diccionarios con claves 'nombre' (str), 'precio' (int) y 'agotado' (bool).
        ahora: datetime con la fecha y hora actual del pedido.

    Returns:
        Tuple[bool, str, datetime | None]:
            - bool: True si el pedido es válido, False si no lo es.
            - str: "OK" si es válido, o una descripción de la regla infringida si no lo es.
            - datetime | None: La hora límite de recogida (ahora + 30 min) si es válido, None si no.
    """
    # Regla 1: Validar día y hora de recepción (Lunes a Sábado, 7:00 - 18:00 inclusive)
    if ahora.weekday() == 6:  # 6 es domingo en Python
        return False, "Solo se reciben pedidos de lunes a sábado", None
    
    if ahora.hour < 7 or ahora.hour > 18:
        return False, "Los pedidos solo se reciben entre las 7:00 y las 18:00", None

    # Regla 2: Validar que haya productos y máximo 5
    if not productos:
        return False, "Un pedido vacío no es válido", None
    
    if len(productos) > 5:
        return False, "Máximo 5 productos por pedido", None

    # Calcular total y validar productos agotados + saldo
    total = 0
    for prod in productos:
        if prod['agotado']:
            return False, "No se pueden pedir productos agotados", None
        
        total += prod['precio']
    
    saldo_actual = estudiante.get('saldo', 0)
    
    # Regla 3: Saldo nunca negativo
    if total > saldo_actual:
        return False, "El saldo del carné no es suficiente para cubrir el pedido", None

    # Si todo pasa, el pedido es válido
    motivo = "OK"
    recoger_antes_de = ahora + timedelta(minutes=30)
    
    return True, motivo, recoger_antes_de
```
