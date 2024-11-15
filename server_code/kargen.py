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
def get_kaszt():
  val = []
  for row in app_tables.kaszt.search():
    if row['Forras'] in get_enabled():
      val += [row]
  return val
@anvil.server.callable
def get_kasztnev():
  kaszt = get_kaszt()
  kasztnev = []
  for i in kaszt:
    kasztnev += [i['Nev']]
  return list(set(kasztnev))
@anvil.server.callable
def pontok(inp:None,kargen):
  anvil.server.call(kargen,"pontok",inp)
@anvil.server.callable
def penz(inp:None,kargen):
  anvil.server.call(kargen,,"penz",inp)