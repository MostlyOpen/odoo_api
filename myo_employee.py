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


def hr_department_export_sqlite(client, args, db_path, table_name):

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
            name,
            new_id INTEGER
            );
        '''
    )

    department_model = client.model('hr.department')
    department_browse = department_model.browse(args)

    department_count = 0
    for department_reg in department_browse:
        department_count += 1

        print(department_count, department_reg.id, department_reg.name.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name
                )
            VALUES(?,?)
            ''', (department_reg.id,
                  department_reg.name,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> department_count: ', department_count)
    print()


def hr_department_import_sqlite(client, args, db_path, table_name):

    hr_department_model = client.model('hr.department')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    hr_department_count = 0
    for row in cursor:
        hr_department_count += 1

        print(
            hr_department_count, row['id'], row['name'],
        )

        hr_department_browse = hr_department_model.browse([('name', '=', row['name']), ])
        if hr_department_browse.id == []:

            values = {
                'name': row['name'],
            }
            hr_department_id = hr_department_model.create(values).id

            cursor2.execute(
                '''
                UPDATE ''' + table_name + '''
                SET new_id = ?
                WHERE id = ?;''',
                (hr_department_id,
                 row['id']
                 )
            )

    conn.commit()
    conn.close()

    print()
    print('--> hr_department_count: ', hr_department_count)


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
            name,
            code,
            work_email,
            department_id,
            address_id,
            job_id,
            user_id,
            image,
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

        job_id = None
        if employee_reg.job_id:
            job_id = employee_reg.job_id.id

        image = None
        if employee_reg.image:
            image = employee_reg.image

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                resource_id,
                name,
                code,
                work_email,
                department_id,
                address_id,
                job_id,
                user_id,
                image
                )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            ''', (employee_reg.id,
                  employee_reg.resource_id.id,
                  employee_reg.name,
                  employee_reg.code,
                  employee_reg.work_email,
                  department_id,
                  employee_reg.address_id.id,
                  job_id,
                  employee_reg.user_id.id,
                  image,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> employee_count: ', employee_count)
    print()


def hr_employee_import_sqlite(
    client, args, db_path, table_name, hr_department_table_name, res_partner_table_name, res_users_table_name
):

    hr_employee_model = client.model('hr.employee')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            resource_id,
            name,
            code,
            work_email,
            department_id,
            address_id,
            job_id,
            user_id,
            image,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    hr_employee_count = 0
    for row in cursor:
        hr_employee_count += 1

        print(
            hr_employee_count, row['id'], row['name'], row['code'],
        )

        hr_employee_browse = hr_employee_model.browse([('name', '=', row['name']), ])
        if hr_employee_browse.id == []:

            department_id = row['department_id']
            new_department_id = False
            if department_id is not None:
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + hr_department_table_name + '''
                    WHERE id = ?;''',
                    (department_id,
                     )
                )
                new_department_id = cursor2.fetchone()[0]

            address_id = row['address_id']
            new_address_id = False
            if department_id is not None:
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + res_partner_table_name + '''
                    WHERE id = ?;''',
                    (address_id,
                     )
                )
                new_address_id = cursor2.fetchone()[0]

            user_id = row['user_id']
            new_user_id = False
            if department_id is not None:
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + res_users_table_name + '''
                    WHERE id = ?;''',
                    (user_id,
                     )
                )
                new_user_id = cursor2.fetchone()[0]

            values = {
                'name': row['name'],
                'code': row['code'],
                'address_id': new_address_id,
                'work_email': row['work_email'],
                'job_id': row['job_id'],
                'department_id': new_department_id,
                'user_id': new_user_id,
                'image': row['image'],
            }
            hr_employee_id = hr_employee_model.create(values).id

            cursor2.execute(
                '''
                UPDATE ''' + table_name + '''
                SET new_id = ?
                WHERE id = ?;''',
                (hr_employee_id,
                 row['id']
                 )
            )

    conn.commit()
    conn.close()

    print()
    print('--> hr_employee_count: ', hr_employee_count)
