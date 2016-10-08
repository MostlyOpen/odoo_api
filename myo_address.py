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
            tag_ids,
            category_ids,
            parent_id,
            name,
            alias,
            code,
            zip,
            country_id,
            state_id,
            city,
            l10n_br_city_id,
            street,
            number,
            street2,
            district,
            phone,
            mobile,
            fax,
            email,
            state,
            notes,
            is_residence,
            active,
            active_log,
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

        parent_id = None
        if address_reg.parent_id:
            parent_id = address_reg.parent_id.id

        alias = None
        if address_reg.alias:
            alias = address_reg.alias

        city = None
        if address_reg.city:
            city = address_reg.city

        street = None
        if address_reg.street:
            street = address_reg.street

        number = None
        if address_reg.number:
            number = address_reg.number

        street2 = None
        if address_reg.street2:
            street2 = address_reg.street2

        district = None
        if address_reg.district:
            district = address_reg.district

        phone = None
        if address_reg.phone:
            phone = address_reg.phone

        mobile = None
        if address_reg.mobile:
            mobile = address_reg.mobile

        fax = None
        if address_reg.fax:
            fax = address_reg.fax

        email = None
        if address_reg.email:
            email = address_reg.email

        notes = None
        if address_reg.notes:
            notes = address_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                tag_ids,
                category_ids,
                parent_id,
                name,
                alias,
                code,
                zip,
                country_id,
                state_id,
                city,
                l10n_br_city_id,
                street,
                number,
                street2,
                district,
                phone,
                mobile,
                fax,
                email,
                state,
                notes,
                is_residence,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (address_reg.id,
                  str(address_reg.tag_ids.id),
                  str(address_reg.category_ids.id),
                  parent_id,
                  address_reg.name,
                  alias,
                  address_reg.code,
                  address_reg.zip,
                  address_reg.country_id.id,
                  address_reg.state_id.id,
                  city,
                  address_reg.l10n_br_city_id.id,
                  street,
                  number,
                  street2,
                  district,
                  phone,
                  mobile,
                  fax,
                  email,
                  address_reg.state,
                  notes,
                  address_reg.is_residence,
                  address_reg.active,
                  address_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> address_count: ', address_count)


def address_import_sqlite(client, args, db_path, table_name, tag_table_name, category_table_name):

    address_model = client.model('myo.address')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    address_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            tag_ids,
            category_ids,
            parent_id,
            name,
            alias,
            code,
            zip,
            country_id,
            state_id,
            city,
            l10n_br_city_id,
            street,
            number,
            street2,
            district,
            phone,
            mobile,
            fax,
            email,
            state,
            notes,
            is_residence,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        address_count += 1

        print(address_count, row['id'], row['name'], row['code'], row['tag_ids'], row['category_ids'])

        values = {
            # 'tag_ids': row['tag_ids'],
            # 'category_ids': row['category_ids'],
            # 'parent_id': row['parent_id'],
            'name': row['name'],
            'alias': row['alias'],
            'code': row['code'],
            'zip': row['zip'],
            'country_id': row['country_id'],
            'state_id': row['state_id'],
            'city': row['city'],
            'l10n_br_city_id': row['l10n_br_city_id'],
            'street': row['street'],
            'number': row['number'],
            'street2': row['street2'],
            'district': row['district'],
            'phone': row['phone'],
            'mobile': row['mobile'],
            'fax': row['fax'],
            'email': row['email'],
            'state': row['state'],
            'notes': row['state'],
            'is_residence': row['is_residence'],
            'active': row['active'],
            'active_log': row['active_log'],
        }
        address_id = address_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (address_id,
             row['id']
             )
        )

        if row['tag_ids'] != '[]':

            tag_ids = row['tag_ids'].split(',')
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

        if row['category_ids'] != '[]':

            category_ids = row['category_ids'].split(',')
            new_category_ids = []
            for x in range(0, len(category_ids)):
                category_id = int(re.sub('[^0-9]', '', category_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + category_table_name + '''
                    WHERE id = ?;''',
                    (category_id,
                     )
                )
                new_category_id = cursor2.fetchone()[0]

                values = {
                    'category_ids': [(4, new_category_id)],
                }
                address_model.write(address_id, values)

                new_category_ids.append(new_category_id)

            print('>>>>>', row[4], new_category_ids)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            tag_ids,
            category_ids,
            parent_id,
            name,
            alias,
            code,
            zip,
            country_id,
            state_id,
            city,
            l10n_br_city_id,
            street,
            number,
            street2,
            district,
            phone,
            mobile,
            fax,
            email,
            state,
            notes,
            is_residence,
            active,
            active_log,
            new_id
        FROM ''' + table_name + '''
        WHERE parent_id IS NOT NULL;
    ''')

    address_count_2 = 0
    for row in cursor:
        address_count_2 += 1

        print(address_count_2, row['id'], row['parent_id'], row['name'], row['code'], row['new_id'])

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
        address_model.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> address_count: ', address_count)
    print('--> address_count_2: ', address_count_2)
