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
def egyszerusitett_kozos(typ, inp):
    if typ == "pontok":
      if inp != None and "edzett" in inp and type(inp["edzett"]) is int:
        print("asd")
        return {"pont":131+inp["edzett"]*3,"szabad":"szépség"}
      else:
        print(inp)
        return {"pont":131,"szabad":"szepseg"}
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
        if "profi" in inp and type(inp["profi"]) is int:
          penz += inp["profi"]*75
        return penz
    elif typ == "elony":
      if "profi" in inp:
        if type(inp["profi"] is int):
          pass#self.profi = 75* inp["profi"]
      if "edzett" in inp:
        if type(inp["edzett"] is int):
          pass#self.edzett = 3 * inp["edzett"]
      if "kepzes" in inp:
        if type(inp["kepzes"] is int):
          pass#self.kepzes = 10 * inp["kepzes"]
      if "hires" in inp:
        if inp["hires"] != False and type(inp["kepzes"] is bool):
          pass#self.elony += "Híres\n"
    elif typ == "get_elony":
      if "szint" in inp:
        return int(inp["szint"])// 5
