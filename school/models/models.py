# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'The students'
    name = fields.Char(String = "Nombre", required=True)
    year = fields.Integer()
    topic_id= fields.Many2one("school.topic")

class Topic(models.Model):
    _name = 'school.topic'
    _description = 'The topics'
    name = fields.Char(String = "Topic Name", required=True)
    students_id= fields.Many2one("school.student", "topic_id")
    
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
