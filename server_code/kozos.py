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
  penz = {"1":30,"2":30}
  if typ == "pontok":
    return {"pont":131,"szabad":"szepseg"}
  elif typ == "penz":
    if "szint" in inp:
      szint = inp["szint"]
      if szint < 4:
        return szint*20
      elif szint > 3 and szint < 8:
        return szint*30
      elif szint > 7:
        return szint*40
