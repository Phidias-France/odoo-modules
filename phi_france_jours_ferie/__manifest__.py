# -*- coding: utf-8 -*-
{
    'name': "French holidays",

    'summary': """
        Generating France public holidays for a calendar.
        """,

    'description': """
        Public holidays are created by calling the webservice https://calendrier.api.gouv.fr/jours-feries
    """,

    'author': "Phidias",
    'website': "http://www.phidias.fr",
    'category': 'Extra Tools',
    'version': '13.0.0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
    'depends': [
        'resource',
    ],

    'data': [
        'wizard/generate_public_holiday.xml',
    ]
}
