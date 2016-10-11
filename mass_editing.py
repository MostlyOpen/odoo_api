#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import print_function


def mass_editing_create(client, name, model, fields):

    mass_object_model = client.model('mass.object')

    ir_model = client.model('ir.model')
    ir_model_fields = client.model('ir.model.fields')
    
    object_model = ir_model.search([('model', '=', model)])
    fields_model = ir_model_fields.search([
        ('model_id', '=', object_model[0]),
        ('name', 'in', fields)
        ])

    values = {
        'name': name,
        'model_id': object_model[0],
        'field_ids': [(6, 0, fields_model)]
    }
    mass_object_new = mass_object_model.create(values)
    mass_object_new.create_action()

    print()
    print('-->', object_model)
    print('-->', fields_model)
    print('-->', mass_object_new.name)
    print()
