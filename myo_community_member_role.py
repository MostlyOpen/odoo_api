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


def community_member_role_export_sqlite(client, args, db_path, table_name):

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

    myo_community_member_role = client.model('myo.community.member.role')
    community_member_role_browse = myo_community_member_role.browse(args)

    community_member_role_count = 0
    for community_member_role in community_member_role_browse:
        community_member_role_count += 1

        print(
            community_member_role_count, community_member_role.id, community_member_role.code,
            community_member_role.name.encode("utf-8"), community_member_role.notes
        )

        code = None
        if community_member_role.code:
            code = community_member_role.code

        description = None
        if community_member_role.description:
            description = community_member_role.description

        notes = None
        if community_member_role.notes:
            notes = community_member_role.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           description,
                           notes
                           )
                       VALUES(?,?,?,?,?)''',
                       (community_member_role.id,
                        community_member_role.name,
                        code,
                        description,
                        notes,
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> community_member_role_count: ', community_member_role_count)


def community_member_role_import_sqlite(client, args, db_path, table_name):

    community_member_role_model = client.model('myo.community.member.role')

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

    community_member_role_count = 0
    for row in cursor:
        community_member_role_count += 1

        print(
            community_member_role_count, row['id'], row['name'], row['code'],
            row['description'], row['notes'],
        )

        values = {
            'name': row['name'],
            'code': row['code'],
            'description': row['description'],
            'notes': row['notes'],
        }
        community_member_role_id = community_member_role_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (community_member_role_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> community_member_role_count: ', community_member_role_count)
