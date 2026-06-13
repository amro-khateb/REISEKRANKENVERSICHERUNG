import asyncio
from datetime import date

import requests
from requests.auth import HTTPBasicAuth
from pyzeebe import ZeebeClient, ZeebeWorker, create_camunda_cloud_channel


API_BASE_URL = "https://travel-insurance-api.aws-playground.viadee.cloud"
API_USERNAME = "user1"
API_PASSWORD = "m7Qb2Xr9"


def search_partner_by_number(partnernummer: str):
    response = requests.get(
        f"{API_BASE_URL}/partners/{partnernummer}",
        auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
        timeout=10
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()


async def main():
    channel = create_camunda_cloud_channel(
        client_id="A.kmCM.C~Y9iiH43Ekvn7H2XtXAJcXEk",
        client_secret="kS_o9egQSufE0h_X70LPwEk1Oh.7MgWBt3sjZ9X9.W09XTUzDU0~-O3JuyL82b6o",
        cluster_id="3a04edcc-94a3-4a93-9148-d2e7791ef583",
        region="fra-1"
    )

    client = ZeebeClient(channel)
    worker = ZeebeWorker(channel)

    @worker.task(task_type="validate-data")
    def validate_data(travelInsurance: dict):
        print("Daten validieren...")

        travel_data = travelInsurance["travelData"]

        beginn = date.fromisoformat(travel_data["start"])
        ende = date.fromisoformat(travel_data["end"])
        kosten = float(travel_data["cost"])

        return {
            "datenGueltig": beginn < ende and beginn > date.today() and kosten > 0,
            "reisebeginnVorReiseende": beginn < ende,
            "reisebeginnInZukunft": beginn > date.today(),
            "reisekostenPositiv": kosten > 0
        }

    @worker.task(task_type="search-vn")
    def search_vn(travelInsurance: dict):
        print("VN im Partnersystem suchen...")

        policy_holder = travelInsurance["policyHolder"]
        partnernummer = policy_holder.get("id", "")

        if partnernummer == "":
            return {
                "partnernummerAngegeben": False,
                "partnerMitPartnernummerGefunden": False
            }

        try:
            partner = search_partner_by_number(partnernummer)

            if partner is None:
                return {
                    "partnernummerAngegeben": True,
                    "partnerMitPartnernummerGefunden": False
                }

            return {
                "partnernummerAngegeben": True,
                "partnerMitPartnernummerGefunden": True,
                "partnerAusApi": partner
            }

        except Exception as e:
            print("Fehler bei VN im Partnersystem suchen:", e)
            return {
                "partnernummerAngegeben": True,
                "partnerMitPartnernummerGefunden": False,
                "apiFehler": True
            }

    print("Worker läuft mit Camunda Cloud...")
    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())