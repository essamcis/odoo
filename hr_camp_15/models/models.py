# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError



class camp_details(models.Model):
    _name='camp.details'
    _description = "Camp Details" 
    
    address = fields.Char('Address',size=64)
    campboss = fields.Many2one('hr.employee','Camp Boss')
    campcode = fields.Char('Camp Code',size=64)
    emp_id = fields.Many2one('hr.employee','Name')
    job = fields.Many2one('hr.job','Job')
    name = fields.Char('Name',size=64)
    noofrooms = fields.Integer(string='Total No. of Beds')
    note = fields.Char('Note',size=64)
    totaloccupants = fields.Integer('Total No. of Occupants')
    totalroomoccupancy = fields.Integer('Total Room Occupancy')
    totalrooms = fields.Integer('Total Rooms')
    rooms = fields.One2many('camp.details.rooms','campcode_id','Room Information')     
    

          
         

class camp_details_rooms(models.Model):
    _name='camp.details.rooms'
    _description = "camp.details.rooms" 
 
    campcode_id = fields.Many2one('camp.details','Camp Code')
    name = fields.Char('Room No',size=64)
    note = fields.Text('Note')
    roomcapacity = fields.Integer('Room Capacity')
    roomoccupancy = fields.Integer('Room Occupancy')
    employee_room = fields.One2many('hr.employee','room_ids','Employee Room Information')
    
    def name_get(self):
        res = super(camp_details_rooms, self).name_get()
        for rom in self:
            if rom and rom.name and rom.roomcapacity :
                if rom.roomoccupancy < rom.roomcapacity:
                    sname = rom.name  +' AVALB: ' + str(rom.roomcapacity - rom.roomoccupancy) 
                    res.append((rom.id,sname))
                else :
                    sname = rom.name  + '  FULL'
                    res.append((rom.id,sname))

        return res


            
   


class camp_transfer(models.Model):
    _name='camp.transfer'
    _description = 'Camp Transfer'

    tran_code = fields.Char('Employee Code', size=64)
    emp_name = fields.Many2one('hr.employee','Employee Name')
    camp_no = fields.Many2one('camp.details','Transfer To Camp')
    emp_job = fields.Many2one('hr.job','Job',readonly=True)
    trn_room = fields.Many2one('camp.details.rooms',string='Transfer To Room' ,
    domain="[('campcode_id','!=', False),('campcode_id','=',camp_no)]")
    

    gender =  fields.Selection([('male', 'Male'),('female', 'Female')], 'Gender',readonly=True)
    camp_cur =  fields.Many2one('camp.details','Current Camp')
    cur_room =  fields.Many2one('camp.details.rooms','Current Room')
    #emp_religion = fields.Related('emp_name', 'emp_religion', type='Char', string='Religion',readonly=True)

    @api.onchange('emp_name')
    def _onchange_emp_name(self):
        self.camp_cur = self.emp_name.camp_ids
        self.cur_room = self.emp_name.room_ids
    
    @api.onchange('camp_cur')
    def _onchange_camp_cur(self):
        self.camp_cur = self.emp_name.camp_ids
        self.cur_room = self.emp_name.room_ids

    @api.onchange('cur_room')
    def _onchange_cur_room(self):
        self.camp_cur = self.emp_name.camp_ids
        self.cur_room = self.emp_name.room_ids

    #@api.onchange('trn_room')
    #def _onchange_trn_room(self):
    #    return {'domain':{'trn_room': [('campcode_id','!=',False),('campcode_id','=',self.camp_no),('roomcapacity','!=',self.trn_room.roomoccupancy)]}}

        

 
class camp_hr(models.Model):
    _inherit = ['hr.employee']
    camp_ids = fields.Many2one('camp.details', string='Related Camp')
    room_ids = fields.Many2one('camp.details.rooms', string='Camp Room No.',domain="[('campcode_id','=','camp_ids')]")

