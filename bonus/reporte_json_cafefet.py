"""Bonus · Parte A: de un mensaje de chat de CafeFET a datos validados con Pydantic.

Adaptado de scripts/reporte_json.py del repositorio de la clase.

    cd bonus
    uv run reporte_json_cafefet.py
    uv run reporte_json_cafefet.py --modelo qwen3.5:0.8b
"""
import argparse
import sys
from typing import Literal
from pydantic import BaseModel, Field
from comun import preguntar

sys.stdout.reconfigure(encoding="utf-8")   # en Windows, la salida redirigida a archivo sería cp1252


class Producto(BaseModel):
    nombre: str
    cantidad: int = Field(ge=1)


class PedidoChat(BaseModel):
    accion: Literal["crear", "modificar", "cancelar", "consultar"]
    productos: list[Producto]
    hora_recogida: str | None          # "HH:MM" en 24 h, o null si el mensaje no la dice
    observaciones: str | None
    faltantes: list[Literal["productos", "hora_recogida"]]


MENSAJES = [
    # Claros
    "Hola, quiero 2 empanadas y un tinto para recoger a las 10:30. La empanada sin ají, porfa.",
    "¿Me apartan un almuerzo ejecutivo y una limonada de coco? Paso a las 12 y media.",
    "Cancelen mi pedido de las 3 de la tarde, ya no voy a poder ir.",
    "En el pedido de las 4 pm cámbienme el jugo de mora por uno de lulo.",
    # Incompletos o ambiguos
    "Quiero lo de siempre.",
    "Dos pandebonos y... no sé, algo de tomar. Paso más tarde.",
]

PROMPT = """Extrae los datos del mensaje que un estudiante envió por chat a CafeFET, la cafetería de la FET.
- accion: crear (pedido nuevo), modificar (cambiar un pedido que ya existe), cancelar o consultar.
- productos: solo los que el mensaje nombra explícitamente, con su cantidad (1 si no la dice).
- hora_recogida: hora concreta en formato HH:MM de 24 horas; null si el mensaje no da una hora concreta.
- observaciones: indicaciones especiales del estudiante; null si no hay.
- faltantes: datos necesarios para preparar el pedido que el mensaje no trae (productos, hora_recogida).
No inventes productos ni horas.
<mensaje>{texto}</mensaje>"""


def alertas_de_negocio(p: PedidoChat) -> list[str]:
    """Reglas de CafeFET que se pueden comprobar en código sobre el JSON ya validado."""
    alertas = []
    total = sum(x.cantidad for x in p.productos)
    if total > 5:
        alertas.append(f"{total} productos: supera el máximo de 5")
    if p.hora_recogida:
        try:
            h, m = map(int, p.hora_recogida.split(":"))
            if not (7 * 60 <= h * 60 + m <= 18 * 60):
                alertas.append(f"hora {p.hora_recogida} fuera del horario 7:00-18:00")
        except ValueError:
            alertas.append(f"hora_recogida con formato inválido: {p.hora_recogida!r}")
    return alertas


ap = argparse.ArgumentParser()
ap.add_argument("--modelo", default="qwen3.5:4b")
a = ap.parse_args()

print(f"# Salida · reporte_json_cafefet.py · modelo {a.modelo}\n")
for i, texto in enumerate(MENSAJES, 1):
    r = preguntar(PROMPT.format(texto=texto), modelo=a.modelo, formato=PedidoChat.model_json_schema())
    print(f"## Mensaje {i}\n\n> {texto}\n")
    try:
        pedido = PedidoChat.model_validate_json(r.message.content)   # falla si el JSON no cumple el esquema
    except Exception as e:
        print(f"**JSON inválido:** {e}\n\n```\n{r.message.content}\n```\n")
        continue
    print("```json")
    print(pedido.model_dump_json(indent=2))
    print("```\n")
    alertas = alertas_de_negocio(pedido)
    print(f"Alertas de negocio: {'; '.join(alertas) if alertas else 'ninguna'}\n")
