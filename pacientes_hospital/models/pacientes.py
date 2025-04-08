# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

    # Modelo De PacientesHospital
class PacientesHospital(models.Model):

    _name = "pacientes.hospital"
    # _inherit = "paciente.medicamento_asignado"
    _description = "Pacientes Hospital"
    _inherit = ['mail.thread'] 
    
        #Campos y relaciones entre Modelos
    name = fields.Char(string="Nombre del Paciente", required=True)
    last_name = fields.Char(string="Apellido del Paciente", required=True)
    age = fields.Integer(string="Edad del Paciente", required=True)
    weight = fields.Integer(string="Peso(Kg)", required=True)
    pathology = fields.Char(string="Patologia", required=True)
    other_pathology = fields.Char(string="Otras Patologias", required=True)
    medicamento_ids = fields.One2many('paciente.medicamento_asignado', 'paciente_id', string="Tratamiento Asignados")
   

        #Compute para medicamentos asignados
    @api.depends('medicamento_ids')
    def _compute_medicamentos_asignados(self):
        for record in self:
            record.medicamentos_asignados = ', '.join([m.medicamento_id.name for m in record.medicamento_ids])

    medicamentos_asignados = fields.Char(string="Medicamentos Asignados", compute='_compute_medicamentos_asignados', store=True, readonly = False)

        #Obtener de los medicamentos_id "cantidad asignada"
    def get_medicamentos_asignados(self):
       return self.medicamento_ids.mapped('cantidad_asignada')
   
   # O directamente en una función compute: (Lo mismo de arriba pero con un compute)
    @api.depends('medicamento_ids.cantidad_asignada')
    def _compute_total_cantidad_asignada(self):
       for record in self:
           record.total_cantidad_asignada = sum(record.medicamento_ids.mapped('cantidad_asignada'))
    total_cantidad_asignada = fields.Float(string="Total Asignado", compute='_compute_total_cantidad_asignada', store=True)

        #Obtener los campos de los medicamentos que son editables
    @api.model
    def _fields(self):
        fields = super()._fields()
        if 'medicamento_ids' in fields:
            fields['medicamento_ids'].readonly = False  # Por ejemplo, si quieres que sea editable
        return fields

        # Estados para los campos
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('saved', 'Guardado'),
        # Puedes agregar más estados según tus necesidades
    ], string='Estado', default='draft')

        # Variable recogiendo los medicamento activos en pacientes
    medicamentos_activos = fields.One2many(
        'paciente.medicamento_asignado', 
        'paciente_id', 
        string="Medicamentos Activos",
        domain=[('active', '=', True)]
    )
        # Variable para fecha final del tratamiento
    proxima_fecha_fin = fields.Date(
        string="Próximo Vencimiento",
        compute='_compute_proxima_fecha_fin',
        store=True
    )
    
    @api.depends('medicamento_ids.fecha_fin')
    def _compute_proxima_fecha_fin(self):
        for record in self:
            active_meds = record.medicamento_ids.filtered(lambda m: m.active)
            if active_meds:
                record.proxima_fecha_fin = min(active_meds.mapped('fecha_fin'))
            else:
                record.proxima_fecha_fin = False

    def action_ver_medicamentos_activos(self):
        return {
            'name': ('Medicamentos Activos'),
            'type': 'ir.actions.act_window',
            'res_model': 'paciente.medicamento_asignado',
            'view_mode': 'tree,form',
            'domain': [('paciente_id', '=', self.id), ('active', '=', True)],
            'context': {'default_paciente_id': self.id}
        }
    
    medicamentos_activos_count = fields.Integer(
        compute='_compute_medicamentos_count',
        string="Tratamientos Activos"
    )
    
    medicamento_ids_count = fields.Integer(
        compute='_compute_medicamentos_count',
        string="Total Tratamientos"
    )

    def _compute_medicamentos_count(self):
        for record in self:
            record.medicamentos_activos_count = len(record.medicamentos_activos)
            record.medicamento_ids_count = len(record.medicamento_ids)






class PacienteMedicamentoAsignado(models.Model):
    _name = 'paciente.medicamento_asignado'
    _description = 'Medicamento Asignado a un Paciente'
    _order = 'fecha_fin desc'

    medicamento_id = fields.Many2one('med.hospital.list', string="Medicamento", required=True)
    cantidad_asignada = fields.Float(string="Cantidad Asignada", required=True)
    fecha_inicio = fields.Date(string="Fecha Inicio", required=True, default=fields.Date.today)
    fecha_fin = fields.Date(string="Fecha Fin", required=True, default=fields.Date.today)
    paciente_id = fields.Many2one('pacientes.hospital', string="Paciente", required=True, ondelete='cascade')
    active = fields.Boolean(string="Activo", default=True, index=True)

    def _auto_init(self):
        # Migración: Asignar fechas a registros existentes
        super()._auto_init()
        self.env.cr.execute("""
            UPDATE paciente_medicamento_asignado
            SET fecha_fin = CURRENT_DATE
            WHERE fecha_fin IS NULL
            """)

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for record in self:
            if record.fecha_fin < record.fecha_inicio:
                raise ValidationError("La fecha fin no puede ser anterior a la fecha de inicio")
    
    @api.constrains('cantidad_asignada')
    def _check_cantidad(self):
        for record in self:
            if record.cantidad_asignada <= 0:
                raise ValidationError("La cantidad asignada debe ser mayor que cero")
            if record.medicamento_id.cantidad < record.cantidad_asignada:
                raise ValidationError(f"No hay suficiente cantidad de {record.medicamento_id.name} en inventario")

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            medicamento = self.env['med.hospital.list'].browse(vals['medicamento_id'])
            if medicamento.cantidad < vals['cantidad_asignada']:
                raise ValidationError(f"Inventario insuficiente de {medicamento.name}")
            
            # Reducir inventario
            medicamento.cantidad -= vals['cantidad_asignada']
        
        return super().create(vals_list)

    def unlink(self):
        # Separar registros activos e inactivos
        active_records = self.filtered(lambda r: r.active)
        inactive_records = self - active_records
        
        # Desactivar registros activos en lugar de eliminarlos
        if active_records:
            active_records.write({'active': False})
            return True
            
        # Eliminar físicamente solo registros inactivos
        return super(PacienteMedicamentoAsignado, inactive_records).unlink()

    @api.model
    def _cron_limpiar_medicamentos_expirados(self):
        hoy = fields.Date.today()
        expirados = self.search([
            ('fecha_fin', '<', hoy),
            ('active', '=', True)
        ])
        
        if expirados:
            logger.info(f"Desactivando {len(expirados)} medicamentos expirados")
            expirados.write({'active': False})

    # Eliminar método action_delete obsoleto
