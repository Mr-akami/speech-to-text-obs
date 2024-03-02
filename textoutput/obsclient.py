"""
ref: https://knowledge.sakura.ad.jp/34497/
ref: https://qiita.com/sylphy_00/items/02c7a21a53966b1753b0
"""

import obsws_python as obs
import re

OBS_PASSWORD = "mystrongpassword"
TARGET_SOURCE_NAME = "Browser"
CSS_TEMPLATE_PATH = "static/subtitle.css"


class ObsClient:

    def __init__(self):
        self.obscl = obs.ReqClient(host="localhost", port=4455, password=OBS_PASSWORD)

        with open(CSS_TEMPLATE_PATH) as f:
            css_template = f.read()
        self.css_template = css_template
        self.css = re.sub(" content: .*;", ' content: "Hello, World!";', css_template)

    def send_message(self, message):
        css = re.sub(" content: .*;", ' content: "' + message + '";', self.css_template)
        try:
            self.obscl.set_input_settings(TARGET_SOURCE_NAME, {"css": css}, True)
        except Exception as e:
            print("Failed to send message to OBS:", e)
            
# try:
#     obscl = obs.ReqClient(host="localhost", port=4455, password=OBS_PASSWORD)
#     # obscl.toggle_input_mute('Mic/Aux')
# except Exception as e:
#     print("Failed to connect to OBS:", e)
#     exit()
