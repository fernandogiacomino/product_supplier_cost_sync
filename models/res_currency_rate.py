from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    @api.constrains('currency_id', 'name', 'company_id')
    def _check_unique_currency_rate_per_day(self):
        for rec in self:
            domain = [
                ('id', '!=', rec.id),
                ('currency_id', '=', rec.currency_id.id),
                ('name', '=', rec.name),
                ('company_id', '=', rec.company_id.id),
            ]
            if self.search_count(domain):
                raise ValidationError(
                    f"Ya existe una tasa de cambio para {rec.currency_id.name} en la fecha {rec.name}."
                )