#!/usr/bin/env python
import copy
import json

import requests
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

binary_paths = {
    "IIU": "idea.sh",
    "IIC": "idea.sh",
    "PCC": "pycharm.sh",
    "PCP": "pycharm.sh",
    "WS": "webstorm.sh",
    "RM": "rubymine.sh",
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


def determine_binary_path(code):
    try:
        return {
            "binary": binary_paths[code],
            "symlink": APP_NAMES[code],
        }
    except KeyError:
        return {}


def fetch_releases_data(platform="linux"):
    product_codes = ",".join(APP_CODES.keys())
    response = requests.get(
        JETBRAINS_RELEASES.format(product_codes=product_codes))
    releases = response.json()

    result = []
    for code, meta in releases.items():
        app = {
            "name": APP_CODES[code],
            "code": code,
        }
        app.update(clean_meta_data(meta[0]))
        app.update(extract_download_link(meta[0], platform))
        app.update(determine_binary_path(code))
        result.append(app)
    return result


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        return [json.dumps(fetch_releases_data())]


if __name__ == '__main__':
    print(json.dumps(fetch_releases_data(), indent=4))
