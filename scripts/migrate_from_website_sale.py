# Migra datos de website_sale a product_web_content.
#
# Uso (con product_web_content YA instalado y website_sale AÚN instalado):
#   1. Respaldar la base de datos.
#   2. odoo shell -c /etc/odoo/odoo.conf -d NOMBRE_BD < migrate_from_website_sale.py
#   3. Revisar el resumen impreso y verificar en la UI antes de desinstalar website_sale.
#
# Es idempotente: no vuelve a copiar imágenes en productos que ya tienen
# imágenes en product.web.image, y solo copia la descripción si el campo
# nuevo está vacío para ese idioma.

Template = env['product.template'].with_context(active_test=False)
has_product_image = 'product.image' in env
langs = [code for code, _name in env['res.lang'].get_installed()]

n_desc = 0
n_img = 0
n_tmpl = 0

for tmpl in Template.search([]):
    touched = False

    # Descripción de ecommerce -> descripción web (por idioma)
    for code in langs:
        t = tmpl.with_context(lang=code)
        src = t.description_ecommerce
        if src and not t.web_description:
            t.web_description = src
            n_desc += 1
            touched = True

    # Imágenes extra de website_sale -> product.web.image
    if has_product_image and not tmpl.web_image_ids:
        images = env['product.image'].search(
            [('product_tmpl_id', '=', tmpl.id)], order='sequence, id')
        for img in images:
            if not img.image_1920:
                continue  # entradas de solo video
            env['product.web.image'].create({
                'name': img.name,
                'sequence': img.sequence,
                'product_tmpl_id': tmpl.id,
                'image_1920': img.image_1920,
            })
            n_img += 1
            touched = True

    n_tmpl += touched

env.cr.commit()
print(f"Productos migrados: {n_tmpl} | descripciones: {n_desc} | imágenes: {n_img}")
