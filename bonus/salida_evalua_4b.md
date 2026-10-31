# Salida · evalua_cafefet.py · modelo qwen3.5:4b

| # | Mensaje | Esperado | v1 | v2 |
|---|---|---|---|---|
| 1 | Quiero un tinto y dos pandebonos para las 9. | PEDIDO | PEDIDO | PEDIDO |
| 2 | Cancelen mi pedido de las 11, por favor. | CANCELACION | CANCELACION | CANCELACION |
| 3 | El sándwich estaba frío y le faltaba el queso. | RECLAMO | RECLAMO | RECLAMO |
| 4 | ¿Hasta qué hora reciben pedidos los sábados? | CONSULTA | CONSULTA | CONSULTA |
| 5 | ¿Cuántos productos puedo pedir como máximo? | CONSULTA | CONSULTA | CONSULTA |
| 6 | La app me dejó pedir un jugo agotado y ahora no me lo entregan. | RECLAMO | RECLAMO | RECLAMO |
| 7 | ¿Todavía hay buñuelos? Si hay, apártenme dos. *(ambiguo)* | PEDIDO | PEDIDO | PEDIDO |
| 8 | Me descontaron el saldo dos veces por el mismo pedido, ¿es normal? *(ambiguo)* | RECLAMO | RECLAMO | RECLAMO |
| 9 | Pedí hace 40 minutos y no alcancé a pasar, ¿me devuelven la plata? *(ambiguo)* | CANCELACION | **RECLAMO** ✗ | CANCELACION |
| 10 | Ya no voy a ir por el almuerzo, ¿lo pueden anular? *(ambiguo)* | CANCELACION | CANCELACION | CANCELACION |

- **v1: 9/10** (ambiguos: 3/4)
- **v2: 10/10** (ambiguos: 4/4)
- Fallan en v1 y no en v2: [9]
- Fallan en v2 y no en v1: ninguno
