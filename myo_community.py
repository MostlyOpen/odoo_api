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


def community_create_community(client, community_name, responsible_name, department_name):

    print('Creating community "' + community_name + '"...')

    community_model = client.model('myo.community')
    res_users_model = client.model('res.users')
    hr_department_model = client.model('hr.department')
    hr_employee_model = client.model('hr.employee')
    community_employee_model = client.model('myo.community.employee')

    res_users_browse = res_users_model.browse([('name', '=', responsible_name), ])
    user_id = res_users_browse.id[0]

    values = {
        'name': community_name,
        'user_id': user_id,
    }
    community_id = community_model.create(values).id

    hr_department_browse = hr_department_model.browse([('name', '=', department_name), ])
    department_id = False
    if hr_department_browse.id != []:

        department_id = hr_department_browse.id[0]

        hr_employee_browse = hr_employee_model.browse([('department_id', '=', department_id), ])
        for hr_employee in hr_employee_browse:
            print('>>>>>', hr_employee.name.encode("utf-8"))

            values = {
                'community_id': community_id,
                'employee_id': hr_employee.id,
                # 'role': role,
            }
            community_employee_model.create(values)

    print()
    print('--> Done')
    print()


def community_export_sqlite(client, args, db_path, table_name):

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
            comm_location,
            date_inclusion,
            user_id,
            notes,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    community_model = client.model('myo.community')
    community_browse = community_model.browse(args)

    community_count = 0
    for community_reg in community_browse:
        community_count += 1

        print(community_count, community_reg.id, community_reg.code, community_reg.name.encode("utf-8"))

        parent_id = None
        if community_reg.parent_id:
            parent_id = community_reg.parent_id.id

        alias = None
        if community_reg.alias:
            alias = community_reg.alias

        comm_location = None
        if community_reg.comm_location:
            comm_location = community_reg.comm_location

        user_id = None
        if community_reg.user_id:
            user_id = community_reg.user_id.id

        notes = None
        if community_reg.notes:
            notes = community_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                tag_ids,
                category_ids,
                parent_id,
                name,
                alias,
                code,
                comm_location,
                date_inclusion,
                user_id,
                notes,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (community_reg.id,
                  str(community_reg.tag_ids.id),
                  str(community_reg.category_ids.id),
                  parent_id,
                  community_reg.name,
                  alias,
                  community_reg.code,
                  comm_location,
                  community_reg.date_inclusion,
                  user_id,
                  notes,
                  community_reg.active,
                  community_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> community_count: ', community_count)


def community_import_sqlite(
    client, args, db_path, table_name, tag_table_name, category_table_name, res_users_table_name
):

    community_model = client.model('myo.community')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    community_count = 0

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
            comm_location,
            date_inclusion,
            user_id,
            notes,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        community_count += 1

        print(community_count, row['id'], row['name'], row['code'], row['tag_ids'], row['category_ids'])

        values = {
            # 'tag_ids': row['tag_ids'],
            # 'category_ids': row['category_ids'],
            # 'parent_id': row['parent_id'],
            'name': row['name'],
            'alias': row['alias'],
            'code': row['code'],
            'comm_location': row['comm_location'],
            'date_inclusion': row['date_inclusion'],
            # 'user_id': row['user_id'],
            'notes': row['notes'],
            'active': row['active'],
            'active_log': row['active_log'],
        }
        community_id = community_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (community_id,
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
                community_model.write(community_id, values)

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
                community_model.write(community_id, values)

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
            community_model.write(community_id, values)

            print('>>>>>', row['user_id'], user_id)

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
            comm_location,
            date_inclusion,
            user_id,
            notes,
            active,
            active_log,
            new_id
        FROM ''' + table_name + '''
        WHERE parent_id IS NOT NULL;
    ''')

    community_count_2 = 0
    for row in cursor:
        community_count_2 += 1

        print(community_count_2, row['id'], row['parent_id'], row['name'], row['code'], row['new_id'])

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
        community_model.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> community_count: ', community_count)
    print('--> community_count_2: ', community_count_2)
