# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api


class player(models.Model):
   _name = 'expanse.player'    
   _description = 'Players of the game'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class colony(models.Model):
   _name = 'expanse.colomny'    
   _description = 'colonies'

   creadacion_data= fields.Datetime(default = fields.Datetime.now())