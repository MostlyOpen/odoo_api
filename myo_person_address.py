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


def person_address_export_sqlite(client, args, db_path, table_name):

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
            person_id,
            address_id,
            role_id,
            sign_in_date,
            sign_out_date,
            notes,
            tag_ids,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    person_address_model = client.model('myo.person.address')
    person_address_browse = person_address_model.browse(args)

    person_address_count = 0
    for person_address_reg in person_address_browse:
        person_address_count += 1

        print(
            person_address_count, person_address_reg.id,
            person_address_reg.person_id.name.encode("utf-8"),
            person_address_reg.address_id.name.encode("utf-8")
        )

        role_id = None
        if person_address_reg.role_id:
            role_id = person_address_reg.role_id.id

        sign_out_date = None
        if person_address_reg.sign_out_date:
            sign_out_date = person_address_reg.sign_out_date

        notes = None
        if person_address_reg.notes:
            notes = person_address_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                person_id,
                address_id,
                role_id,
                sign_in_date,
                sign_out_date,
                notes,
                tag_ids,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            ''', (person_address_reg.id,
                  person_address_reg.person_id.id,
                  person_address_reg.address_id.id,
                  role_id,
                  person_address_reg.sign_in_date,
                  sign_out_date,
                  notes,
                  str(person_address_reg.tag_ids.id),
                  person_address_reg.active,
                  person_address_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_address_count: ', person_address_count)
