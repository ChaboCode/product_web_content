from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    web_purchase = fields.Boolean(
        string='Compra en línea',
        help='Este producto podrá pagarse en el sitio web'
    )
    web_description = fields.Html(
        string='Descripción web',
        translate=True,
        sanitize_attributes=False,
    )
    web_image_ids = fields.One2many(
        'product.web.image',
        'product_tmpl_id',
        string='Imágenes adicionales',
        copy=True,
    )
