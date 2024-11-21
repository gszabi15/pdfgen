import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_enabled():
  enabled = []
  for row in app_tables.enabled.search():
    enabled += [row['Nev']] if row['enabled'] else []
  return enabled
  
@anvil.server.callable
def get_faj():
  val = []
  for row in app_tables.faj.search():
    if row['Forras'] in get_enabled():
      val += [row]
  return val

@anvil.server.callable
def get_fajnev():
  faj = get_faj()
  fajnev = []
  for i in faj:
    fajnev += [i['Nev']]
  return list(set(fajnev))
@anvil.server.callable
def get_kaszt(faj:None):
  val = []
  for row in app_tables.kaszt.search():
    if row['Forras'] in get_enabled():
      if faj != None:
        for row2 in app_tables.faj_kaszt.search():
          if row2['Faj'] == faj and row2["I/N"] and (row['Nev'] == row2['Kaszt'] or row2['Kaszt'] == "*"):
            val += [row]
      else:
        val += [row]
  return val

@anvil.server.callable
def get_kasztnev(faj:None):
  kaszt = get_kaszt(faj)
  kasztnev = []
  for i in kaszt:
    kasztnev += [i['Nev']]
  return list(set(kasztnev))
@anvil.server.callable
def get_korkat(faj):
  val = []
  for row in app_tables.faj.search():
    if row['Nev'] == faj and row['Korkategoria'] != None:
      val += [row['Korkategoria']]
  return val
@anvil.server.callable
def get_korkatmod(i:None):
  if i != None:
    row = app_tables.korkategoria.search()[i]
    return {'Nev':row['Nev'],'szam':row['szam'],'mod':{'ero':row['ero'],'gyorsasag':row['gyorsasag'],'ugyesseg':row['ugyesseg'],'allokepessg':row['allokepesseg'],'egeszseg':row['egeszseg'],'szepseg':row['szepseg']}}
@anvil.server.callable
def pontok(kargen,inp:None):
  return anvil.server.call(kargen,"pontok",inp)
@anvil.server.callable
def penz(kargen,inp:None):
  return anvil.server.call(kargen,"penz",inp)