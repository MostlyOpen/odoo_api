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

import sqlite3


def hr_department_create(client, department_name):

    hr_department_model = client.model('hr.department')

    hr_department_browse = hr_department_model.browse([('name', '=', department_name), ])
    if hr_department_browse.id == []:

        values = {
            'name': department_name,
        }
        hr_department_model.create(values)


def employee_create_from_user(client, user_login, job_title, department_name):

    print('Configuring employee "' + user_login + '"...')

    employee_model = client.model('res.users')
    hr_employee_model = client.model('hr.employee')
    hr_job_model = client.model('hr.job')
    hr_department_model = client.model('hr.department')

    employee_browse = employee_model.browse([('login', '=', user_login), ])
    user_ids = employee_browse.id

    if user_ids == []:
        print('-->  User "' + user_login + '"does not exist!')
    else:

        user = employee_browse[0]

        hr_employee_browse = hr_employee_model.browse([('name', '=', user.name), ])
        employee_ids = hr_employee_browse.id

        if employee_ids != []:
            print('-->  Employee "' + user.name + '"already exists!')
        else:

            job_id = False
            hr_job_browse = hr_job_model.browse([('name', '=', job_title), ])
            if hr_job_browse.id != []:
                job_id = hr_job_browse[0].id

            department_id = False
            hr_department_browse = hr_department_model.browse([('name', '=', department_name), ])
            if hr_department_browse.id != []:
                department_id = hr_department_browse[0].id

            values = {
                'name': user.name,
                'address_id': user.partner_id.id,
                'work_email': user.partner_id.email,
                'job_id': job_id,
                'department_id': department_id,
                'user_id': user.id,
            }
            hr_employee_model.create(values)

    print()
    print('--> Done')
    print()


def hr_employee_export_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute(
        '''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY,
            resource_id,
            code,
            work_email,
            department_id,
            address_id,
            job_id,
            user_id,
            new_id INTEGER
            );
        '''
    )

    employee_model = client.model('hr.employee')
    employee_browse = employee_model.browse(args)

    employee_count = 0
    for employee_reg in employee_browse:
        employee_count += 1

        print(employee_count, employee_reg.id, employee_reg.name.encode("utf-8"))

        department_id = None
        if employee_reg.department_id:
            department_id = employee_reg.department_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                resource_id,
                code,
                work_email,
                department_id,
                address_id,
                job_id,
                user_id
                )
            VALUES(?,?,?,?,?,?,?,?)
            ''', (employee_reg.id,
                  employee_reg.resource_id.id,
                  employee_reg.code,
                  employee_reg.work_email,
                  department_id,
                  employee_reg.address_id.id,
                  employee_reg.job_id.id,
                  employee_reg.user_id.id,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> employee_count: ', employee_count)
    print()
