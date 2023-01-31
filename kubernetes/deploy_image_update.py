#!/bin/python

import sys
from ruamel.yaml import YAML

def main(argv):
    with open(argv[0], 'r') as yaml_file:
        yaml=YAML(typ='rt')
        data = list(yaml.load_all(yaml_file))
        for doc in data:
            if doc['kind'] == 'Deployment':
                for container in doc['spec']['template']['spec']['containers']:
                    if container['image'].startswith(argv[1]):
                        container['image'] = argv[2]
                        break
                break

    with open(argv[0], 'w') as dump_file:
        yaml.dump_all(data, dump_file)

if __name__ == "__main__":
    main(sys.argv[1:])
