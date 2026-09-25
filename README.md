# G502 X DPI

A small personal tool for my Logitech G502 X LIGHTSPEED, built using [OpenLogi](https://github.com/AprilNEA/OpenLogi) as the HID++ protocol reference. This is an independent Python implementation; OpenLogi is not a runtime dependency.

## Version 1

- Minimal dark web UI with numeric DPI input.
- Mouse discovery, connection status, current DPI, and device-reported range/step.
- DPI validation, apply, read-back confirmation, and error messages.
- Local Python backend using `hidapi`, restricted to loopback with same-origin write checks.

Targets the `046D:C547` receiver and identifies the mouse by its reported name. No button remapping, macros, or onboard profile saving yet.

## Run

Requires Windows and Python 3.12+. From the repository root:

```powershell
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r module/Backend/requirements.txt
& ./.venv/Scripts/python.exe module/Backend/Src/Server.py
```

Open [http://127.0.0.1:8765](http://127.0.0.1:8765). Use this address rather than `localhost`. Stop with Ctrl+C. Pass `--port 8766` to change the port, or `--probe` for read-only discovery without starting the web server.

If the mouse is unreachable, wake it and retry discovery; close G HUB if access conflicts occur.

## Agent guide

- `module/Frontend/`: plain HTML, CSS, and JavaScript; no build step.
- `module/Backend/Src/`: HTTP routes, device service, HID transport, and HID++ protocol.
- `module/Api/OpenApi.yaml`: API contract.
- `Docs/`: architecture, protocol details, and third-party notices.
- `Scripts/Start.ps1`: optional launcher.
- Use PascalCase for custom names and `/` in paths. Preserve standard library and tool-required names. Keep code comments in Chinese.
- Keep changes in the current task. Do not leave test code or change real device settings without a requested value.

## Hardware status

Read-only discovery confirmed G502 X LIGHTSPEED at 800 DPI, with a 100–25600 range and step 50. Intermittent unreachable responses were also observed. Real-device DPI writes and power-cycle persistence have not been verified. Version 1 changes the current DPI only; G HUB or onboard profiles may override it.

## Credits

Thanks to [OpenLogi](https://github.com/AprilNEA/OpenLogi) for the protocol reference. Attribution and licensing details: [ThirdPartyNotices](Docs/ThirdPartyNotices.md). Implementation notes: [ProtocolNotes](Docs/ProtocolNotes.md).
