# -*- coding: utf-8 -*-
{
    'name': "Pacientes Modulo",
    'version' : "1.0",
    'summary' : "Pacientes",
    'sequence' : -1,
    'description' : """Modulo de Pacientes""",
    'category' : "OWL 3",
    'depends' : ['base',
                 'mail',
                 'web',],
    'data' : [
        "security/ir.model.access.csv",
        "views/pacientes_view.xml",
    ],
    'demo' : [],
    'installable' : True,
    'application' : True,
    'assets' : {
        'web.assets_backend': [
        ],
    }
}