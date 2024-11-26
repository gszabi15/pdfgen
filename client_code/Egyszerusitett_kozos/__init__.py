from ._anvil_designer import Egyszerusitett_kozosTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Egyszerusitett_kozos(Egyszerusitett_kozosTemplate):

  def __init__(self, **properties):
    self.karakteralkotas = "egyszerusitett_kozos"
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.elonyelosztva = 0
    # Any code you write here will run before the form opens.
    self.faj.items = anvil.server.call('get_fajnev')
    self.pont = anvil.server.call("pontok",self.karakteralkotas,{"edzett":int(self.elony_edzett.text)}) #anvil.server.call("pontok","egyszerusitett_kozos",None)
    self.enabled = anvil.server.call("get_enabled")
    if "UT" in self.enabled:
      self.eszleles_column.visible = True
    else:
      self.eszleles_column.visible = False
      self.eszleles = 0
    self.szazalek_change()
    self.elonynum = anvil.server.call("egyszerusitett_kozos","get_elony",{"szint":self.szint.text})
    self.kp_change()
  def up10(self,inp):
    if inp > 10:
      return inp-10
    else:
      return 0
  def kp_change(self):
    self.kp = anvil.server.call("getkp",self.karakteralkotas,{"faj":self.faj.selected_value,"kaszt":self.kaszt.selected_value,"szint":int(self.szint.text),"kepzes":int(self.elony_kepzes.text)})
    self.szabad_kp_label.text = "Szabad KP: " + str(self.kp)
    self.tudomanyos_kp_label.text = "(Csak) Tudományos KP: "+str(self.up10(self.intelligencia.text))
    self.nem_tudomanyos_kp_label.text = "(Csak) Nem tudományos KP: "+str(self.up10(self.ugyesseg.text))
    self.tkp = self.up10(self.intelligencia.text)
    self.ntkp = self.up10(self.ugyesseg.text)
    
    """{
  "alap": 10,
  "szintenkent": 4
}"""
  def szazalek_change(self,**event_args):
    alap = self.ugyesseg.text
    val = {"titkosajto_kereses":self.titkosajto_kereses,"ugras":self.ugras,"eses":self.eses,"maszas":self.maszas,"zsebmetszes":self.zsebmetszes,"zarnyitas":self.zarnyitas,"rejtozes":self.rejtozes,"koteltanc":self.koteltanc,"lopozas":self.lopozas,"csapdafelfedezes":self.csapdafelfedezes}
    for i in list(val.keys()):
      val[i].text = self.up10(alap) 
  def pontok_change(self, **event_args):
    self.szazalek_change()
    self.kp_change()
    if "pont" in self.pont:
      rempont = self.pont["pont"]
      text = ""
      val = {"ero":self.ero,"gyorsasag":self.gyorsasag,"ugyesseg":self.ugyesseg,"allokepesseg":self.allokepesseg,"egeszseg":self.egeszseg,"szépség":self.szepseg,"intelligencia":self.intelligencia,"akaratero":self.akaratero,"asztral":self.asztral,"eszleles":self.eszleles}
      if "szabad" in self.pont and self.pont["szabad"] in val:
        if val[self.pont["szabad"]].text is not None:
           text = "+ "+self.pont["szabad"] + " ("+str(val[self.pont["szabad"]].text)+")"
        for i in list(val.keys()):
          if i != self.pont["szabad"]:
            if type(val[i].text) is int:
              rempont -= val[i].text
      else:
        for i in list(val.keys()):
          rempont -= val[i].text
      self.pontok.text = str(rempont) + " pont " + text
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
   self.kp_change()
  def uipenz(self):
    self.penz.content = "kezdő arany: " + str(anvil.server.call('penz',self.karakteralkotas,{"szint":int(self.szint.text), "profi":int(self.elony_profi.text)}))+"AP"
  def szint_change(self, **event_args):
    if type(self.szint.text) is int:
      old = self.elonynum
      self.elonynum = anvil.server.call("egyszerusitett_kozos","get_elony",{"szint":int(self.szint.text)})
      self.elony_label.text = "Előnyök: "+ str(self.elonynum - self.elonyelosztva)
      if old > self.elonynum or self.elonynum <= 0:
        self.reset_elonyok()
      if self.elonynum > 0:
        self.elonyok_panel.visible = True
      else:
        self.elonyok_panel.visible = False
      self.uipenz()
      self.kp_change()
      
  def elony_bool(self,b,res):
    if res:
      self.elony_hires_add.visible = True
      self.elony_hires_del.visable = False
  def reset_elonyok(self):
    self.elony_profi.text = 0
    self.elony_profi_del.enabled = False
    self.elony_profi_add.enabled = True
    self.elony_kepzes.text = 0
    self.elony_kepzes_del.enabled = False
    self.elony_kepzes_add.enabled = True
    self.elony_edzett.text = 0
    self.elony_edzett_del.enabled = False
    self.elony_edzett_add.enabled = True
    self.elony_idos.text = 0
    self.elony_idos_del.enabled = False
    self.elony_idos_add.enabled = True
    self.elony_kivul_tagasabb.text = 0
    self.elony_kivul_tagasabb_del.enabled = False
    self.elony_kivul_tagasabb_add.enabled = True
    self.elonyelosztva = 0
  def del_elony_button(self,obj,add,delete):
    if int(obj.text) > 0:
      self.elonyelosztva -= 1
      self.elony_label.text = "Előnyök: "+ str(self.elonynum - self.elonyelosztva)
      obj.text = int(obj.text) - 1
      if obj.text == "0":
        delete.enabled = False
    if self.elonynum - self.elonyelosztva > 0:
      add.enabled = True
  def add_elony_button(self,obj,add,delete):
    if self.elonynum > 0 and (self.elonynum - self.elonyelosztva) > 0:
      self.elonyelosztva += 1
      self.elony_label.text = "Előnyök: "+ str(self.elonynum - self.elonyelosztva)
      obj.text = int(obj.text) + 1
      delete.enabled = True
      
      if self.elonynum - self.elonyelosztva == 0:
        add.enabled = False

  
  def elony_profi_add_click(self, **event_args):
    obj = self.elony_profi
    add = self.elony_profi_add
    delete = self.elony_profi_del
    self.add_elony_button(obj,add,delete)
    anvil.server.call("egyszerusitett_kozos","elony",{"profi":int(obj.text)})
    self.uipenz()
  def elony_profi_del_click(self, **event_args):
    obj = self.elony_profi
    add = self.elony_profi_add
    delete = self.elony_profi_del
    self.del_elony_button(obj,add,delete)
    self.uipenz()
    
  def elony_kepzes_add_click(self, **event_args):
    obj = self.elony_kepzes
    add = self.elony_kepzes_add
    delete = self.elony_kepzes_del
    self.add_elony_button(obj,add,delete)
    self.kp_change()
    
  def elony_kepzes_del_click(self, **event_args):
    obj = self.elony_kepzes
    add = self.elony_kepzes_add
    delete = self.elony_kepzes_del
    self.del_elony_button(obj,add,delete)
    self.kp_change()


  def elony_edzett_add_click(self, **event_args):
    obj = self.elony_edzett
    add = self.elony_edzett_add
    delete = self.elony_edzett_del
    self.add_elony_button(obj,add,delete)
    self.pont = anvil.server.call("pontok",self.karakteralkotas,{"edzett":int(obj.text)})
    self.pontok_change()
  def elony_edzett_del_click(self, **event_args):
    obj = self.elony_edzett
    add = self.elony_edzett_add
    delete = self.elony_edzett_del
    self.del_elony_button(obj,add,delete)
    self.pont = anvil.server.call("pontok",self.karakteralkotas,{"edzett":int(obj.text)})
    self.pontok_change()

  def link_1_click(self, **event_args):
    self.elony_profi_info.visible = not self.elony_profi_info.visible

  def elony_meregellenallas_link_click(self, **event_args):
    self.elony_meregellenallas_info.visible = not self.elony_meregellenallas_info.visible

  def elony_change_button(self,add,delete):
    add.visible = not add.visible
    delete.visible = not delete.visible
  
  def elony_hires_add_click(self, **event_args):
    add = self.elony_hires_add
    delete = self.elony_hires_del
    self.elony_change_button(add,delete)

  def elony_hires_del_click(self, **event_args):
    add = self.elony_hires_add
    delete = self.elony_hires_del
    self.elony_change_button(add,delete)

      


