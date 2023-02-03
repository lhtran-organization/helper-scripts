import argparse
from ruamel.yaml import YAML

def update_manifest(manifest_type, file_path, images):
    base_images_dict = {}
    for image in images:
        base_images_dict[image.split(':')[0]] = image.split(':')[1]

    with open(file_path, 'r') as yaml_file:
        yaml=YAML(typ='rt')
        data = list(yaml.load_all(yaml_file))
        for doc in data:
            if doc['kind'] == 'Deployment':
                for container in doc['spec']['template']['spec']['containers']:
                    image_name = container['image'].split(':')[0]
                    if image_name in base_images_dict.keys():
                        container['image'] = image_name+":"+base_images_dict.get(image_name)

    with open(file_path, 'w') as dump_file:
        yaml.dump_all(data, dump_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'Update image in Deployment or Stateful',
                    description = 'Update image in Deployment or Stateful Kubernetes manifests. It can update multiple instances if image(s) is/are matched')
    parser.add_argument("type", choices=["deployment", "statefulset"], help="Type of manifest (deployment or statefulset)")
    parser.add_argument('-f', '--file', required=True, help='Path to the manifest file')
    parser.add_argument('-i','--image', required=True, help='Container image to update', nargs='+')
    args = parser.parse_args()
    update_manifest(args.type, args.file, args.image)