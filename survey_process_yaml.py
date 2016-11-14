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

import yaml
import xlwt


def survey_label_matrix(
    doc, yaml_out_file, xml_file, txt_file, key1, key2, key3, key4, question_type, question_id, question_nr,
    label_sequence
):

    global sheet
    global row_nr
    global matrix_col_row_nr
    global matrix_col_nr
    global first_matrix_col_row_nr
    global matrix_col_nrs
    global matrix_row_nrs
    global style_choice

    _value_ = doc[key1][key2][key3][key4]['value'].encode("utf-8")
    _model_ = doc[key1][key2][key3][key4]['model']
    if label_sequence < 100:
        _id_ = question_id + '_0' + str(label_sequence / 10)
        _nr_ = question_nr + '.' + str(label_sequence / 10)
    else:
        _id_ = question_id + '_' + str(label_sequence / 10)
        _nr_ = question_nr + '.' + str(label_sequence / 10)
    _question_id_ = question_id
    _sequence_ = str(label_sequence)

    yaml_out_file.write('            %s:\n' % (_id_))
    yaml_out_file.write('                model: %s\n' % (_model_))
    yaml_out_file.write('                value: \'%s\'\n' % (_value_))

    # _value_ = '[' + _id_ + '] ' + _value_

    if _model_ == 'survey.label.col':
        txt_file.write('            [col]%s\n' % (_value_))
    if _model_ == 'survey.label.row':
        txt_file.write('            [row]%s\n' % (_value_))

    if _model_ == 'survey.label.row':
        row = sheet.row(row_nr)
        row.write(0, '[' + key4 + ']')
        _value_ = '' + _nr_ + '. ' + _value_
        row.write(5, _value_.decode("utf-8"))
        matrix_row_nrs = matrix_row_nrs + [row_nr]
        # for col_nr in matrix_col_nrs:
        #     # row.write(col_nr + 2, '.')
        #     row.write(col_nr, '.')
        row_nr += 2
    if _model_ == 'survey.label.col':
        row = sheet.row(matrix_col_row_nr)
        row.write(matrix_col_nr, '[' + key4 + ']')
        # matrix_col_nrs = matrix_col_nrs + [matrix_col_nr]
        # matrix_col_nr += 2
        row = sheet.row(matrix_col_row_nr + 1)
        row.write(matrix_col_nr, _value_.decode("utf-8"))
        # matrix_col_nr += 2
        for matrix_row_nr in matrix_row_nrs:
            style_dot = xlwt.easyxf('align: vertical center, horizontal right;')
            row = sheet.row(matrix_row_nr)
            row.write(matrix_col_nr, '.', style=style_dot)

            row.write(matrix_col_nr + 1, None, style=style_choice)

        matrix_col_nr += 3

    xml_file.write('                    <record model="%s" id="%s">\n' % ('survey.label', _id_))
    xml_file.write('                        <field name="value">%s</field>\n' % (_value_))
    if _model_ == 'survey.label.col':
        xml_file.write('                        <field name="question_id" ref="%s"/>\n' % (_question_id_))
    if _model_ == 'survey.label.row':
        xml_file.write('                        <field name="question_id_2" ref="%s"/>\n' % (_question_id_))
    xml_file.write('                        <field name="sequence" eval="%s"/>\n' % (_sequence_))

    yaml_out_file.write('\n')

    xml_file.write('                    </record>\n')
    xml_file.write('\n')


def survey_label(
    doc, yaml_out_file, xml_file, txt_file, key1, key2, key3, key4, question_type, question_id, question_nr,
    label_sequence
):

    global sheet
    global row_nr
    global style_choice

    _value_ = doc[key1][key2][key3][key4]['value'].encode("utf-8")
    _model_ = doc[key1][key2][key3][key4]['model']
    if label_sequence < 100:
        _id_ = question_id + '_0' + str(label_sequence / 10)
    else:
        _id_ = question_id + '_' + str(label_sequence / 10)
    _question_id_ = question_id
    _sequence_ = str(label_sequence)

    yaml_out_file.write('            %s:\n' % (_id_))
    yaml_out_file.write('                model: %s\n' % (_model_))
    yaml_out_file.write('                value: \'%s\'\n' % (_value_))

    # _value_ = '[' + _id_ + '] ' + _value_

    txt_file.write('            %s\n' % (_value_))

    style_dot = xlwt.easyxf('align: vertical center, horizontal right;')
    row = sheet.row(row_nr)
    row.write(0, '[' + key4 + ']')
    row.write(4, '.', style=style_dot)

    row.write(5, None, style=style_choice)

    row.write(6, _value_.decode("utf-8"))
    row_nr += 1

    xml_file.write('                    <record model="%s" id="%s">\n' % (_model_, _id_))
    xml_file.write('                        <field name="value">%s</field>\n' % (_value_))
    xml_file.write('                        <field name="question_id" ref="%s"/>\n' % (_question_id_))
    xml_file.write('                        <field name="sequence" eval="%s"/>\n' % (_sequence_))

    yaml_out_file.write('\n')

    xml_file.write('                    </record>\n')
    xml_file.write('\n')


def survey_question(doc, yaml_out_file, xml_file, txt_file, key1, key2, key3, page_id, page_nr, question_sequence):

    global sheet
    global row_nr
    global matrix_col_row_nr
    global matrix_col_nr
    global matrix_col_nrs
    global matrix_row_nrs
    global style_choice

    _page_id_ = page_id
    if question_sequence < 100:
        _id_ = page_id + '_0' + str(question_sequence / 10)
        _nr_ = page_nr + '.' + str(question_sequence / 10)
    else:
        _id_ = page_id + '_' + str(question_sequence / 10)
        _nr_ = page_nr + '.' + str(question_sequence / 10)
    _sequence_ = str(question_sequence)

    _model_ = doc[key1][key2][key3]['model']
    _question_ = doc[key1][key2][key3]['question'].encode("utf-8")
    _type_ = doc[key1][key2][key3]['type']
    _constr_mandatory_ = str(doc[key1][key2][key3]['constr_mandatory'])
    _constr_error_msg_ = doc[key1][key2][key3]['constr_error_msg'].encode("utf-8")

    if _type_ == 'free_text' or _type_ == 'textbox' or _type_ == 'datetime':

        yaml_out_file.write('        %s:\n' % (_id_))
        yaml_out_file.write('            model: %s\n' % (_model_))
        yaml_out_file.write('            question: \'%s\'\n' % (_question_))
        yaml_out_file.write('            type: %s\n' % (_type_))
        yaml_out_file.write('            constr_mandatory: %s\n' % (_constr_mandatory_))
        yaml_out_file.write('            constr_error_msg: \'%s\'\n' % (_constr_error_msg_))
        yaml_out_file.write('\n')

        # _question_ = '[' + _id_ + '] ' + _question_
        _question_ = '' + _nr_ + '. ' + _question_

        txt_file.write('        %s\n' % (_question_))
        txt_file.write('            (%s)\n' % (_type_))
        if _type_ == 'free_text':
            txt_file.write('            ' + '____________________________________\n' +
                           '            ' + '____________________________________\n' +
                           '            ' + '____________________________________\n' +
                           '            ' + '____________________________________\n')
        else:
            txt_file.write('            ' + '____________________________________\n')

        style_dot = xlwt.easyxf('align: vertical center, horizontal right;')
        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _question_.decode("utf-8"))
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _type_.decode("utf-8"))
        row.hidden = True
        row_nr += 2
        if _type_ == 'free_text':
            style_b_unlocked = xlwt.easyxf('border: bottom THIN; protection: cell_locked false; font: bold on;')
            style_b = xlwt.easyxf('border: bottom THIN;')
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            row.write(4, '.', style=style_dot)
            row.write(5, None, style=style_b_unlocked)
            for i in range(6, 15):
                row.write(i, None, style=style_b)
            row_nr += 1
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            row.write(4, '.', style=style_dot)
            row.write(5, None, style=style_b_unlocked)
            for i in range(6, 15):
                row.write(i, None, style=style_b)
            row_nr += 1
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            row.write(4, '.', style=style_dot)
            row.write(5, None, style=style_b_unlocked)
            for i in range(6, 15):
                row.write(i, None, style=style_b)
            row_nr += 1
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            row.write(4, '.', style=style_dot)
            row.write(5, None, style=style_b_unlocked)
            for i in range(6, 15):
                row.write(i, None, style=style_b)
            row_nr += 1
        else:
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            row.write(4, '.', style=style_dot)

            style_b_unlocked = xlwt.easyxf('border: bottom THIN; protection: cell_locked false; font: bold on;')
            style_b = xlwt.easyxf('border: bottom THIN;')
            row.write(5, None, style=style_b_unlocked)
            for i in range(6, 15):
                row.write(i, None, style=style_b)

            row_nr += 1
        row_nr += 1

        xml_file.write('                <!-- %s -->\n' % (_question_))
        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, _id_))
        xml_file.write('                    <field name="question">%s</field>\n' % (_question_))
        xml_file.write('                    <field name="type">%s</field>\n' % (_type_))
        xml_file.write('                    <field name="page_id" ref="%s"/>\n' % (_page_id_))
        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_sequence_))
        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' % (_constr_mandatory_))
        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' % (_constr_error_msg_))
        xml_file.write('                </record>\n')
        xml_file.write('\n')

    if _type_ == 'simple_choice':

        _display_mode_ = doc[key1][key2][key3]['display_mode']
        _column_nb_ = doc[key1][key2][key3]['column_nb']
        _comments_allowed_ = str(doc[key1][key2][key3]['comments_allowed'])
        _comments_message_ = doc[key1][key2][key3]['comments_message'].encode("utf-8")

        yaml_out_file.write('        %s:\n' % (_id_))
        yaml_out_file.write('            model: %s\n' % (_model_))
        yaml_out_file.write('            question: \'%s\'\n' % (_question_))
        yaml_out_file.write('            type: %s\n' % (_type_))
        yaml_out_file.write('            display_mode: %s\n' % (_display_mode_))
        yaml_out_file.write('            column_nb: %s\n' % (_column_nb_))
        yaml_out_file.write('            constr_mandatory: %s\n' % (_constr_mandatory_))
        yaml_out_file.write('            constr_error_msg: \'%s\'\n' % (_constr_error_msg_))
        yaml_out_file.write('            comments_allowed: %s\n' % (_comments_allowed_))
        yaml_out_file.write('            comments_message: \'%s\'\n' % (_comments_message_))
        yaml_out_file.write('\n')

        # _question_ = '[' + _id_ + '] ' + _question_
        _question_ = '' + _nr_ + '. ' + _question_

        txt_file.write('        %s\n' % (_question_))
        txt_file.write('            (%s)\n' % (_type_))

        style_string = '''
            font: bold on;
            borders: left THIN, right THIN, top THIN, bottom THIN;
            align: vertical center, horizontal center;
            protection: cell_locked false;
        '''
        style_choice = xlwt.easyxf(style_string)

        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _question_.decode("utf-8"))
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _type_.decode("utf-8"))
        row.hidden = True
        row_nr += 2

        xml_file.write('                <!-- %s -->\n' % (_question_))
        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, _id_))
        xml_file.write('                    <field name="question">%s</field>\n' % (_question_))
        xml_file.write('                    <field name="type">%s</field>\n' % (_type_))
        xml_file.write('                    <field name="page_id" ref="%s"/>\n' % (_page_id_))
        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_sequence_))
        xml_file.write('                    <field name="display_mode">%s</field>\n' % (_display_mode_))
        xml_file.write('                    <field name="column_nb">%s</field>\n' % (_column_nb_))
        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' % (_constr_mandatory_))
        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' % (_constr_error_msg_))
        xml_file.write('                    <field name="comments_allowed">%s</field>\n' % (_comments_allowed_))
        xml_file.write('                    <field name="comments_message">%s</field>\n' % (_comments_message_))
        xml_file.write('                </record>\n')
        xml_file.write('\n')

        label_sequence = 0
        for key4 in sorted(doc[key1][key2][key3].keys()):
            try:
                _model_ = doc[key1][key2][key3][key4]['model']
                print('            ', key4, _model_)
                if _model_ == 'survey.label':
                    label_sequence += 10
                    survey_label(
                        doc, yaml_out_file, xml_file, txt_file, key1, key2, key3, key4, _type_, _id_, _nr_,
                        label_sequence
                    )
            except Exception, e:
                print('>>>>>', e.message, e.args)

        if _comments_allowed_ == 'True':
            txt_file.write('            %s____________________________________\n' % (_comments_message_))

        if _comments_allowed_ == 'True':
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            row.write(6, _comments_message_.decode("utf-8"))
            row_nr += 2
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            style_dot = xlwt.easyxf('align: vertical center, horizontal right;')
            row.write(6, '.', style=style_dot)

            style_b_unlocked = xlwt.easyxf('border: bottom THIN; protection: cell_locked false; font: bold on;')
            style_b = xlwt.easyxf('border: bottom THIN;')
            row.write(7, None, style=style_b_unlocked)
            for i in range(8, 17):
                row.write(i, None, style=style_b)

            row_nr += 2
        else:
            row_nr += 1

    if _type_ == 'multiple_choice':

        _column_nb_ = doc[key1][key2][key3]['column_nb']
        _comments_allowed_ = str(doc[key1][key2][key3]['comments_allowed'])
        _comments_message_ = doc[key1][key2][key3]['comments_message'].encode("utf-8")

        yaml_out_file.write('        %s:\n' % (_id_))
        yaml_out_file.write('            model: %s\n' % (_model_))
        yaml_out_file.write('            question: \'%s\'\n' % (_question_))
        yaml_out_file.write('            type: %s\n' % (_type_))
        yaml_out_file.write('            column_nb: %s\n' % (_column_nb_))
        yaml_out_file.write('            constr_mandatory: %s\n' % (_constr_mandatory_))
        yaml_out_file.write('            constr_error_msg: \'%s\'\n' % (_constr_error_msg_))
        yaml_out_file.write('            comments_allowed: %s\n' % (_comments_allowed_))
        yaml_out_file.write('            comments_message: \'%s\'\n' % (_comments_message_))
        yaml_out_file.write('\n')

        # _question_ = '[' + _id_ + '] ' + _question_
        _question_ = '' + _nr_ + '. ' + _question_

        txt_file.write('        %s\n' % (_question_))
        txt_file.write('            (%s)\n' % (_type_))

        style_string = '''
            font: bold on;
            borders: left DOTTED, right DOTTED, top DOTTED, bottom DOTTED;
            align: vertical center, horizontal center;
            protection: cell_locked false;
        '''
        style_choice = xlwt.easyxf(style_string)

        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _question_.decode("utf-8"))
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _type_.decode("utf-8"))
        row.hidden = True
        row_nr += 2

        xml_file.write('                <!-- %s -->\n' % (_question_))
        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, _id_))
        xml_file.write('                    <field name="question">%s</field>\n' % (_question_))
        xml_file.write('                    <field name="type">%s</field>\n' % (_type_))
        xml_file.write('                    <field name="page_id" ref="%s"/>\n' % (_page_id_))
        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_sequence_))
        xml_file.write('                    <field name="column_nb">%s</field>\n' % (_column_nb_))
        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' % (_constr_mandatory_))
        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' % (_constr_error_msg_))
        xml_file.write('                    <field name="comments_allowed">%s</field>\n' % (_comments_allowed_))
        xml_file.write('                    <field name="comments_message">%s</field>\n' % (_comments_message_))
        xml_file.write('                </record>\n')
        xml_file.write('\n')

        label_sequence = 0
        for key4 in sorted(doc[key1][key2][key3].keys()):
            try:
                _model_ = doc[key1][key2][key3][key4]['model']
                print('            ', key4, _model_)
                if _model_ == 'survey.label':
                    label_sequence += 10
                    survey_label(
                        doc, yaml_out_file, xml_file, txt_file, key1, key2, key3, key4, _type_, _id_, _nr_,
                        label_sequence
                    )
            except Exception, e:
                print('>>>>>', e.message, e.args)

        if _comments_allowed_ == 'True':
            txt_file.write('            %s____________________________________\n' % (_comments_message_))

        if _comments_allowed_ == 'True':
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            row.write(6, _comments_message_.decode("utf-8"))
            row_nr += 2
            row = sheet.row(row_nr)
            row.write(0, '[' + key3 + ']')
            style_dot = xlwt.easyxf('align: vertical center, horizontal right;')
            row.write(6, '.', style=style_dot)

            style_b_unlocked = xlwt.easyxf('border: bottom THIN; protection: cell_locked false; font: bold on;')
            style_b = xlwt.easyxf('border: bottom THIN;')
            row.write(7, None, style=style_b_unlocked)
            for i in range(8, 17):
                row.write(i, None, style=style_b)

            row_nr += 2
        else:
            row_nr += 1

    if _type_ == 'matrix':

        _matrix_subtype_ = str(doc[key1][key2][key3]['matrix_subtype'])

        yaml_out_file.write('        %s:\n' % (_id_))
        yaml_out_file.write('            model: %s\n' % (_model_))
        yaml_out_file.write('            question: \'%s\'\n' % (_question_))
        yaml_out_file.write('            type: %s\n' % (_type_))
        yaml_out_file.write('            matrix_subtype: %s\n' % (_matrix_subtype_))
        yaml_out_file.write('            constr_mandatory: %s\n' % (_constr_mandatory_))
        yaml_out_file.write('            constr_error_msg: \'%s\'\n' % (_constr_error_msg_))
        yaml_out_file.write('\n')

        # _question_ = '[' + _id_ + '] ' + _question_
        _question_ = '' + _nr_ + '. ' + _question_

        txt_file.write('        %s\n' % (_question_))
        txt_file.write('            (%s, %s)\n' % (_type_, _matrix_subtype_))

        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _question_.decode("utf-8"))
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, '[' + key3 + ']')
        row.write(4, _type_ + '_' + _matrix_subtype_)
        row.hidden = True
        row_nr += 1

        xml_file.write('                <!-- %s -->\n' % (_question_))
        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, _id_))
        xml_file.write('                    <field name="question">%s</field>\n' % (_question_))
        xml_file.write('                    <field name="type">%s</field>\n' % (_type_))
        xml_file.write('                    <field name="matrix_subtype">%s</field>\n' % (_matrix_subtype_))
        xml_file.write('                    <field name="page_id" ref="%s"/>\n' % (_page_id_))
        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_sequence_))
        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' % (_constr_mandatory_))
        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' % (_constr_error_msg_))
        xml_file.write('                </record>\n')
        xml_file.write('\n')

        row_nr += 1
        matrix_col_row_nr = row_nr
        matrix_col_nr = 8
        matrix_col_nrs = []
        matrix_row_nrs = []
        row_nr += 3

        style_string = '''
            font: bold on;
            borders: left THIN, right THIN, top THIN, bottom THIN;
            align: vertical center, horizontal center;
            protection: cell_locked false;
        '''
        style_choice = xlwt.easyxf(style_string)

        row_matrix_col = sheet.row(matrix_col_row_nr)
        row_matrix_col.write(0, '[]')
        sheet.row(matrix_col_row_nr).hidden = True

        label_sequence = 0
        for key4 in sorted(doc[key1][key2][key3].keys()):
            try:
                _model_ = doc[key1][key2][key3][key4]['model']
                print('            ', key4, _model_)
                if _model_ == 'survey.label.col' or _model_ == 'survey.label.row':
                    label_sequence += 10
                    survey_label_matrix(
                        doc, yaml_out_file, xml_file, txt_file, key1, key2, key3, key4, _type_, _id_, _nr_,
                        label_sequence
                    )
            except Exception, e:
                print('>>>>>', e.message, e.args)

        row_nr += 1


def survey_page(doc, yaml_out_file, xml_file, txt_file, key1, key2, survey_id, page_sequence):

    global sheet
    global row_nr

    _title_ = doc[key1][key2]['title'].encode("utf-8")
    _model_ = doc[key1][key2]['model']
    if page_sequence < 100:
        _id_ = survey_id + '_0' + str(page_sequence / 10)
        _nr_ = '' + str(page_sequence / 10)
    else:
        _id_ = survey_id + '_' + str(page_sequence / 10)
        _nr_ = str(page_sequence / 10)
    _description_ = doc[key1][key2]['description'].encode("utf-8")
    _survey_id_ = key1
    _sequence_ = str(page_sequence)

    yaml_out_file.write('    %s:\n' % (_id_))
    yaml_out_file.write('        model: %s\n' % (_model_))
    yaml_out_file.write('        title: \'%s\'\n' % (_title_))
    yaml_out_file.write('        description: \'%s\'\n' % (_description_))
    yaml_out_file.write('\n')

    # _title_ = '[' + _id_ + '] ' + _title_
    _title_ = '' + _nr_ + '. ' + _title_
    # _description_ = '[' + _id_ + '] ' + _description_

    txt_file.write('    %s\n' % (_title_))

    row = sheet.row(row_nr)
    row.write(0, '[' + key2 + ']')
    row.write(3, _title_.decode("utf-8"))
    row_nr += 1
    row = sheet.row(row_nr)
    row.write(0, '[' + key2 + ']')
    row.write(3, _description_.decode("utf-8"))
    row_nr += 2

    xml_file.write('            <!-- %s -->\n' % (_title_))
    xml_file.write('            <record model="%s" id="%s">\n' % (_model_, _id_))
    xml_file.write('                <field name="title">%s</field>\n' % (_title_))
    xml_file.write('                <field name="survey_id" ref="%s"/>\n' % (_survey_id_))
    xml_file.write('                <field name="sequence" eval="%s"/>\n' % (_sequence_))
    xml_file.write('                <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' % (_description_))
    xml_file.write('            </record>' + '\n')
    xml_file.write('\n')

    question_sequence = 0
    for key3 in sorted(doc[key1][key2].keys()):
        try:
            _model_ = doc[key1][key2][key3]['model']
            print('        ', key3, _model_)
            if _model_ == 'survey.question':

                question_sequence += 10
                survey_question(
                    doc, yaml_out_file, xml_file, txt_file, key1, key2, key3, _id_, _nr_, question_sequence
                )
        except Exception, e:
            print('>>>>>', e.message, e.args)


def survey(doc, yaml_out_file, xml_file, txt_file, key1):

    global sheet
    global row_nr

    _title_ = doc[key1]['title'].encode("utf-8")
    _model_ = doc[key1]['model']
    _id_ = key1
    _stage_id_ = doc[key1]['stage_id']
    _auth_required_ = doc[key1]['auth_required']
    _users_can_go_back_ = doc[key1]['users_can_go_back']
    _description_ = doc[key1]['description'].encode("utf-8")
    _thank_you_message_ = doc[key1]['thank_you_message'].encode("utf-8")

    yaml_out_file.write('%s:\n' % (key1))
    yaml_out_file.write('    model: %s\n' % (_model_))
    yaml_out_file.write('    title: \'%s\'\n' % (_title_))
    yaml_out_file.write('    stage_id: %s\n' % (_stage_id_))
    yaml_out_file.write('    auth_required: %s\n' % (_auth_required_))
    yaml_out_file.write('    users_can_go_back: %s\n' % (_users_can_go_back_))
    yaml_out_file.write('    description: \'%s\'\n' % (_description_))
    yaml_out_file.write('    thank_you_message: \'%s\'\n' % (_thank_you_message_))
    yaml_out_file.write('\n')

    _title_ = '[' + _id_ + '] ' + _title_
    # _description_ = '[' + _id_ + '] ' + _description_

    txt_file.write('%s\n' % (_title_))

    row = sheet.row(row_nr)
    row.write(0, '[' + key1 + ']')
    row.write(2, _title_.decode("utf-8"))
    row_nr += 1
    row = sheet.row(row_nr)
    row.write(0, '[' + key1 + ']')
    row.write(2, _description_.decode("utf-8"))
    row_nr += 2

    xml_file.write('        <!-- %s -->\n' % (_title_))
    xml_file.write('        <record model="%s" id="%s">\n' % (_model_, _id_))
    xml_file.write('            <field name="title">%s</field>\n' % (_title_))
    xml_file.write('            <field name="stage_id" ref="%s"/>\n' % (_stage_id_))
    xml_file.write('            <field name="auth_required" eval="%s"/>\n' % (_auth_required_))
    xml_file.write('            <field name="users_can_go_back" eval="%s"/>\n' % (_users_can_go_back_))
    xml_file.write('            <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' % (_description_))
    xml_file.write(
        '            <field name="thank_you_message">&lt;p&gt;%s&lt;/p&gt;</field>\n' % (_thank_you_message_)
    )
    xml_file.write('        </record>\n')
    xml_file.write('\n')

    page_sequence = 0
    for key2 in sorted(doc[key1].keys()):
        try:
            _model_ = doc[key1][key2]['model']
            print('    ', key2, _model_)
            if _model_ == 'survey.page':
                page_sequence += 10
                survey_page(doc, yaml_out_file, xml_file, txt_file, key1, key2, key1, page_sequence)
        except Exception, e:
            print('>>>>>', e.message, e.args)


def survey_process_yaml(yaml_filename, yaml_out_filename, xml_filename, txt_filename, xls_filename):

    global sheet
    global row_nr

    yaml_file = open(yaml_filename, 'r')
    doc = yaml.load(yaml_file)

    yaml_out_file = open(yaml_out_filename, "w")
    txt_file = open(txt_filename, "w")
    xml_file = open(xml_filename, "w")

    xml_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    xml_file.write('<openerp>\n')
    xml_file.write('    <data noupdate="0">\n')
    xml_file.write('\n')

    book = xlwt.Workbook()

    for key1 in sorted(doc.keys()):
        _model_ = doc[key1]['model']
        print(key1, _model_)
        if _model_ == 'survey.survey':

            row_nr = 0
            sheet = book.add_sheet(key1)
            row = sheet.row(row_nr)
            row.write(0, '[' + key1 + ']')
            row_nr += 1

            survey(doc, yaml_out_file, xml_file, txt_file, key1)

            sheet.col(0).hidden = True

            for i in range(100):
                sheet.col(i).width = 256 * 2

            sheet.protect = True
            sheet.password = "OpenSesame"

            book.save(xls_filename)

    xml_file.write('    </data>\n')
    xml_file.write('</openerp>\n')

    yaml_file.close()
    yaml_out_file.close()
    txt_file.close()
    xml_file.close()
