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


def employee_create_from_user(client, user_login, job_title):

    print('Configuring employee "' + user_login + '"...')

    res_users_model = client.model('res.users')
    hr_employee_model = client.model('hr.employee')
    hr_job_model = client.model('hr.job')

    res_users_browse = res_users_model.browse([('login', '=', user_login), ])
    user_ids = res_users_browse.id

    if user_ids == []:
        print('-->  User "' + user_login + '"does not exist!')
    else:

        user = res_users_browse[0]

        hr_employee_browse = hr_employee_model.browse([('name', '=', user.name), ])
        employee_ids = hr_employee_browse.id

        if employee_ids != []:
            print('-->  Employee "' + user.name + '"already exists!')
        else:

            job_id = False
            hr_job_browse = hr_job_model.browse([('name', '=', job_title), ])
            if hr_job_browse.id != []:
                job_id = hr_job_browse[0].id

            values = {
                'name': user.name,
                'address_id': user.partner_id.id,
                'work_email': user.partner_id.email,
                'job_id': job_id,
                'user_id': user.id,
            }
            hr_employee_model.create(values)

    print()
    print('--> Done')
    print()
