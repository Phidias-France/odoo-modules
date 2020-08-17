"""
Calcul des 11 jours de fêtes légales en France d'une année donnée (aaaa)

@author: hbouia (Created on Sat Mar 21 2015)
@author: ddeyris (pudated on Sat June 6 2020)
"""
import pytz
import requests
import json

from odoo import api, fields, models
from datetime import datetime, time

API_CALENDRIER_GOUV_FR = 'https://calendrier.api.gouv.fr/jours-feries/%s.json'


class PublicHolidayFrWizard(models.TransientModel):
    _name = "wizard.public_holiday.fr"
    _description = "Generate public holiday"

    @api.model
    def default_get(self, fields):
        res = super(PublicHolidayFrWizard, self).default_get(fields)
        res_id = self._context.get('active_id')
        res_model = self._context.get('active_model')
        res.update({'res_id': res_id, 'res_model': res_model})
        return res

    res_model = fields.Char('Related Document Model', required=True)
    res_id = fields.Integer('Related Document ID', required=True)
    zone = fields.Selection([
        ('alsace-moselle', 'Alsace/Moselle'),
        ('guadeloupe', 'Guadeloupe'),
        ('guyane', 'Guyane'),
        ('la-reunion', u'La Réunion'),
        ('martinique', 'Martinique'),
        ('mayotte', 'Mayotte'),
        ('metropole', u'Métropole'),
        ('nouvelle-caledonie', u'Nouvelle Caledonie'),
        ('polynesie-francaise', u'Polynesie Française'),
        ('saint-barthelemy', u'Saint Barthélemy'),
        ('saint-martin', 'Saint Martin'),
        ('saint-pierre-et-miquelon', 'Saint-Pierre et Miquelon'),
        ('wallis-et-futuna', 'Wallis et Futuna'),
    ] , string="Zone", default="metropole", required=True)

    def generate(self):
        calendar_tz = self.env['resource.calendar'].browse(self.res_id).tz
        calendar_local = pytz.timezone(calendar_tz)

        dates = self.get_days_from_api_gov()
        current_year = datetime.now().year

        for (date, name) in dates.items():
            date_local = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=calendar_local)
            if current_year <= date_local.year:
                date_start = calendar_local.localize(datetime.combine(date_local, time.min), is_dst=None).astimezone(
                    pytz.utc)
                date_end = calendar_local.localize(datetime.combine(date_local, time.max), is_dst=None).astimezone(
                    pytz.utc)
                day_public_holiday = self.env['resource.calendar.leaves'].search([
                    ('calendar_id', '=', self.res_id),
                    ('date_from', '=', datetime.strftime(date_start, "%Y-%m-%d %H:%M:%S")),
                    ('date_to', '=', datetime.strftime(date_end, "%Y-%m-%d %H:%M:%S"))
                ])
                if not day_public_holiday:
                    self.env['resource.calendar.leaves'].create({
                        'name': name,
                        'calendar_id': self.res_id,
                        'resource_id': False,
                        'date_from': datetime.strftime(date_start, "%Y-%m-%d %H:%M:%S"),
                        'date_to': datetime.strftime(date_end, "%Y-%m-%d %H:%M:%S"),
                    })

    def get_days_from_api_gov(self):
        url = API_CALENDRIER_GOUV_FR % self.zone
        r = requests.get(url)
        dates = json.loads(r.text)
        return dates
