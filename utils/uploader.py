from Shinomiya.Src.logger import *
import requests
import json
import os
import re


class Akira:
    def __init__(self, token, cookie):
        self._find_path_re = r'path:\s+"(/[^"]+)"'
        self._set(token, cookie)
        self._regenerate()

    def _regenerate(self):
        self._headers = {
            "Cookie": self._cookie
        }
        self._upload_page_url = "https://cloud.tsinghua.edu.cn/u/d/{}/".format(self._token)
        self._query_upload_url = "https://cloud.tsinghua.edu.cn/api/v2.1/upload-links/{}/upload/".format(self._token)
        iprint("Upload page url set to {}".format(self._upload_page_url))
        iprint("Query upload url set to {}".format(self._query_upload_url))

    def _set(self, _token, _cookie):
        assert _token is not None, "Token must be filled"
        assert _cookie is not None, "Cookie must be filled"
        self._token = _token
        self._cookie = _cookie

    def _check_health(self):
        health_response = requests.get(self._upload_page_url, headers=self._headers)
        if health_response.status_code == 200:
            iprint("Upload page valid.")
            content = health_response.content.decode("UTF-8")
            match = re.search(self._find_path_re, content)
            if match:
                self._parent_dir = match.group(1)
                iprint("Extracted parent dir: {}".format(self._parent_dir))
            else:
                eprint("Cannot locate parent dir in the HTML content.")
                eprint("You have to specify the parent dir when posting")
                self._parent_dir = None
            return True
        else:
            eprint("Upload page invalid, check your token.")
            return False

    def _get_upload_link(self):
        if not self._check_health():
            return False
        query_response = requests.get(self._query_upload_url, headers=self._headers)
        if not query_response.status_code == 200:
            eprint("Get upload link failed with code {}".format(query_response.status_code))
            eprint(query_response.content)
            return False
        response = json.loads(query_response.content)
        self._upload_link = response["upload_link"]
        iprint("Successfully got upload link {}".format(self._upload_link))
        return True

    def set(self, token, cookie):
        self._set(token, cookie)
        self._regenerate()

    def upload(self, path_to_file, parent_dir=None):
        assert self._get_upload_link()
        assert os.path.exists(path_to_file), "{} not exists".format(path_to_file)
        assert self._parent_dir is not None or parent_dir is not None, "A parent dir should be filled"
        file_parent_dir = self._parent_dir if self._parent_dir else parent_dir
        files = {
            "file": (path_to_file, open(path_to_file, "rb"), "application/octet-stream"),
            "parent_dir": (None, file_parent_dir),
        }
        response = requests.post(self._upload_link, headers=self._headers, files=files)
        if not response.status_code == 200:
            eprint("Upload failed with code {}".format(response.status_code))
            eprint(response.content)
            return
        iprint("Successfully uploaded {} to {}".format(path_to_file, file_parent_dir))
