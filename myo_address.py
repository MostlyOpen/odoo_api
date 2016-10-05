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
import re


def address_export_sqlite(client, args, db_path, table_name):

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
            code,
            tag_ids,
            zip,
            country_id,
            state_id,
            l10n_br_city_id,
            street,
            number,
            street2,
            district,
            phone,
            mobile,
            state,
            notes,
            new_id INTEGER
            );
        '''
    )

    address_model = client.model('myo.address')
    address_browse = address_model.browse(args)

    address_count = 0
    for address_reg in address_browse:
        address_count += 1

        print(address_count, address_reg.id, address_reg.code, address_reg.name.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                code,
                tag_ids,
                zip,
                country_id,
                state_id,
                l10n_br_city_id,
                street,
                number,
                street2,
                district,
                phone,
                mobile,
                state,
                notes
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (address_reg.id,
                  address_reg.name,
                  address_reg.code,
                  str(address_reg.tag_ids.id),
                  address_reg.zip,
                  address_reg.country_id.id,
                  address_reg.state_id.id,
                  address_reg.l10n_br_city_id.id,
                  address_reg.street,
                  address_reg.number,
                  address_reg.street2,
                  address_reg.district,
                  address_reg.phone,
                  address_reg.mobile,
                  address_reg.state,
                  address_reg.notes,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> address_count: ', address_count)


def address_import_sqlite(client, args, db_path, table_name, tag_table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    address_count = 0

    try:
        data = cursor.execute(
            '''
            SELECT
                id,
                name,
                code,
                tag_ids,
                zip,
                country_id,
                state_id,
                l10n_br_city_id,
                street,
                number,
                street2,
                district,
                phone,
                mobile,
                state,
                notes,
                new_id
            FROM ''' + table_name + ''';
            '''
        )

        address_model = client.model('myo.address')

        print(data)
        print([field[0] for field in cursor.description])
        for row in cursor:
            address_count += 1

            print(address_count, row[0], row[1], row[2], row[3])

            values = {
                'name': row[1],
                'code': row[2],
                # 'tag_ids': row[3],
                'zip': row[4],
                'country_id': row[5],
                'state_id': row[6],
                'l10n_br_city_id': row[7],
                'street': row[8],
                'number': row[9],
                'street2': row[10],
                'district': row[11],
                'phone': row[12],
                'mobile': row[13],
                'state': row[14],
                'notes': row[15],
            }
            address_id = address_model.create(values).id

            cursor2.execute(
                '''
               UPDATE ''' + table_name + '''
               SET new_id = ?
               WHERE id = ?;''',
                (address_id,
                 row[0]
                 )
            )

            if row[3] != '[]':

                tag_ids = row[3].split(',')
                new_tag_ids = []
                for x in range(0, len(tag_ids)):
                    tag_id = int(re.sub('[^0-9]', '', tag_ids[x]))
                    cursor2.execute(
                        '''
                        SELECT new_id
                        FROM ''' + tag_table_name + '''
                        WHERE id = ?;''',
                        (tag_id,
                         )
                    )
                    new_tag_id = cursor2.fetchone()[0]

                    values = {
                        'tag_ids': [(4, new_tag_id)],
                    }
                    address_model.write(address_id, values)

                    new_tag_ids.append(new_tag_id)

                print('>>>>>', row[4], new_tag_ids)

    except Exception as e:
        print('>>>>>', e)

    conn.commit()
    conn.close()

    print()
    print('--> address_count: ', address_count)
