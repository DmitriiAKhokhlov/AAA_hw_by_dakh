import json
import keyword


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class ColorizeMixin:
    def __init__(self, repr_color_code=33):
        self.repr_color_code = repr_color_code

    def repr(self):
        return f'\033[1;{self.repr_color_code};01m {self.title} | {self.price} ₽'


class Advert(ColorizeMixin, DotDict):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.dotdict_to_attr()

    @staticmethod
    def py_to_dotdict(data):
        ad = DotDict(data)
        ind = 1
        while ind > 0:
            ind = 0
            for key, val in ad.items():
                if type(val) == dict:
                    ad[key] = Advert.py_to_dotdict(val)
                    ind = 1
        return ad

    @property
    def price(self):
        if 'price' not in self.data:
            return 0
        else:
            if self.data['price'] < 0:
                raise ValueError('price must be >= 0')
            else:
                return self.data['price']

    def dotdict_to_attr(self):
        data_dot = self.py_to_dotdict(self.data)
        for key in data_dot:
            if key != 'price':
                if not keyword.iskeyword(key):
                    self.__dict__[key] = data_dot[key]
                else:
                    self.__dict__[key + '_'] = data_dot[key]
            self.price


if __name__ == '__main__':
    lesson_str = """{
    "title": "python", "price": 0,
    "location": {
    "address": "город Москва, Лесная, 7",
    "metro_stations": ["Белорусская"]
    }
    }"""

    print('test 1. We expect to get \'город Москва, Лесная, 7\'')
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad.location.address)

    # This test is commented since is gives ValueError due to negative price
    # print('test_2')
    # lesson_str = '{"title": "python", "price": -1}'
    # lesson = json.loads(lesson_str)
    # lesson_ad = Advert(lesson)

    print('test_3. Define price=0 if it does not given')
    lesson_str = '{"title": "python"}'
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad.price)

    print('test_4. Color feature')
    corgi = {
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }

    corgi_ad = Advert(corgi)
    print(corgi_ad.repr())

    print('test 5. Check attribute \'class_\'')
    print(corgi_ad.class_)
