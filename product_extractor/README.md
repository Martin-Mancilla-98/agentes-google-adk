# product_extractor — Salida estructurada con `output_schema`

Un agente que lee la descripción de un producto y devuelve **siempre** un JSON con la misma forma, validado por Pydantic.

## Qué demuestra

- `output_schema=ProductInfo`: ADK obliga al modelo a responder con la estructura del modelo Pydantic (`product_name`, `price`, `storage`, `color`), con tipos validados y valores por defecto.
- `output_key="extracted_product"`: la respuesta se guarda en el estado de la sesión bajo esa clave, lista para que otro agente o el código de la aplicación la use.
- Limitación importante: un agente con `output_schema` **no puede usar herramientas** ni transferir a otros agentes; solo produce la estructura.

## Probar

```bash
adk web
```

Elegir `product_extractor` y describir un producto:

- `Quiero el iPhone 15 Pro de 256GB en titanio negro, sale 999 dólares`
- `Vi una notebook Lenovo de 1TB a $850`

Qué observar: la respuesta es JSON puro. En la pestaña **State** aparece `extracted_product` con el objeto. En el segundo ejemplo, `color` toma el valor por defecto `"No se especifica"`.
