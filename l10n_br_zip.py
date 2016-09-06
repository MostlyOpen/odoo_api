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
