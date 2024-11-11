from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
  #def click(self, **properties):
  #  self.outlined_button_1.visible = 0
  def __init__(self, **properties):
    #self.column_panel_1.width = "700px"
    #self.column_panel_4.width = "950px"
    #self.harcertekek.width = "1550px"
    #self.varazstargyak.items = [{'varazstargyak': '', 'hatas': '','mp':'','db':''}]
    self.init_components(**properties)
    #self.outlined_button_1.add_event_handler('click',self.click)
    # Any code you write here will run before the form opens.
    self.repeating_panel_2.items = {'varazstargyak_1':'','varazstargyak_2':'','varazstargyak_3':'','varazstargyak_4':'','varazstargyak_5':''}
    #self.repeating_panel.items = {'ke':'','te':'','ve':'','ce':''}
    self.fegyver_1.items = ['']*3
    self.fegyver_2.items = ['']
    self.fegyver_3.items = ['']
    self.lathato_felszereles.items = ['']*1 #15
    self.nem_lathato_felszereles.items = ['']*1 #15
    self.kepzettsegek_1.items = ['']*1 #21
    self.kepzettsegek_2.items = ['']*1 #21
    self.mergek.items = ['']*4
    self.rendezvenyek.items = ['']*1 #6
    #self.fegyver_sebzes_1.items = {'tam':'','sebzes':''}
    #self.fegyver_pajzs_1.items = {'pajzs':''}