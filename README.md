<div style="display: flex; align-items: center;">
  <img width="150" alt="home-assistant-wordmark-vertical-color-on-light" src="https://github.com/dgtal1/extalife_custom_component/assets/27864579/491d9e84-822f-4947-bf9e-805f16900401">
  <a href="https://www.forumextalife.pl/" style="margin-left: 10px;">
    <img src="https://yt3.ggpht.com/ytc/AKedOLRdji2oMcII8lorhHubp4V0mptIxdYMYJf25crN=s176-c-k-c0x00ffffff-no-rj" alt="ExtaLife Logo" width="200"/>
  </a>
</div>
<p></p>

ZAMEL Exta Life integration with Home Assistant based on custom component.
### Supported devices
* Switches: ROP-21, ROP-22, ROM-24
* Dimmers: RDP-21
* LED controllers: SLR-21, SLR-22
* Smart sockets: ROG-21
* Roller blind controllers: SRP-22, SRM-22
* Heating controller: RGT-01, GKN-01
* Sensors: RCT-21, RCT-22, RNK-21&RNK-22 built-in temperature sensor, flood sensor RCZ-21, motion sensor RCR-21, window sensor RCK-21, multisensor RCM-21, 3-phase energy meter MEM-21

### Exta Free supported devices (via EFC-01 controller):
* Switches: ROP-01, ROP-02, ROP-05, ROP-06, ROP-07, ROM-01, ROM-10
* Dimmers: RDP-01, RDP-02, RDP-11
* Smart sockets: RWG-01
* Roller blind controllers: SRP-02, SRP-03, ROB-01

**Note:** Certain switches are mapped into Home Asistant light entities depending on icon assigned to them. This is to support voice control by Google Assistant and others and because switches are mostly used for light control.
### Setup
Make sure you copied the integration to `custom_components` folder in your `config` directory.
The integration is setup from Home Assistant GUI (Integrations screen). Search for "Exta Life" on the list of possible integrations. If it's not visible - clear your browser chache and refresh page.
The integration supports Integration Options - search for it on the Exta Life integration badge in Integrations GUI.

Discussion, news and many more on https://www.forumextalife.pl/

<a href="https://buycoffee.to/dgtal1" target="_blank"><img src="https://buycoffee.to/btn/buycoffeeto-btn-primary.svg" style="width: 159px" alt="But me a coffee with buycoffee.to"></a>
