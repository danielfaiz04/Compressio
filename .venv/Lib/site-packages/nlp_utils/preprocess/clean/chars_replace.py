from typing import Union, List


class CharsReplace:
    def __init__(self, mapping: dict):
        self.mapping = mapping

    @classmethod
    def from_kv(cls, source: Union[list, str], target: Union[list, str]) -> "CharReplace":
        if isinstance(source, str):
            source = list(source)
        if isinstance(target, str):
            target = list(target)

        assert len(source) == len(target)

        mapping = dict(zip(source, target))
        self = cls(mapping)

        return self

    @classmethod
    def from_dict(cls, dict_data: dict) -> "CharReplace":
        self = cls(dict_data)
        return self

    def __call__(self, data: List[List[str]]) -> List[List[str]]:
        return self.batch_process(data)

    def batch_process(self, data: List[List[str]]) -> List[List[str]]:
        return [self.process(i) for i in data]

    def process(self, data: List[str]) -> List[str]:
        return [self.mapping.get(i, i) for i in data]
