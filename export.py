#!/usr/bin/env python
# -*- coding: utf-8 -*-
import handler
import config
import service
import sys

email = config.auth.get('email')
password = config.auth.get('password')

export_type = sys.argv[1]

if export_type == 'text':
    word_handler = handler.Text(config.sources.get('text'))
elif export_type == 'kindle':
    word_handler = handler.Kindle(config.sources.get('kindle'))
elif export_type == 'csv':
    word_handler = handler.Csv(config.sources.get('csv'))
else:
    raise Exception('unsupported type')

word_handler.read()

lingualeo = service.Lingualeo(email, password)
lingualeo.auth()

for word_dto in word_handler.get():
    # word = word_dto.text.lower().encode('utf-8')
    text = word_dto.text.lower()
    translate = word_dto.translate.lower()
    response = lingualeo.add_word(text, translate)

    if response.get("status") == "ok":
        print("Add word: " + text.strip())

    if response.get("error_msg"):
        print("Error: " + response["error_msg"])
