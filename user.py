import binascii


class User:
    def __init__(self, user_data):
        self._original_user_data = user_data
        self._modified_user_data = user_data

    def get_display_name(self):
        data_length = len(self._original_user_data)
        return binascii.unhexlify(self._original_user_data[data_length-66:data_length]).replace(b"\x00", b"").decode("utf-8")

    @staticmethod
    def _get_level(data):
        level = binascii.unhexlify(data[256:258])
        return int.from_bytes(level, byteorder="little")

    def set_level(self, level):
        level = binascii.hexlify(int.to_bytes(level, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[256:264], level)

    @staticmethod
    def _get_echoes(data):
        echoes = binascii.unhexlify(data[264:272])
        return int.from_bytes(echoes, byteorder="little")

    def set_echoes(self, echoes):
        echoes = binascii.hexlify(int.to_bytes(echoes, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[264:272], echoes)

    @staticmethod
    def _get_insight(data):
        insight = binascii.unhexlify(data[232:234])
        return int.from_bytes(insight, byteorder="little")

    def set_insight(self, insight):
        insight = binascii.hexlify(int.to_bytes(insight, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[232:240], insight)

    @staticmethod
    def _get_health(data):
        # Note that there are 3 health values stored at index 8:16, 16:24 and 24:32 for some reason.
        # It does not match sometimes. Not sure what is going on
        health = binascii.unhexlify(data[16:24])
        return int.from_bytes(health, byteorder="little")

    def set_health(self, health):
        health = binascii.hexlify(int.to_bytes(health, byteorder="little", length=4))
        print(health)
        for i in range(1, 4):
            self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[i * 8:(i + 1) * 8],
                                                                        health)

    @staticmethod
    def _get_stamina(data):
        # Like health there are 3 stamina values stored at 64:72, 72:80, 80:88
        stamina = binascii.unhexlify(data[64:66])
        return int.from_bytes(stamina, byteorder="little")

    def set_stamina(self, stamina):
        stamina = binascii.hexlify(int.to_bytes(stamina, byteorder="little", length=4))
        for i in range(1, 4):
            self._modified_user_data = self._modified_user_data.replace(
                self._modified_user_data[56 + i * 8:56 + (i + 1) * 8], stamina)

    @staticmethod
    def _get_vitality(data):
        vitality = binascii.unhexlify(data[96:98])
        return int.from_bytes(vitality, byteorder="little")

    def set_vitality(self, vitality):
        vitality = binascii.hexlify(int.to_bytes(vitality, byteorder="little", length=1))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[96:98], vitality)

    @staticmethod
    def _get_endurance(data):
        endurance = binascii.unhexlify(data[112:114])
        return int.from_bytes(endurance, byteorder="little")

    def set_endurance(self, endurance):
        endurance = binascii.hexlify(int.to_bytes(endurance, byteorder="little", length=1))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[112:114], endurance)

    @staticmethod
    def _get_strength(data):
        strength = binascii.unhexlify(data[144:146])
        return int.from_bytes(strength, byteorder="little")

    def set_strength(self, strength):
        strength = binascii.hexlify(int.to_bytes(strength, byteorder="little", length=1))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[144:146], strength)

    @staticmethod
    def _get_skill(data):
        skill = binascii.unhexlify(data[160:162])
        return int.from_bytes(skill, byteorder="little")

    def set_skill(self, skill):
        skill = binascii.hexlify(int.to_bytes(skill, byteorder="little", length=1))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[160:162], skill)

    @staticmethod
    def _get_bloodtinge(data):
        bloodtinge = binascii.unhexlify(data[176:178])
        return int.from_bytes(bloodtinge, byteorder="little")

    def set_bloodtinge(self, bloodtinge):
        bloodtinge = binascii.hexlify(int.to_bytes(bloodtinge, byteorder="little", length=1))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[176:178], bloodtinge)

    @staticmethod
    def _get_arcane(data):
        arcane = binascii.unhexlify(data[192:194])
        return int.from_bytes(arcane, byteorder="little")

    def set_arcane(self, arcane):
        arcane = binascii.hexlify(int.to_bytes(arcane, byteorder="little", length=1))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[192:194], arcane)

    def set_all_stats(self, values):
        funcs = [self.set_level, self.set_echoes, self.set_insight, self.set_health, self.set_stamina,
                 self.set_vitality, self.set_endurance, self.set_strength, self.set_skill, self.set_bloodtinge,
                 self.set_arcane]
        for func, value in zip(funcs, values):
            func(int(value))
            print("-----")
            print(self._original_user_data)
            print(self._modified_user_data)
            print("-----")
        # self.set_endurance(int(values[6]))

    def _get_stats_as_string(self, original: bool):
        if original:
            var_used = self._original_user_data
        else:
            var_used = self._modified_user_data
        return "User data: {}\n".format(var_used) + (
            "User level: {}\n"
            "User echoes: {}\n"
            "User insight: {}\n"
            "User health: {}\n"
            "User stamina: {}\n"
            "User vitality: {}\n"
            "User endurance: {}\n"
            "User strength: {}\n"
            "User skill: {}\n"
            "User bloodtinge: {}\n"
            "User arcane: {}\n"
        ).format(*(x(var_used) for x in [self._get_level,
                                         self._get_echoes,
                                         self._get_insight,
                                         self._get_health,
                                         self._get_stamina,
                                         self._get_vitality,
                                         self._get_endurance,
                                         self._get_strength,
                                         self._get_skill,
                                         self._get_bloodtinge,
                                         self._get_arcane]))

    def get_original_stats_as_string(self):
        return self._get_stats_as_string(True)

    def get_modified_stats_as_string(self):
        return self._get_stats_as_string(False)

    def _get_stats(self, original: bool):
        if original:
            var_used = self._original_user_data
        else:
            var_used = self._modified_user_data
        return (x(var_used) for x in [self._get_level,
                                      self._get_echoes,
                                      self._get_insight,
                                      self._get_health,
                                      self._get_stamina,
                                      self._get_vitality,
                                      self._get_endurance,
                                      self._get_strength,
                                      self._get_skill,
                                      self._get_bloodtinge,
                                      self._get_arcane])

    def get_original_stats(self):
        return self._get_stats(True)

    def get_modified_stats(self):
        return self._get_stats(False)

    def apply_changes(self, data, filename):
        data = data.replace(self._original_user_data, self._modified_user_data)
        with open(filename + "_modded", "wb") as f:
            f.write(binascii.unhexlify(data))
