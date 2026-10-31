# Salida · prompt3_casos.txt

- Comando: `ollama run qwen-demo --think=false < reto3/prompt3_casos.txt`
- Fecha: 2026-10-31 17:08 · Tiempo: 144 s

---

| Caso | Entrada | Resultado esperado | Criterio que cubre |
| :--- | :--- | :--- | :--- |
| CP1 | **Entrada**: Estudiante "Juan Pérez" con saldo de 20€ en el carné. Hace clic en "Repetir pedido" tras haber comprado ayer un *Cappuccino* (4.50€) y una *Croissant* (2.00€).<br>**Contexto**: Fecha actual: 15/10/2023, Hora: 12:30 PM.<br>**Estado previo**: El sistema recuerda el pedido de ayer correctamente. | **Resultado**: La pantalla se actualiza mostrando automáticamente el *Cappuccino* y la *Croissant* con sus precios originales (4.50€ y 2.00€). El total del carrito es de 6.50€. No aparecen productos nuevos ni opciones de selección manual para estos ítems. | CA1 |
| CP2 | **Entrada**: Estudiante "María García" con saldo de 5€ en el carné. Hace clic en "Repetir pedido".<br>**Contexto**: Fecha actual: 16/10/2023, Hora: 09:15 AM.<br>**Estado previo**: No tiene pedidos registrados en el historial del sistema (es su primera vez). | **Resultado**: El carrito de compras permanece vacío. Se muestra un mensaje informativo al usuario indicando que no hay pedidos anteriores para repetir. | CA1 |
| CP3 | **Entrada**: Estudiante "Carlos Ruiz" con saldo de 10€ en el carné. Hace clic en "Repetir pedido".<br>**Contexto**: Fecha actual: 17/10/2023, Hora: 14:00 PM.<br>**Estado previo**: Su último pedido fue hace 3 días (fuera del límite de retención de 24h). | **Resultado**: El carrito permanece vacío. Se muestra un mensaje indicando que el pedido anterior ha caducado y no puede ser repetido automáticamente. | CA1 |
