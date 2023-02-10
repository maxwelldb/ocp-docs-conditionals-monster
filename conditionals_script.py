#!/usr/bin/env python
import os
import re
from itertools import chain

# TODO: Modify for CLI use later.
# project_path = os.path.abspath(os.curdir)
project_path = "/home/max/Development/openshift-docs"
modules_path = os.path.join(project_path, "modules")


def collect_modules(location):
    module_collection = []

    modules_list = os.listdir(location)

    for module in modules_list:
        if module.endswith(".adoc"):
            module_collection.append(module)

    return module_collection


def find_ifevals_in_module(adoc_content):
    ifevals_collection = []
    ifeval_re = re.compile(r'ifeval::\["{context}"\s*==\s*".*"\](?:\n|.)*?endif::\[\]')

    for ifeval in re.findall(ifeval_re, adoc_content):
        ifevals_collection.append(ifeval)

    return ifevals_collection


def get_contexts_from_ifeval(ifeval):
    context_re = re.compile(r'\["{context}"\s==\s"([a-z0-9-]+)"\]')
    contexts = re.findall(context_re, ifeval)
    if contexts:
        return contexts
    else:
        return None


def get_attrs_from_ifeval(ifeval):
    attr_re = re.compile(r":([A-Za-z-!]+):")
    attributes = re.findall(attr_re, ifeval)
    if attributes:
        return attributes
    else:
        return None


def compare_contexts(contexts):
    return None

def compare_attrs(attrs):
    return None


def main():
    module_collection = collect_modules(modules_path)

    for module in module_collection:
        mod = os.path.join(modules_path, module)
        contexts = []
        attrs = []
        with open(mod, "r") as file:
            print(file.name)
            module_content = file.read()
            for ifeval in find_ifevals_in_module(module_content):
                contexts.append(get_contexts_from_ifeval(ifeval))
                attrs.append(get_attrs_from_ifeval(ifeval))

        print(list(chain.from_iterable(contexts)))
        try:
            print(list(chain.from_iterable(attrs)))
        except:
            print(f"yikes in {file.name}")

    # get contexts should have two of each term
    #   - fail and alert if not
    # get attrs should look for matching attributes--one declaration, one negation


if __name__ == "__main__":
    main()
