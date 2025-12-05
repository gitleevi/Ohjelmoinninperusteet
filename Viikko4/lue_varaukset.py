#Lue_varaukset.py Viikko4 - Leevi Korpi

#ID|Nimi|Sähköposti|Puhelin|Päivä|Kello|Kesto|Hinta|True/False|Tila|Lisätty

from datetime import datetime, date, time

class Varaus:
    def __init__(self, varaus_id, nimi, sahkoposti, puhelin,
                 pvm, aika, kesto, hinta, vahvistettu,
                 tila, lisätty):

        self.varaus_id = varaus_id
        self.nimi = nimi
        self.sähköposti = sahkoposti
        self.puhelin = puhelin
        self.pvm = pvm
        self.aika = aika
        self.kesto = kesto
        self.hinta = hinta
        self.vahvistettu = vahvistettu
        self.tila = tila
        self.lisätty = lisätty


    def __str__(self):
        return f"{self.varaus_id} | {self.nimi} | {self.sähköposti} | {self.puhelin} | {self.pvm} | {self.aika} | {self.kesto} | {self.hinta} | {self.vahvistettu} | {self.tila} | {self.lisätty}"

def muunna_varaustiedot(rivi):
    varaus_id = int(rivi[0])
    nimi = rivi[1]
    sahkoposti = rivi[2]
    puhelin = rivi[3]

    varauksen_pvm = date.fromisoformat(rivi[4])
    varauksen_klo = time.fromisoformat(rivi[5])

    varauksen_kesto = int(rivi[6])
    hinta = float(rivi[7])

    varaus_vahvistettu = (rivi[8] == "True")

    varattu_tila = rivi[9]
    varaus_luotu = datetime.fromisoformat(rivi[10])

    return Varaus(
        varaus_id, nimi, sahkoposti, puhelin,
        varauksen_pvm, varauksen_klo,
        varauksen_kesto, hinta,
        varaus_vahvistettu, varattu_tila,
        varaus_luotu
    )



def lue_varaukset():
    varaukset = []
    with open("varaukset.txt", "r", encoding="utf-8") as tiedosto:
        for rivi in tiedosto:
            rivi = rivi.strip()
            osat = rivi.split("|")
            varaukset.append(osat)
    return varaukset



def main():
    varaukset = lue_varaukset()
    

    print("Luetut varaukset (muuntamattomat):")
    for v in varaukset: 
        print(v)

    print("\n1) Luetut vahvistetut varaukset (muunnetut):")  #Tulosta vahvistettujen varausten tiedot
    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)
        
        if v.vahvistettu: # Käytetään olion atribuuttia
            pvm = v.pvm.strftime("%d.%m.%Y")
            klo = v.aika.strftime("%H.%M")
            print(f"- {v.nimi}, {v.tila}, {pvm} klo {klo}")


    print("\n2) Pitkät varaukset (≥ 3 h)")  #Tulostetaan varaukset, joiden kesto on vähintään 3 tuntia

    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)
        
        if v.kesto >= 3:
            pvm = v.pvm.strftime("%d.%m.%Y")
            klo = v.aika.strftime("%H.%M")
            print(f"- {v.nimi}, {pvm} klo {klo}, kesto {v.kesto} h, {v.tila}")


    print("\n3) Varausten vahvistusstatus")  #Tulostetaan jokaisen varauksen vahvistusstatus

    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)

        if v.vahvistettu:
            print(f"{v.nimi} → Vahvistettu")
        else:
            print(f"{v.nimi} → Ei vahvistettu")


    print("\n4) Vahvistusten yhteenveto")  #Tulostetaan yhteenveto vahvistetuista ja vahvistamattomista varauksista

    vahvistetut = 0
    vahvistamattomat = 0

    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)

        if v.vahvistettu:
            vahvistetut += 1
        else:
            vahvistamattomat += 1

    print(f"- Vahvistettuja varauksia: {vahvistetut} kpl")
    print(f"- Vahvistamattomia varauksia: {vahvistamattomat} kpl")


    print("\n5) Hinta yhteensä")  #Tulostetaan varausten kokonaishinta

    kokonaishinta = 0.0
    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)
        if v.vahvistettu:
            kokonaishinta += v.hinta

    hinta_str = f"{kokonaishinta:.2f}".replace(".", ",")   # Muutetaan piste desimaalipilkuksi

    print(f"{hinta_str} €")

        
    print("\nBONUS1: Kallein varaus") #Etsitään varauksista kallein

    kallein = None
    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)
        if (kallein is None) or (v.hinta > kallein.hinta):
            kallein = v

    hinta_str = f"{kallein.hinta:.2f}".replace(".", ",")  #Muutetaan hinta pilkulla

    print("Kallein varaus:")
    print(f"- Nimi: {kallein.nimi}")
    print(f"- Varattu tila: {kallein.tila}")
    print(f"- Päivä: {kallein.pvm.strftime('%d.%m.%Y')}")
    print(f"- Kellonaika: {kallein.aika.strftime('%H.%M')}")
    print(f"- Kesto: {kallein.kesto} h")
    print(f"- Kokonaishinta: {hinta_str} €")

    
    print("\nBONUS2: Varausten määrä päivittäin") #Lasketaan varaukset päivittäin)

    paivamaarat = {}

    for rivi in varaukset: 
        v = muunna_varaustiedot(rivi)
        pvm_str = v.pvm.strftime("%d.%m.%Y")
        if pvm_str not in paivamaarat:
            paivamaarat[pvm_str] = 0
        paivamaarat[pvm_str] += 1

    print("Varausten määrät päivittäin:")
    for pvm, maara in paivamaarat.items():
        print(f"- {pvm}: {maara} kpl")

    
    print("\nBONUS3: Suodata varaukset tilan mukaan") #Suodatetaan varaukset tilan mukaan
    haettu_tila = input("Anna tilan nimi: ")

    print(f"\nVaraukset tilaan '{haettu_tila}':")
    loytyi = False

    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)
        if v.tila == haettu_tila:
            pvm = v.pvm.strftime("%d.%m.%Y")
            klo = v.aika.strftime("%H.%M")
            print(f"- {v.nimi}, {pvm} klo {klo}, kesto {v.kesto} h")
            loytyi = True

    if not loytyi:
        print("Ei varauksia kyseiseen tilaan.")


    print("\nBONUS4: Tulevat varaukset") #Näytetään tulevat varaukset
    pvm_syote = input("Anna päivämäärä (pp.kk.vvvv): ")
    paiva, kk, vv = map(int, pvm_syote.split("."))
    rajapvm = date(vv, kk, paiva)
    
    print("\nVaraukset annetun päivän jälkeen:")
    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)
        if v.pvm > rajapvm:
            pvm = v.pvm.strftime("%d.%m.%Y")
            klo = v.aika.strftime("%H.%M")
            print(f"- {v.nimi}, {pvm} klo {klo}, {v.tila}")


    print("\nBONUS5: Vahvistettujen varausten keskimääräinen kestoaika")

    kestot = []
    for rivi in varaukset:
        v = muunna_varaustiedot(rivi)
        if v.vahvistettu:
            kestot.append(v.kesto)

    if kestot:
        keskiarvo = sum(kestot) / len(kestot)
        keskiarvo_str = f"{keskiarvo:.1f}".replace(".", ",")
        print(f"Vahvistettujen varausten keskimääräinen kestoaika: {keskiarvo_str} h")
    else:
        print("Ei vahvistettuja varauksia.")        


if __name__ == "__main__":
    main()      