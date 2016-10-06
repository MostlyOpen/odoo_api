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

import re
import requests
import sqlite3


def search_by_cep(client, zip_code):

    l10n_br_zip = client.model('l10n_br.zip')
    l10n_br_base_city = client.model('l10n_br_base.city')

    l10n_br_zip_browse = l10n_br_zip.browse([('zip', '=', re.sub('[^0-9]', '', zip_code)), ])
    print(l10n_br_zip_browse.id)
    if l10n_br_zip_browse.id == []:

        try:
            url_viacep = 'http://viacep.com.br/ws/' + \
                zip_code + '/json/unicode/'
            obj_viacep = requests.get(url_viacep)
            res = obj_viacep.json()
            # print('\n', res, '\n')
            print(res)
            if res:
                l10n_br_base_city_browse = l10n_br_base_city.browse([
                    ('ibge_code', '=', res['ibge'][2:]),
                    ('state_id.code', '=', res['uf']),
                ])
                l10n_br_city = l10n_br_base_city_browse[0]
                values = {
                    'zip': re.sub('[^0-9]', '', res['cep']),
                    'street': res['logradouro'],
                    'district': res['bairro'],
                    'country_id': l10n_br_city.state_id.country_id.id,
                    'state_id': l10n_br_city.state_id.id,
                    'l10n_br_city_id': l10n_br_city.id,
                }
                l10n_br_zip.create(values)

        except Exception as e:
            print(e.message)


def l10n_br_zip_export_sqlite(client, args, db_path, table_name):

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
            zip,
            street_type,
            street,
            district,
            country_id,
            state_id,
            l10n_br_city_id,
            new_id INTEGER
            );
        '''
    )

    l10n_br_zip_model = client.model('l10n_br.zip')
    l10n_br_zip_browse = l10n_br_zip_model.browse(args)

    l10n_br_zip_count = 0
    for l10n_br_zip_reg in l10n_br_zip_browse:
        l10n_br_zip_count += 1

        print(l10n_br_zip_count, l10n_br_zip_reg.id, l10n_br_zip_reg.zip)

        street_type = None
        if l10n_br_zip_reg.street_type:
            street_type = l10n_br_zip_reg.street_type

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                zip,
                street_type,
                street,
                district,
                country_id,
                state_id,
                l10n_br_city_id
                )
            VALUES(?,?,?,?,?,?,?,?)
            ''', (l10n_br_zip_reg.id,
                  l10n_br_zip_reg.zip,
                  street_type,
                  l10n_br_zip_reg.street,
                  l10n_br_zip_reg.district,
                  l10n_br_zip_reg.country_id.id,
                  l10n_br_zip_reg.state_id.id,
                  l10n_br_zip_reg.l10n_br_city_id.id,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> l10n_br_zip_count: ', l10n_br_zip_count)


def l10n_br_zip_import_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute(
        '''
        SELECT
            id,
            zip,
            street_type,
            street,
            district,
            country_id,
            state_id,
            l10n_br_city_id,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    l10n_br_zip_model = client.model('l10n_br.zip')

    print(data)
    print([field[0] for field in cursor.description])
    l10n_br_zip_count = 0
    for row in cursor:
        l10n_br_zip_count += 1

        print(l10n_br_zip_count, row[0], row[1], row[2])

        values = {
            'zip': row[1],
            'street_type': row[2],
            'street': row[3],
            'district': row[4],
            'country_id': row[5],
            'state_id': row[6],
            'l10n_br_city_id': row[7],
        }
        l10n_br_zip_id = l10n_br_zip_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (l10n_br_zip_id,
             row[0]
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> l10n_br_zip_count: ', l10n_br_zip_count)
