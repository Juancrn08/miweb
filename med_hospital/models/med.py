# -*- coding: utf-8 -*-
from odoo import api, fields, models

class MedHospital(models.Model):
    _name = 'med.hospital.list'
    _description = 'MedHospital List'

    name = fields.Char(string='Medicamento', required = True)
    cantidad = fields.Float(string='Cantidad en inventario', default= '0', required = True)
    # forma = fields.Selection([
    #     ('tableta','Tableta'),
    #     ('ampula','Ampula'),
    #     ('capsula','Capsula'),
    #     ('jarabe','Jarabe'),
    #     ('bulbo','Bulbo'),
    #     ('bolsa','Bolsa'),
    #     ('suspencion','Suspencion')
    # ], string='Unidad de medida', default='tableta')
    # gramaje = fields.Integer(string='Dosis de presentacion')
    # tipoGR = fields.Selection([
    #     ('miligramo','miligramo'),
    #     ('mililitro','mililitro'),
    #     ('microgramo','microgramo'),
    # ], string='Tipo de Gramaje', default='miligramo')
