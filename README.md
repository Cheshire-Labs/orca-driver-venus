# Orca Venus Driver

This repository holds the **Orca submethod library** for Hamilton Venus. A Venus method uses it to read the values Orca sends it.

In Orca v2, the Venus driver itself ships with Orca. You do not install anything from this repository except the library. Setup, the pick and place hook Venus methods, volume and tip tracking, and errors are covered in the Orca docs: [Hamilton Venus](https://cheshirelabs.io/docs/orca/venus/).

The Python package `orca-driver-venus` on PyPI is for Orca v1 only. Its last version is tagged [`orca-v1-legacy`](https://github.com/Cheshire-Labs/orca-driver-venus/tree/orca-v1-legacy).

## Submethod library

The library comes in two versions, one per instrument:

- `venus_submethod/mlstar`: Microlab STAR and STARlet.
- `venus_submethod/vantage`: Vantage.

A Venus installation supports one instrument and has only that instrument's Hamilton library. Each version includes its instrument's library, so the other version fails to load with "cannot open include file". Add the version for your instrument to your Venus method in the Venus Method Editor. Both versions have the same file names and functions, so a Venus method's steps are the same on either instrument.

### Hamilton libraries it needs

The library reads Orca's values with Hamilton's HSLJson library, and HSLJson needs Hamilton's ASW Standard library. Venus does not include either one. Install both from Hamilton's download site before you add the Orca library:

- [HSLJson Library v2.0.1](https://download.hamiltonsupport.com/wl/?id=vBtXgHqwGjjLLVzXmtPaxyzkIREcPhAX)
- [ASW Standard v16](https://download.hamiltonsupport.com/wl/?id=VQY0XAzTfcT7KY29A1YJtZVFwZ7GMOO2&path=Hamilton%20Libraries%2FASW%20Standard%20v16.zip&mode=grid)

Without ASW Standard, Venus reports "cannot open include file: 'ASWStandard\TraceLevel\TraceLevel.hsl'" from `HSLJson.hsl`, followed by many `TRACE_LEVEL` errors.

### `ORCA::Initialize(useDefaultValues)`

Call this at the start of the Venus method.

- `0`: read the values Orca sent.
- `1`: ignore Orca and use each call's default value. Use this to run the Venus method in Venus without Orca.

### `GetConfigProperty_Float(propertyName, defaultValue, value)`
### `GetConfigProperty_String(propertyName, defaultValue, value)`
### `GetConfigProperty_Integer(propertyName, defaultValue, value)`

Read one value into a Venus variable.

- `propertyName`: the name of the value in Orca.
- `defaultValue`: used when the Venus method called `ORCA::Initialize(1)`.
- `value`: the Venus variable that receives the value.

## When Orca starts a Venus method

Orca starts a whole Venus method with HxRun, passes it values, and waits for it to run to the end. It never runs part of a Venus method.

A Venus method started by `run_protocol` receives every key of the dictionary passed to it. For example, `run_protocol("MyFolder\\AddBuffer.hsl", {"vol": 50})` gives the Venus method `vol`.

A pick or place hook Venus method receives `labware_name`, `labware_type`, `site` and `barcode`. A missing site or barcode is an empty string.

Every Venus method Orca starts also receives `action`, which says why it was started: `run`, `initialize`, `open`, `close`, `prepare_for_place`, `notify_placed`, `prepare_for_pick` or `notify_picked`. `action` is reserved: a value named `action` passed to `run_protocol` is replaced with `run`.

Each hook has its own setting, so how you organize the Venus methods is up to you:

- **One Venus method per hook.** Each Venus method does one job and can ignore `action`.
- **One Venus method for several hooks.** Set several hooks to the same `.hsl` file. That Venus method reads `action` and uses it to decide what to do. It still runs completely every time it is started.

Orca writes the values to `%TEMP%\CheshireLabs\Orca\actionConfig.json` just before it starts the Venus method, and the library reads them from there.
