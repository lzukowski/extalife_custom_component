import logging
from pprint import pformat

# from homeassistant.components.extalife import ExtaLifeChannel
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature, DOMAIN as DOMAIN_CLIMATE
from homeassistant.components.climate.const import (
    HVACAction,
    HVACMode,
)
from homeassistant.core import HomeAssistant

from . import ExtaLifeChannel
from .helpers.const import DOMAIN_VIRTUAL_CLIMATE_SENSOR
from .helpers.core import Core
from .pyextalife import ExtaLifeAPI             # pylint: disable=syntax-error

_LOGGER = logging.getLogger(__name__)


# Exta Life logic
# set temp: set state to 1. Controller returns state = 0. State = 0 means work_mode should be set to false
# set auto: set state to 0. Controller returns state = 1. State = 1 means work_mode should be set to true

# map Exta Life "work_mode" field
EXTA_HVAC_MODE = {
    True: HVACMode.AUTO,
    False: HVACMode.HEAT,
}

# map Exta Life notification "state" field
EXTA_STATE_HVAC_MODE = {
    1: HVACMode.AUTO,
    0: HVACMode.HEAT,
}

# map Exta Life "work_mode" field
HVAC_MODE_EXTA = {
    HVACMode.AUTO: True,
    HVACMode.HEAT: False
}

# map Exta Life "power" field
EXTA_HVAC_ACTION = {
    1: HVACAction.HEATING,
    0: HVACAction.IDLE
}

# map HA action to Exta Life "state" field
HVAC_ACTION_EXTA = {
    HVACAction.HEATING: 1,
    HVACAction.IDLE: 0
}

# map HA HVAC mode to Exta Life action
HA_MODE_ACTION = {
    HVACMode.AUTO: ExtaLifeAPI.ACTN_SET_RGT_MODE_AUTO,
    HVACMode.HEAT: ExtaLifeAPI.ACTN_SET_RGT_MODE_MANUAL
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """setup via configuration.yaml not supported anymore"""

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up an Exta Life heat controllers """

    core = Core.get(config_entry.entry_id)
    channels = core.get_channels(DOMAIN_CLIMATE)

    _LOGGER.debug("Discovery: %s", pformat(channels))
    async_add_entities([ExtaLifeClimate(device, config_entry) for device in channels])

    core.pop_channels(DOMAIN_CLIMATE)

class ExtaLifeClimate(ExtaLifeChannel, ClimateEntity):
    """Representation of Exta Life Thermostat."""

    def __init__(self, channel_data, config_entry: ConfigEntry):
        super().__init__(channel_data, config_entry)

        self.push_virtual_sensor_channels(DOMAIN_VIRTUAL_CLIMATE_SENSOR, channel_data)

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def max_temp(self):
        return 50

    @property
    def min_temp(self):
        return 5

    @property
    def target_temperature_step(self):
        return 0.5

    @property
    def precision(self):
        return 0.5

    @property
    def hvac_action(self):
        # for now there's no data source to show it. data.power does not reflect this information
        return None

    @property
    def hvac_mode(self):
        return EXTA_HVAC_MODE.get(self.channel_data.get("work_mode"))

    @property
    def hvac_modes(self):
        return [HVACMode.AUTO, HVACMode.HEAT]

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode (heat, auto => manual, auto)."""
        if await self.async_action(HA_MODE_ACTION.get(hvac_mode), value=self.channel_data.get("value")):
            self.channel_data["work_mode"] = HVAC_MODE_EXTA.get(hvac_mode)
            self.async_schedule_update_ha_state()

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return float(int(self.channel_data.get("temperature")) / 10.0)

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return float(self.channel_data.get("value") / 10.0)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperatures."""
        temperature = kwargs.get(ATTR_TEMPERATURE)

        if temperature is None:
            return
        temp_el = temperature * 10.0

        if await self.async_action(ExtaLifeAPI.ACTN_SET_TMP, value=temp_el):
            self.channel_data["value"] = temp_el
            self.channel_data["work_mode"] = HVAC_MODE_EXTA[HVACMode.HEAT]
            self.async_schedule_update_ha_state()

    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        attr = super().extra_state_attributes
        if attr is None:
            attr = {}
        data = self.channel_data
        attr.update(
            {
                "waiting_to_synchronize": data.get("waiting_to_synchronize"),
                "temperature_old": data.get("temperature_old")
            }
        )

        return attr

    def on_state_notification(self, data):
        """ React on state notification from controller """
        state = data.get("state")

        ch_data = self.channel_data.copy()
        ch_data["work_mode"] = True if state == 1 else False
        ch_data["value"] = data.get("value")        # update set (target) temperature

        # update only if notification data contains new status; prevent HA event bus overloading
        if ch_data != self.channel_data:
            self.channel_data.update(ch_data)

            # synchronize DataManager data with processed update & entity data
            self.sync_data_update_ha()
