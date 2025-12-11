#Viikko5, Tehtävä A - Leevi Korpi

# Copyright (c) 2025 Leevi Korpi
# License: MIT

from __future__ import annotations

import csv
from datetime import datetime, date
from typing import List, Dict, Tuple


def lue_data(tiedoston_nimi: str) -> List[Dict[str, object]]:  #Lukee CSV-tiedoston ja palauttaa listan mittausrivejä
    """Lukee CSV-tiedoston ja palauttaa listan rivejä, joissa aika on datetime ja arvot Wh-yksikössä."""

    rivit: List[Dict[str, float]] = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        lukija = csv.DictReader(f, delimiter=",")
        for row in lukija:
            aika = datetime.fromisoformat(row["aika"]) #Muunnetaan aika datetime-olioksi
            kulutus_v1 = float(row["kulutus_v1"])
            kulutus_v2 = float(row["kulutus_v2"])
            kulutus_v3 = float(row["kulutus_v3"])
            tuotanto_v1 = float(row["tuotanto_v1"])
            tuotanto_v2 = float(row["tuotanto_v2"])
            tuotanto_v3 = float(row["tuotanto_v3"])

            rivit.append(
                {
                    "aika": aika,
                    "kulutus_v1": kulutus_v1,
                    "kulutus_v2": kulutus_v2,
                    "kulutus_v3": kulutus_v3,
                    "tuotanto_v1": tuotanto_v1,
                    "tuotanto_v2": tuotanto_v2,
                    "tuotanto_v3": tuotanto_v3
                }
            )
    return rivit


def ryhmittele_paivittain(rivit: List[Dict[str, float]]) -> Dict[date, List[Dict[str, float]]]:  
    """Ryhmittelee mittausrivit päivämäärän mukaan sanakirjaksi."""
    paiva_dict: Dict[date, List[Dict[str, float]]] = {}
    for rivi in rivit:
        paiva = rivi["aika"].date()
        if paiva not in paiva_dict:
            paiva_dict[paiva] = []
        paiva_dict[paiva].append(rivi)
    return paiva_dict


def summa_wh_paivalle(
        paivan_rivit: List[Dict[str, float]]
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]: # Laskee päivän kokoaissummat Wh-yksikköinä, erikseen kulutukselle ja tuotannolle
    
    k1 = k2 = k3 = 0.0
    t1 = t2 = t3 = 0.0 
    for r in paivan_rivit:
        k1 += r["kulutus_v1"]
        k2 += r["kulutus_v2"]
        k3 += r["kulutus_v3"]
        t1 += r["tuotanto_v1"]
        t2 += r["tuotanto_v2"]
        t3 += r["tuotanto_v3"]
    return (k1, k2, k3), (t1, t2, t3)


def wh_to_kwh(arvo_wh: float) -> float: #Muuntaa Wh-arvon kWh-arvoksi
    """Muuntaa Wh-arvon kWh-arvoksi"""
    return arvo_wh / 1000.0

def muodosta_pvm_str(paiva: date) -> str: #Muodostaa päivämäärämerkkijonon muodossa "pp.kk.vvvv"
    """Muodostaa päivämäärämerkkijonon muodossa pv.kk.vvvv (esim. 13.10.2025)."""
    return f"{paiva.day}.{paiva.month}.{paiva.year}"
    
def muotoile_kaksi_desimaalia_pilkulla(arvo: float) -> str: #Muotoilee liukuluvun merkkijonoksi, jossa on kaksi desimaalia ja pilkku desimaalierottimena
    """Muotoilee luvun kahden desimaalin tarkkuudella ja vaihtaa desimaalipisteen pilkuksi."""
    s = f"{arvo:.2f}"
    return s.replace(".", ",")

def paivan_nimi_suomeksi(paiva: date) -> str:  #Palauttaa viikonpäivän nimen suomeksi annetulle päivämäärälle
    """Palauttaa annetun päivämäärän viikonpäivän nimen suomeksi (maanantai–sunnuntai)."""
    nimet = [
        "maanantai",
        "tiistai",
        "keskiviikko",
        "torstai",
        "perjantai",
        "lauantai",
        "sunnuntai",
    ]
    return nimet[paiva.weekday()]


def tulosta_raportti(paiva_summat_kwh: Dict[date, Tuple[Tuple[float, float, float], Tuple[float, float, float]]]) -> None:  # Tulostaa konsoliin selkeän taulukon kulutuksesta viikonpäivän mukaan
    """Tulostaa konsoliin taulukon, jossa näkyy päiväkohtainen kulutus ja tuotanto (kWh, vaiheittain)."""
    print("Viikon 42 Sähkönkulutus ja -tuontanto (kWh, vaiheittain)")
    print()
    print(
        "Päivä     Pvm     Kulutus (kWh)     Tuotanto (kWh)"
    )
    print(
        "(pv.kk.vvvv)                  V1     V2     V3      |     V1     V2     V3"
    )
    print("-" * 75)

    for paiva in sorted(paiva_summat_kwh.keys()): # Järjestetään päivät nousevaan järjestykseen
        (k1, k2, k3), (t1, t2, t3) = paiva_summat_kwh[paiva]
        
        k1s = muotoile_kaksi_desimaalia_pilkulla(k1)
        k2s = muotoile_kaksi_desimaalia_pilkulla(k2)
        k3s = muotoile_kaksi_desimaalia_pilkulla(k3)
        t1s = muotoile_kaksi_desimaalia_pilkulla(t1)
        t2s = muotoile_kaksi_desimaalia_pilkulla(t2)
        t3s = muotoile_kaksi_desimaalia_pilkulla(t3)

        paivan_nimi = paivan_nimi_suomeksi(paiva)
        pvm_str = muodosta_pvm_str(paiva)

        print(
            f"{paivan_nimi:<12}  {pvm_str:<12}  {k1s:>6}  {k2s:>6}  {k3s:>6}  |  {t1s:>6}  {t2s:>6}  {t3s:>6}"
        )


def laske_paiva_summat_kwh(   # Laskee päiväkohtaiset tummat ja muuttaa Wh -> kWh
    paiva_data: Dict[date, List[Dict[str, float]]]
) -> Dict[date, Tuple[Tuple[float,float, float], Tuple[float, float, float]]]:
    """Laskee päiväkohtaiset summat Wh-yksikössä ja muuntaa ne kWh-yksikköön vaiheittain."""
    
    tulos: Dict[date, Tuple[Tuple[float, float, float], Tuple[float, float, float]]] = {}
    for paiva, rivit in paiva_data.items():
        kulutus_wh, tuotanto_wh = summa_wh_paivalle(rivit)
        kulutus_kwh =tuple(wh_to_kwh(x) for x in kulutus_wh)
        tuotanto_kwh = tuple(wh_to_kwh(x) for x in tuotanto_wh)
        tulos[paiva] = (kulutus_kwh, tuotanto_kwh)
    return tulos

def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee yhteenvedot ja tulostaa raportin."""
    tiedosto = "viikko42.csv"
    rivit = lue_data(tiedosto)
    paiva_data = ryhmittele_paivittain(rivit)
    paiva_summat_kwh = laske_paiva_summat_kwh(paiva_data)
    tulosta_raportti(paiva_summat_kwh)

if __name__ == "__main__":
    main()


