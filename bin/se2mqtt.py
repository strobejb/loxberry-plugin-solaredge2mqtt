import solaredge
import json
import paho.mqtt.client as mqtt #import the client1

import argparse
import sys
import time
import os
import configparser
import json
import logging

def publish_sync(mq, topic, value):
    pr = mq.publish(topic, value, qos=2, retain=True)
    pr.wait_for_publish()

def run(APIKEY, SITEID, mqclient):
    se = solaredge.Solaredge(APIKEY)
    j = se.get_current_power_flow(SITEID)
    print(json.dumps(j, indent=2))

    scpf = j['siteCurrentPowerFlow']
    power = scpf['STORAGE']['currentPower']
    status = scpf['STORAGE']['status']
    if status == 'Charging':
      power = power * -1 

    publish_sync(mqclient, "solaredge/storage/status", status)
    publish_sync(mqclient, "solaredge/storage/current_power", power)
    publish_sync(mqclient, "solaredge/storage/charge_level",  scpf['STORAGE']['chargeLevel'])
    publish_sync(mqclient, "solaredge/grid/current_power",    scpf['GRID']['currentPower'])
    publish_sync(mqclient, "solaredge/pv/current_power",      scpf['PV']['currentPower'])
    publish_sync(mqclient, "solaredge/load/current_power",    scpf['LOAD']['currentPower'])

    return

def main(args):

    if not os.path.exists(args.configfile):
        logging.critical("Plugin configuration file missing {0}".format(args.configfile))
        sys.exit(-1)

    pluginconfig = configparser.ConfigParser()
    pluginconfig.read(args.configfile)
    apikey = pluginconfig.get('SE2MQTT', 'APIKEY')
    siteid = pluginconfig.get('SE2MQTT', 'SITEID')
    enabled = pluginconfig.get('SE2MQTT', 'ENABLED')

    if enabled != "1":
        logging.warning("Plugin is not enabled in configuration - exiting")
        sys.exit(-1)

    configbase = os.environ.get("LBSCONFIG", default="../config")
    configpath = os.path.join(configbase, "general.json")
    logging.info(f'Reading: {configpath}')

    with open(configpath, "r") as f:
        data = json.load(f)

    if not data["Mqtt"]:
        logging.critical("MQTT Broker not found - please check plugin configuration")
        sys.exit(-1)
        
    mqttd = data["Mqtt"]
    logging.info(f'MQTT Broker: {mqttd["Brokeruser"]}@{mqttd["Brokerhost"]}:{mqttd["Brokerport"]}')

    mqclient = mqtt.Client("P1") #create new instance
    mqclient.username_pw_set(username=mqttd["Brokeruser"], password=mqttd["Brokerpass"])
    mqclient.connect(mqttd["Brokerhost"], port=int(mqttd["Brokerport"]))
    mqclient.loop_start()
    
    run(apikey, siteid, mqclient)
    time.sleep(1)
    mqclient.loop_stop()
    mqclient.disconnect()

    # exit with errorlevel 0
    sys.exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Loxberry SolarEdge2MQTT Plugin.")
    parser.add_argument("--logfile", 
                        default="se2mqtt.log",
                        help="specifies logfile path")
    parser.add_argument("--configfile", 
                        default="..\\config\\se2mqtt-test.cfg",
                        help="specifies plugin configuration file path")

    args = parser.parse_args()

    #
    # Configure logging
    #
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(filename=args.logfile,
                        filemode='w', 
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',)

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logging.info("using plugin log file {0}".format(args.logfile))

    # 
    try:
        main(args)
    except Exception as e:
        logging.critical(e, exc_info=True)
