# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase


class TestPublicHolidatFranceCommon(TransactionCase):

    def _define_calendar(self, name, attendances, tz):
        return self.env['resource.calendar'].create({
            'name': name,
            'tz': tz,
            'attendance_ids': [
                (0, 0, {
                    'name': '%s_%d' % (name, index),
                    'hour_from': att[0],
                    'hour_to': att[1],
                    'dayofweek': str(att[2]),
                })
                for index, att in enumerate(attendances)
            ],
        })

    def setUp(self):
        super(TestPublicHolidatFranceCommon, self).setUp()

        # UTC+1 winter, UTC+2 summer
        self.calendar = self._define_calendar('40 Hours', [(8, 16, i) for i in range(5)], 'Europe/Brussels')
