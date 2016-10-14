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


def community_create_community(client, community_name, responsible_name, department_name):

    print('Creating community "' + community_name + '"...')

    community_model = client.model('myo.community')
    res_users_model = client.model('res.users')
    hr_department_model = client.model('hr.department')
    hr_employee_model = client.model('hr.employee')
    community_employee_model = client.model('myo.community.employee')

    res_users_browse = res_users_model.browse([('name', '=', responsible_name), ])
    user_id = res_users_browse.id[0]

    values = {
        'name': community_name,
        'user_id': user_id,
    }
    community_id = community_model.create(values).id

    hr_department_browse = hr_department_model.browse([('name', '=', department_name), ])
    department_id = hr_department_browse.id[0]

    hr_employee_browse = hr_employee_model.browse([('department_id', '=', department_id), ])
    for hr_employee in hr_employee_browse:
        print('>>>>>', hr_employee.name.encode("utf-8"))

        values = {
            'community_id': community_id,
            'employee_id': hr_employee.id,
            # 'role': role,
        }
        community_employee_model.create(values)

    print()
    print('--> Done')
    print()
