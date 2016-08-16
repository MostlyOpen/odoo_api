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


def clv_tag_export_sqlite(client, args, db_path, table_name):

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
            notes TEXT,
            new_id INTEGER
            );
    ''')

    clv_tag = client.model('clv_tag')
    tag_browse = clv_tag.browse(args)

    tag_count = 0
    for tag in tag_browse:
        tag_count += 1

        print(tag_count, tag.id, tag.code, tag.name.encode("utf-8"), tag.notes)

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           notes
                           )
                       VALUES(?,?,?,?)''',
                       (tag.id,
                        tag.name,
                        tag.code,
                        tag.notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)


def myo_tag_export_sqlite(client, args, db_path, table_name):

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
            notes TEXT,
            new_id INTEGER
            );
    ''')

    myo_tag = client.model('myo.tag')
    tag_browse = myo_tag.browse(args)

    tag_count = 0
    for tag in tag_browse:
        tag_count += 1

        print(tag_count, tag.id, tag.code, tag.name.encode("utf-8"), tag.notes)

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           notes
                           )
                       VALUES(?,?,?,?)''',
                       (tag.id,
                        tag.name,
                        tag.code,
                        tag.notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)


def myo_tag_import_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            notes,
            new_id
        FROM ''' + table_name + ''';
    ''')

    myo_tag = client.model('myo.tag')

    print(data)
    print([field[0] for field in cursor.description])
    tag_count = 0
    for row in cursor:
        tag_count += 1

        print(tag_count, row[0], row[1], row[2], row[3], row[4])

        values = {
            'name': row[1],
            'code': row[2],
            'notes': row[3],
        }
        tag_id = myo_tag.create(values).id

        cursor2.execute('''
                       UPDATE ''' + table_name + '''
                       SET new_id = ?
                       WHERE id = ?;''',
                        (tag_id,
                         row[0]
                         )
                        )

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)
