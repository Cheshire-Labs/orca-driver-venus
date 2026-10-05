# Orca Venus Driver

This repository holds the **ORCA submethod library** for Hamilton Venus. A Venus method uses it to read the values Orca sends it.

In Orca v2, the Venus driver itself ships with Orca. You do not install anything from this repository except the library. Setup, the pick and place hook methods, volume and tip tracking, and errors are covered in the Orca docs: [Hamilton Venus](https://cheshirelabs.io/orca/venus).

The Python package `orca-driver-venus` on PyPI is for Orca v1 only. Its last version is tagged [`orca-v1-legacy`](https://github.com/Cheshire-Labs/orca-driver-venus/tree/orca-v1-legacy).

## Submethod library

The `venus_submethod` folder contains the library. Add it to your method in the Venus Method Editor.

### `ORCA::Initialize(useDefaultValues)`

Call this at the start of the method.

- `0`: read the values Orca sent.
- `1`: ignore Orca and use each call's default value. Use this to run the method in Venus without Orca.

### `GetConfigProperty_Float(propertyName, defaultValue, value)`
### `GetConfigProperty_String(propertyName, defaultValue, value)`
### `GetConfigProperty_Integer(propertyName, defaultValue, value)`

Read one value into a Venus variable.

- `propertyName`: the name of the value in Orca.
- `defaultValue`: used when the method called `ORCA::Initialize(1)`.
- `value`: the Venus variable that receives the value.

## Values a method receives

A method run by `run_protocol` receives every key of the dictionary passed to it, for example `run_protocol("MyFolder\\AddBuffer.hsl", {"vol": 50})` gives the method `vol`.

A pick or place hook method receives `action`, `labware_name`, `labware_type`, `site` and `barcode`. Read them all with `GetConfigProperty_String`. A missing site or barcode is an empty string.

Every method Orca starts also receives `action`, which says why it ran: `run`, `initialize`, `open`, `close`, `prepare_for_place`, `notify_placed`, `prepare_for_pick` or `notify_picked`. Each hook can name its own method, and then the method can ignore `action`. To handle several hooks in one method, point them at the same `.hsl` file, read `action` with `GetConfigProperty_String`, and branch on it with an If statement. `action` is reserved: a value named `action` passed to `run_protocol` is replaced with `run`.

Orca writes the values to `%TEMP%\CheshireLabs\Orca\actionConfig.json` just before it starts the method, and the library reads them from there.
