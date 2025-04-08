# -*- coding: utf-8 -*-
{
    'name': "Medicamentos",
    'version' : "1.0",
    'summary' : "Inventario de Medicamentos",
    'sequence' : -1,
    'description' : """Inventario de Medicamentos para Hospital General""",
    'category' : "Healthcare",
    'depends' : ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'views/med.xml',
    ],
    'demo' : [],
    'installable' : True,
    'application' : True,
    'assets' : {
        'web.assets_backend': [],
    }
}