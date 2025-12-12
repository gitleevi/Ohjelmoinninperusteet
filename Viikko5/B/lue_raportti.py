# Copyright (c) 2025 Leevi Korpi
# License: MIT


from datetime import datetime, date
from typing import List, Dict



def lue_data(tiedoston_nimi: str) -> list[Dict]:
    """Lukee CSV-tiedoston ja palauttaa rivit sopivassa rakenteessa."""
    
    data = []

    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f) # Ohitetaan otsikkorivi

        for rivi in f:
            osat = rivi.strip().split(";")

            aika_str = osat[0]
            kulutus = list(map(float, osat[1:4]))
            tuotanto = list(map(float, osat[4:7]))

            # Muutetaan Wh -> kWh
            kulutus_kwh = [x / 1000 for x in kulutus]
            tuotanto_kwh = [x / 1000 for x in tuotanto]

            data.append({
                "aika": datetime.fromisoformat(aika_str),
                "kulutus_v1": kulutus_kwh[0],
                "kulutus_v2": kulutus_kwh[1],
                "kulutus_v3": kulutus_kwh[2],
                "tuotanto_v1": tuotanto_kwh[0],
                "tuotanto_v2": tuotanto_kwh[1],
                "tuotanto_v3": tuotanto_kwh[2],
            })

    return data


def laske_paivayhteenvedot(data: list[Dict]) -> Dict[date, Dict]:
    """Laskee päiväkohtaiset summat yhdelle viikolle"""

    paiva_dict: Dict[date, Dict[str, float]] = {}

    for rivi in data:
        paiva = rivi["aika"].date()
        if paiva not in paiva_dict:
            paiva_dict[paiva] = {
                "kulutus_v1": 0.0,
                "kulutus_v2": 0.0,
                "kulutus_v3": 0.0,
                "tuotanto_v1": 0.0,
                "tuotanto_v2": 0.0,
                "tuotanto_v3": 0.0,
            }

        paiva_dict[paiva]["kulutus_v1"] += rivi["kulutus_v1"]
        paiva_dict[paiva]["kulutus_v2"] += rivi["kulutus_v2"]
        paiva_dict[paiva]["kulutus_v3"] += rivi["kulutus_v3"]
        paiva_dict[paiva]["tuotanto_v1"] += rivi["tuotanto_v1"]
        paiva_dict[paiva]["tuotanto_v2"] += rivi["tuotanto_v2"]
        paiva_dict[paiva]["tuotanto_v3"] += rivi["tuotanto_v3"]

    return paiva_dict


def paivan_nimi_suomeksi(paiva: date) -> str:
    """Palauttaa annetun päivämäärän viikonpäivän nimen suomeksi."""
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


def muotoile_kaksi_desimaalia_pilkulla(arvo: float) -> str:
    """Muotoilee luvun kahden desimaalin tarkkuudella ja vaihtaa pisteen pilkuksi"""
    return f"{arvo:.2f}".replace(".", ",")

def muodosta_pvm_str(paiva: date) -> str:
    """Muodostaa päivämäärän merkkijonoksi muodossa pv.kk.vvvv"""
    return f"{paiva.day}.{paiva.month}.{paiva.year}"

def muodosta_raporttirivit(
    viikon_numero: int, 
    yhteenveto: Dict[date, Dict]
) -> List[str]:
    """Muodostaa viikkokohtaiset raporttirivit tekstimuotoon.
       Palauttaa listan merkkijonoja, jotka voidaan kirjoittaa tiedostoon."""
    
    rivit: list[str] = []

    rivit.append(f"Viikon {viikon_numero} sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
    rivit.append("")
    rivit.append("Päivä         Pvm          Kulutus [kWh]                 Tuotanto [kWh]")
    rivit.append("                          v1      v2      v3              v1     v2     v3")
    rivit.append("-" * 75)

    for paiva in sorted(yhteenveto.keys()):
        paiva_tiedot = yhteenveto[paiva]

        paivan_nimi = paivan_nimi_suomeksi(paiva)
        pvm_str = muodosta_pvm_str(paiva)


        k1 = muotoile_kaksi_desimaalia_pilkulla(paiva_tiedot["kulutus_v1"])
        k2 = muotoile_kaksi_desimaalia_pilkulla(paiva_tiedot["kulutus_v2"])
        k3 = muotoile_kaksi_desimaalia_pilkulla(paiva_tiedot["kulutus_v3"])
        t1 = muotoile_kaksi_desimaalia_pilkulla(paiva_tiedot["tuotanto_v1"])
        t2 = muotoile_kaksi_desimaalia_pilkulla(paiva_tiedot["tuotanto_v2"])
        t3 = muotoile_kaksi_desimaalia_pilkulla(paiva_tiedot["tuotanto_v3"])

        rivit.append(
            f"{paivan_nimi:<12} {pvm_str:<12}  {k1:>6}  {k2:>6}  {k3:>6}      {t1:>6}  {t2:>6}  {t3:>6}"
        )


    rivit.append("\n")
    return rivit


def kirjoita_tiedostoon(rivit: list[str], nimi: str = "yhteenveto.txt") -> None:
    """Kirjoittaa raporttirivit tiedostoon."""

    with open(nimi, "w", encoding="utf-8") as f:
        for rivi in rivit:
            f.write(rivi + "\n")

def main() -> None:
    """Ohjelman pääfunktio."""

    # Luetaan kaikkien kolmen viikon data
    data41 = lue_data("viikko41.csv")
    data42 = lue_data("viikko42.csv")
    data43 = lue_data("viikko43.csv")

    # Lasketaan päiväkohtaiset yhteenvedot
    yhteenveto41 = laske_paivayhteenvedot(data41)
    yhteenveto42 = laske_paivayhteenvedot(data42)
    yhteenveto43 = laske_paivayhteenvedot(data43)

    # Muodostetaan raporttirivit
    rivit = []
    rivit += muodosta_raporttirivit(41, yhteenveto41)
    rivit += muodosta_raporttirivit(42, yhteenveto42)
    rivit += muodosta_raporttirivit(43, yhteenveto43)

    # Kirjoitetaan raportti tiedostoon
    kirjoita_tiedostoon(rivit)

if __name__ == "__main__":
    main()