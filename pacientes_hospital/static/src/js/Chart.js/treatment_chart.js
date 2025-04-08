odoo.define('pacientes_hospital.treatment_chart', function (require) {
    "use strict";
    const AbstractField = require('web.AbstractField');
    const registry = require('web.field_registry');

    const TreatmentChartWidget = AbstractField.extend({
        _render: function () {
            const data = {
                labels: ['Activos', 'Históricos'],
                datasets: [{
                    data: [
                        this.recordData.medicamentos_activos_count,
                        this.recordData.medicamento_ids_count - this.recordData.medicamentos_activos_count
                    ],
                    backgroundColor: ['#4CAF50', '#9E9E9E']
                }]
            };
            new Chart(this.el, {
                type: 'doughnut',
                data: data
            });
        }
    });

    registry.add('treatment_chart', TreatmentChartWidget);
});