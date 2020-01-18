from typing import List


class Normalizer(object):
    def __init__(self):
        pass

    def action(self, data):
        pass


class TitleNormalizer(Normalizer):
    def action(self, data):
        if data['title'].lower() in ['guest',
                                     'uknown',
                                     'anonymous',
                                     'untitled']:
            data['title'] = ''
        return data


class AuthorNormalizer(Normalizer):
    def action(self, data):
        if data['author'].lower() in ['guest',
                                      'uknown',
                                      'anonymous',
                                      'untitled']:
            data['author'] = ''
        return data


class DateNormalizer(Normalizer):
    def action(self, data):
        return data


class ContentNormalizer(Normalizer):
    def action(self, data):
        data["content"] = data["content"].strip()
        return data


class DataNormalizerRunner(object):
    def __init__(self, normalizers: List[Normalizer]):
        self.normalizers = normalizers

    def normalize_data(self, data):
        for normalizer in self.normalizers:
            data = normalizer.action(data=data)
