# Orca Venus Driver

This repository holds the **ORCA submethod library** for Hamilton Venus. A Venus method uses it to read the values Orca sends it.

In Orca v2, the Venus driver itself ships with Orca. You do not install anything from this repository except the library. Setup, the pick and place hook Venus methods, volume and tip tracking, and errors are covered in the Orca docs: [Hamilton Venus](https://cheshirelabs.io/orca/venus).

The Python package `orca-driver-venus` on PyPI is for Orca v1 only. Its last version is tagged [`orca-v1-legacy`](https://github.com/Cheshire-Labs/orca-driver-venus/tree/orca-v1-legacy).

## Submethod library

The `venus_submethod` folder contains the library. Add it to your Venus method in the Venus Method Editor.

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
