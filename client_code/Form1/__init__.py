from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
  #def click(self, **properties):
  #  self.outlined_button_1.visible = 0
  def __init__(self, **properties):
    self.column_panel_1.width = "1110px"
    self.column_panel_4.width = "500px"
    #self.varazstargyak.items = [{'varazstargyak': '', 'hatas': '','mp':'','db':''}]
    self.init_components(**properties)
    #self.outlined_button_1.add_event_handler('click',self.click)
    # Any code you write here will run before the form opens.
    self.repeating_panel_2.items = {'varazstargyak_1':'','varazstargyak_2':'','varazstargyak_3':'','varazstargyak_4':'','varazstargyak_5':''}
    self.repeating_panel.items = {'ke_1':'','te_1':'','ve_1':'','ce_1':''}