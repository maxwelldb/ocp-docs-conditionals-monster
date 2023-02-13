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
    if contexts is None or len(contexts) == 0:
        return None
    else:
        context_dict = {}
        for context in contexts:
            if context in context_dict:
                context_dict[context] += 1
            else:
                context_dict[context] = 1
        for context, count in context_dict.items():
            if count % 2 != 0:
                print(f"Mismatch detected for context {context}")

def compare_attrs(attrs):
    if attrs is None or len(attrs) == 0:
        return None
    else:
        attr_dict = {}
        for attr in attrs:
            if attr[0] == "!":
                attr = attr[1:]
                if attr in attr_dict:
                    attr_dict[attr] -= 1
                else:
                    attr_dict[attr] = -1
            else:
                if attr in attr_dict:
                    attr_dict[attr] += 1
                else:
                    attr_dict[attr] = 1
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
