# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import random
from datetime import timedelta, datetime

class player(models.Model):
    _name = 'ernon2.player'
    _description = 'Jugadores'

    name = fields.Char(required = True)
    tipo = fields.Many2one('ernon2.tipoplayer')
    subtipo = fields.Many2one('ernon2.subtipo')
    danyo = fields.Integer(default = 0)
    puntos = fields.Integer(default = 0)
    objetos = fields.One2many('ernon2.objetos', 'objetos_player')
    terrenoActual = fields.Many2one('ernon2.terrenos')
    lista_objeto = fields.Many2many('ernon2.objetos', compute='lista_objetos')
    
    @api.onchange('tipo')
    def onchange_tipoClase(self):
        print(self.tipo.subtipo.ids)
        return {
            'domain': {
                'subtipo': [('id', 'in', self.tipo.subtipo.ids)],
            }
        }
    
    @api.depends('puntos')
    def lista_objetos(self):
        for c in self:
            c.lista_objeto = self.env['ernon2.objetos'].search([( "puntos", "<=", c.puntos )])
            
    
    @api.depends('danyo')
    def compute_danyo(self):
        for player in self:
            player.danyo = player.danyo
         
    def boton_terreno(self):
        for b in self:  
            listaTerrenos = self.env['ernon2.terrenos'].search([])
            b.terrenoActual = random.choice(listaTerrenos)
           
    def boton_aceptar_terreno(self):
        for b in self:
            b.danyo = b.danyo + b.terrenoActual.danyo
            
          
           
    @api.model
    def produce(self):  # ORM CRON
        self.search([]).produce_puntos()

    def produce_puntos(self):
        for player in self:
            puntos = player.puntos + 5

            player.write({
                "puntos": puntos
            })

    @api.constrains('name')
    def check_name(self):
        for b in self:
            if b.name == " ":
                raise ValidationError("No hay nombre")
  
  
class tipoPlayer (models.Model):
    _name = 'ernon2.tipoplayer'
    _description = 'Tipo de player'
    
    name = fields.Char( string ="tipo")
    descripcion = fields.Text()
    imagen = fields.Image(max_width = 500, max_height = 500)
    hogar = fields.Many2one('ernon2.terrenos')
    subtipo = fields.One2many('ernon2.subtipo', 'tipo_player')
   
    

class subtipo (models.Model):
    _name = 'ernon2.subtipo'
    _description = 'Subtipos'
    
    name = fields.Char( string ="tipo")
    descripcion = fields.Text()
    grupo = fields.Char (string = "tipo")
    imagen = fields.Image(max_width = 800, max_height = 800)
    tipo_player = fields.Many2one('ernon2.tipoplayer')
    
    
class angeles (models.Model):
    _name = 'ernon2.angeles'
    _description = 'Ángeles'
    
    description = fields.Text()
    avatar = fields.Image(max_width = 300, max_height = 300)
    tipoAngeles = fields.Selection([('1', "Serafines"), ('2',"Potestades"), ('3', "Principados")]) 
   
   
class demonios (models.Model):
    _name = 'ernon2.demonios'
    _description = 'Demonios'
    
    description = fields.Text()
    avatar = fields.Image(max_width = 300, max_height = 300)
    tipoAngeles = fields.Selection([('1', "Serafines"), ('2',"Potestades"), ('3', "Principados")]) 
    
    
class angelescaidos (models.Model):
    _name = 'ernon2.angelescaidos'
    _description = 'Ángeles caídos'
    
    description = fields.Text()
    avatar = fields.Image(max_width = 300, max_height = 300)
    tipoAngeles = fields.Selection([('1', "Serafines"), ('2',"Potestades"), ('3', "Principados")])   
        
        
class terrenos (models.Model):
    _name = 'ernon2.terrenos'
    _description = 'Terrenos'
    
    name = fields.Char()
    beneficio = fields.Char()
    danyo = fields.Integer()
    imagen = fields.Image(max_width = 500, max_height = 500)
    playerTerreno = fields.One2many('ernon2.player','terrenoActual', ondelete = "cascade")
    
            
class objetos (models.Model):
    _name = 'ernon2.objetos'
    _description = 'Objetos'
    
    name = fields.Char()
    descripcion = fields.Char()
    danyo = fields.Integer()
    puntos = fields.Integer()
    imagen = fields.Image(max_width = 500, max_height = 500)
    objetos_player = fields.Many2one('ernon2.player', ondelete = "set null")
 
    def boton_comprar_objetos(self):
        for c in self:  
           player = self.env['ernon2.player'].browse(self.env.context['ctx_player'])[0]
           player.danyo += c.danyo
           player.puntos -= c.puntos 
               
class battle(models.Model):
    _name = 'ernon2.battle'
    _description = 'Batallas'

    name = fields.Char()
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now)
    date_end = fields.Datetime(compute = 'tiempo_espera')  
    time = fields.Float(compute='tiempo_espera')
    progress = fields.Float()
    player1 = fields.Many2one('ernon2.player')
    player2 = fields.Many2one('ernon2.player')
    terreno1 = fields.Many2one('ernon2.player')
    terreno2 = fields.Many2one('ernon2.player')
    winner = fields.Many2one()
    draft = fields.Boolean()   
   
    @api.onchange('player1')
    def onchange_eleccion_player1(self):
        self.name = self.player1.name
        return {
            'domain': {
            'player2': [('id', '!=', self.player1.id)],
            }
        }
   
    @api.onchange('player2')
    def onchange_player2(self):
        return {
            'domain': {
            'player1': [('id', '!=', self.player2.id)],
            }
        }

    @api.depends('terreno1', 'terreno2')
    def tiempo_espera(self):
        for b in self:
            b.date_end = fields.Datetime.now()
            
            if (b.player1.terrenoActual != b.player2.terrenoActual):
                b.time += 5 
                
                b.date_end = fields.Datetime.to_string(
                fields.Datetime.from_string(b.date_start) + timedelta(days=b.time))
                
                print(b.terreno2.terrenoActual)
                
    
