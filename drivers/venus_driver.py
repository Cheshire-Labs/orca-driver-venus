from core.drivers.driver_interfaces import ILabwarePlaceableDriver


import subprocess
from typing import Any, Dict, Optional


class VenusProtocolDriver(ILabwarePlaceableDriver):

    def __init__(self, name: str):
        self._name = name
        self._exe_path = r"C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe"
        self._is_initialized = False
        self._is_running = False
        self._init_protocol = "initialize.hsl"
        self._picked_protocol = "picked.hsl"
        self._placed_protocol = "placed.hsl"
        self._prepare_pick_protocol = "prepare_pick.hsl"
        self._prepare_place_protocol = "prepare_place.hsl"

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_initialized(self) -> bool:
        return self._is_initialized

    def set_init_options(self, init_options: Dict[str, Any]) -> None:
        self._init_options = init_options
        if "init-protocol" in self._init_options.keys():
            self._init_protocol = self._init_options["init-protocol"]
        if "hxrun-path" in self._init_options.keys():
            self._exe_path = self._init_options["hxrun-path"]
        if "picked-protocol" in self._init_options.keys():
            self._picked_protocol = self._init_options["picked-protocol"]
        if "placed-protocol" in self._init_options.keys():
            self._placed_protocol = self._init_options["placed-protocol"]
        if "prepare-pick-protocol" in self._init_options.keys():
            self._prepare_pick_protocol = self._init_options["prepare-pick-protocol"]
        if "prepare-place-protocol" in self._init_options.keys():
            self._prepare_place_protocol = self._init_options["prepare-place-protocol"]

    async def initialize(self) -> None:
        await self.execute("run", {"method": self._init_protocol})
        self._is_initialized = True

    @property
    def is_running(self) -> bool:
        return self._is_running

    async def prepare_for_place(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        await self.execute("run", {"method": self._prepare_place_protocol})

    async def prepare_for_pick(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        await self.execute("run", {"method": self._prepare_pick_protocol})

    async def notify_picked(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        await self.execute("run", {"method": self._picked_protocol})

    async def notify_placed(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        await self.execute("run", {"method": self._placed_protocol})

    async def execute(self, command: str, options: Dict[str, Any]) -> None:
        if command == "run":
            if 'method' not in options.keys():
                raise KeyError("The venus method was not provided in the command options")
            method = options["method"]
            self._execute_protocol(method)
        else:
            raise NotImplementedError(f"The action '{command}' is unknown for {self._name} of type {type(self).__name__}")

    def _execute_protocol(self, hsl_path: str) -> None:
        try:
            self._is_running = True
            subprocess.run([self._exe_path, "-t", hsl_path], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        finally:
            self._is_running = False