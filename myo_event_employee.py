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


def event_employee_export_sqlite(client, args, db_path, table_name):

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
            event_id,
            employee_id,
            role_id,
            notes,
            active,
            new_id INTEGER
            );
        '''
    )

    event_employee_model = client.model('myo.event.employee')
    event_employee_browse = event_employee_model.browse(args)

    event_employee_count = 0
    for event_employee_reg in event_employee_browse:
        event_employee_count += 1

        print(
            event_employee_count, event_employee_reg.id,
            event_employee_reg.event_id.name.encode("utf-8"),
            event_employee_reg.employee_id.name.encode("utf-8")
        )

        role_id = None
        if event_employee_reg.role_id:
            role_id = event_employee_reg.role_id.id

        notes = None
        if event_employee_reg.notes:
            notes = event_employee_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                event_id,
                employee_id,
                role_id,
                notes,
                active
                )
            VALUES(?,?,?,?,?,?)
            ''', (event_employee_reg.id,
                  event_employee_reg.event_id.id,
                  event_employee_reg.employee_id.id,
                  role_id,
                  notes,
                  event_employee_reg.active,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> event_employee_count: ', event_employee_count)


def event_employee_import_sqlite(
    client, args, db_path, table_name, tag_table_name, role_table_name, event_table_name, employee_table_name
):

    event_employee_model = client.model('myo.event.employee')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    event_employee_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            event_id,
            employee_id,
            role_id,
            notes,
            active,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        event_employee_count += 1

        print(
            event_employee_count, row['id'], row['event_id'], row['employee_id'], row['role_id']
        )

        values = {
            # 'event_id': row['event_id'],
            # 'employee_id': row['employee_id'],
            # 'role_id': row['role_id'],
            'notes': row['notes'],
            'active': row['active'],
        }
        event_employee_id = event_employee_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (event_employee_id,
             row['id']
             )
        )

        if row['event_id']:

            event_id = row['event_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + event_table_name + '''
                WHERE id = ?;''',
                (event_id,
                 )
            )
            event_id = cursor2.fetchone()[0]

            values = {
                'event_id': event_id,
            }
            event_employee_model.write(event_employee_id, values)

            print('>>>>>', row['event_id'], event_id)

        if row['employee_id']:

            employee_id = row['employee_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + employee_table_name + '''
                WHERE id = ?;''',
                (employee_id,
                 )
            )
            employee_id = cursor2.fetchone()[0]

            values = {
                'employee_id': employee_id,
            }
            event_employee_model.write(event_employee_id, values)

            print('>>>>>', row['employee_id'], employee_id)

        if row['role_id']:

            role_id = row['role_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + role_table_name + '''
                WHERE id = ?;''',
                (role_id,
                 )
            )
            role_id = cursor2.fetchone()[0]

            values = {
                'role_id': role_id,
            }
            event_employee_model.write(event_employee_id, values)

            print('>>>>>', row['role_id'], role_id)

    conn.commit()
    conn.close()

    print()
    print('--> event_employee_count: ', event_employee_count)
