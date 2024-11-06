from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
  #def click(self, **properties):
  #  self.outlined_button_1.visible = 0
  def __init__(self, **properties):
    self.column_panel_1.width = "700px"
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.outlined_button_1.add_event_handler('click',self.click)
    # Any code you write here will run before the form opens.

