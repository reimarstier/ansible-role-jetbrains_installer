#!/usr/bin/env python
import copy
import json

from ansible.module_utils.urls import open_url
from ansible.plugins.lookup import LookupBase

JETBRAINS_RELEASES = "https://data.services.jetbrains.com/products/releases?code={product_codes}&latest=true&type=release&build="

APP_CODES = {
    "TBA": "Toolbox App",
    "IIU": "IntelliJ IDEA Ultimate",
    "IIC": "IntelliJ IDEA Community",
    "PCC": "PyCharm Community",
    "PCP": "PyCharm Professional",
    "WS": "Webstorm",
    "PS": "PhpStorm",
    "RS": "ReSharper",
    "RD": "Rider",
    "CL": "CLion",
    "DG": "DataGrip",
    "RM": "RubyMine",
    "AC": "AppCode",
    "GO": "GoLand",
    "RC": "ReSharper C++",
    "DP": "ReSharper DotTrace",
    "DM": "ReSharper DotMemory",
    "DC": "ReSharper DotCover",
    "DPK": "ReSharper DotPeek",
    "YTD": "YouTrack",
    "TC": "TeamCity",
    "US": "Upsource",
    "HB": "Hub",
    "MPS": "MPS",
    "PCE": "PyCharm Edu"
}

APP_NAMES = {
    "TBA": "toolbox",
    "IIU": "intellij",
    "IIC": "intellij",
    "PCC": "pycharm",
    "PCP": "pycharm",
    "WS": "webstorm",
    "PS": "phpstorm",
    "RS": "resharper",
    "RD": "rider",
    "CL": "clion",
    "DG": "datagrip",
    "RM": "rubymine",
    "AC": "appcode",
    "GO": "goland",
    "RC": "resharper",
    "DP": "resharper",
    "DM": "resharper",
    "DC": "resharper",
    "DPK": "resharper",
    "YTD": "youtrack",
    "TC": "teamcity",
    "US": "upsource",
    "HB": "hub",
    "MPS": "mps",
    "PCE": "pycharm"
}

binary_paths_override = {
    "IIU": "idea.sh",
    "IIC": "idea.sh",
}

image_paths_override = {
    "IIU": "idea.png",
    "IIC": "idea.png",
}

def clean_meta_data(meta):
    keep = copy.copy(meta)
    delete_keys = ["type", "downloads", "patches", "notesLink", "whatsnew",
                   "uninstallFeedbackLinks"]
    for to_delete in delete_keys:
        try:
            keep.pop(to_delete)
        except KeyError:
            pass
    return keep


def extract_download_link(meta, platform):
    try:
        downloads = {"download": meta["downloads"][platform]["link"]}
    except KeyError:
        downloads = {}
    return downloads


def fetch_releases_data(platform="linux"):
    product_codes = ",".join(APP_CODES.keys())
    response = open_url(JETBRAINS_RELEASES.format(product_codes=product_codes), method="GET")
    releases = json.loads(response.read())

    result = []
    for code, meta in releases.items():
        app = {
            "name": APP_CODES[code],
            "code": code,
            "binary": f"{APP_NAMES[code]}.sh",
            "symlink": APP_NAMES[code],
            "image_name": f"{APP_NAMES[code]}.png"
        }
        app.update(clean_meta_data(meta[0]))
        app.update(extract_download_link(meta[0], platform))
        if code in image_paths_override:
            app["image_name"] = image_paths_override[code]
        if code in binary_paths_override:
            app["binary"] = binary_paths_override[code]

        result.append(app)
    return result


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        return [json.dumps(fetch_releases_data())]


if __name__ == '__main__':
    print(json.dumps(fetch_releases_data(), indent=4))
