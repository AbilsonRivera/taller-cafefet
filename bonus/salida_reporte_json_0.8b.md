# Salida · reporte_json_cafefet.py · modelo qwen3.5:0.8b

## Mensaje 1

> Hola, quiero 2 empanadas y un tinto para recoger a las 10:30. La empanada sin ají, porfa.

```json
{
  "accion": "crear",
  "productos": [
    {
      "nombre": "Empanada sin ají",
      "cantidad": 2
    }
  ],
  "hora_recogida": "10:30",
  "observaciones": null,
  "faltantes": []
}
```

Alertas de negocio: ninguna

## Mensaje 2

> ¿Me apartan un almuerzo ejecutivo y una limonada de coco? Paso a las 12 y media.

```json
{
  "accion": "crear",
  "productos": [
    {
      "nombre": "almuerzo ejecutivo",
      "cantidad": 1
    },
    {
      "nombre": "limonada de coco",
      "cantidad": 1
    }
  ],
  "hora_recogida": "12:30",
  "observaciones": "",
  "faltantes": [
    "productos"
  ]
}
```

Alertas de negocio: ninguna

## Mensaje 3

> Cancelen mi pedido de las 3 de la tarde, ya no voy a poder ir.

```json
{
  "accion": "cancelar",
  "productos": [],
  "hora_recogida": null,
  "observaciones": "Ya no voy a poder ir.",
  "faltantes": [
    "productos",
    "hora_recogida"
  ]
}
```

Alertas de negocio: ninguna

## Mensaje 4

> En el pedido de las 4 pm cámbienme el jugo de mora por uno de lulo.

```json
{
  "accion": "crear",
  "productos": [
    {
      "nombre": "Lulo",
      "cantidad": 1
    }
  ],
  "hora_recogida": "16:00",
  "observaciones": "Cambio de jugo de mora por lulo.",
  "faltantes": []
}
```

Alertas de negocio: ninguna

## Mensaje 5

> Quiero lo de siempre.

```json
{
  "accion": "crear",
  "productos": [
    {
      "nombre": "Café especial",
      "cantidad": 1
    },
    {
      "nombre": "Chocolate",
      "cantidad": 1
    }
  ],
  "hora_recogida": "09:00",
  "observaciones": "Quiero lo de siempre.",
  "faltantes": [
    "productos",
    "hora_recogida"
  ]
}
```

Alertas de negocio: ninguna

## Mensaje 6

> Dos pandebonos y... no sé, algo de tomar. Paso más tarde.

```json
{
  "accion": "crear",
  "productos": [
    {
      "nombre": "Pandeboón",
      "cantidad": 1
    },
    {
      "nombre": "Pandeboón",
      "cantidad": 1
    }
  ],
  "hora_recogida": null,
  "observaciones": "algo de tomar",
  "faltantes": [
    "productos",
    "hora_recogida"
  ]
}
```

Alertas de negocio: ninguna

