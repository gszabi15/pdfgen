from ._anvil_designer import Egyszerusitett_kozosTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.http
import json



class Egyszerusitett_kozos(Egyszerusitett_kozosTemplate):
  def call_server_function(self, func_name, params):
    url = "https://szabyte.hu/api"
    response = anvil.http.request(
          url,
          method="POST",
          data={"function": func_name, "params": params},
          json=True
    )
    return response
  def __init__(self, **properties):
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.faj.items = anvil.server.call('get_fajnev')
    
    self.pont = call_server_function("pontok",("egyszerusitett_kozos",None)) #anvil.server.call("pontok","egyszerusitett_kozos",None)
    self.enabled = anvil.server.call("get_enabled")
    if "UT" in self.enabled:
      self.eszleles_column.visible = True
    else:
      self.eszleles_column.visible = False
      self.eszleles = 0
    self.szazalek_change()
    self.elonynum = anvil.server.call("egyszerusitett_kozos","get_elony",{"szint":self.szint.text})
  def up10(self,inp):
    if inp > 10:
      return inp-10
    else:
      return 0
  def szazalek_change(self,**event_args):
    alap = self.ugyesseg.text
    val = {"titkosajto_kereses":self.titkosajto_kereses,"ugras":self.ugras,"eses":self.eses,"maszas":self.maszas,"zsebmetszes":self.zsebmetszes,"zarnyitas":self.zarnyitas,"rejtozes":self.rejtozes,"koteltanc":self.koteltanc,"lopozas":self.lopozas,"csapdafelfedezes":self.csapdafelfedezes}
    for i in list(val.keys()):
      val[i].text = self.up10(alap) 
  def pontok_change(self, **event_args):
    self.szazalek_change()
    if "pont" in self.pont:
      rempont = self.pont["pont"]
      text = ""
      val = {"ero":self.ero,"gyorsasag":self.gyorsasag,"ugyesseg":self.ugyesseg,"allokepesseg":self.allokepesseg,"egeszseg":self.egeszseg,"szepseg":self.szepseg,"intelligencia":self.intelligencia,"akaratero":self.akaratero,"asztral":self.asztral,"eszleles":self.eszleles}
      if "szabad" in self.pont:
        for i in val:
          pass
        if self.pont["szabad"] in val:
          if val[self.pont["szabad"]].text is not None:
            text = "+ "+self.pont["szabad"] + "("+str(val[self.pont["szabad"]].text)+")"
          for i in list(val.keys()):
            if i != self.pont["szabad"]:
              if type(val[i].text) is int:
                rempont -= val[i].text
      else:
        for i in list(val.keys()):
          rempont -= val[i].text
      self.pontok.text = str(rempont) + " " + text
  def panel1_visable(self):
    if self.faj.selected_value is not None and self.kaszt.selected_value is not None:
      self.column_panel_3.visible = True
    else:
      self.column_panel_3.visible = False
  def faj_change(self, **event_args):
    self.panel1_visable()
    if self.faj.selected_value is not None:
      self.korkat = anvil.server.call('get_korkat', self.faj.selected_value)
      self.kor.text = self.korkat[0]["2"][0]
      self.korkategoria()
      self.korkat_panel.visible = True
      self.kaszt.enabled = True
      self.kaszt.items = anvil.server.call('get_kasztnev', self.faj.selected_value)
    else:
      self.kaszt.enabled = False
      self.korkat_panel.visible = False
      self.kaszt.selected_value = None
  def korkategoria(self, **event_args):
    val = 0
    for i in self.korkat:
      for y in i:
        print(i[y])
        if type(i[y][0]) is int and i[y][0]  <= int(self.kor.text) and (i[y][1] == "-" or ((int(self.kor.text) <= i[y][1]) if type(i[y][1]) is int else False)):
          mod = anvil.server.call("get_korkatmod",int(y)-1)
          self.korkat_label.text = mod['szam'] + " " + "Korkategória " + "(" + mod['Nev'] + ") " + str(i[y][0]) + "-" + (str(i[y][1]) if type(i[y][1]) is int else " ") + " év"
          self.korkat_ero.text = mod["mod"]["ero"]
          self.korkat_gyorsasag.text = mod["mod"]["gyorsasag"]
          self.korkat_ugyesseg.text = mod["mod"]["ugyesseg"]
          self.korkat_allokepesseg.text = mod["mod"]["allokepessg"]
          self.korkat_egeszseg.text = mod["mod"]["egeszseg"]
          self.korkat_szepseg.text = mod["mod"]["szepseg"]
          return int(y)
  def kaszt_change(self, **event_args):
   self.panel1_visable()

  def szint_change(self, **event_args):
    if type(self.szint.text) is int:
      self.elonynum = anvil.server.call("egyszerusitett_kozos","get_elony",{"szint":int(self.szint.text)})
      self.elony_label.text = "Előnyök: "+ str(self.elonynum)
      self.penz.content = "kezdő arany: " + str(anvil.server.call('penz',"egyszerusitett_kozos",{"szint":int(self.szint.text)}))+"AP"

  def elony_profi_add_click(self, **event_args):
    if self.elonynum != 0:
      self.elonynum -= 1
      self.elony_label.text = "Előnyök: "+ str(self.elonynum)
      self.elony_profi.text = int(self.elony_profi.text) + 1
      self.elony_profi_del.enabled = True
      if self.elonynum == 0:
        self.elony_profi_add.enabled = False
  def elony_profi_del_click(self, **event_args):
    if int(self.elony_profi.text) > 0:
      self.elonynum += 1
      self.elony_label.text = "Előnyök: "+ str(self.elonynum)
      self.elony_profi.text = int(self.elony_profi.text) - 1
      if self.elony_profi.text == "0":
        self.elony_profi_del.enabled = False
    if self.elonynum != 0:
      self.elony_profi_add.enabled = True
 
  def elony_profi_change(self, **event_args):
    self.pontok_change()

      


