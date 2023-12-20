"""Lib setup"""

from equationsdk.equation_api import EquationAPI
from equationsdk.device import EquationDevice
from equationsdk.dto import EnergyConsumptionData
from equationsdk.model import *

username = "philipelizp+equation@gmail.com"
password = "gagveb-byzto0-Pifxub"

def handle_error_and_exit(resp):
    print("Error: {}".format(resp.error_message))
    exit(1)

def create_device(
    device_data,
    device_id: str
) -> EquationDevice:
    """Process a device from the API and add or update it.

    Return the device if it's new or None if it's an existing one.
    """

    device_data_data = device_data.get("data", None)

    if not device_data_data:
        return None

    # New device.
    return EquationDevice(
        device_info=device_data,
        device_id=device_id,
        energy_data=None,
        latest_fw=None,
    )

if __name__ == '__main__':
    api = EquationAPI(username, password)
    api.initialize_authentication()
    resp = api.get_installations()
    if not resp.success:
        handle_error_and_exit(resp)

    insts = resp.data
    for inst_id in insts:
        resp = api.get_installation_devices(inst_id)
        latest_fw = api.get_latest_firmware()

        if not resp.success:
            handle_error_and_exit(resp)

        devs = resp.data
        print(devs)

        for dev_id in devs:
            resp = api.get_device(dev_id)
            if not resp.success:
                handle_error_and_exit(resp)
            
            dev = create_device(resp.data, dev_id)
            print(dev.name, dev.power, dev.mode, dev.preset, dev.temp)
            print(resp.data)
            print()
