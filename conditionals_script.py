#!/usr/bin/env python
import os
import re
from itertools import chain

# TODO: Modify for CLI use later.
# project_path = os.path.abspath(os.curdir)
project_path = "/home/max/Development/openshift-docs"
modules_path = os.path.join(project_path, "modules")


def collect_modules(location):
    return [module for module in os.listdir(location) if module.endswith(".adoc")]


def find_ifevals_in_module(adoc_content):
    ifeval_re = re.compile(r'ifeval::\["{context}"\s*==\s*".*"\](?:\n|.)*?endif::\[\]')
    return re.findall(ifeval_re, adoc_content)

def get_contexts_from_ifeval(ifeval):
    context_re = re.compile(r'\["{context}"\s==\s"([a-z0-9-]+)"\]')
    contexts = re.findall(context_re, ifeval)
    return contexts or None


def get_attrs_from_ifeval(ifeval):
    attr_re = re.compile(r":([A-Za-z-!]+):")
    attributes = re.findall(attr_re, ifeval)
    return attributes or None


def compare_contexts(contexts):
    if not contexts:
        return
    context_dict = {}
    for context in contexts:
        context_dict[context] = context_dict.get(context, 0) + 1
    for context, count in context_dict.items():
        if count % 2 != 0:
            print(f"Mismatch detected for context {context}")

def compare_attrs(attrs):
    if not attrs:
        return
    attr_dict = {}
    for attr in attrs:
        if attr[0] == "!":
            attr = attr[1:]
            attr_dict[attr] = attr_dict.get(attr, 0) - 1
        else:
            attr_dict[attr] = attr_dict.get(attr, 0) + 1
    for attr, count in attr_dict.items():
        if count != 0:
            print(f"Mismatch detected for attribute {attr}")


def main():
    module_collection = collect_modules(modules_path)

    for module in module_collection:
        mod = os.path.join(modules_path, module)
        contexts = []
        attrs = []
        with open(mod, "r") as file:
            print(f"Scanning {mod}")
            module_content = file.read()
            for ifeval in find_ifevals_in_module(module_content):
                contexts.append(get_contexts_from_ifeval(ifeval))
                attrs.append(get_attrs_from_ifeval(ifeval))
        try:
            contexts = list(chain.from_iterable(contexts))
            attrs = list(chain.from_iterable(attrs))
            if contexts is not None or attrs is not None:
                compare_contexts(contexts)
                compare_attrs(attrs)
        except:
            # Try block is bad at the moment. Improve. Too many NoneTypes that I'm not dealing with in compare functions.
            print(f"NoneType error in {mod}")





if __name__ == "__main__":
    main()
