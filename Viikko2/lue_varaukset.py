from datetime import datetime, timedelta

def lue_varaukset(tiedostonimi):
    with open(tiedostonimi, "r", encoding="utf-8") as f:
        rivit = f.readlines()

    yhteishinta = 0

    for rivi in rivit:
        rivi = rivi.strip()
        if not rivi:
            continue

        v = rivi.split("|")

        numero = int(v[0])
        nimi = v[1]
        paiva = datetime.strptime(v[2], "%Y-%m-%d").date()
        aika = datetime.strptime(v[3], "%H:%M").time()
        tunnit = int(v[4])
        hinta = float(v[5])
        maksettu = v[6].lower() == "true"
        kohde = v[7]
        puhelin = v[8]
        email = v[9]

        kokonaishinta = tunnit * hinta
        yhteishinta += kokonaishinta

        loppu = (datetime.combine(paiva, aika) + timedelta(hours=tunnit)).time()

        hinta_s = f"{hinta:.2f}".replace('.', ',')
        kokonaishinta_s = f"{kokonaishinta:.2f}".replace('.', ',')

        print(f"Varausnumero: {numero}")
        print(f"Varaaja: {nimi}")
        print(f"Päivämäärä: {paiva.strftime('%d.%m.%Y')}")
        print(f"Aloitusaika: {aika.strftime('%H.%M')}")
        print(f"Loppumisaika: {loppu.strftime('%H.%M')}")
        print(f"Tuntimäärä: {tunnit}")
        print(f"Tuntihinta: {hinta_s} €")
        print(f"Kokonaishinta: {kokonaishinta_s} €")
        print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
        print(f"Kohde: {kohde}")
        print(f"Puhelin: {puhelin}")
        print(f"Sähköposti: {email}")
        print("-" * 30)

    print(f"Kaikkien varausten yhteishinta: {yhteishinta:.2f}".replace('.', ',') + " €")

lue_varaukset("varaukset.txt")
