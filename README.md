# Loxberry Plugin: SolarEdge-2-MQTT

Loxberry plugin to integrate SolarEdge inverters with Loxone. The plugin polls the SolarEdge cloud API every 5 minutes and publishes the statistics to the local MQTT gateway that must also be installed. The miniserver can read the MQTT topics using virtual inputs.

## Installation

Install this plugin like any other. The MQTT Gateway plugin must be installed as well.

## Configuration

Provide your Solaredge API key, and Site ID in the plugin configuration. 

![](https://raw.githubusercontent.com/strobejb/loxberry-plugin-solaredge2mqtt/assets/se2mqtt-config.png)

## MQTT Topics

The plugin publishes the following inverter data to the MQTT topics below: 

| Topic | Value |
| --- | --- |
| `solaredge_grid_current_power` | Grid power import (or export) | 
| `solaredge_pv_current_power` | Solar power generation | 
| `solaredge_storage_current_power` | Battery power (nagative for charging, positive for drawing) | 
| `solaredge_storage_charge_level` | Battery charge level (percent) | 
| `solaredge_load_current_power` | Power consumption by the house | 

## Miniserver config

To access these values on the miniserver:

* Create a Virtual Input for each value you want to read.
* Set the name of the virtual input to the MQTT topic name (above).
* Set the permissions on each input so that the loxberry user can write to them.

It is suggest to use the new Energy Flow Monitor in Loxone 13.1, and the new meter blocks as follows:

![](https://raw.githubusercontent.com/strobejb/loxberry-plugin-solaredge2mqtt/assets/mqtt-loxone.png)

![](https://raw.githubusercontent.com/strobejb/loxberry-plugin-solaredge2mqtt/assets/energy-flow.png)


