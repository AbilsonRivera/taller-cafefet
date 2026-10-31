# Salida · prompt3_casos_v2.txt

- Comando: `ollama run qwen-demo --think=false < reto3/prompt3_casos_v2.txt`
- Fecha: 2026-10-31 17:17 · Tiempo: 126 s

---

| Caso | Entrada | Resultado esperado | Criterio que cubre |
| :--- | :--- | :--- | :--- |
| CA1.1 | Usuario repite "Cappuccino" (precio 4,50€) y tiene saldo de 10€. El producto estaba en el último pedido y está disponible. | Se crea el nuevo pedido, se descuenta 4,50€ del carné y se muestra confirmación de compra exitosa. | CA1 |
| CA2.1 | Usuario intenta repetir "Cappuccino" (precio 4,50€) y "Croissant" (precio 3,00€). El "Cappuccino" está agotado. Saldo: 10€. | El sistema muestra el pedido con el "Cappuccino" marcado como no seleccionable (gris/rojo), impide añadirlo al carrito y bloquea la finalización de compra. | CA2 |
| CA3.1 | Usuario intenta repetir un pedido total de 8,00€ pero su saldo actual es de 5€. | El sistema muestra mensaje de error "Saldo insuficiente", cancela la operación sin restar dinero del carné y mantiene el saldo en 5€. | CA3 |
| CA4.1 | Usuario intenta finalizar un pedido repetido realizado hace 35 minutos (más de 30 min). Saldo actual: 10€. | El sistema detecta que el pedido caducó, cancela automáticamente la transacción, devuelve los fondos al carné y muestra mensaje "Pedido expirado". | CA4 |
