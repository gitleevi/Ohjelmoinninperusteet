# Copyright (c) 2025 Leevi Korpi

# License: MIT

from __future__ import annotations

from datetime import datetime, date

from typing import List, Dict, Tuple

import csv


def lue_data(tiedoston_nimi: str) -> list:
    """Lukee CSV-tiedoston ja palauttaa rivit sopivassa rakenteessa."""
    data = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for rivi in reader:
            aika = datetime.fromisoformat(rivi["Aika"])
            kulutus = fi_float(rivi["Kulutus (netotettu) kWh"])
            tuotanto = fi_float(rivi["Tuotanto (netotettu) kWh"])
            lampo = fi_float(rivi["Vuorokauden keskilämpötila"])
            data.append({
                "aika": aika,
                "kulutus": kulutus,
                "tuotanto": tuotanto,
                "lampo": lampo
            })
    return data        


def paivittain(data: List[Dict]) -> Dict[date, Dict[str, float]]:
    """
    Aggregoi tuntidata päiväkohtaiseksi:
    - kulutus_sum (kWh)
    - tuotanto_sum (kWh)
    - lampo_avg (°C) (tuntien keskiarvo; käytännössä sama koko päivälle)
    """
    kooste: Dict[date, Dict[str, float]] = {}
    laskuri: Dict[date, int] = {}

    for d in data:
        pvm = d["aika"].date()
        if pvm not in kooste:
            kooste[pvm] = {"kulutus_sum": 0.0, "tuotanto_sum": 0.0, "lampo_sum": 0.0}
            laskuri[pvm] = 0

        kooste[pvm]["kulutus_sum"] += d["kulutus"]
        kooste[pvm]["tuotanto_sum"] += d["tuotanto"]
        kooste[pvm]["lampo_sum"] += d["lampo"]
        laskuri[pvm] += 1

    for pvm in kooste:
        kooste[pvm]["lampo_avg"] = kooste[pvm]["lampo_sum"] / max(laskuri[pvm], 1)

    return kooste


def hae_max_min_paiva(kooste: Dict[date, Dict[str, float]]) -> Tuple[Tuple[date,float], Tuple[date, float]]:
    """Palauttaa (max_päivä, max_kulutus) ja (min_päivä, min_kulutus) päiväkohtaisesta koosteesta."""
    if not kooste:
        raise ValueError("Ei dataa koosteessa.")
    
    max_pvm = max(kooste, key=lambda p: kooste[p]["kulutus_sum"])
    min_pvm = min(kooste, key=lambda p: kooste[p]["kulutus_sum"])
    return (max_pvm, kooste[max_pvm]["kulutus_sum"]), (min_pvm, kooste[min_pvm]["kulutus_sum"])


def nayta_paavalikko() -> str:
    """Tulostaa päävalikon ja palauttaa käyttäjän valinnan merkkijonona."""
    print("\nValitse raporttityyppi:")
    print("1) Päiväkohtainen yhteenveto aikaväliltä")
    print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
    print("3) Vuoden 2025 kokonaisyhteenveto")
    print("4) Lopeta ohjelma")
    return input("Valintasi: ").strip()


def pyydä_paiva(prompt: str) -> date:
    """Kysyy päivämäärän muodossa pv.kk.vvvv ja palauttaa date-oliona."""
    while True:
        try:
            pvm_str = input(prompt).strip()
            paiva, kk, vuosi = map(int, pvm_str.split("."))
            return date(vuosi, kk, paiva)
        except ValueError:
            print("Virheellinen päivämäärä. Yritä uudelleen (muoto pv.kk.vvvv).")


def pyydä_kuukausi() -> int:
    """Kysyy kuukauden numeron 1-12."""
    while True:
        try:
            kk = int(input("Anna kuukauden numero (1-12): ").strip())
            if 1 <= kk <= 12:
                return kk
            print("Kuukausi 1-12.")
        except ValueError:
            print("Virheellinen syöte. Anna numero 1-12.")


def luo_paivaraportti(data: list) -> list[str]:
    """Muodostaa päiväkohtaisen raportin valitulle aikavälille."""
    alku = pyydä_paiva("Anna alkupäivä (pv.kk.vvvv): ")
    loppu = pyydä_paiva("Anna loppupäivä(pv.kk.vvvv): ")

    if loppu < alku:
        alku, loppu = loppu, alku
    
    valitut = [d for d in data if alku <= d["aika"].date() <= loppu]
    if not valitut:
        return [f"Ei dataa valitulta aikaväliltä ({fi_pvm(alku)} - {fi_pvm(loppu)})."]
    
    kokonais_kulutus = sum (d["kulutus"] for d in valitut)
    kokonais_tuotanto = sum (d["tuotanto"] for d in valitut)
    keski_lampo = sum(d["lampo"] for d in valitut) / len(valitut)
    nettokuorma = kokonais_kulutus - kokonais_tuotanto

    kooste = paivittain(valitut)
    (max_pvm, max_kul), (min_pvm, min_kul) = hae_max_min_paiva(kooste)

    rivit = [
        "Päiväkohtainen yhteenveto (aikaväli)",
        f"Aikaväli: {fi_pvm(alku)} - {fi_pvm(loppu)}",
        "-" * 50,
        f"Kokonaiskulutus: {fi_2dp(kokonais_kulutus)} kWh",
        f"Kokonaistuotanto: {fi_2dp(kokonais_tuotanto)} kWh",
        f"Nettokuorma (kulutus - tuotanto): {fi_2dp(nettokuorma)} kWh",
        f"Keskilämpötila (tuntien keskiarvo): {fi_2dp(keski_lampo)} °C",
        "-" * 50,
        f"Suurin päiväkulutus: {fi_pvm(max_pvm)} | {fi_2dp(max_kul)} kWh | lämpö {fi_2dp(kooste[max_pvm]['lampo_avg'])} °C",
        f"Pienin päiväkulutus: {fi_pvm(min_pvm)} | {fi_2dp(min_kul)} kWh | lämpö {fi_2dp(kooste[min_pvm]['lampo_avg'])} °C",
    ]
    return rivit


def luo_kuukausiraportti(data: list) -> list[str]:
    """Muodostaa kuukausikohtaisen yhteenvedon valitulle kuukaudelle."""
    kk = pyydä_kuukausi()
    valitut = [d for d in data if d["aika"].month == kk]

    if not valitut:
        return [f"Ei dataa valitulta kuukaudelta ({kk}/2025)."]
    
    kokonais_kulutus = sum(d["kulutus"] for d in valitut)
    kokonais_tuotanto = sum(d["tuotanto"] for d in valitut)
    keski_lampo = sum(d["lampo"] for d in valitut) / len(valitut)
    nettokuorma = kokonais_kulutus - kokonais_tuotanto

    kooste = paivittain(valitut)
    (max_pvm, max_kul), (min_pvm, min_kul) = hae_max_min_paiva(kooste)

    rivit = [
        "Kuukausikohtainen yhteenveto",
        f"Kuukausi: {kk}/2025",
        "-" * 50,
        f"Kokonaiskulutus: {fi_2dp(kokonais_kulutus)} kWh",
        f"Kokonaistuotanto: {fi_2dp(kokonais_tuotanto)} kWh",
        f"Nettokuorma (kulutus - tuotanto): {fi_2dp(nettokuorma)} kWh",
        f"Keskilämpötila (tuntien keskiarvo): {fi_2dp(keski_lampo)} °C",
        "-" * 50,
        f"Suurin päiväkulutus: {fi_pvm(max_pvm)} | {fi_2dp(max_kul)} kWh | lämpö {fi_2dp(kooste[max_pvm]['lampo_avg'])} °C",
        f"Pienin päiväkulutus: {fi_pvm(min_pvm)} | {fi_2dp(min_kul)} kWh | lämpö {fi_2dp(kooste[min_pvm]['lampo_avg'])} °C",
    ]
    return rivit
    

def luo_vuosiraportti(data: list) -> list[str]:
    """Muodostaa koko vuoden yhteenvedon."""
    if not data:
        return "[Ei dataa vuodesta 2025.]"
    
    kokonais_kulutus = sum(d["kulutus"] for d in data)
    kokonais_tuotanto = sum(d["tuotanto"] for d in data)
    keski_lampo = sum(d["lämpö"] for d in data) /len(data)
    nettokuorma = kokonais_kulutus - kokonais_tuotanto

    kooste = paivittain(data)
    (max_pvm, max_kul), (min_pvm, min_kul) = hae_max_min_paiva(kooste)

    rivit = [
        "Vuoden 2025 kokonaisyhteenveto",
        "-" * 50 ,
        f"Kokonaistuotanto: {fi_2dp(kokonais_tuotanto)} kWh",
        f"Kokonaistuotanto: {fi_2dp(kokonais_tuotanto)} kWh",
        f"Nettokuorma (kulutus - tuotanto): {fi_2dp(nettokuorma)} kWh",
        f"Keskilämpötila (tuntien keskiarvo): {fi_2dp(keski_lampo)} °C",
        "-" * 50,
        f"Suurin päiväkulutus: {fi_pvm(max_pvm)} | {fi_2dp(max_kul)} kWh | lämpö {fi_2dp(kooste[max_pvm]['lampo_avg'])} °C",
        f"Pienin päiväkulutus: {fi_pvm(min_pvm)} | {fi_2dp(min_kul)} kWh | lämpö {fi_2dp(kooste[min_pvm]['lampo_avg'])} °C",
    ]
    return rivit

def tulosta_raportti_konsoliin(rivit: list[str]) -> None:
    """Tulostaa raportin rivit konsoliin."""
    print()
    for rivi in rivit:
        print(rivi)


def kirjoita_raportti_tiedostoon(rivit: list[str]) -> None:
    """Kirjoittaa raportin rivit tiedostoon raportti.txt."""
    with open("raportti.txt", "w", encoding="utf-8") as f:
        for rivi in rivit:
            f.write(rivi + "\n")
    print("Raportti kirjoitettu tiedostoon raportti.txt")


def fi_float(luku_str: str) -> float:
    """Muuntaa suomalaisen desimaalipilkun sisältävän luvun floatiksi."""
    return float(luku_str.replace(",", "."))


def fi_2dp(luku: float) -> str:
    """Palauttaa luvun kahden desimaalin tarkkuudella ja pilkku desimaalierottimena."""
    return f"{luku:.2f}".replace(".", ",")


def fi_pvm(pvm: date) -> str:
    """Palauttaa päivämäärän muodossa pv.kk.vvvv."""
    return f"{pvm.day}.{pvm.month}.{pvm.year}"


def main() -> None:
    """Ohjelman pääfunktio: lukee datan, näyttää valikot ja ohjaa raporttien luomista."""
    try: 
        data = lue_data("2025.csv")
    except FileNotFoundError:
        print("Virhe: Tiedostoa 2025.csv ei löytynyt.")
        return
    except KeyError as e:
        print(f"Virhe: CSV-otsikoissa ei ollut odotettua saraketta: {e}")
        print("Varmista, että CSV:n otsikkorivi on muodossa:")
        print("Aika;Kulutus (netotettu kWh;Tuotanto (netotettu) kWh;Vuorokauden keskilämpötila")
        return
    
    while True:
        valinta = nayta_paavalikko()

        if valinta == "1":
            raportti = luo_paivaraportti(data)
        elif valinta == "2":
            raportti = luo_kuukausiraportti(data)
        elif valinta == "3":
            raportti = luo_vuosiraportti(data)
        elif valinta == "4":
            print("Ohjelma lopetetaan.")
            break
        else:
            print("Virheellinen valinta.")
            continue

        tulosta_raportti_konsoliin(raportti)

        while True:
            print("\nMitä haluat tehdä seuraavaksi?")
            print("1) Kirjoita raportti tiedostoon raportti.txt")
            print("2 Luo uusi raportti.")
            print("3 Lopeta.")
            jatko = input("Valintasi: ").strip()

            if jatko == "1":
                kirjoita_raportti_tiedostoon(raportti)
            elif jatko == "2":
                break 
            elif jatko == "3":
                print("Ohjelma lopetetaan.")
                return
            else:
                print("Virheellinen valinta.")


if __name__ == "__main__":
    main()
