# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class TravelSchedule(models.Model):
	_name = 'travel.schedule'

	departure = fields.Many2one('travel.pool.city', required=True)
	destination = fields.Many2one('travel.pool.city', required=True)
	departure_date = fields.Date('Departure Date',required=True)
	# departure_time = fields.Float('Departure Time',required=True)
	vehicle = fields.Many2one('fleet.vehicle', required=True)
	order_list = fields.One2many('travel.order', 'schedule_id')
	pool_list_dep = fields.One2many('travel.pool.line', 'schedule')
	pool_list_dest = fields.One2many('travel.pool.line', 'schedule')
	price = fields.Float('Price', required=True)
	name = fields.Char(string='Schedule Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New Schedule'))

	@api.model
	def create(self, vals):
		if vals.get('name', _('New Schedule')) == _('New Schedule'):
			vals['name'] = self.env['ir.sequence'].next_by_code('travel.schedule') or _('New Schedule')
			result = super(TravelSchedule, self).create(vals)

		return result

	def get_max_seats(self):
		return self.vehicle.seats;

class PoolLine(models.Model):
	_name = 'travel.pool.line'
	schedule = fields.Many2one('travel.schedule', string="Schedule",ondelete='cascade')
	pool_location = fields.Many2one('travel.pool.place')
	name = fields.Char(compute="_compute_pool_name", store=False)
	departure_perpool = fields.Float('Departure Time')

	@api.multi
	def _compute_pool_name(self):
		for record in self:
			record.name = record.pool_location.city_ids.city + '/' + record.pool_location.address

	def get_schedule(self):
		return self.schedule

#class Vehicle(models.Model):
#	_inherit = 'fleet.vehicle'

#	schedule_id = fields.Many2one('travel.schedule')
