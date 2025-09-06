# product_supplier_cost_sync 

Módulo para Odoo que permite definir descuentos encadenados usando una cadena tipo `5+3+10`, aplicarlos sobre el precio del proveedor, y actualizar automáticamente el costo del producto (`standard_price`) en la moneda de la empresa.

## ⚙️ Funciones

- Calcula automáticamente el descuento total desde `discount_chain`
- Aplica el descuento sobre el precio de proveedor (`price`)
- Convierte el precio neto desde la moneda del proveedor a la moneda de la empresa usando el tipo de cambio más reciente disponible
- Actualiza automáticamente el costo estándar del producto y sus variantes
- Compatible con multiempresa y multimoneda
- Soporta importaciones desde CSV/Excel
- Valida el formato de la cadena de descuentos
- Compatible con Odoo 17+

## 🧮 Ejemplo de cálculo

Para una cadena `"5+3+10"` y un precio en dólares:
- Precio base (USD): $100
- Descuento total aplicado: **17.065%**
- Precio neto: **$82.94**
- Tipo de cambio USD/ARS: **900**
- Costo actualizado en ARS: **$74.646**

> ⚠️ El tipo de cambio se toma automáticamente de la fecha más reciente disponible en `res.currency.rate`.

## ⚡ Acción manual para recalcular costos por tipo de cambio

El módulo incluye una **acción de servidor** llamada:

> `Actualizar costos por tipo de cambio actualizado hoy`

Esta acción:
- Recorre todos los proveedores que tienen moneda diferente a la de la empresa.
- Verifica si el tipo de cambio de esa moneda fue actualizado hoy.
- Si corresponde, recalcula y actualiza el costo (`standard_price`) automáticamente.

🔐 Solo está disponible para usuarios con permisos de administración.

🧠 Ideal para ejecutarla manualmente luego de actualizar tipos de cambio (por API o archivo).

## 📍 Ubicación del menú

Podés ejecutar la acción manualmente desde:

**Facturación > Configuración > Monedas > Actualizar costos por tipo de cambio**

🔐 Solo visible para usuarios con permisos de administración.

## 🛠️ Instalación

1. Copiar el módulo en tu carpeta de `addons`
2. Actualizar la lista de módulos
3. Instalar desde la interfaz de Odoo

## 📥 Importación

Podés importar productos o tarifas de proveedor incluyendo estos campos:

- `discount_chain`: Ej. `5+3+10`
- `price`: Precio bruto
- `currency_id`: Moneda del proveedor

El módulo calculará automáticamente el descuento, realizará la conversión de moneda, y actualizará el costo (`standard_price`).

## 🔍 Registro automático

Toda actualización del precio de proveedor (sea por importación o edición manual) actualizará automáticamente el costo del producto.

## 🧑‍💻 Autor

Desarrollado por [Fernando Giacomino](https://github.com/fernandogiacomino) con ayuda de Copilot ✨

## 📄 Licencia

Este módulo está disponible bajo la licencia LGPL-3.0.