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
    self.faj.items = anvil.server.call('get_fajnev')
    self.kaszt.items = anvil.server.call('get_kasztnev')
    self.pont = anvil.server.call("pontok","egyszerusitett_kozos",None)
  def pontok_change(self, **event_args):
    if "pont" in self.pont:
      rempont = self.pont["pont"]
      text = ""
      val = {"ero":self.ero,"gyorsasag":self.gyorsasag,"ugyesseg":self.ugyesseg,"allokepesseg":self.allokepesseg,"egeszseg":self.egeszseg,"szepseg":self.szepseg,"intelligencia":self.intelligencia,"akaratero":self.akaratero,"asztral":self.asztral,"eszleles":self.eszleles}
      if "szabad" in self.pont:
        for i in val:
          pass
        if self.szabad in val:
          text = "+ "+self.pont["szabad"] + "("+str(val[self.pont["szabad"]].text)+")"
          for i in list(val.keys()):
            if i != self.szabad:
              rempont -= val[i].text
      else:
        for i in list(val.keys()):
          rempont -= val[i].text
      self.pontok.text = rempont + " " + text
  def panel1_visable(self):
    if self.faj.selected_value != None and self.kaszt.selected_value != None:
      self.column_panel_3.visible = True
    else:
      self.column_panel_3.visible = False
  def faj_change(self, **event_args):
    self.panel1_visable()
    if self.faj.selected_value != None:
      self.kaszt.enabled = True
    else:
      self.kaszt.enabled = False
      self.kaszt.selected_value = None

  def kaszt_change(self, **event_args):
   self.panel1_visable()

  def szint_change(self, **event_args):
    if type(self.szint.text) is int:
      self.penz.content = "kezdő arany: " + str(anvil.server.call('penz',"egyszerusitett_kozos",{"szint":int(self.szint.text)}))+"AP"


