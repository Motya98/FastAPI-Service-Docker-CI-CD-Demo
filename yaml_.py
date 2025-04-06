from pathlib import Path
import yaml


class CRUDYaml:
    @staticmethod
    def read(yaml_name) -> dict:
        with open(CRUDYaml.get_path(yaml_name), 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_path(yaml_name) -> Path:
        return Path(__file__).parent / yaml_name


if __name__ == '__main__':
    print(CRUDYaml.read('config.yaml'))
