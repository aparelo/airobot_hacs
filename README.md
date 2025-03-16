# Airobot thermostat Integration for Home Assistant

This integration adds support for [Airobot smart thermostats](https://airobothome.com/en/smart-thermostat/) to Home Assistant. It has currently only been tested with the standalone 230V thermostat. It should also work with the room controller, but that has not been validated.

# Installation

## Manual installation

Just copy the airobot folder into the custom_components/ folder under your config/ folder in Home Assistant. 

## Installation using HACS

TBD, once I get it published to HACS.


# Set up

## Enabling the local API on your thermostat

First you need to follow the instructions in the official setup guide to connect the thermostat to your Wifi network. The stup guide can be found [here](https://airobothome.com/documents/heating/airobot-heating-thermostat-en.pdf). Installation chapter, step 10.

Once the thermostat has been connected to Wifi you can enable the local api. You can follow the official instructions for that as well. Those can be found [here](https://airobothome.com/documents/heating/airobot-heating-local-api-guide-en.pdf) in the Overview chapter.

## Getting the required credentials

You need the following credentials to set up the integration. Thermostat ID and password. These can be found from the thermostat menu under Settings -> Connectivity -> Mobile app.

Note down the id and password at the bottom of that screen. You can also scan the QR code with your phone to read the credentials.

## Integration setup

The integration can be set up using the Home assistant UI. The config accepts the following parameters

**username:** The username from the previous step

**password:** Password from the previous step

**host (optional)**: The ip address or hostname of the thermostat. Must start with http://. If not provided then the hostname is generated automatically from the username.

# Exposed entities

The integration exposes the following entities for each thermostat.

**climate** - Climate entity for the thermostat. Allows the setting of the target temperature and shows the current temperature and humidity measurements. Also shows the current state of the thermostat (Heating or idle) and allows the changing of modes (HOME, AWAY and BOOST).

**co2_sensor** - Only for thermostats with a CO2 sensor. Shows the current CO2 value.

**aqi_sensor** - Only for thermostats with a CO2 sensor. Shows the current AQI value.

**device_uptime_sensor** - Shows the thermostat uptime in seconds

**heating_uptime_sensor** - Shows the heating uptime in seconds

**errors_sensor** - Shows if there are any errors detected. 0 means no errors and any value above 0 means that is an error. Unfortunately the exact error codes are not documented.

**reboot_button** - Button to reboot the thermostat

**recalibrate_co2_button** - Button to reclibrate the CO2 sensor.

**actuator_exercise_disabled_switch** - Switch to disable the actuator exercise mode.

**childlock_enabled_switch** - Switch to enable and disable the child lock.
