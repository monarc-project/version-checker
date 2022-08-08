from sqlalchemy.ext.associationproxy import _AssociationList


class RightMixin:
    @staticmethod
    def _fields_base_read():
        return set()

    @staticmethod
    def _fields_export_csv():
        return {
            "software",
            "software_version",
            "http_referrer",
            "user_agent_browser",
            "user_agent_version",
            "user_agent_language",
            "user_agent_platform",
            "timestamp",
        }

    @classmethod
    def fields_export_csv(cls):
        return cls._fields_base_read().union(cls._fields_export_csv())

    def __getitem__(self, key):
        if not hasattr(self, "__dump__"):
            self.__dump__ = {}
        return self.__dump__.get(key)

    def __setitem__(self, key, value):
        if not hasattr(self, "__dump__"):
            self.__dump__ = {}
        self.__dump__[key] = value

    def dump(self):
        dico = {k: getattr(self, k) for k in self.fields_export_csv()}
        if hasattr(self, "__dump__"):
            dico.update(self.__dump__)
        for key, value in dico.items():  # preventing association proxy to die
            if isinstance(value, _AssociationList):
                dico[key] = list(value)
        return dico
