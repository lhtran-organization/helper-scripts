import getopt, sys
from ruamel.yaml import YAML

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:i:", ['file=','image='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    deployment_file_path = ''
    images = {}
    for o, a in opts:
        if o in ['-f', '--file']:
            deployment_file_path = a
        elif o in ['-i', '--image']:
            images[a.split(':')[0]] = a.split(':')[1]
        else:
            assert False, "unhandled option"


    with open(deployment_file_path, 'r') as yaml_file:
        yaml=YAML(typ='rt')
        data = list(yaml.load_all(yaml_file))
        for doc in data:
            if doc['kind'] == 'Deployment':
                for container in doc['spec']['template']['spec']['containers']:
                    image_name = container['image'].split(':')[0]
                    if image_name in images.keys():
                        container['image'] = image_name+":"+images.get(image_name)

    with open(deployment_file_path, 'w') as dump_file:
        yaml.dump_all(data, dump_file)

if __name__ == "__main__":
    main()