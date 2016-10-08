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


def address_category_export_sqlite(client, args, db_path, table_name):

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
            parent_id,
            name,
            code,
            description,
            notes,
            color,
            new_id INTEGER
            );
    ''')

    myo_address_category = client.model('myo.address.category')
    address_category_browse = myo_address_category.browse(args)

    address_category_count = 0
    for address_category in address_category_browse:
        address_category_count += 1

        print(
            address_category_count, address_category.id, address_category.code,
            address_category.name.encode("utf-8"), address_category.notes
        )

        parent_id = None
        if address_category.parent_id:
            parent_id = address_category.parent_id.id

        notes = None
        if address_category.notes:
            notes = address_category.notes

        color = None
        if address_category.color:
            color = address_category.color

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           parent_id,
                           name,
                           code,
                           description,
                           notes,
                           color
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (address_category.id,
                        parent_id,
                        address_category.name,
                        address_category.code,
                        address_category.description,
                        notes,
                        color
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> address_category_count: ', address_category_count)


def address_category_import_sqlite(client, args, db_path, table_name):

    address_category_model = client.model('myo.address.category')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            parent_id,
            name,
            code,
            description,
            notes,
            color,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    address_category_count = 0
    for row in cursor:
        address_category_count += 1

        print(
            address_category_count, row['id'], row['parent_id'], row['name'], row['code'],
            row['description'], row['notes'], row['color']
        )

        values = {
            'name': row['name'],
            'code': row['code'],
            'description': row['description'],
            'notes': row['notes'],
            'color': row['color'],
        }
        address_category_id = address_category_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (address_category_id,
             row['id']
             )
        )

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            parent_id,
            name,
            code,
            description,
            notes,
            color,
            new_id
        FROM ''' + table_name + '''
        WHERE parent_id IS NOT NULL;
    ''')

    address_category_count_2 = 0
    for row in cursor:
        address_category_count_2 += 1

        print(address_category_count_2, row['id'], row['parent_id'], row['name'], row['code'], row['new_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['parent_id'],
             )
        )
        new_parent_id = cursor2.fetchone()[0]

        print('>>>>>', row['id'], row['new_id'], row['parent_id'], new_parent_id)

        values = {
            'parent_id': new_parent_id,
        }
        address_category_model.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> address_category_count: ', address_category_count)
    print('--> address_category_count_2: ', address_category_count_2)
