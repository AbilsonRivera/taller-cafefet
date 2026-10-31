# Salida · prompt3_casos_v3.txt

- Comando: `ollama run qwen-demo --think=false < reto3/prompt3_casos_v3.txt`
- Fecha: 2026-10-31 17:24 · Tiempo: 386 s

---

| Caso | Entrada | Resultado esperado | Criterio que cubre |
| :--- | :--- | :--- | :--- |
| CA1-01 | **Entrada**: Repetir pedido del día lunes 10:00 AM.<br>**Productos**: Tinto ($2.000), Empanada ($3.500).<br>**Saldo Carné**: $6.000 (suficiente para el total de $5.500). | Se crea el nuevo pedido, se descuenta $5.500 del saldo y se muestra confirmación de compra exitosa. | CA1 |
| CA2-01 | **Entrada**: Repetir pedido del día lunes 10:00 AM.<br>**Productos**: Tinto ($2.000), Empanada ($3.500).<br>**Estado actual**: La empanada está agotada, el tinto disponible.<br>**Saldo Carné**: $6.000. | El sistema muestra la empanada como opción gris/no seleccionable; al intentar añadir, bloquea la acción y permite finalizar solo con el tinto ($2.000). | CA2 |
| CA3-01 | **Entrada**: Repetir pedido del día lunes 10:00 AM.<br>**Productos**: Tinto ($2.000), Empanada ($3.500).<br>**Saldo Carné**: $4.000 (insuficiente para el total de $5.500). | El sistema muestra un mensaje de error indicando saldo insuficiente y cancela la operación sin restar dinero al carné. | CA3 |
| CA4-01 | **Entrada**: Intentar finalizar/consultar pedido realizado originalmente el sábado 17:30 PM.<br>**Tiempo transcurrido**: Más de 30 minutos desde la hora de entrega original (ej. hoy 8:00 AM).<br>**Saldo Carné**: $6.000. | El sistema cancela automáticamente el pedido, devuelve los $5.500 al carné y muestra mensaje de "Pedido expirado". | CA4 |

*Nota: Se han verificado que cada criterio (CA1, CA2, CA3, CA4) tiene al menos un caso de prueba correspondiente.*
