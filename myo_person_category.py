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


def person_category_export_sqlite(client, args, db_path, table_name):

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

    myo_person_category = client.model('myo.person.category')
    person_category_browse = myo_person_category.browse(args)

    person_category_count = 0
    for person_category in person_category_browse:
        person_category_count += 1

        print(
            person_category_count, person_category.id, person_category.code,
            person_category.name.encode("utf-8"), person_category.notes
        )

        parent_id = None
        if person_category.parent_id:
            parent_id = person_category.parent_id.id

        notes = None
        if person_category.notes:
            notes = person_category.notes

        color = None
        if person_category.color:
            color = person_category.color

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
                       (person_category.id,
                        parent_id,
                        person_category.name,
                        person_category.code,
                        person_category.description,
                        notes,
                        color
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> person_category_count: ', person_category_count)
