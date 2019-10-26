# -*- coding: utf-8 -*-
# Copyright 2017-2018 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID


def init_test_model(env, model_cls):
    registry = env.registry
    cr = env.cr
    model = model_cls._build_model(registry, cr)
    model._prepare_setup(cr, SUPERUSER_ID)
    model._setup_base(cr, SUPERUSER_ID, partial=False)
    model._setup_fields(cr, SUPERUSER_ID, partial=False)
    model._setup_complete(cr, SUPERUSER_ID)
    model._auto_init(cr, {'module': __name__})


def _zip(iter1, iter2):
    i = 0
    iter1 = iter(iter1)
    iter2 = iter(iter2)
    while True:
        i1 = next(iter1, None)
        i2 = next(iter2, None)
        if i1 is None and i2 is None:
            return
        yield i, i1, i2
        i += 1


def assert_matrix(matrix, expected):
    for i, row, expected_row in _zip(matrix.iter_rows(), expected):
        if row is None and expected_row is not None:
            raise AssertionError("not enough rows")
        if row is not None and expected_row is None:
            raise AssertionError("too many rows")
        for j, cell, expected_val in _zip(row.iter_cells(), expected_row):
            assert (cell and cell.val) == expected_val, \
                "%s != %s in row %s col %s" % \
                (cell and cell.val, expected_val, i, j)
