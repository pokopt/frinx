"""Handles reading iface configuration."""
import json


def extractor(group_name, iface_config):
    """Extract all iface information from provided config."""
    extracted = {}
    try:
        extracted["name"] = group_name + str(iface_config["name"])
    except KeyError as excpt:
        print(excpt)
        return None

    try:
        extracted["description"] = iface_config["description"]
    except KeyError:
        extracted["description"] = None

    try:
        extracted["max_frame_size"] = iface_config["mtu"]
    except KeyError:
        extracted["max_frame_size"] = None

    try:
        extracted["port_channel_id"] = iface_config[
            "Cisco-IOS-XE-ethernet:channel-group"
        ]["number"]
    except KeyError:
        extracted["port_channel_id"] = None

    extracted["config"] = iface_config
    return extracted


extractors = {
    "Port-channel": lambda config: extractor("Port-channel", config),
    "GigabitEthernet": lambda config: extractor("GigabitEthernet", config),
    "TenGigabitEthernet": lambda config: extractor("TenGigabitEthernet", config),
}


def extract_ifaces(input_file):
    """Find iface config in provided input file and process it."""
    extracted_ifaces = []
    with open(input_file, "r") as in_file:
        content = json.load(in_file)
        ifaces = content["frinx-uniconfig-topology:configuration"][
            "Cisco-IOS-XE-native:native"
        ]["interface"]
        for iface_group, extract_fction in extractors.items():
            for iface in ifaces[iface_group]:
                extracted_ifaces.append(extract_fction(iface))

    return extracted_ifaces
