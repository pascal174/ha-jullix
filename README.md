# Jullix EMS — Home Assistant Custom Integration

Een HACS-compatibele custom integration voor het Jullix energiebeheersysteem.

## Functionaliteit

- **Lokale polling** (geen internet nodig) van de Jullix gateway
- **Optionele cloud-data** via de Jullix platform-API
- Alle entities gegroepeerd onder één **Jullix EMS** device
- Configuratie volledig via de UI (geen YAML nodig)

## Sensors (lokaal)

| Sensor | Eenheid |
|--------|---------|
| Solar Power | W |
| Solar Energy Total | kWh |
| Battery Power | W |
| Battery SOC | % |
| Battery Voltage | V |
| Energy Charged | kWh |
| Energy Discharged | kWh |
| Grid Power In | W |
| Grid Power Out | W |
| Net Power | W |
| Energy Import T1/T2 | kWh |
| Energy Export T1/T2 | kWh |
| Voltage L1/L2/L3 | V |
| Water Usage | m³ |
| EV Charger Power | W |
| EV Battery SOC | % |
| EV Charger Temperature | °C |
| EV Max Current | A |
| EV Charger State | - |

## Binary sensors (lokaal)

| Sensor | Klasse |
|--------|--------|
| EV Charger Occupied | occupancy |
| EV Three Phase Active | power |
| Battery Fault | problem |
| Solar Fault | problem |

## Installatie

### Via HACS
1. Voeg deze repository toe als custom repository in HACS
2. Installeer "Jullix EMS"
3. Herstart Home Assistant

### Manueel
1. Kopieer de map `custom_components/jullix` naar je HA `custom_components` map
2. Herstart Home Assistant

## Configuratie

1. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen**
2. Zoek op "Jullix"
3. Vul het IP-adres in van je Jullix gateway (standaard: `192.168.2.150`)
4. Optioneel: schakel cloud-data in en vul je installatie-ID en API-token in
   - Token aanmaken via [mijn.jullix.be](https://mijn.jullix.be) → Profiel → API-tokens

## Vereisten

- Home Assistant 2024.1 of nieuwer
- Jullix gateway bereikbaar op het lokale netwerk
