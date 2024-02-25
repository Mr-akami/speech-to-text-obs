"""
ref: https://knowledge.sakura.ad.jp/34497/
ref: https://qiita.com/sylphy_00/items/02c7a21a53966b1753b0
"""

import obsws_python as obs
import re

OBS_PASSWORD = "mystrongpassword"
TARGET_SOURCE_NAME = "Browser"
CSS_TEMPLATE_PATH = "static/subtitle.css"
with open(CSS_TEMPLATE_PATH) as f:
    CSS_TEMPLATE = f.read()


class ObsClient:

    def __init__(self):
        self.obscl = obs.ReqClient(host="localhost", port=4455, password=OBS_PASSWORD)

        with open(CSS_TEMPLATE_PATH) as f:
            css_template = f.read()
        self.css = re.sub(" content: .*;", ' content: "Hello, World!";', css_template)

    def send_to_obs(self, message):
        # ws = obs.obsws(OBS_PASSWORD)
        # ws.connect()
        # ws.call(obs.requests.SetTextGDIPlusProperties(TARGET_SOURCE_NAME, text=message, css=CSS_TEMPLATE))
        # ws.disconnect()
        # css = re.sub(' content: ".*";', f' content: "{message}";', CSS_TEMPLATE)
        css = re.sub(" content: .*;", ' content: "' + message + '";', CSS_TEMPLATE)
        print(css)
        try:
            obscl.set_input_settings(TARGET_SOURCE_NAME, {"css": css}, True)
        except Exception as e:
            print("Failed to set input settings:", e)
            exit()

    def run(self):
        # obscl = obs.ReqClient(host="localhost", port=4455, password=OBS_PASSWORD)
        # obscl.toggle_input_mute('Mic/Aux')
        message = "Hello, World!"
        css = re.sub(" content: .*;", ' content: "' + message + '";', CSS_TEMPLATE)
        self.obscl.set_input_settings(TARGET_SOURCE_NAME, {"css": css}, True)
        # self.send_to_obs("Hello, World!!!!!")


# try:
#     obscl = obs.ReqClient(host="localhost", port=4455, password=OBS_PASSWORD)
#     # obscl.toggle_input_mute('Mic/Aux')
# except Exception as e:
#     print("Failed to connect to OBS:", e)
#     exit()
