# Salida · prompt_nuevo.txt

- Comando: `ollama run qwen-demo --think=false < reto1/prompt_nuevo.txt`
- Fecha: 2026-10-31 16:57 · Tiempo: 76 s

---

```python
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any

def crear_pedido(
    estudiante: Dict[str, int], 
    productos: List[Dict[str, Any]], 
    ahora: datetime
) -> Tuple[bool, str, datetime]:
    """
    Valida un pedido anticipado de CafeFET y calcula la hora límite de recogida.

    Args:
        estudiante: Diccionario con 'saldo' (int).
        productos: Lista de diccionarios con 'nombre', 'precio' y 'agotado'.
        ahora: datetime de la hora actual del pedido.

    Returns:
        Tupla (aceptado, motivo, recoger_antes_de):
            - aceptado: bool indicando si el pedido es válido.
            - motivo: "OK" o descripción del error.
            - recoger_antes_de: datetime límite o None si rechazado.
    """
    # Regla 1: Días y horas (Lun-Sab, 7:00-18:00)
    if ahora.weekday() == 6 or ahora.hour < 7 or ahora.hour > 18:
        return False, "Horario inválido", None

    # Regla 2: Máximo 5 productos y no vacío
    if len(productos) == 0 or len(productos) > 5:
        return False, "Cantidad de productos inválida", None

    total = sum(p['precio'] for p in productos if not p['agotado'])

    # Regla 4: Productos agotados
    if any(p['agotado'] for p in productos):
        return False, "Producto(s) agotado(s)", None

    # Regla 3: Saldo suficiente
    if estudiante['saldo'] < total:
        return False, "Saldo insuficiente", None

    # Si todo es válido, calcular hora límite (ahora + 30 min)
    recoger_antes_de = ahora + timedelta(minutes=30)
    return True, "OK", recoger_antes_de
```
