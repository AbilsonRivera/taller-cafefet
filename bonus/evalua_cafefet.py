"""Bonus · Parte B: evaluar dos versiones de un prompt con casos etiquetados a mano.

Adaptado de scripts/evalua.py del repositorio de la clase.

    cd bonus
    uv run evalua_cafefet.py
    uv run evalua_cafefet.py --modelo qwen3.5:0.8b
"""
import argparse
import sys
import re
import unicodedata
from comun import preguntar

sys.stdout.reconfigure(encoding="utf-8")   # en Windows, la salida redirigida a archivo sería cp1252

CATEGORIAS = ["PEDIDO", "CANCELACION", "RECLAMO", "CONSULTA"]

# (mensaje, etiqueta del equipo, ¿ambiguo?)
CASOS = [
    ("Quiero un tinto y dos pandebonos para las 9.", "PEDIDO", False),
    ("Cancelen mi pedido de las 11, por favor.", "CANCELACION", False),
    ("El sándwich estaba frío y le faltaba el queso.", "RECLAMO", False),
    ("¿Hasta qué hora reciben pedidos los sábados?", "CONSULTA", False),
    ("¿Cuántos productos puedo pedir como máximo?", "CONSULTA", False),
    ("La app me dejó pedir un jugo agotado y ahora no me lo entregan.", "RECLAMO", False),
    # Ambiguos: la etiqueta es una decisión del equipo
    ("¿Todavía hay buñuelos? Si hay, apártenme dos.", "PEDIDO", True),
    ("Me descontaron el saldo dos veces por el mismo pedido, ¿es normal?", "RECLAMO", True),
    ("Pedí hace 40 minutos y no alcancé a pasar, ¿me devuelven la plata?", "CANCELACION", True),
    ("Ya no voy a ir por el almuerzo, ¿lo pueden anular?", "CANCELACION", True),
]

V1 = """Clasifica el mensaje que un estudiante envió al chat de CafeFET en UNA categoría: PEDIDO, CANCELACION, RECLAMO o CONSULTA.
Responde solo con la categoría.
Mensaje: "{mensaje}\""""

V2 = """Clasifica el mensaje que un estudiante envió al chat de CafeFET, la cafetería de la FET, en UNA categoría.
- PEDIDO: quiere pedir o apartar productos, aunque lo escriba como pregunta.
- CANCELACION: quiere anular un pedido o recuperar el saldo de un pedido que no recogió (los pedidos que no se recogen en 30 minutos se cancelan y se devuelve el saldo), aunque lo escriba como pregunta.
- RECLAMO: algo salió mal con un cobro, un producto, la entrega o la app, aunque lo escriba como pregunta.
- CONSULTA: pregunta sobre horarios, reglas, menú o saldo, sin pedido, cancelación ni falla de por medio.

Ejemplos:
"¿Les queda pan de yuca? Si sí, guárdenme uno." -> PEDIDO
"No pude recoger mi almuerzo a tiempo, ¿qué pasa con mi plata?" -> CANCELACION
"El tinto me lo cobraron dos veces, ¿por qué?" -> RECLAMO

Responde solo con PEDIDO, CANCELACION, RECLAMO o CONSULTA.
Mensaje: "{mensaje}\""""


def normalizar(texto):
    """Quita tildes para que CANCELACIÓN y CANCELACION cuenten igual."""
    return "".join(c for c in unicodedata.normalize("NFD", texto.upper()) if unicodedata.category(c) != "Mn")


def clasificar(plantilla, mensaje, modelo):
    r = preguntar(plantilla.format(mensaje=mensaje), modelo=modelo, num_predict=10)
    m = re.search("|".join(CATEGORIAS), normalizar(r.message.content))
    return m.group(0) if m else r.message.content.strip()


ap = argparse.ArgumentParser()
ap.add_argument("--modelo", default="qwen3.5:4b")
a = ap.parse_args()

resultados = {}
for nombre, plantilla in [("v1", V1), ("v2", V2)]:
    resultados[nombre] = [clasificar(plantilla, m, a.modelo) for m, _, _ in CASOS]

print(f"# Salida · evalua_cafefet.py · modelo {a.modelo}\n")
print("| # | Mensaje | Esperado | v1 | v2 |")
print("|---|---|---|---|---|")
for i, (mensaje, esperado, ambiguo) in enumerate(CASOS, 1):
    celdas = []
    for nombre in ("v1", "v2"):
        obtenido = resultados[nombre][i - 1]
        celdas.append(obtenido if obtenido == esperado else f"**{obtenido}** ✗")
    marca = " *(ambiguo)*" if ambiguo else ""
    print(f"| {i} | {mensaje}{marca} | {esperado} | {celdas[0]} | {celdas[1]} |")

print()
for nombre in ("v1", "v2"):
    ok = sum(o == e for o, (_, e, _) in zip(resultados[nombre], CASOS))
    ok_amb = sum(o == e for o, (_, e, amb) in zip(resultados[nombre], CASOS) if amb)
    total_amb = sum(amb for _, _, amb in CASOS)
    print(f"- **{nombre}: {ok}/{len(CASOS)}** (ambiguos: {ok_amb}/{total_amb})")

arreglados = [i for i, ((_, e, _), o1, o2) in enumerate(zip(CASOS, resultados["v1"], resultados["v2"]), 1)
              if o1 != e and o2 == e]
empeorados = [i for i, ((_, e, _), o1, o2) in enumerate(zip(CASOS, resultados["v1"], resultados["v2"]), 1)
              if o1 == e and o2 != e]
print(f"- Fallan en v1 y no en v2: {arreglados or 'ninguno'}")
print(f"- Fallan en v2 y no en v1: {empeorados or 'ninguno'}")
