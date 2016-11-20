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


def community_employee_export_sqlite(client, args, db_path, table_name):

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
            community_id,
            employee_id,
            role_id,
            notes,
            active,
            new_id INTEGER
            );
        '''
    )

    community_employee_model = client.model('myo.community.employee')
    community_employee_browse = community_employee_model.browse(args)

    community_employee_count = 0
    for community_employee_reg in community_employee_browse:
        community_employee_count += 1

        print(
            community_employee_count, community_employee_reg.id,
            community_employee_reg.community_id.name.encode("utf-8"),
            community_employee_reg.employee_id.name.encode("utf-8")
        )

        role_id = None
        if community_employee_reg.role_id:
            role_id = community_employee_reg.role_id.id

        notes = None
        if community_employee_reg.notes:
            notes = community_employee_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                community_id,
                employee_id,
                role_id,
                notes,
                active
                )
            VALUES(?,?,?,?,?,?)
            ''', (community_employee_reg.id,
                  community_employee_reg.community_id.id,
                  community_employee_reg.employee_id.id,
                  role_id,
                  notes,
                  community_employee_reg.active,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> community_employee_count: ', community_employee_count)


def community_employee_import_sqlite(
    client, args, db_path, table_name, tag_table_name, role_table_name, community_table_name, employee_table_name
):

    community_employee_model = client.model('myo.community.employee')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    community_employee_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            community_id,
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
        community_employee_count += 1

        print(
            community_employee_count, row['id'], row['community_id'], row['employee_id'], row['role_id']
        )

        values = {
            # 'community_id': row['community_id'],
            # 'employee_id': row['employee_id'],
            # 'role_id': row['role_id'],
            'notes': row['notes'],
            'active': row['active'],
        }
        community_employee_id = community_employee_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (community_employee_id,
             row['id']
             )
        )

        if row['community_id']:

            community_id = row['community_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + community_table_name + '''
                WHERE id = ?;''',
                (community_id,
                 )
            )
            community_id = cursor2.fetchone()[0]

            values = {
                'community_id': community_id,
            }
            community_employee_model.write(community_employee_id, values)

            print('>>>>>', row['community_id'], community_id)

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
            community_employee_model.write(community_employee_id, values)

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
            community_employee_model.write(community_employee_id, values)

            print('>>>>>', row['role_id'], role_id)

    conn.commit()
    conn.close()

    print()
    print('--> community_employee_count: ', community_employee_count)
