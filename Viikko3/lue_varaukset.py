
#Ohjelma lukee varaukset.txt -tiedoston rivit, pilkkoo rivit listaksi,
#ja hakee sekä tulostaa varausken tiedot erillisten funktioiden avulla

#Leevi, 22.11.25

#Varausnumero: 123
#Varaaja: Leevi Korpi
#Päivämäärä: 31.10
#Aloitusaika: 10.00
#Tuntimäärä: 2
#Tuntihinta: 19,95 €
#Kokonaishinta: 39,90 €
#Maksettu: Kyllä
#Kohde: Kokoustila A
#Puhelin: 0401234567
#Sähköposti: leevi.korpi@example.com


from datetime import datetime, date, time


def hae_varausnumero(varaus: list[str]) -> int:
    numero = int(varaus[0])
    return numero

def hae_varaaja(varaus: list[str]) -> str:
    nimi =varaus[1].strip()
    return nimi

def hae_paiva(varaus: list[str]) -> str:
    pvm = date.fromisoformat(varaus[2])
    valmis = pvm.strftime("%d.%m.%Y")
    return valmis

def hae_aloitusaika(varaus: list[str]) -> str:
    aika = time.fromisoformat(varaus[3])
    valmis = aika.strftime("%H.%M")
    return valmis

def hae_tuntimaara(varaus: list[str]) -> int:
    määrä = int(varaus[4])
    return määrä


def hae_tuntihinta(varaus: list[str]) -> str:
    hinta = float(varaus[5])
    muotoiltu = f"{hinta:.2f}".replace(".",",") + " €"
    return muotoiltu

def laske_kokonaishinta(varaus: list[str]) -> str:
    tunnit = int(varaus[4])
    hinta = float(varaus[5])
    kokonaishinta = tunnit * hinta
    muotoiltu = f"{kokonaishinta:.2f}".replace(".",",") + " €"
    return muotoiltu

def hae_maksettu(varaus: list[str]) -> str:
    teksti ="Kyllä" if varaus[6] == "True" else "Ei"
    return teksti

def hae_kohde(varaus: list[str]) -> str:
    kohde = varaus[7]
    return kohde

def hae_puhelin(varaus: list[str]) -> str:
    puhelin = varaus[8]
    return puhelin

def hae_sahkoposti(varaus: list[str]) -> str:
    sahkoposti = varaus[9]
    return sahkoposti


def tulosta_varaus(varaus: list[str]) -> None:
    numero = hae_varausnumero(varaus)
    nimi = hae_varaaja(varaus)
    paiva = hae_paiva(varaus)
    aika = hae_aloitusaika(varaus)
    tunnit = hae_tuntimaara(varaus)
    tuntihinta = hae_tuntihinta(varaus)
    kokonaishinta = laske_kokonaishinta(varaus)
    maksettu = hae_maksettu(varaus)
    kohde = hae_kohde(varaus)
    puhelin = hae_puhelin(varaus)
    sposti = hae_sahkoposti(varaus)


    print(f"Varausnumero: {numero}")
    print(f"Varaaja: {nimi}")
    print(f"Päivämäärä: {paiva}")
    print(f"Aloitusaika: {aika}")
    print(f"Tuntimäärä: {tunnit}")
    print(f"Tuntihinta: {tuntihinta}")
    print(f"Kokonaishinta: {kokonaishinta}")
    print(f"Maksettu: {maksettu}")
    print(f"Kohde: {kohde}")
    print(f"Puhelin: {puhelin}")
    print(f"Sähköposti: {sposti}")


def main():
    tiedosto = "varaukset.txt"

    with open(tiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            rivi = rivi.strip()
            
            # Ohita tyhjät rivit
            if not rivi:
                continue

            # Ohita otsikkorivi
            if rivi.lower().startswith("nro|"):
                continue

            varaus = rivi.split("|")

            print()  # Tyhjä rivi varauksien väliin
            print("-" * 30) # Erotinviiva varauksien väliin
            tulosta_varaus(varaus)


if __name__ == "__main__":
    main()