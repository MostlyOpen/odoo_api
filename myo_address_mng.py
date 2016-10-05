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


def address_mng_create_address(client, batch_name, state):

    address_mng_model = client.model('myo.address.mng')
    address_model = client.model('myo.address')

    address_mng_browse = address_mng_model.browse([('batch_name', '=', batch_name), ('state', '=', state), ])

    rownum = 0
    for address_mng_reg in address_mng_browse:

        print(rownum, address_mng_reg.name)

        tag_ids = []
        for tag_id in address_mng_reg.tag_ids.id:
            tag_ids = tag_ids + [(4, tag_id)]

        values = {
            'name': address_mng_reg.name,
            # 'code': '/',
            'zip': address_mng_reg.zip,
            'street': address_mng_reg.street,
            'number': address_mng_reg.number,
            'street2': address_mng_reg.street2,
            'district': address_mng_reg.district,
            'country_id': address_mng_reg.country_id,
            'state_id': address_mng_reg.state_id,
            'l10n_br_city_id': address_mng_reg.l10n_br_city_id,
            'phone': address_mng_reg.phone,
            'mobile': address_mng_reg.mobile,
            'tag_ids': tag_ids,
        }
        address_reg_new = address_model.create(values)

        values = {
            "address_id": address_reg_new.id,
            "code": address_reg_new.code,
            "state": 'done',
        }
        address_mng_model.write(address_mng_reg.id, values)

        rownum += 1

    print()
    print('--> rownum: ', rownum - 1)
