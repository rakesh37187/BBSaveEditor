import binascii

from gem_data_conversion import gem_shapes, gem_effects


class Gem:
    def __init__(self, gem_data):
        self._original_gem_data = gem_data
        self._modified_gem_data = gem_data

    def __str__(self):
        return "Original gem data: {}\nModified gem data: {}".format(self._original_gem_data, self._modified_gem_data)

    @staticmethod
    def _get_gem_id(data):
        return data[0:8]

    @staticmethod
    def _get_gem_source(data):
        return data[8:16]

    @staticmethod
    def _get_gem_quantity(data):
        return int(data[16:24][0:2].decode("utf-8"))

    @staticmethod
    def _get_gem_shape(data):
        return gem_shapes.get(data[24:32])

    @staticmethod
    def _get_effect_1(data):
        return gem_effects.get(data[32:40])

    def set_effect_1(self, effect_hex):
        self._modified_gem_data = self._modified_gem_data.replace(self._modified_gem_data[32:40], effect_hex)

    @staticmethod
    def _get_effect_2(data):
        return gem_effects.get(data[40:48])

    def set_effect_2(self, effect_hex):
        self._modified_gem_data = self._modified_gem_data.replace(self._modified_gem_data[40:48], effect_hex)

    @staticmethod
    def _get_effect_3(data):
        return gem_effects.get(data[48:56])

    def set_effect_3(self, effect_hex):
        self._modified_gem_data = self._modified_gem_data.replace(self._modified_gem_data[48:56], effect_hex)

    def _get_stats(self, original: bool):
        if original:
            var_used = self._original_gem_data
        else:
            var_used = self._modified_gem_data
        return "Gem data: {}\n".format(var_used) + (
            "Gem ID: {}\n"
            "Gem source: {}\n"
            "Gem quantity: {}\n"
            "Gem shape: {}\n"
            "Gem effect 1: {}\n"
            "Gem effect 2: {}\n"
            "Gem effect 3: {}"
        ).format(*(x(var_used) for x in [self._get_gem_id,
                                                        self._get_gem_source,
                                                        self._get_gem_quantity,
                                                        self._get_gem_shape,
                                                        self._get_effect_1,
                                                        self._get_effect_2,
                                                        self._get_effect_3]))

    def get_original_stats(self):
        return self._get_stats(True)

    def get_modified_stats(self):
        return self._get_stats(False)

    def apply_changes(self, data, filename):
        data = data.replace(self._original_gem_data, self._modified_gem_data)
        with open(filename + "_modded", "wb") as f:
            f.write(binascii.unhexlify(data))
