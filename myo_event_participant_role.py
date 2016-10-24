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


def event_participant_role_export_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute('''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY,
            name,
            code,
            description,
            notes,
            new_id INTEGER
            );
    ''')

    myo_event_participant_role = client.model('myo.event.participant.role')
    event_participant_role_browse = myo_event_participant_role.browse(args)

    event_participant_role_count = 0
    for event_participant_role in event_participant_role_browse:
        event_participant_role_count += 1

        print(
            event_participant_role_count, event_participant_role.id, event_participant_role.code,
            event_participant_role.name.encode("utf-8"), event_participant_role.notes
        )

        code = None
        if event_participant_role.code:
            code = event_participant_role.code

        description = None
        if event_participant_role.description:
            description = event_participant_role.description

        notes = None
        if event_participant_role.notes:
            notes = event_participant_role.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           description,
                           notes
                           )
                       VALUES(?,?,?,?,?)''',
                       (event_participant_role.id,
                        event_participant_role.name,
                        code,
                        description,
                        notes,
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> event_participant_role_count: ', event_participant_role_count)


def event_participant_role_import_sqlite(client, args, db_path, table_name):

    event_participant_role_model = client.model('myo.event.participant.role')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            description,
            notes,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    event_participant_role_count = 0
    for row in cursor:
        event_participant_role_count += 1

        print(
            event_participant_role_count, row['id'], row['name'], row['code'],
            row['description'], row['notes'],
        )

        values = {
            'name': row['name'],
            'code': row['code'],
            'description': row['description'],
            'notes': row['notes'],
        }
        event_participant_role_id = event_participant_role_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (event_participant_role_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> event_participant_role_count: ', event_participant_role_count)
