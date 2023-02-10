#!/usr/bin/env python
import os

# TODO: Modify for CLI use later.
# project_path = os.path.abspath(os.curdir)
project_path = '/home/max/Development/openshift-docs'
modules_path = os.path.join(project_path, 'modules')


def collect_modules(modules_location):

    module_collection = []

    modules_list = os.listdir(modules_location)

    for module in modules_list:
        if module.endswith('.adoc'):
            module_collection.append(module)

    return module_collection

collect_modules(modules_path)