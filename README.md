# REISEKRANKENVERSICHERUNG
# 🛡️ Reisekrankenversicherung - Prozessautomatisierung mit Camunda 8

Dieses Repository enthält die vollständige **End-to-End-Automatisierung** eines Antragsprozesses für eine Reisekrankenversicherung. Das Projekt demonstriert eindrucksvoll die nahtlose Integration von modellgetriebener Prozesssteuerung (**BPMN**), komplexer Entscheidungslogik (**DMN**) und modernen Microservice-Architekturen (**Python Zeebe Worker** & **REST-APIs**).

Entwickelt von **Team G1** an der **TU Dortmund**.

---

## 📑 Inhaltsverzeichnis
1. [Projektbeschreibung](#-projektbeschreibung)
2. [Highlights & Features](#-highlights--features)
3. [Technologie-Stack](#-technologie-stack)
4. [Architektur & Projektstruktur](#-architektur--projektstruktur)
5. [Geschäftslogik (DMN)](#-geschäftslogik-dmn)
6. [Human-in-the-Loop](#-human-in-the-loop)
7. [Installation & Setup](#-installation--setup)

---

## 📖 Projektbeschreibung
Das Ziel dieses Projekts ist die Überführung eines manuellen, zeitaufwändigen Versicherungsprozesses in einen hocheffizienten, automatisierten Workflow. 
Sobald ein Kunde einen Antrag stellt, wird dieser vollständig digital verarbeitet. Dies umfasst die Validierung der Reisedaten, die Währungsumrechnung, Bonitäts- und Sicherheitsprüfungen, das Partnerdaten-Management (Suche und Neuanlage) sowie die finale Policierung und den Versand der Vertragsunterlagen.

## ✨ Highlights & Features
* **Straight-Through Processing (STP):** Fehlerfreie Anträge durchlaufen den Prozess in wenigen Sekunden komplett dunkelverarbeitet (automatisiert).
* **API-First Ansatz:** * *Externe APIs:* Anbindung der Frankfurter API (Währungsumrechnung), API-Ninjas (Telefonnummern-Validierung) und des Auswärtigen Amtes (Reisewarnungen).
  * *Interne APIs:* Anbindung von simulierten Backend-Systemen für Partnerverwaltung (`Partner-API`) und Vertragsmanagement (`Insurance-Policy-API`).
* **Out-of-the-Box Connectoren:** Nutzung nativer Camunda Connectoren (HTTP JSON, SendGrid/Mailtrap) für effiziente API-Calls und automatisierte E-Mail-Kommunikation.
* **Fehlertoleranz:** Integrierte Retry-Mechanismen und Timeouts (z.B. bei API-Ausfällen).

## 🛠️ Technologie-Stack
* **Prozess-Engine:** Camunda 8 Cloud (SaaS)
* **Modellierung:** Camunda Web Modeler (BPMN 2.0, DMN 1.3, Camunda Forms)
* **Backend / Worker:** Python 3.10+
* **Zeebe Client:** `pyzeebe`
* **Kommunikation:** RESTful APIs, gRPC (Zeebe)

## 🏗️ Architektur & Projektstruktur
Die Business-Logik ist vom Prozessablauf entkoppelt. Camunda Cloud orchestriert den Ablauf, während der lokal (oder in der Cloud) laufende Python-Worker die eigentlichen Service Tasks ausführt.

```text
📦 reisekrankenversicherung
 ┣ 📂 models/                 # Camunda Modelle
 ┃ ┣ 📜 reisekrankenversicherung_prozess.bpmn
 ┃ ┣ 📜 Alter_Wohnort_Personen_pruefen.dmn
 ┃ ┣ 📜 Selbstbehalt_bestimmen.dmn
 ┃ ┗ 📜 *.form                # Camunda Forms (Benutzeroberflächen)
 ┣ 📂 src/                    # Python Worker Code
 ┃ ┣ 📜 main.py               # Einstiegspunkt, startet Worker & Cloud-Channel
 ┃ ┣ 📜 config.py             # Konfigurationsdatei (Credentials, URLs)
 ┃ ┣ 📜 tasks.py              # Registrierung der Camunda Service Tasks (@worker.task)
 ┃ ┣ 📜 partner_api.py        # Logik für das Partner-System (Suchen/Anlegen)
 ┃ ┣ 📜 insurance_api.py      # Logik für Vertragsablage & Dokumentenversand
 ┃ ┗ 📜 utils.py              # Hilfsfunktionen (z.B. Daten-Normalisierung)
 ┗ 📜 README.md
