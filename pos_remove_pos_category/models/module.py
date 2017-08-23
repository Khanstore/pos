# -*- coding: utf-8 -*-
# Copyright (C) 2015-TODAY Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class Module(models.Model):

    _inherit = 'ir.module.module'

    def module_uninstall(self, cr, uid, ids, context=None):

        context = context or {}

        for module in self.browse(cr, uid, ids, context=context):
            if module.name == 'pos_remove_pos_category':

                # As we have loose previous POS categs restore them
                # in a sane empty state

                cr.execute('UPDATE product_template SET pos_categ_id=NULL')

                # And restore original constraint
                cr.execute('''
                    ALTER TABLE product_template
                    DROP CONSTRAINT IF EXISTS
                    product_template_pos_categ_id_fkey
                ''')

                cr.execute('''
                    ALTER TABLE product_template ADD CONSTRAINT
                    "product_template_pos_categ_id_fkey"
                    FOREIGN KEY (pos_categ_id)
                    REFERENCES pos_category(id) ON DELETE SET NULL;
                ''')

                # Restore POS category menu action
                # in SQL because pool/env is not available here
                cr.execute('''
                    UPDATE ir_act_window iaw SET res_model='pos.category'
                    FROM ir_model_data imd
                    WHERE
                        iaw.id = imd.res_id AND
                        imd.model = 'ir.actions.act_window' AND
                        imd.name = 'product_pos_category_action'
                ''')

                break

        return super(Module, self).module_uninstall(
            cr, uid, ids, context=context
        )
