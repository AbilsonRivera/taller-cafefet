"""Reto 4 · Parte B reproducida desde código: los mismos mensajes de parte_b_comandos.txt.

El chat de `ollama run` reenvía en cada turno toda la conversación al servidor (/api/chat)
con las opciones fijadas con /set. Este script hace exactamente eso, pero además muestra
cuántos tokens leyó el modelo en cada turno (prompt_eval_count), para ver el recorte.

    uv run reto4/parte_b_chat.py > reto4/salida_parte_b.md
"""
import sys
from ollama import chat

sys.stdout.reconfigure(encoding="utf-8")   # en Windows, la salida redirigida a archivo sería cp1252

MODELO = "qwen-demo"
OPCIONES = {"num_ctx": 512}          # equivale a /set parameter num_ctx 512
MARCA = "CafeFET responde:"

REGLA_CHAT = f"Regla: empieza SIEMPRE tu respuesta con «{MARCA}». ¿Entendido?"
REGLA_SYSTEM = f"Empieza SIEMPRE tu respuesta con «{MARCA}»."
P1 = ("Explica en al menos 400 palabras cómo funciona un pedido anticipado en CafeFET, desde que "
      "el estudiante lo hace en la app hasta que lo recoge en la cafetería.")
P2 = "Explica en al menos 400 palabras cómo debe manejar CafeFET el saldo del carné para que nunca quede negativo."


def turno(historial, texto, etiqueta):
    historial.append({"role": "user", "content": texto})
    r = chat(model=MODELO, messages=historial, options=OPCIONES, think=False)
    respuesta = r.message.content
    historial.append({"role": "assistant", "content": respuesta})
    cumple = respuesta.lstrip(" «\"*#").startswith(MARCA)
    palabras = len(respuesta.split())
    print(f"### {etiqueta}\n")
    print(f"- Mensaje enviado: «{texto}»")
    print(f"- Mensajes en el historial enviado: {len(historial) - 1}")
    print(f"- Tokens que el modelo realmente leyó (prompt_eval_count): {r.prompt_eval_count}")
    print(f"- Tokens generados: {r.eval_count} · Palabras: {palabras}")
    print(f"- ¿Empieza con «{MARCA}»? **{'SÍ' if cumple else 'NO'}**\n")
    print("```text")
    print(respuesta.strip())
    print("```\n")
    return cumple


print("# Salida · Reto 4 · Parte B (qwen-demo, num_ctx 512, --think=false)\n")
print("## Versión A · la regla como mensaje del chat\n")
historial = []
turno(historial, REGLA_CHAT, "A0 · la regla")
a1 = turno(historial, P1, "A1 · primera pregunta larga")
a2 = turno(historial, P2, "A2 · segunda pregunta larga")

print("## Versión B · la misma regla como system prompt\n")
historial = [{"role": "system", "content": REGLA_SYSTEM}]
b1 = turno(historial, P1, "B1 · primera pregunta larga")
b2 = turno(historial, P2, "B2 · segunda pregunta larga")

print("## Resumen\n")
print("| Versión | Dónde está la regla | Respuesta 1 | Respuesta 2 |")
print("|---|---|---|---|")
print(f"| A | Mensaje del chat | {'SÍ' if a1 else 'NO'} | {'SÍ' if a2 else 'NO'} |")
print(f"| B | System prompt | {'SÍ' if b1 else 'NO'} | {'SÍ' if b2 else 'NO'} |")
