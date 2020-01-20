# -*- coding: utf-8 -*-
{
    'name': "Accommodation Labor Camps Management  ",

    'summary': """
        Employee accommodation/Camp Managment """,

    'description': """
        add accommodation /Camp Module to system 
        allow camp boss to assign room for each employee
        build camp room structure 
        link with Hr module 
        transfer employee from one camp to another 
    """,

    'author': "ODOO Intelligent Technology Dubai",
    'website': "http://odoo.ae",
	'email': "essam@odoo.ae",
    'license': "AGPL-3",
    'price': 185.99,
    'currency': 'EUR',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'views/views.xml','security/ir.model.access.csv',
    ],
	'images': ['static/description/Banner.png'],
}