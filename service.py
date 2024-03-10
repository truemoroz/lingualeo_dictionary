#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
# import urllib2
# from urllib.request import build_opener, HTTPCookieProcessor
# from urllib.parse import urlencode
import json
import requests
# from http.cookiejar import CookieJar
# from cookielib import CookieJar


class Lingualeo:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        # self.cj = CookieJar()
        self.cookies = {}

    def auth(self):
        url = "https://lingualeo.com/api/auth"
        values = {
            "type": "mixed",
            "credentials": {
                "email": self.email,
                "password": self.password
            }
        }
        response = self.get_content(url, values)
        self.cookies = {
            "remember": response["accessToken"],
            "userId": str(response["userId"])
        }
        # return self.get_content(url, values)

    # def add_word(self, word, tword, context):
    def add_word(self, word, tword):
        url = "https://api.lingualeo.com/SetWords"
        # values = {
        #     "word": word,
        #     "tword": tword,
        #     "context": context,
        # }
        values = {
            "apiVersion": "1.0.1",
            "op": "actionWithWords {action: add}",
            "data": [
                {
                    "action": "add",
                    "mode": "0",
                    "wordIds": "null",
                    "valueList": {
                        # "wordSetId": 1,
                        "wordValue": word,
                        "translation": {
                            "id": 0,
                            "tr": tword,
                            # "main": 1,
                            # "selected": 1
                        }
                    }
                }
            ],
            "userData": {
                "nativeLanguage": "lang_id_src"
            },
            "iDs": [
                {}
            ]
        }
        return self.get_content(url, values)

    def get_translates(self, word):
        url = "http://api.lingualeo.com/gettranslates?word=" + urllib.quote_plus(word)

        try:
            result = self.get_content(url, {})
            translate = result["translate"][0]
            return {
                "is_exist": translate["is_user"],
                "word": word,
                "tword": translate["value"].encode("utf-8")
            }
        except Exception as e:
            return e.message

    # def get_content(self, url, values):
    #     data = urlencode(values)
    #
    #     # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
    #     opener = build_opener(HTTPCookieProcessor(self.cj))
    #     req = opener.open(url, data)
    #
    #     return json.loads(req.read())
    def get_content(self, url, values):
        # data = urlencode(values).encode() if values else None
        headers = {"Content-Type": "application/json"}

        # opener = build_opener(HTTPCookieProcessor(self.cj))
        # req = opener.open(url, data)
        # response = json.loads(req.read())
        response = requests.post(url, headers=headers, data=json.dumps(values), cookies=self.cookies).json()
        # return json.loads(req.read())
        return response
