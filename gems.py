import binascii

from gem_data_conversion import gem_shapes, gem_effects


class Gem:
    def __init__(self, gem_data):
        self._original_gem_data = gem_data
        self._modified_gem_data = gem_data

    def __str__(self):
        return "Original gem data: {}\nModified gem data: {}".format(self._original_gem_data, self._modified_gem_data)

    @staticmethod
    def get_gem_id(data):
        return data[0:8].decode("utf-8")

    @staticmethod
    def _get_gem_source(data):
        return data[8:16].decode("utf-8")

    @staticmethod
    def _get_gem_quantity(data):
        return int(data[16:24][0:2].decode("utf-8"))

    @staticmethod
    def _get_gem_shape(data):
        return "{}, {}".format(data[24:32].decode("utf-8"), gem_shapes.get(data[24:32]))

    def set_gem_shape(self, data):
        data = data[0:8].encode()
        self._modified_gem_data = self._modified_gem_data.replace(self._modified_gem_data[24:32], data)

    @staticmethod
    def _get_effect(data, effect_number):
        index_begin = 32 + 8 * effect_number
        index_end = 32 + 8 * (effect_number + 1)
        # return data[index_begin:index_end].decode("utf-8")
        return "{}, {}".format(data[index_begin:index_end].decode("utf-8"), gem_effects.get(data[index_begin:index_end]))

    def _get_effect_1(self, data):
        return self._get_effect(data, 0)

    def _get_effect_2(self, data):
        return self._get_effect(data, 1)

    def _get_effect_3(self, data):
        return self._get_effect(data, 2)

    def set_effect_1(self, effect_hex):
        effect_hex = effect_hex[0:8].encode()
        self._modified_gem_data = self._modified_gem_data.replace(self._modified_gem_data[32:40], effect_hex)

    def set_effect_2(self, effect_hex):
        print(effect_hex)
        effect_hex = effect_hex[0:8].encode()
        print(effect_hex)
        self._modified_gem_data = self._modified_gem_data.replace(self._modified_gem_data[40:48], effect_hex)

    def set_effect_3(self, effect_hex):
        effect_hex = effect_hex[0:8].encode()
        self._modified_gem_data = self._modified_gem_data.replace(self._modified_gem_data[48:56], effect_hex)

    def set_all_stats(self, values):
        funcs = [self.set_gem_shape, self.set_effect_1, self.set_effect_2, self.set_effect_3]
        for func, value in zip(funcs, values[3:6]):
            func(value)

    def _get_stats(self, original: bool):
        if original:
            var_used = self._original_gem_data
        else:
            var_used = self._modified_gem_data
        return (x(var_used) for x in [self.get_gem_id,
                                      self._get_gem_source,
                                      self._get_gem_quantity,
                                      self._get_gem_shape,
                                      self._get_effect_1,
                                      self._get_effect_2,
                                      self._get_effect_3])

    def get_original_stats(self):
        return self._get_stats(True)

    def get_modified_stats(self):
        return self._get_stats(False)

    def apply_changes(self, data, filename):
        data = data.replace(self._original_gem_data, self._modified_gem_data)
        with open(filename + "_modded", "wb") as f:
            f.write(binascii.unhexlify(data))
