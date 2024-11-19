from ._anvil_designer import BeallitasokTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Beallitasok(BeallitasokTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def faj_szerkesztes_click(self, **event_args):
    open_form('faj', my_parameter=self.faj_dropdown.text)
