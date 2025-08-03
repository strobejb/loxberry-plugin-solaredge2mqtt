# Loxberry Plugin: SolarEdge-2-MQTT

Loxberry plugin to integrate SolarEdge inverters with Loxone. The plugin polls the SolarEdge cloud API every 5 minutes and publishes the statistics to the local MQTT gateway that must also be installed. The miniserver can read the MQTT topics using virtual inputs.

## Installation

Install this plugin like any other. If you are using Loxberry 2.x then the MQTT Gateway plugin must be installed as well.

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

The plugin publishes to the `solaredge/#` topic. Set up an MQTT subscription on your loxberry for this topic (http://loxberry/admin/system/mqtt-gateway.cgi?form=subscriptions)

## Miniserver config

To access these values on the miniserver:

* Create a Virtual Input for each value you want to read.
* Set the name of the virtual input to the MQTT topic name (above).
* Set the permissions on each input so that the loxberry user can write to them.

It is suggest to use the new Energy Flow Monitor in Loxone 13.1, and the new meter blocks as follows:

![](https://raw.githubusercontent.com/strobejb/loxberry-plugin-solaredge2mqtt/assets/mqtt-loxone.png)

![](https://raw.githubusercontent.com/strobejb/loxberry-plugin-solaredge2mqtt/assets/energy-flow.png)



## Testing & Development

Testing the python component is possible on Windows / Linux:

1. Copy `config/se2mqtt.py` to `config/se2mqtt-test.py`
2. Set the appropriate values for `APIKEY` and `SITEID` in the new `se2mqtt-test.py` and set `ENABLED=1`
3. Create a new file `config/general.json` with the following content:
```
{
    "Mqtt": {
        "Brokeruser": "MQTT Server User",
        "Brokerpass": "<MQTT Server Password
>",
        "Brokerport": <MQTT Server Port>,
        "Brokerhost": "<MQTT Server IP>"
    }
}
```
Obtain all the above values from the MQTT settings page on your loxberry (https://loxberry/admin/system/mqtt.cgi)

4. `cd` to  the `bin` directory
4. Run `pip install -r requirements.txt` 
5. Run `python se2mqtt.py` 

The python script will read the SolarEdge data using the configured API & SiteID, and will publish to the `solaredge/#` topic. It will also display the result to stdout. 

When the plugin runs on Loxberry, it is invoked using a CRON-job every 5 minutes.
