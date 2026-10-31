# Salida · prompt2_criterios_v2.txt

- Comando: `ollama run qwen-demo --think=false < reto3/prompt2_criterios_v2.txt`
- Fecha: 2026-10-31 17:12 · Tiempo: 145 s

---

CA1. Pedido repetido exitoso (regla 4)
- Dado que el producto solicitado estaba en mi último pedido y actualmente está disponible
- Cuando repito ese pedido con un solo clic
- Entonces se crea el nuevo pedido, se descuenta el saldo del carné y se confirma la compra

CA2. Producto agotado impide repetición (regla 4)
- Dado que uno de los productos de mi último pedido está actualmente agotado
- Cuando intento repetir mi pedido completo con un solo clic
- Entonces el sistema me muestra el producto agotado como opción no seleccionable y no permite finalizar la compra

CA3. Saldo insuficiente impide repetición (regla 3)
- Dado que el saldo actual de mi carné es menor al precio total del último pedido
- Cuando intento repetir mi pedido con un solo clic
- Entonces el sistema me indica que no hay saldo suficiente y cancela la operación sin restar dinero

CA4. Pedido no recogido en tiempo (regla 5)
- Dado que mi pedido repetido fue realizado hace más de 30 minutos
- Cuando intento finalizar o consultar el estado del pedido
- Entonces el sistema cancela automáticamente el pedido y devuelve el saldo al carné
