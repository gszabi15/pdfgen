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
            print(dir(component))
            if hasattr(component, 'text'):
                row_data.append(component.text)
            elif hasattr(component, 'checked'):  # Pl.: CheckBox esetén
                row_data.append(component.checked)
                print(component.checked)
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
                if hasattr(component, 'text'):
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
                if hasattr(component, 'text'):
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
