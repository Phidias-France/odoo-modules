# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime
from pytz import timezone, utc

from odoo import fields
from odoo.addons.phi_france_jours_ferie.tests.common import TestPublicHolidatFranceCommon


def datetime_tz(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
    """ Return a `datetime` object with a given timezone (if given). """
    dt = datetime(year, month, day, hour, minute, second, microsecond)
    return timezone(tzinfo).localize(dt) if tzinfo else dt


def datetime_str(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
    """ Return a fields.Datetime value with the given timezone. """
    dt = datetime(year, month, day, hour, minute, second, microsecond)
    if tzinfo:
        dt = timezone(tzinfo).localize(dt).astimezone(utc)
    return fields.Datetime.to_string(dt)


class TestPublicHolidatFrance(TestPublicHolidatFranceCommon):
    def setUp(self):
        super(TestPublicHolidatFrance, self).setUp()

    def test_public_holiday_france(self):

        self.calendar_public_holiday_wizard = self.env['wizard.public_holiday.fr'].create({
            'res_id': self.calendar.id,
            'res_model': 'resource.calendar',
        })

        self.calendar_public_holiday_wizard.generate()

        current_year = datetime.now().year

        leaves_this_year = self.env['resource.calendar.leaves'].search([
            ('resource_id', '=', False),
            ('calendar_id', '=', self.calendar.id),
            ('date_from', '>=', datetime_str(current_year, 1, 1, 0, 0, 0, tzinfo=self.calendar.tz)),
            ('date_to', '<=', datetime_str(current_year, 12, 31, 23, 59, 59, tzinfo=self.calendar.tz)),
        ])

        self.assertEqual(len(leaves_this_year), 11)

        leaves_new_year = self.env['resource.calendar.leaves'].search([
            ('resource_id', '=', False),
            ('calendar_id', '=', self.calendar.id),
            ('date_from', '=', datetime_str(current_year, 1, 1, 0, 0, 0, tzinfo=self.calendar.tz)),
            ('date_to', '=', datetime_str(current_year, 1, 1, 23, 59, 59, tzinfo=self.calendar.tz)),
        ])

        self.assertEqual(leaves_new_year.name, "1er janvier")