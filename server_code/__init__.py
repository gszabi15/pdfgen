import json
import pdf4
import kargen
import kozos
import anvil.server

kkargen = kozos.kozos()
@anvil.server.callable
def egyszerusitett_kozos(typ, inp):
    kkargen.egyszerusitett_kozos(typ,inp)

if __name__ == "__main__":
    anvil.server.connect("server_2RIHQYHC6A2TJ3LPQBKOKDHP-DWZPA6GTTRW72Y56")

    while 1:
        pass

