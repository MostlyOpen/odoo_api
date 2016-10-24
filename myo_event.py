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
# import re


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
