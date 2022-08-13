import abc
import json


class Parser(abc.ABC):
    @staticmethod
    def parse(filename) -> dict:
        raise NotImplementedError


class JsonParser(Parser):

    @staticmethod
    def parse(filename) -> dict:
        with open(filename, 'r') as file:
            content = file.read().strip()

        data = json.loads(content)

        return data


class XmlParser(Parser):

    @staticmethod
    def parse(filename) -> dict:
        pass
