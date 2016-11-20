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


def event_export_sqlite(client, args, db_path, table_name):

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
            description,
            code,
            sequence,
            planned_hours,
            date_inclusion,
            date_foreseen,
            date_start,
            date_deadline,
            user_id,
            notes,
            color,
            active,
            state,
            active_log,
            address_id,
            new_id INTEGER
            );
        '''
    )

    event_model = client.model('myo.event')
    event_browse = event_model.browse(args)

    event_count = 0
    for event_reg in event_browse:
        event_count += 1

        print(event_count, event_reg.id, event_reg.code, event_reg.name.encode("utf-8"))

        description = None
        if event_reg.description:
            description = event_reg.description

        planned_hours = None
        if event_reg.planned_hours:
            planned_hours = event_reg.planned_hours

        date_foreseen = None
        if event_reg.date_foreseen:
            date_foreseen = event_reg.date_foreseen

        date_start = None
        if event_reg.date_start:
            date_start = event_reg.date_start

        date_deadline = None
        if event_reg.date_deadline:
            date_deadline = event_reg.date_deadline

        user_id = None
        if event_reg.user_id:
            user_id = event_reg.user_id.id

        notes = None
        if event_reg.notes:
            notes = event_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                tag_ids,
                category_ids,
                name,
                description,
                code,
                sequence,
                planned_hours,
                date_inclusion,
                date_foreseen,
                date_start,
                date_deadline,
                user_id,
                notes,
                color,
                state,
                active,
                active_log,
                address_id
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (event_reg.id,
                  str(event_reg.tag_ids.id),
                  str(event_reg.category_ids.id),
                  event_reg.name,
                  description,
                  event_reg.code,
                  event_reg.sequence,
                  planned_hours,
                  event_reg.date_inclusion,
                  date_foreseen,
                  date_start,
                  date_deadline,
                  user_id,
                  notes,
                  event_reg.color,
                  event_reg.state,
                  event_reg.active,
                  event_reg.active_log,
                  event_reg.address_id.id,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> event_count: ', event_count)


def event_import_sqlite(
    client, args, db_path, table_name, tag_table_name, category_table_name, res_users_table_name, address_table_name
):

    event_model = client.model('myo.event')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    event_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            tag_ids,
            category_ids,
            name,
            description,
            code,
            sequence,
            planned_hours,
            date_inclusion,
            date_foreseen,
            date_start,
            date_deadline,
            user_id,
            notes,
            color,
            active,
            state,
            active_log,
            address_id,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        event_count += 1

        print(event_count, row['id'], row['name'], row['code'], row['tag_ids'], row['category_ids'])

        values = {
            # 'tag_ids': row['tag_ids'],
            # 'category_ids': row['category_ids'],
            'name': row['name'],
            'description': row['description'],
            'code': row['code'],
            'sequence': row['sequence'],
            'planned_hours': row['planned_hours'],
            'date_inclusion': row['date_inclusion'],
            'date_foreseen': row['date_foreseen'],
            'date_start': row['date_start'],
            'date_deadline': row['date_deadline'],
            # 'user_id': row['user_id'],
            'notes': row['notes'],
            'color': row['color'],
            'active': row['active'],
            'state': row['state'],
            'active_log': row['active_log'],
            # 'address_id': row['address_id'],
        }
        event_id = event_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (event_id,
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
                event_model.write(event_id, values)

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
                event_model.write(event_id, values)

                new_category_ids.append(new_category_id)

            print('>>>>>', row[4], new_category_ids)

        if row['user_id']:

            user_id = row['user_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + res_users_table_name + '''
                WHERE id = ?;''',
                (user_id,
                 )
            )
            user_id = cursor2.fetchone()[0]

            values = {
                'user_id': user_id,
            }
            event_model.write(event_id, values)

            print('>>>>>', row['user_id'], user_id)

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
            event_model.write(event_id, values)

            print('>>>>>', row['address_id'], address_id)

    conn.commit()
    conn.close()

    print()
    print('--> event_count: ', event_count)
