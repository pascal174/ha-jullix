# Jullix EMS — Home Assistant Custom Integration

> ⚠️ **Disclaimer:** This is an unofficial, community-made integration.
> It is **not** affiliated with, endorsed by, or supported by Jullix.
> For official Jullix support, visit [mijn.jullix.be](https://mijn.jullix.be).

A HACS-compatible custom integration for the Jullix energy management system.

## Features

- **Local polling** — fast and reliable, no internet required
- **Optional cloud data** — additional details via the Jullix platform API
- All entities grouped under one **Jullix EMS** device
- Fully configurable via the UI — no YAML required

## Local Sensors

| Sensor | Unit |
|--------|------|
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
| Energy Import T1 | kWh |
| Energy Import T2 | kWh |
| Energy Export T1 | kWh |
| Energy Export T2 | kWh |
| Voltage L1 | V |
| Voltage L2 | V |
| Voltage L3 | V |
| Water Usage | m³ |
| EV Charger Power | W |
| EV Battery SOC | % |
| EV Charger Temperature | °C |
| EV Max Current | A |
| EV Charger State | — |

## Local Binary Sensors

| Sensor | Class |
|--------|-------|
| EV Charger Occupied | occupancy |
| EV Three Phase Active | power |
| Battery Fault | problem |
| Solar Fault | problem |

## Installation

### Via HACS
1. Add this repository as a custom repository in HACS
2. Install "Jullix EMS"
3. Restart Home Assistant

### Manual
1. Copy the `custom_components/jullix` folder to your HA `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for "Jullix"
3. Enter the IP address of your Jullix gateway (default: `192.168.2.150`)
4. Optional: enable cloud data and enter your installation ID and API token
   - Create a token at [mijn.jullix.be](https://mijn.jullix.be) → Profile → API tokens

## Requirements

- Home Assistant 2024.1 or newer
- Jullix gateway reachable on your local network

## Contributing

Pull requests are welcome! Please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)