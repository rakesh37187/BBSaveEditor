import binascii


class User:
    def __init__(self, user_data):
        self._original_user_data = user_data
        self._modified_user_data = user_data

    @staticmethod
    def _get_level(data):
        level = binascii.unhexlify(data[256:264])
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
        self._modified_user_data =  self._modified_user_data.replace(self._modified_user_data[264:272], echoes)

    @staticmethod
    def _get_insight(data):
        insight = binascii.unhexlify(data[232:240])
        return int.from_bytes(insight, byteorder="little")

    def set_insight(self, insight):
        insight = binascii.hexlify(int.to_bytes(insight, byteorder="little", length=4))
        self._modified_user_data =  self._modified_user_data.replace(self._modified_user_data[232:240], insight)

    @staticmethod
    def _get_health(data):
        # Note that there are 3 health values stored at index 8:16, 16:24 and 24:32 for some reason.
        # It does not match sometimes. Not sure what is going on
        health = binascii.unhexlify(data[16:24])
        return int.from_bytes(health, byteorder="little")

    def set_health(self, health):
        health = binascii.hexlify(int.to_bytes(health, byteorder="little", length=4))
        for i in range(1, 4):
            self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[i*8:(i+1)*8], health)

    @staticmethod
    def _get_stamina(data):
        # Like health there are 3 stamina values stored at 64:72, 72:80, 80:88
        stamina = binascii.unhexlify(data[64:72])
        return int.from_bytes(stamina, byteorder="little")

    def set_stamina(self, stamina):
        stamina = binascii.hexlify(int.to_bytes(stamina, byteorder="little", length=4))
        for i in range(1, 4):
            self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[56+i*8:56+(i+1)*8], stamina)

    @staticmethod
    def _get_vitality(data):
        vitality = binascii.unhexlify(data[96:104])
        return int.from_bytes(vitality, byteorder="little")

    def set_vitality(self, vitality):
        vitality = binascii.hexlify(int.to_bytes(vitality, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[96:104], vitality)

    @staticmethod
    def _get_endurance(data):
        endurance = binascii.unhexlify(data[112:120])
        return int.from_bytes(endurance, byteorder="little")

    def set_endurance(self, endurance):
        endurance = binascii.hexlify(int.to_bytes(endurance, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[112:120], endurance)

    @staticmethod
    def _get_strength(data):
        strength = binascii.unhexlify(data[144:152])
        return int.from_bytes(strength, byteorder="little")

    def set_strength(self, strength):
        strength = binascii.hexlify(int.to_bytes(strength, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[144:152], strength)

    @staticmethod
    def _get_skill(data):
        skill = binascii.unhexlify(data[160:168])
        return int.from_bytes(skill, byteorder="little")

    def set_skill(self, skill):
        skill = binascii.hexlify(int.to_bytes(skill, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[160:168], skill)

    @staticmethod
    def _get_bloodtinge(data):
        bloodtinge = binascii.unhexlify(data[176:184])
        return int.from_bytes(bloodtinge, byteorder="little")

    def set_bloodtinge(self, bloodtinge):
        bloodtinge = binascii.hexlify(int.to_bytes(bloodtinge, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[176:184], bloodtinge)

    @staticmethod
    def _get_arcane(data):
        arcane = binascii.unhexlify(data[192:200])
        return int.from_bytes(arcane, byteorder="little")

    def set_arcane(self, arcane):
        arcane = binascii.hexlify(int.to_bytes(arcane, byteorder="little", length=4))
        self._modified_user_data = self._modified_user_data.replace(self._modified_user_data[176:184], arcane)

    def _get_stats(self, original: bool):
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

    def get_original_stats(self):
        return self._get_stats(True)

    def get_modified_stats(self):
        return self._get_stats(False)

    def apply_changes(self, data, filename):
        data = data.replace(self._original_user_data, self._modified_user_data)
        with open(filename + "_modded", "wb") as f:
            f.write(binascii.unhexlify(data))


