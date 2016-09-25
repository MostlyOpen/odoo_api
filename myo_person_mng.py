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


def person_mng_search_address(client, batch_name, state):

    person_mng_model = client.model('myo.person.mng')

    person_mng_browse = person_mng_model.browse([('batch_name', '=', batch_name), ('state', '=', state), ])

    rownum = 0
    for person_mng_reg in person_mng_browse:

        print(rownum, person_mng_reg.name)

        values = {
            "address_id": person_mng_reg.address_mng_id.address_id.id,
        }
        person_mng_model.write(person_mng_reg.id, values)

        rownum += 1

    print()
    print('--> rownum: ', rownum - 1)
    print()


def person_mng_create_person(client, batch_name, state):

    person_mng_model = client.model('myo.person.mng')
    person_model = client.model('myo.person')
    person_address_model = client.model('myo.person.address')

    person_mng_browse = person_mng_model.browse([('batch_name', '=', batch_name), ('state', '=', state), ])

    rownum = 0
    for person_mng_reg in person_mng_browse:

        print(rownum, person_mng_reg.name)

        tag_ids = []
        for tag_id in person_mng_reg.tag_ids.id:
            tag_ids = tag_ids + [(4, tag_id)]

        values = {
            'name': person_mng_reg.name,
            # 'code': '/',
            'gender': person_mng_reg.gender,
            'birthday': person_mng_reg.birthday,
            'tag_ids': tag_ids,
            "address_id": person_mng_reg.address_id.id,
        }
        person_reg_new = person_model.create(values)

        values = {
            'person_id': person_reg_new.id,
            "address_id": person_mng_reg.address_id.id,
        }
        person_address_model.create(values)

        values = {
            "person_id": person_reg_new.id,
            "code": person_reg_new.code,
            "state": 'done',
        }
        person_mng_model.write(person_mng_reg.id, values)

        rownum += 1

    print()
    print('--> rownum: ', rownum - 1)
    print()
