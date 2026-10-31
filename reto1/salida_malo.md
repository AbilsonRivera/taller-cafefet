# Salida · prompt_malo.txt

- Comando: `ollama run qwen-demo --think=false < reto1/prompt_malo.txt`
- Fecha: 2026-10-31 16:55 · Tiempo: 101 s

---

Aquí tienes un ejemplo completo de cómo crear una función para gestionar pedidos en **JavaScript**. Este código incluye la lógica para validar los datos, calcular el total y guardar el pedido en un array (simulando una base de datos).

### Ejemplo: Función `crearPedido`

```javascript
// Simulación de una base de datos vacía
let pedidos = [];

/**
 * Crea un nuevo pedido.
 * @param {string} idCliente - Identificador único del cliente.
 * @param {string} producto - Nombre del producto o servicio.
 * @param {number} cantidad - Cantidad a comprar (debe ser mayor a 0).
 * @param {number} precioUnitario - Precio por unidad.
 * @returns {Object} Objeto con el estado del pedido o un mensaje de error.
 */
function crearPedido(idCliente, producto, cantidad, precioUnitario) {
    // 1. Validaciones básicas
    if (!idCliente || !producto) {
        return { exito: false, mensaje: "El ID del cliente y el producto son obligatorios." };
    }

    if (cantidad <= 0 || isNaN(cantidad)) {
        return { exito: false, mensaje: "La cantidad debe ser un número mayor a cero." };
    }

    if (precioUnitario < 0) {
        return { exito: false, mensaje: "El precio no puede ser negativo." };
    }

    // 2. Cálculos
    const total = cantidad * precioUnitario;

    // 3. Crear el objeto del pedido
    const nuevoPedido = {
        id: Date.now(), // Genera un ID único basado en la fecha actual
        cliente: idCliente,
        producto: producto,
        cantidad: cantidad,
        precioUnitario: precioUnitario,
        total: total,
        fecha: new Date().toLocaleString()
    };

    // 4. Guardar en la "base de datos" (array)
    pedidos.push(nuevoPedido);

    // 5. Retornar resultado exitoso
    return {
        exito: true,
        mensaje: `Pedido creado exitosamente para ${idCliente}. Total: $${total.toFixed(2)}`,
        pedido: nuevoPedido
    };
}

// --- Pruebas de la función ---

console.log("--- Creando Pedido 1 ---");
const resultado1 = crearPedido("C001", "Laptop Gamer", 2, 1200);
if (resultado1.exito) {
    console.log(resultado1.mensaje);
    console.log(`ID del pedido: ${resultado1.pedido.id}`);
}

console.log("\n--- Creando Pedido 2 (Error de cantidad) ---");
const resultado2 = crearPedido("C002", "Mouse Inalámbrico", -5, 20);
if (!resultado2.exito) {
    console.log(resultado2.mensaje);
}

console.log("\n--- Verificando todos los pedidos guardados ---");
pedidos.forEach((p, index) => {
    console.log(`Pedido ${index + 1}: Cliente ${p.cliente}, Total $


