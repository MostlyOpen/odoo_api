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


def ir_sequence_export_sqlite(client, args, db_path, table_name, conn_string):

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
            implementation,
            code,
            active,
            company_id,
            prefix,
            suffix,
            use_date_range,
            padding,
            number_increment,
            number_next,
            postgres_last_value,
            new_id INTEGER
            );
        '''
    )

    pg_conn = psycopg2.connect(conn_string)
    pg_cursor = pg_conn.cursor()

    ir_sequence_model = client.model('ir.sequence')
    ir_sequence_browse = ir_sequence_model.browse(args)

    ir_sequence_count = 0
    for ir_sequence_reg in ir_sequence_browse:
        ir_sequence_count += 1

        query = "SELECT last_value, increment_by, is_called FROM ir_sequence_%03d" % ir_sequence_reg.id
        pg_cursor.execute(query)
        row = pg_cursor.fetchone()
        postgres_last_value = row[0]

        print(
            ir_sequence_count, ir_sequence_reg.id, ir_sequence_reg.name.encode("utf-8"), ir_sequence_reg.code,
            postgres_last_value,
        )

        prefix = None
        if ir_sequence_reg.prefix:
            prefix = ir_sequence_reg.prefix

        suffix = None
        if ir_sequence_reg.suffix:
            suffix = ir_sequence_reg.suffix

        suffix = None
        if ir_sequence_reg.suffix:
            suffix = ir_sequence_reg.suffix

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                implementation,
                code,
                active,
                company_id,
                prefix,
                suffix,
                use_date_range,
                padding,
                number_increment,
                number_next,
                postgres_last_value
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (ir_sequence_reg.id,
                  ir_sequence_reg.name,
                  ir_sequence_reg.implementation,
                  ir_sequence_reg.code,
                  ir_sequence_reg.active,
                  ir_sequence_reg.company_id.id,
                  prefix,
                  suffix,
                  ir_sequence_reg.use_date_range,
                  ir_sequence_reg.padding,
                  ir_sequence_reg.number_increment,
                  ir_sequence_reg.number_next,
                  postgres_last_value,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> ir_sequence_count: ', ir_sequence_count)


def ir_sequence_import_sqlite(client, args, db_path, table_name, conn_string):

    # ir_sequence_model = client.model('ir.sequence')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            implementation,
            code,
            active,
            company_id,
            prefix,
            suffix,
            use_date_range,
            padding,
            number_increment,
            number_next,
            postgres_last_value,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    pg_conn = psycopg2.connect(conn_string)
    pg_cursor = pg_conn.cursor()

    ir_sequence_count = 0
    for row in cursor:
        ir_sequence_count += 1

        print(
            ir_sequence_count, row['id'], row['name'], row['implementation'], row['code'],
            row['prefix'], row['padding'], row['number_increment'], row['number_next'], row['postgres_last_value']
        )

        query = "SELECT last_value, increment_by, is_called FROM ir_sequence_%03d" % row['id']
        pg_cursor.execute(query)
        row2 = pg_cursor.fetchone()
        postgres_last_value = row2[0]

        my_table = row['code'][:-5].replace('.', '_')
        query2 = "SELECT MAX(id) FROM %s;" % my_table
        pg_cursor.execute(query2)
        row3 = pg_cursor.fetchone()
        max_id = row3[0]

        print('>>>>>', my_table, row['postgres_last_value'], postgres_last_value, max_id)

        if postgres_last_value < max_id:
            if row['postgres_last_value'] > max_id:
                query3 = "SELECT setval('ir_sequence_%03d', %d);" % (row['id'], row['postgres_last_value'])
                print('>>>>>>>>>>>>>>>', query3)
                pg_cursor.execute(query3)
                row4 = pg_cursor.fetchone()
                print('>>>>>>>>>>>>>>>', row4[0])
            else:
                query3 = "SELECT setval('ir_sequence_%03d', %d);" % (row['id'], max_id)
                print('>>>>>>>>>>>>>>>', query3)
                pg_cursor.execute(query3)
                row4 = pg_cursor.fetchone()
                print('>>>>>>>>>>>>>>>', row4[0])

    conn.commit()
    conn.close()

    print()
    print('--> ir_sequence_count: ', ir_sequence_count)
