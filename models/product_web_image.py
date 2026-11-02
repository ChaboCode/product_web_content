from odoo import fields, models


class ProductWebImage(models.Model):
    _name = 'product.web.image'
    _description = 'Imagen adicional de producto'
    _order = 'sequence, id'

    name = fields.Char(string='Nombre')
    sequence = fields.Integer(string='Secuencia', default=10)
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Producto',
        required=True,
        ondelete='cascade',
        index=True,
    )
    # Vacío = imagen general; con valores = solo para variantes que tengan alguno de ellos
    product_template_attribute_value_ids = fields.Many2many(
        'product.template.attribute.value',
        string='Valores de variante',
        domain="[('product_tmpl_id', '=', product_tmpl_id)]",
        help='Dejar vacío para una imagen general. Si se indican valores '
             '(p. ej. "Tablero Digital"), la imagen aplica solo a las variantes que los tengan.',
    )

    image_1920 = fields.Image(string='Imagen', max_width=1920, max_height=1920)
    image_1024 = fields.Image(
        string='Imagen 1024', related='image_1920',
        max_width=1024, max_height=1024, store=True,
    )
    image_512 = fields.Image(
        string='Imagen 512', related='image_1920',
        max_width=512, max_height=512, store=True,
    )
    image_128 = fields.Image(
        string='Imagen 128', related='image_1920',
        max_width=128, max_height=128, store=True,
    )
