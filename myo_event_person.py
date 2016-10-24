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


def event_person_export_sqlite(client, args, db_path, table_name):

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
            person_id,
            role_id,
            notes,
            active,
            new_id INTEGER
            );
        '''
    )

    event_person_model = client.model('myo.event.person')
    event_person_browse = event_person_model.browse(args)

    event_person_count = 0
    for event_person_reg in event_person_browse:
        event_person_count += 1

        print(
            event_person_count, event_person_reg.id,
            event_person_reg.event_id.name.encode("utf-8"),
            event_person_reg.person_id.name.encode("utf-8"),
            event_person_reg.role_id
        )

        role_id = None
        if event_person_reg.role_id:
            role_id = event_person_reg.role_id.id

        notes = None
        if event_person_reg.notes:
            notes = event_person_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                event_id,
                person_id,
                role_id,
                notes,
                active
                )
            VALUES(?,?,?,?,?,?)
            ''', (event_person_reg.id,
                  event_person_reg.event_id.id,
                  event_person_reg.person_id.id,
                  role_id,
                  notes,
                  event_person_reg.active,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> event_person_count: ', event_person_count)


def event_person_import_sqlite(
    client, args, db_path, table_name, tag_table_name, role_table_name, event_table_name, person_table_name
):

    event_model = client.model('myo.event.person')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    event_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            event_id,
            person_id,
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
        event_count += 1

        print(
            event_count, row['id'], row['event_id'], row['person_id'], row['role_id']
        )

        values = {
            # 'event_id': row['event_id'],
            # 'person_id': row['person_id'],
            # 'role_id': row['role_id'],
            'notes': row['notes'],
            'active': row['active'],
        }
        event_id = event_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (event_id,
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
            event_model.write(event_id, values)

            print('>>>>>', row['event_id'], event_id)

        if row['person_id']:

            person_id = row['person_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + person_table_name + '''
                WHERE id = ?;''',
                (person_id,
                 )
            )
            person_id = cursor2.fetchone()[0]

            values = {
                'person_id': person_id,
            }
            event_model.write(event_id, values)

            print('>>>>>', row['person_id'], person_id)

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
            event_model.write(event_id, values)

            print('>>>>>', row['role_id'], role_id)

    conn.commit()
    conn.close()

    print()
    print('--> event_count: ', event_count)
