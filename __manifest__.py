{
    'name': 'Product Supplier Cost Sync',
    'version': '1.0',
    'summary': 'Actualiza el costo del producto desde precios de proveedor con descuentos y conversión de moneda',
    'depends': ['product', 'purchase'],
    'author': 'Fernando + Copilot',
    'data': ['views/update_costs_by_currency_rate_action.xml',
             'views/product_supplierinfo_views.xml',
             'views/menu_update_costs_action.xml'],
    'category': 'Inventory',
    'installable': True,
    'auto_install': False,
}