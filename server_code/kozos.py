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

class kozos():
  def __init__(self):
    self.elony =""
    self.edzett = 0
    self.profi = 0
  
  def egyszerusitett_kozos(self,typ, inp):
    if typ == "pontok":
      return {"pont":131+self.edzett,"szabad":"szepseg"}
    elif typ == "penz":
    
      if "szint" in inp:
        print(inp)
        szint = inp["szint"]
        penz = 0
        if szint < 4:
          penz = szint*20
        elif szint > 3 and szint < 8:
          penz = szint*30
        elif szint > 7:
          penz = szint*40
        penz += self.profi
        return penz
    elif typ == "elony":
      if "profi" in inp:
        if inp["profi"] > 0 and type(inp["profi"] is int):
          profi = 75* inp["profi"]
      if "edzett" in inp:
        if inp["edzett"] > 0 and type(inp["edzett"] is int):
          edzett = 3 * inp["edzett"]
      if "kepzes" in inp:
        if inp["kepzes"] > 0 and type(inp["kepzes"] is int):
          edzett = 10 * inp["kepzes"]
      if "hires" in inp:
        if inp["hires"] != False and type(inp["kepzes"] is bool):
          self.elony += "Híres\n"
    elif typ == "get_elony":
      if "szint" in inp:
        return int(inp["szint"])// 5
