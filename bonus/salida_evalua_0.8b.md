# Salida · evalua_cafefet.py · modelo qwen3.5:0.8b

| # | Mensaje | Esperado | v1 | v2 |
|---|---|---|---|---|
| 1 | Quiero un tinto y dos pandebonos para las 9. | PEDIDO | PEDIDO | PEDIDO |
| 2 | Cancelen mi pedido de las 11, por favor. | CANCELACION | CANCELACION | CANCELACION |
| 3 | El sándwich estaba frío y le faltaba el queso. | RECLAMO | **PEDIDO** ✗ | RECLAMO |
| 4 | ¿Hasta qué hora reciben pedidos los sábados? | CONSULTA | **PEDIDO** ✗ | CONSULTA |
| 5 | ¿Cuántos productos puedo pedir como máximo? | CONSULTA | **PEDIDO** ✗ | **PEDIDO** ✗ |
| 6 | La app me dejó pedir un jugo agotado y ahora no me lo entregan. | RECLAMO | **PEDIDO** ✗ | **PEDIDO** ✗ |
| 7 | ¿Todavía hay buñuelos? Si hay, apártenme dos. *(ambiguo)* | PEDIDO | PEDIDO | PEDIDO |
| 8 | Me descontaron el saldo dos veces por el mismo pedido, ¿es normal? *(ambiguo)* | RECLAMO | RECLAMO | RECLAMO |
| 9 | Pedí hace 40 minutos y no alcancé a pasar, ¿me devuelven la plata? *(ambiguo)* | CANCELACION | **PEDIDO** ✗ | **PEDIDO** ✗ |
| 10 | Ya no voy a ir por el almuerzo, ¿lo pueden anular? *(ambiguo)* | CANCELACION | **RECLAMO** ✗ | CANCELACION |

- **v1: 4/10** (ambiguos: 2/4)
- **v2: 7/10** (ambiguos: 3/4)
- Fallan en v1 y no en v2: [3, 4, 10]
- Fallan en v2 y no en v1: ninguno
