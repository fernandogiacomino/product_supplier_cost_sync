from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    discount_chain = fields.Char(
        string="Descuento Secuencial",
        help="Permite añadir varios descuentos que se aplican en cadena. Ej: 5+3+10"
    )
    discount = fields.Float("Descuento (%)")

    @api.onchange("discount_chain")
    def _onchange_discount_chain(self):
        for rec in self:
            rec._compute_discount_from_chain_onchange()

    def _compute_discount_from_chain_onchange(self):
        if self.discount_chain:
            try:
                discounts = [float(d.strip()) for d in self.discount_chain.split("+") if d.strip()]
                result = 1.0
                for d in discounts:
                    result *= (1 - d / 100)
                self.discount = round((1 - result) * 100, 4)
            except Exception:
                self.discount = 0.0
        else:
            self.discount = 0.0

    @api.model
    def create(self, vals):
        vals = self._compute_discount_from_chain(vals)
        record = super().create(vals)
        record._update_standard_price()
        return record

    def write(self, vals):
        vals = self._compute_discount_from_chain(vals)
        res = super().write(vals)
        for rec in self:
            if 'price' in vals or 'discount_chain' in vals:
                rec._update_standard_price()
        return res

    def _compute_discount_from_chain(self, vals):
        chain = vals.get("discount_chain")
        if chain:
            try:
                discounts = [float(d.strip()) for d in chain.split("+") if d.strip()]
                result = 1.0
                for d in discounts:
                    result *= (1 - d / 100)
                vals["discount"] = round((1 - result) * 100, 4)
            except Exception:
                vals["discount"] = 0.0
        elif "discount_chain" in vals:
            vals["discount"] = 0.0
        return vals

    def _update_standard_price(self):
        for rec in self:
            product = rec.product_tmpl_id
            if not product or not rec.price:
                continue

            discount = rec.discount or 0.0
            net_price = rec.price * (1 - discount / 100.0)

            supplier_currency = rec.currency_id or rec.company_id.currency_id
            company_currency = rec.company_id.currency_id

            if supplier_currency != company_currency:
                latest_rate = supplier_currency.rate_ids.filtered(
                    lambda r: r.name <= date.today()
                ).sorted(key=lambda r: r.name, reverse=True)
                if latest_rate:
                    rate = latest_rate[0].rate
                    converted_price = net_price * rate
                else:
                    converted_price = net_price  # fallback sin conversión
            else:
                converted_price = net_price

            product.standard_price = converted_price
            for variant in product.product_variant_ids:
                variant.standard_price = converted_price

    @api.constrains("discount_chain")
    def _check_discount_chain_format(self):
        for rec in self:
            if rec.discount_chain:
                for d in rec.discount_chain.split("+"):
                    d_clean = d.strip().replace(".", "", 1)
                    if not d_clean.replace(".", "", 1).isdigit():
                        raise ValidationError(
                            _("La cadena de descuentos contiene un valor inválido: '%s'.") % d
                        )

    @api.model
    def ejecutar_actualizacion_costos_tipo_cambio(self):
        today = fields.Date.today()
        actualizados_por_moneda = {}  # moneda → cantidad

        suppliers = self.search([
            ('currency_id', '!=', False),
            ('currency_id.name', '!=', self.env.company.currency_id.name)
        ])

        for rec in suppliers:
            latest_rate = rec.currency_id.rate_ids.filtered(
                lambda r: r.name <= today
            ).sorted(key=lambda r: r.name, reverse=True)

            if latest_rate:
                rec._update_standard_price()
                moneda = rec.currency_id.name
                actualizados_por_moneda[moneda] = actualizados_por_moneda.get(moneda, 0) + 1

        if not actualizados_por_moneda:
            return _("No se actualizó ningún producto (no hay tasas válidas).")

        detalle = "\n".join([
            _("💱 %(moneda)s: %(cantidad)d producto(s) actualizado(s)") % {
                'moneda': moneda, 'cantidad': cantidad
            } for moneda, cantidad in actualizados_por_moneda.items()
        ])

        return _("✅ Costos actualizados por tipo de cambio:\n\n") + detalle