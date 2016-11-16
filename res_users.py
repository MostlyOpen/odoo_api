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
import psycopg2
import re


def res_users_create_user(client, company_name, lang, tz, user_name, user_email, user_pw, user_image):

    print('Configuring user "' + user_email + '"...')

    res_partner_model = client.model('res.partner')
    res_company_model = client.model('res.company')
    res_users_model = client.model('res.users')
    res_groups_model = client.model('res.groups')

    res_users_browse = res_users_model.browse([('login', '=', user_email), ])
    user_ids = res_users_browse.id
    if user_ids != []:
        print('-->  User "' + user_email + '"already exists!')
    else:

        args = [('name', '=', company_name), ]

        res_users_browse = res_users_model.browse(args)
        parent_id = res_users_browse[0].id

        res_company_browse = res_company_model.browse(args)
        company_id = res_company_browse[0].id

        args = [('name', '=', 'Employee'), ]

        res_group_browse = res_groups_model.browse(args)
        group_id = res_group_browse[0].id

        values = {
            'name': user_name,
            'customer': False,
            'employee': False,
            'is_company': False,
            'email': user_email,
            'website': '',
            'parent_id': parent_id,
            'company_id': company_id,
            'tz': tz,
            'lang': lang
        }
        partner_id = res_partner_model.create(values).id

        values = {
            'name': user_name,
            'partner_id': partner_id,
            'company_id': company_id,
            'login': user_email,
            'password': user_pw,
            'image': user_image,
            'groups_id': [(6, 0, [])],
        }
        user_id = res_users_model.create(values).id

        values = {
            'groups_id': [(6, 0, [group_id])],
        }
        res_users_model.write(user_id, values)

    print()
    print('--> Done')
    print()


def res_users_export_sqlite(client, args, db_path, table_name, conn_string):

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
            partner_id,
            company_id,
            login,
            password_crypt,
            image,
            groups_id,
            new_id INTEGER
            );
        '''
    )

    pg_conn = psycopg2.connect(conn_string)
    pg_cursor = pg_conn.cursor()

    res_users_model = client.model('res.users')
    res_users_browse = res_users_model.browse(args)

    res_users_count = 0
    for res_users_reg in res_users_browse:
        res_users_count += 1

        print(res_users_count, res_users_reg.id, res_users_reg.name.encode("utf-8"))

        pg_cursor.execute("""
            SELECT login, password_crypt
            FROM res_users
            WHERE login = '""" + res_users_reg.login + """'
            """)

        row = pg_cursor.fetchone()

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                partner_id,
                company_id,
                login,
                password_crypt,
                image,
                groups_id
                )
            VALUES(?,?,?,?,?,?,?,?)
            ''', (res_users_reg.id,
                  res_users_reg.name,
                  res_users_reg.partner_id.id,
                  res_users_reg.company_id.id,
                  res_users_reg.login,
                  row[1],
                  res_users_reg.image,
                  str(res_users_reg.groups_id.id),
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> res_users_count: ', res_users_count)
    print()


def res_users_import_sqlite(client, args, db_path, table_name):

    res_users_model = client.model('res.users')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            partner_id,
            company_id,
            login,
            password_crypt,
            image,
            groups_id,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    res_users_count = 0
    for row in cursor:
        res_users_count += 1

        print(
            res_users_count, row['id'], row['name'], row['login'],
        )

        res_users_browse = res_users_model.browse([('name', '=', row['name']), ])
        if res_users_browse.id == []:

            values = {
                'name': row['name'],
                'partner_id': row['partner_id'],
                'company_id': row['company_id'],
                'login': row['login'],
                'password_crypt': row['password_crypt'],
                'image': row['image'],
                # 'groups_id': row['groups_id'],
            }
            res_users_id = res_users_model.create(values).id

            cursor2.execute(
                '''
                UPDATE ''' + table_name + '''
                SET new_id = ?
                WHERE id = ?;''',
                (res_users_id,
                 row['id']
                 )
            )

            if row['groups_id'] != '[]':

                groups_id = row['groups_id'].split(',')
                new_groups_id = []
                for x in range(0, len(groups_id)):
                    group_id = int(re.sub('[^0-9]', '', groups_id[x]))
                    # cursor2.execute(
                    #     '''
                    #     SELECT new_id
                    #     FROM ''' + group_table_name + '''
                    #     WHERE id = ?;''',
                    #     (group_id,
                    #      )
                    # )
                    # new_group_id = cursor2.fetchone()[0]

                    values = {
                        'groups_id': [(4, group_id)],
                    }
                    res_users_model.write(res_users_id, values)

                    new_groups_id.append(group_id)

                print('>>>>>', row[4], new_groups_id)

    conn.commit()
    conn.close()

    print()
    print('--> res_users_count: ', res_users_count)
