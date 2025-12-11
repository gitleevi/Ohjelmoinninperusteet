#Lue_varaukset.py Viikko7 - Leevi Korpi


from datetime import datetime, date, time

    
def muunna_varaustiedot(rivi: list[str]) -> dict:
    return {
        "id": int(rivi[0]),
        "nimi": rivi[1],
        "sahkoposti": rivi[2],
        "puhelin": rivi[3],
        "pvm": date.fromisoformat(rivi[4]),
        "aika": time.fromisoformat(rivi[5]),
        "kesto": int(rivi[6]),
        "hinta": float(rivi[7]),
        "vahvistettu": (rivi[8] == "True"),
        "kohde": rivi[9],
        "luotu": datetime.fromisoformat(rivi[10])
    }
    



def lue_varaukset() -> list[dict]:
    varaukset = []
    with open("varaukset.txt", "r", encoding="utf-8") as tiedosto:
        for rivi in tiedosto:
            rivi = rivi.strip()
            osat = rivi.split("|")
            varaukset.append(muunna_varaustiedot(osat))
    return varaukset



def main():
    varaukset = lue_varaukset()
    

    #print("Luetut varaukset (muuntamattomat):")
    #for v in varaukset: 
        #print(v)

    print("\n1) Luetut vahvistetut varaukset (muunnetut):")  #Tulosta vahvistettujen varausten tiedot
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            pvm = varaus["pvm"].strftime("%d.%m.%Y")
            klo = varaus["aika"].strftime("%H.%M")
            print(f"- {varaus['nimi']}, {varaus['kohde']}, {pvm} klo {klo}")
        
        
    print("\n2) Pitkät varaukset (≥ 3 h)")  #Tulostetaan varaukset, joiden kesto on vähintään 3 tuntia
    for varaus in varaukset: 
        if varaus["kesto"] >= 3:
            pvm = varaus["pvm"].strftime("%d.%m.%Y")
            klo = varaus["aika"].strftime("%H.%M")
            print(f"- {varaus['nimi']}, {pvm} klo {klo}, kesto {varaus['kesto']} h, {varaus['kohde']}")


    print("\n3) Varausten vahvistusstatus")  #Tulostetaan jokaisen varauksen vahvistusstatus
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"{varaus['nimi']} -> Vahvistettu")
        else: 
            print(f"{varaus['nimi']} -> Ei vahvistettu")


    print("\n4) Vahvistusten yhteenveto")  #Tulostetaan yhteenveto vahvistetuista ja vahvistamattomista varauksista
    vahvistetut = sum(1 for varaus in varaukset if varaus["vahvistettu"])
    vahvistamattomat = sum(1 for varaus in varaukset if not varaus["vahvistettu"])

    print(f"- Vahvistettuja varauksia: {vahvistetut} kpl")
    print(f"- Vahvistamattomia varauksia: {vahvistamattomat} kpl")


    print("\n5) Hinta yhteensä")  #Tulostetaan varausten kokonaishinta
    kokonaishinta = sum(varaus["hinta"] for varaus in varaukset if varaus["vahvistettu"])
    hinta_str = f"{kokonaishinta:.2f}".replace(".", ",")
    print(f"{hinta_str} €")


if __name__ == "__main__":
    main()         