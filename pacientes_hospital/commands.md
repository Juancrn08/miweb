python odoo-bin -r Juancrn01 -w 1234 --addons-path=addons -d odoo -i base
python odoo-bin -r Juancrn01 -w 1234 --addons-path=addons -d odoo -u med_hospital,pacientes_hospital



Vista orignal sin Qweb
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data>
        <!-- Vista Tree para Medicamentos Asignados -->
        <record id="paciente_medicamento_asignado_tree_view" model="ir.ui.view">
            <field name="name">paciente.medicamento.asignado.tree</field>
            <field name="model">paciente.medicamento_asignado</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="medicamento_id"/>
                    <field name="fecha_inicio"/>
                    <field name="fecha_fin"/>
                    <field name="cantidad_asignada"/>
                    <field name="active" invisible="1"/>
                </tree>
            </field>
        </record>

        <!-- Vista Tree para Pacientes -->
        <record id="pacientes_hospital_tree_form_view" model="ir.ui.view">
            <field name="name">pacientes.hospital.tree</field>
            <field name="model">pacientes.hospital</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="last_name"/>
                    <field name="age"/>
                    <field name="proxima_fecha_fin" widget="date"/>
                    <field name="pathology"/>
                </tree>
            </field>
        </record>

        <!-- Vista Formulario para Pacientes -->
        <record id="pacientes_hospital_form_view" model="ir.ui.view">
            <field name="name">pacientes.hospital.form</field>
            <field name="model">pacientes.hospital</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <group>
                                <field name="name"/>
                                <field name="last_name"/>
                                <field name="age"/>
                                <field name="proxima_fecha_fin" widget="date"/>
                            </group>
                            <group>
                                <field name="pathology"/>
                                <field name="other_pathology"/>
                            </group>
                        </group>
                        
                        <notebook>
                            <page string="Tratamiento Activo">
                                <field name="medicamentos_activos" mode="tree,form">
                                    <tree editable="bottom">
                                        <field name="medicamento_id"/>
                                        <field name="fecha_inicio" widget="date"/>
                                        <field name="fecha_fin" widget="date"/>
                                        <field name="cantidad_asignada"/>
                                    </tree>
                                    <form>
                                        <group>
                                            <field name="medicamento_id"/>
                                            <field name="fecha_inicio" widget="date"/>
                                            <field name="fecha_fin" widget="date"/>
                                            <field name="cantidad_asignada"/>
                                        </group>
                                    </form>
                                </field>
                            </page>
                            <page string="Histórico de Tratamientos">
                                <field name="medicamento_ids" domain="[('active', '=', False)]">
                                    <tree>
                                        <field name="medicamento_id"/>
                                        <field name="fecha_inicio" widget="date"/>
                                        <field name="fecha_fin" widget="date"/>
                                        <field name="cantidad_asignada"/>
                                    </tree>
                                </field>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- Acción y Menú Principal -->
        <record id="action_pacientes_hospital" model="ir.actions.act_window">
            <field name="name">Pacientes</field>
            <field name="res_model">pacientes.hospital</field>
            <field name="view_mode">tree,form</field>
            <field name="context">{'search_default_active': 1}</field>
        </record>
        
        <menuitem name="Pacientes" 
                  id="menu_pacientes_hospital" 
                  sequence="10" 
                  action="action_pacientes_hospital"/>
    </data>
</odoo>

    Vista Qweb #1
    <?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data>
        <!-- Vista Tree de Pacientes con QWeb -->
        <record id="pacientes_hospital_tree_view" model="ir.ui.view">
            <field name="name">pacientes.hospital.tree</field>
            <field name="model">pacientes.hospital</field>
            <field name="arch" type="xml">
                <tree decoration-danger="proxima_fecha_fin &lt; current_date" 
                      decoration-success="not medicamentos_activos">
                    <field name="name"/>
                    <field name="last_name"/>
                    <field name="medicamentos_activos"/>
                    <field name="age" widget="progressbar" options="{'current_value': age, 'max_value': 100}"/>
                    <field name="proxima_fecha_fin" widget="date"/>
                    <field name="pathology"/>
                    <field name="state" widget="badge"/>
                </tree>
            </field>
        </record>

        <!-- Vista Formulario con QWeb -->
        <record id="pacientes_hospital_form_view" model="ir.ui.view">
            <field name="name">pacientes.hospital.form</field>
            <field name="model">pacientes.hospital</field>
            <field name="arch" type="xml">
                <form>
                    <header>
                        <field name="state" widget="statusbar" 
                        statusbar_visible="draft,saved" 
                        options="{'clickable': '1'}"/>
                    </header>
                    <sheet>
                        <group class="row">
                            <group class="col-6">
                                <label string="Datos Básicos" for="basic_info" class="oe_edit_only"/>
                                    <div class="o_group">
                                        <field name="age" widget="numeric_step" 
                                        options="{'step': 1, 'min': 0, 'max': 120}"/>
                                        <field name="weight" widget="float_time"/>
                                    </div>
                            </group>
                            <group class="col-6">
                                <label string="Información Médica" for="medical_info" class="oe_edit_only"/>
                                    <div class="o_group">
                                        <field name="pathology" widget="many2one_tags"/>
                                        <field name="other_pathology" widget="text" 
                                        placeholder="Otras condiciones relevantes..."/>
                                    </div>
                            </group>
                        </group>

                        <notebook>
                            <page string="Tratamiento Activo">
                                <div class="alert alert-info" role="alert" 
                                     attrs="{'invisible': [('proxima_fecha_fin', '&gt;', context_today().strftime('%Y-%m-%d'))]}">
                                    ¡El tratamiento está próximo a vencer!
                                </div>
                                
                                <field name="medicamentos_activos" mode="tree,kanban">
                                    <kanban class="o_kanban_mobile">
                                        <templates>
                                            <t t-name="kanban-box">
                                                <div class="oe_kanban_global_click">
                                                    <div class="o_kanban_card_header">
                                                        <field name="medicamento_id"/>
                                                    </div>
                                                    <div class="o_kanban_card_content">
                                                        <div>Desde: <field name="fecha_inicio"/></div>
                                                        <div>Hasta: <field name="fecha_fin"/></div>
                                                        <div>Dosis: <field name="cantidad_asignada"/></div>
                                                    </div>
                                                </div>
                                            </t>
                                        </templates>
                                    </kanban>
                                    
                                    <tree editable="bottom">
                                        <field name="medicamento_id" widget="many2one_avatar"/>
                                        <field name="fecha_inicio" widget="date"/>
                                        <field name="fecha_fin" widget="date" 
                                               options="{'datepicker': {'minDate': '2000-01-01', 'maxDate': '2100-01-01'}}"/>
                                        <field name="cantidad_asignada" widget="float_time"/>
                                    </tree>
                                </field>
                            </page>
                            
                            <page string="Histórico">
                                <field name="medicamento_ids" domain="[('active', '=', False)]">
                                    <tree>
                                        <field name="medicamento_id"/>
                                        <field name="fecha_inicio" widget="date"/>
                                        <field name="fecha_fin" widget="date"/>
                                        <field name="cantidad_asignada"/>
                                        <field name="active" invisible="1"/>
                                    </tree>
                                </field>
                            </page>
                            
                            <page string="Reportes">
                                <div class="o_container">
                                    <div class="row mt16">
                                        <div class="col-6">
                                            <div class="card">
                                                <div class="card-header">Resumen de Tratamientos</div>
                                                <div class="card-body">
                                                    <t t-call="web.html_container">
                                                        <div id="treatment_chart"/>
                                                        <script>
                                                            function initChart() {
                                                                var data = {
                                                                    labels: ['Activos', 'Históricos'],
                                                                    datasets: [{
                                                                        data: [record.medicamentos_activos_count, record.medicamento_ids_count - record.medicamentos_activos_count],
                                                                        backgroundColor: ['#4CAF50', '#9E9E9E']
                                                                    }]
                                                                };
                                                                new Chart(document.getElementById('treatment_chart'), {
                                                                    type: 'doughnut',
                                                                    data: data
                                                                });
                                                            }
                                                            initChart();
                                                        </script>
                                                    </t>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </page>
                        </notebook>
                    </sheet>
                  
                    <div class="oe_chatter">
                        <field name="message_follower_ids" widget="mail_followers"/>
                        <field name="activity_ids" widget="mail_activity"/>
                        <field name="message_ids" widget="mail_thread"/>
                    </div>
            </form>      
            </field>
        </record>
    </data>
</odoo>