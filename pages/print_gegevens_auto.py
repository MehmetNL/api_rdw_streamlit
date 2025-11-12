import sqlite3

def print_gegevens(info2):
    if len(info2) == 0:
        print(f"Geen auto gevonden met het opgegeven bouwjaar")
    else:
        print("{0:15s} {1:25s} {2:25s} {3:25s} {4:25} {5:25s} {6:25s} {7:25s} {8:26s}".format("Kenteken", "Merk",
                                                                                          "Model",
                                                                                          "Kleur", "Bouwjaar",
                                                                                          "Nieuw_prijs",
                                                                                          "Brandstof",
                                                                                          "Aantal_zitplaats",
                                                                                          "Registratie_land"))

        print("{0:15s} {1:25s} {2:25s} {3:25s} {4:25} {5:25s} {6:25s} {7:25s} {8:26s}".format("-" * 15, "-" * 25,
                                                                                          "-" * 25,
                                                                                          "-" * 25, "-" * 25,
                                                                                          "-" * 25,
                                                                                          "-" * 25, "-" * 25,
                                                                                          "-" * 25))

        for i in info2:
            print("{0:15s} {1:25s} {2:25s} {3:25s} {4:25s} {5:25s} {6:25s} {7:25s} {8:26s}".format(i[0], i[1], i[2],
                                                                                               i[3],
                                                                                               i[4][:4],
                                                                                               i[5], i[6], i[7],
                                                                                               i[8]))
