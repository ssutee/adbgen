#!/usr/bin/env python

import sys
import json

from libs.table import AndroidTable
from libs.content_provider import AndroidContentProvider
from libs.open_helper import AndroidOpenHelper
from libs.model_base import AndroidModelBase

def main():
    input_file = sys.argv[1]
    with open(input_file) as fin:
        json_object = json.load(fin)

        for table in json_object['tables']:
            AndroidTable(
                json_object['package'], 
                table, 
                json_object[table]['columns'], 
                json_object[table].get('indexes')).create_file()
                
            AndroidModelBase(
                json_object['package'],
                table,
                json_object[table]['columns']
            ).create_file()

        AndroidOpenHelper(
            json_object['package'],
            json_object['prefix'],
            json_object['database'],
            json_object['tables']
        ).create_file()

        AndroidContentProvider(
            json_object['package'],
            json_object['prefix'],
            json_object['tables']
        ).create_file()

if __name__ == '__main__':
    main()