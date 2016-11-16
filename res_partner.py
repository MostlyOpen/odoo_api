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


def res_partner_export_sqlite(client, args, db_path, table_name):

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
            customer,
            employee,
            is_company,
            email,
            website,
            parent_id,
            company_id,
            tz,
            lang,
            image,
            new_id INTEGER
            );
        '''
    )

    res_partner_model = client.model('res.partner')
    res_partner_browse = res_partner_model.browse(args)

    res_partner_count = 0
    for res_partner_reg in res_partner_browse:
        res_partner_count += 1

        print(res_partner_count, res_partner_reg.id, res_partner_reg.name.encode("utf-8"))

        company_id = None
        if res_partner_reg.company_id:
            company_id = res_partner_reg.company_id.id

        parent_id = None
        if res_partner_reg.parent_id:
            parent_id = res_partner_reg.parent_id.id

        website = None
        if res_partner_reg.website:
            website = res_partner_reg.website

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                customer,
                employee,
                is_company,
                email,
                website,
                parent_id,
                company_id,
                tz,
                lang,
                image
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (res_partner_reg.id,
                  res_partner_reg.name,
                  res_partner_reg.customer,
                  res_partner_reg.employee,
                  res_partner_reg.is_company,
                  res_partner_reg.email,
                  website,
                  parent_id,
                  company_id,
                  res_partner_reg.tz,
                  res_partner_reg.lang,
                  res_partner_reg.image,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> res_partner_count: ', res_partner_count)
    print()


def res_partner_import_sqlite(client, args, db_path, table_name):

    res_partner_model = client.model('res.partner')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            customer,
            employee,
            is_company,
            email,
            website,
            parent_id,
            company_id,
            tz,
            lang,
            image,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    res_partner_count = 0
    for row in cursor:
        res_partner_count += 1

        print(
            res_partner_count, row['id'], row['name'], row['email'],
        )

        res_partner_browse = res_partner_model.browse([('name', '=', row['name']), ])
        if res_partner_browse.id == []:

            values = {
                'name': row['name'],
                'customer': row['customer'],
                'employee': row['employee'],
                'is_company': row['is_company'],
                'email': row['email'],
                'website': row['website'],
                # 'parent_id': row['parent_id'],
                'company_id': row['company_id'],
                'tz': row['tz'],
                'lang': row['lang'],
                'image': row['image'],
            }
            res_partner_id = res_partner_model.create(values).id

            cursor2.execute(
                '''
                UPDATE ''' + table_name + '''
                SET new_id = ?
                WHERE id = ?;''',
                (res_partner_id,
                 row['id']
                 )
            )

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            name,
            customer,
            employee,
            is_company,
            email,
            website,
            parent_id,
            company_id,
            tz,
            lang,
            image,
            new_id
        FROM ''' + table_name + '''
        WHERE parent_id IS NOT NULL;
    ''')

    res_partner_count_2 = 0
    for row in cursor:
        res_partner_count_2 += 1

        print(res_partner_count_2, row['id'], row['parent_id'], row['name'], row['new_id'])

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
        res_partner_model.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> res_partner_count: ', res_partner_count)
    print('--> res_partner_count_2: ', res_partner_count_2)
