from ._anvil_designer import Egyszerusitett_kozosTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Egyszerusitett_kozos(Egyszerusitett_kozosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
  def panel1_visable(self):
    if self.faj.selected_value != "Faj" and self.kaszt.selected_value != "Kaszt":
      self.column_panel_3.visible = True
    else:
      self.column_panel_3.visible = False
  def faj_change(self, **event_args):
    self.panel1_visable()
    if self.faj.selected_value != "Faj":
      self.kaszt.enabled = True
    else:
      self.kaszt.enabled = False
      self.kaszt.selected_value = "Kaszt"

  def kaszt_change(self, **event_args):
   self.panel1_visable()
    
