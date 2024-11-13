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
    self.varazstargyak.items = {'varazstargyak_1':'','varazstargyak_2':'','varazstargyak_3':'','varazstargyak_4':'','varazstargyak_5':''}
    #self.column_panel_9.width = 680+470+15
    #self.repeating_panel.items = {'ke':'','te':'','ve':'','ce':''}
    self.fegyver_1.items = ['']*3
    self.fegyver_2.items = ['']
    self.fegyver_3.items = ['']
    self.elony.items = ['']*1 #5
    self.hatrany.items = ['']*1 #5
    self.lathato_felszereles.items = [{'felszereles':''}] #15
    self.nem_lathato_felszereles.items = ['']*1 #15
    self.kepzettsegek_1.items = ['']*1 #21
    self.kepzettsegek_2.items = ['']*1 #21
    self.mergek.items = ['']*4
    self.rendezvenyek.items = ['']*1 #6
    self.zsakmany.items = ['']*1 #7
    #self.fegyver_sebzes_1.items = {'tam':'','sebzes':''}
    #self.fegyver_pajzs_1.items = {'pajzs':''}
  def getrow(self,panel):
    current_data = []
    for row in panel.get_components():
        row_data = []
        for component in row.get_components():
            if hasattr(component, 'checked'):  # Pl.: CheckBox esetén
                row_data.append(component.checked)
            elif hasattr(component, 'text') and not hasattr(component, 'checked'):
                row_data.append(component.text)
            elif hasattr(component, 'value'):  # Egyéb komponens esetén
                row_data.append(component.value)
        current_data.append(row_data)
    return current_data
  def addrow(self,panel):
    panel_data = self.getrow(panel)
    if panel_data and panel_data[0]:
        empty_row = ['' if isinstance(value, str) else False for value in panel_data[0]]
    else:
        empty_row = [] 
    panel_data.append(empty_row)
    panel.items = panel_data
    for i, row in enumerate(panel.get_components()):
        for j, component in enumerate(row.get_components()):
            if j < len(panel_data[i]):
                if hasattr(component, 'text') and not hasattr(component, 'checked'):
                    component.text = panel_data[i][j]
                elif hasattr(component, 'checked'):
                    component.checked = panel_data[i][j]
                elif hasattr(component, 'value'):
                    component.value = panel_data[i][j]
  def delrow(self,panel,index=-1):
    panel_data = self.getrow(panel)
    if not panel_data:
        return
    panel_data.pop(index)
    panel.items = panel_data
    for i, row in enumerate(panel.get_components()):
        for j, component in enumerate(row.get_components()):
            if j < len(panel_data[i]):
                if hasattr(component, 'text') and not hasattr(component, 'checked'):
                    component.text = panel_data[i][j]
                elif hasattr(component, 'checked'):
                    component.checked = panel_data[i][j]
                elif hasattr(component, 'value'):
                    component.value = panel_data[i][j]
                
                  
  def lathato_felszereles_add_click(self, **event_args):
    self.addrow(self.lathato_felszereles)
    if len(self.lathato_felszereles.items) > 1:
      self.lathato_felszereles_del.enabled = True
    if len(self.lathato_felszereles.items) == 15:
      self.lathato_felszereles_add.enabled = False
    
  def lathato_felszereles_del_click(self, **event_args):
    self.delrow(self.lathato_felszereles)
    if len(self.lathato_felszereles.items) == 1:
      self.lathato_felszereles_del.enabled = False
    if len(self.lathato_felszereles.items) < 15:
      self.lathato_felszereles_add.enabled = True

  def felszereles_add_click(self, **event_args):
    self.addrow(self.nem_lathato_felszereles)
    if len(self.nem_lathato_felszereles.items) > 1:
      self.nem_lathato_felszereles_del.enabled = True
    if len(self.nem_lathato_felszereles.items) == 15:
      self.nem_lathato_felszereles_add.enabled = False

  def felszereles_del_click(self, **event_args):
    self.delrow(self.nem_lathato_felszereles)
    if len(self.nem_lathato_felszereles.items) == 1:
      self.nem_lathato_felszereles_del.enabled = False
    if len(self.nem_lathato_felszereles.items) < 15:
      self.nem_lathato_felszereles_add.enabled = True

  def kepzettseg1_add_click(self, **event_args):
    rep = self.kepzettsegek_1
    add = self.kepzettseg1_add
    delete = self.kepzettseg1_del
    self.addrow(rep)
    if len(rep.items) > 1:
      delete.enabled = True
    if len(rep.items) == 21:
      add.enabled = False

  def kepzettseg1_del_click(self, **event_args):
    rep = self.kepzettsegek_1
    add = self.kepzettseg1_add
    delete = self.kepzettseg1_del
    self.delrow(rep)
    if len(rep.items) == 1:
      delete.enabled = False
    if len(rep.items) < 21:
      add.enabled = True

  def kepzettseg2_add_click(self, **event_args):
    rep = self.kepzettsegek_2
    add = self.kepzettseg2_add
    delete = self.kepzettseg2_del
    self.addrow(rep)
    if len(rep.items) > 1:
      delete.enabled = True
    if len(rep.items) == 21:
      add.enabled = False

  def kepzettseg2_del_click(self, **event_args):
    rep = self.kepzettsegek_2
    add = self.kepzettseg2_add
    delete = self.kepzettseg2_del
    self.delrow(rep)
    if len(rep.items) == 1:
      delete.enabled = False
    if len(rep.items) < 21:
      add.enabled = True

  def rendezveny_add_click(self, **event_args):
    rep = self.rendezvenyek
    add = self.rendezveny_add
    delete = self.rendezveny_del
    self.addrow(rep)
    if len(rep.items) > 1:
      delete.enabled = True
    if len(rep.items) == 6:
      add.enabled = False

  def rendezveny_del_click(self, **event_args):
    rep = self.rendezvenyek
    add = self.rendezveny_add
    delete = self.rendezveny_del
    self.delrow(rep)
    if len(rep.items) == 1:
      delete.enabled = False
    if len(rep.items) < 6:
      add.enabled = True

  def zsakmany_add_click(self, **event_args):
    rep = self.zsakmany
    add = self.zsakmany_add
    delete = self.zsakmany_del
    self.addrow(rep)
    if len(rep.items) > 1:
      delete.enabled = True
    if len(rep.items) == 7:
      add.enabled = False

  def zsakmany_del_click(self, **event_args):
    rep = self.zsakmany
    add = self.zsakmany_add
    delete = self.zsakmany_del
    self.delrow(rep)
    if len(rep.items) == 1:
      delete.enabled = False
    if len(rep.items) < 7:
      add.enabled = True
  def getfegyver(self):
    out = []
    for i in range(3):
      for row in (self.fegyver_1.get_components() if i == 0 else self.fegyver_2.get_components() if i == 1 else self.fegyver_3.get_components() if i == 2 else []):
        fegyver = []
        fegyver += [row.nev.text]
        fegyver += [row.ke.text]
        fegyver += [row.te.text]
        fegyver += [row.ve.text]
        fegyver += [row.tam.text]
        fegyver += [row.sebzes.text]
        fegyver += [row.pajzs.text]
        fegyver += [row.magikus.checked]
        fegyver += [row.aldott.checked]
        out += [fegyver]
      
    return out
  def mentes_click(self, **event_args):
    elony = [item for sublist in self.getrow(self.elony) for item in sublist]
    hatrany = [item for sublist in self.getrow(self.hatrany) for item in sublist]
    print()
    data = {
    "": {
        "alap": [self.nev.text, self.kor_box.text, self.kaszt_box.text, self.faj_box.text, self.vallas_box.text, self.szarmazas_box.text, self.csillagjegy_box.text, self.rend_box.text, self.rang_box.text, self.csapat_box.text, self.falka_box.text, self.jelmondat_box.text, self.jelmondat2_box.text,self.szint.text,self.jellem_1.text,self.jellem_2.text],
        "stat": [self.ero.text, self.gyorsasag.text, self.ugyesseg.text, self.allokepesseg.text, self.egeszseg.text, self.szepseg.text, self.intelligencia.text, self.akaratero.text, self.asztral.text, self.eszleles.text],
        "szazalek": [self.titkosajto_kereses.text, self.ugras.text, self.eses.text, self.maszas.text, self.zsebmetszes.text, self.zarnyitas.text, self.rejtozes.text, self.koteltanc.text, self.lopozas.text, self.csapdafelfedezes.text],
        "elony": elony + ['']*(5-len(elony)),
        "hatrany": hatrany + ['']*(5-len(hatrany)), 
        "varazstargyak": self.getrow(self.varazstargyak),
        "fegyver_nelkuli": [self.ke.text, self.te.text, self.ve.text, self.ce.text],
        "fegyver": self.getfegyver(),
        "pszi": [self.pszi.text, self.termeszetes_asztral.text, self.statikus_asztral.text, self.dinamikus_asztral.text, self.me_asztral.text, self.termeszetes_mental.text, self.statikus_mental.text, self.dinamikus_mental.text, self.me_mental.text, self.pszi_af.checked, self.pszi_mf.checked, self.pszi_pyarroni.checked, self.pszi_slan.checked, self.pszi_kyr.checked, self.pszi_siopa.checked],
        "varazsero": [self.mana.text, self.od.text, self.verpont.text, self.elet.checked, self.lelek.checked, self.termeszet.checked, self.halal.checked],
        "vert": [self.vert.text, self.ep.text, self.fp.text, self.sfe.text, self.mgt.text, self.nehezvert_af.checked, self.nehezvert_mf.checked],
        "levonasok": [["","","",""],["","","",""]],
        "penz": [[self.arany_1.text, self.ezust_1.text, self.rez_1.text, self.hol_1.text],[self.arany_2.text, self.ezust_2.text, self.rez_2.text, self.hol_2.text],[self.arany_3.text, self.ezust_3.text, self.rez_3.text, self.hol_3.text]],
        "nyelv": [[[self.nyelv_1.text,self.nyelv_2.text,self.nyelv_3.text,self.nyelv_4.text,self.nyelv_5.text],[self.nyelv_1_szint.text,self.nyelv_2_szint.text,self.nyelv_3_szint.text,self.nyelv_4_szint.text,self.nyelv_5_szint.text]],[[self.nyelv_6.text,self.nyelv_7.text,self.nyelv_8.text,self.nyelv_9.text,self.nyelv_10.text],[self.nyelv_6_szint.text,self.nyelv_7_szint.text,self.nyelv_8_szint.text,self.nyelv_9_szint.text,self.nyelv_10_szint.text]]],
        "felszereles": [self.getrow(self.lathato_felszereles),self.getrow(self.nem_lathato_felszereles)],
        "kepzettseg": [self.getrow(self.kepzettsegek_1),self.getrow(self.kepzettsegek_2)],
        "mergek": self.getrow(self.mergek),
        "tarsak": [[self.allat_faj.text, self.allat_nev.text, self.allat_ep.text, self.allat_fp.text, self.allat_ke.text, self.allat_te.text, self.allat_ve.text, self.allat_tam.text, self.allat_sebzes.text, self.allat_teher.text, self.allat_megjegyzes.text], [self.kisero_faj.text, self.kisero_nev.text, self.kisero_ep.text, self.kisero_fp.text, self.kisero_ke.text, self.kisero_te.text, self.kisero_ve.text, self.kisero_tam.text, self.kisero_sebzes.text, self.kisero_teher.text, self.kisero_megjegyzes.text]],
        "talalkozok": self.getrow(self.rendezvenyek),
        "tp": self.tp.text, 
        "zsakmany": self.getrow(self.zsakmany)
    }
}
    anvil.media.download(anvil.server.call('retgenpdf',data,self.nev.text.replace(" ","_")+"_karakterlap"))

  def elony_add_click(self, **event_args):
    rep = self.elony
    add = self.elony_add
    delete = self.elony_del
    self.addrow(rep)
    if len(rep.items) > 1:
      delete.enabled = True
    if len(rep.items) == 4:
      add.enabled = False

  def elony_del_click(self, **event_args):
    rep = self.elony
    add = self.elony_add
    delete = self.elony_del
    self.delrow(rep)
    if len(rep.items) == 1:
      delete.enabled = False
    if len(rep.items) < 4:
      add.enabled = True

  def hatrany_del_click(self, **event_args):
    rep = self.hatrany
    add = self.hatrany_add
    delete = self.hatrany_del
    self.delrow(rep)
    if len(rep.items) > 1:
      delete.enabled = True
    if len(rep.items) == 4:
      add.enabled = False

  def hatrany_add_click(self, **event_args):
    rep = self.hatrany
    add = self.hatrany_add
    delete = self.hatrany_del
    self.addrow(rep)
    if len(rep.items) > 1:
      delete.enabled = True
    if len(rep.items) == 4:
      add.enabled = False
