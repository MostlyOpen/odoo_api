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


def person_export_sqlite(client, args, db_path, table_name):

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
            name,
            alias,
            code,
            gender,
            marital,
            birthday,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    person_model = client.model('myo.person')
    person_browse = person_model.browse(args)

    person_count = 0
    for person_reg in person_browse:
        person_count += 1

        print(person_count, person_reg.id, person_reg.code, person_reg.name.encode("utf-8"))

        alias = None
        if person_reg.alias:
            alias = person_reg.alias

        marital = None
        if person_reg.marital:
            marital = person_reg.marital

        spouse_id = None
        if person_reg.spouse_id:
            spouse_id = person_reg.spouse_id.id

        father_id = None
        if person_reg.father_id:
            father_id = person_reg.father_id.id

        mother_id = None
        if person_reg.mother_id:
            mother_id = person_reg.mother_id.id

        responsible_id = None
        if person_reg.responsible_id:
            responsible_id = person_reg.responsible_id.id

        identification_id = None
        if person_reg.identification_id:
            identification_id = person_reg.identification_id

        otherid = None
        if person_reg.otherid:
            otherid = person_reg.otherid

        rg = None
        if person_reg.rg:
            rg = person_reg.rg

        cpf = None
        if person_reg.cpf:
            cpf = person_reg.cpf

        country_id = None
        if person_reg.country_id:
            country_id = person_reg.country_id.id

        notes = None
        if person_reg.notes:
            notes = person_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                tag_ids,
                category_ids,
                name,
                alias,
                code,
                gender,
                marital,
                birthday,
                spouse_id,
                father_id,
                mother_id,
                responsible_id,
                identification_id,
                otherid,
                rg,
                cpf,
                country_id,
                date_inclusion,
                state,
                notes,
                address_id,
                is_patient,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (person_reg.id,
                  str(person_reg.tag_ids.id),
                  str(person_reg.category_ids.id),
                  person_reg.name,
                  alias,
                  person_reg.code,
                  person_reg.gender,
                  marital,
                  person_reg.birthday,
                  spouse_id,
                  father_id,
                  mother_id,
                  responsible_id,
                  identification_id,
                  otherid,
                  rg,
                  cpf,
                  country_id,
                  person_reg.date_inclusion,
                  person_reg.state,
                  notes,
                  person_reg.address_id.id,
                  person_reg.is_patient,
                  person_reg.active,
                  person_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)


def person_import_sqlite(client, args, db_path, table_name, tag_table_name, category_table_name, address_table_name):

    person_model = client.model('myo.person')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    person_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            tag_ids,
            category_ids,
            name,
            alias,
            code,
            gender,
            marital,
            birthday,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        person_count += 1

        print(person_count, row['id'], row['name'], row['code'], row['tag_ids'], row['category_ids'])

        values = {
            # 'tag_ids': row['tag_ids'],
            # 'category_ids': row['category_ids'],
            'name': row['name'],
            'alias': row['alias'],
            'code': row['code'],
            'gender': row['gender'],
            'marital': row['marital'],
            'birthday': row['birthday'],
            'spouse_id': row['spouse_id'],
            'father_id': row['father_id'],
            'mother_id': row['mother_id'],
            'responsible_id': row['responsible_id'],
            'identification_id': row['identification_id'],
            'otherid': row['otherid'],
            'rg': row['rg'],
            'cpf': row['cpf'],
            'country_id': row['country_id'],
            'date_inclusion': row['date_inclusion'],
            'state': row['state'],
            'notes': row['notes'],
            # 'address_id': row['address_id'],
            'is_patient': row['is_patient'],
            'active': row['active'],
            'active_log': row['active_log'],
        }
        person_id = person_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (person_id,
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
                person_model.write(person_id, values)

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
                person_model.write(person_id, values)

                new_category_ids.append(new_category_id)

            print('>>>>>', row['category_ids'], new_category_ids)

        if row['address_id']:

            address_id = row['address_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + address_table_name + '''
                WHERE id = ?;''',
                (address_id,
                 )
            )
            address_id = cursor2.fetchone()[0]

            values = {
                'address_id': address_id,
            }
            person_model.write(person_id, values)

            print('>>>>>', row['address_id'], address_id)

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)
