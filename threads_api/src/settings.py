import json
import hashlib
import time

class Settings:

    def __init__(self):
        """
        Construct the object.

        Arguments:
            settings: (dict/str): a settings dictionary or a path to a JSON file.
        """
        self._encrypted_token = None
        self._timezone_offset = -14400
        self._device_id = self.generate_android_device_id()
        self._device_manufacturer = 'OnePlus'
        self._device_model = 'ONEPLUS+A3010'
        self._device_android_version = 25
        self._device_android_release = '7.1.1'

    def set_encrypted_token(self, encrypted_token):
        self._encrypted_token = encrypted_token

    def load_settings(self, path):
        """
        Load session settings

        Parameters
        ----------
        path: Path
            Path to storage file

        Returns
        -------
        Dict
            Current session settings as a Dict
        """
        with open(path, "r") as fp:
            self.set_settings(json.load(fp))
            return self.settings
        return None

    def dump_settings(self, path):
        """
        Serialize and save session settings

        Parameters
        ----------
        path: Path
            Path to storage file

        Returns
        -------
        Bool
        """
        with open(path, "w") as fp:
            json.dump(self.get_settings(), fp, indent=4)
        return True
    
    def get_settings(self):
        """
        Get current session settings

        Returns
        -------
        Dict
            Current session settings as a Dict
        """
        return {
            'authentication': {
                'encrypted_token': self._encrypted_token,
            },
            'timezone': {
                'offset': self._timezone_offset,
            },
            'device': {
                'id': self._device_id,
                'manufacturer': self._device_manufacturer,
                'model': self._device_model,
                'android_version': self._device_android_version,
                'android_release': self._device_android_release,
            },
        }


    def set_settings(self, settings):
        if settings is None:
            raise Exception("Provide valid settings to set")

        self._encrypted_token = settings.get('authentication').get('token')
        self._timezone_offset = settings.get('timezone').get('offset')
        self._device_id = settings.get('device').get('id')
        self._device_manufacturer = settings.get('device').get('manufacturer')
        self._device_model = settings.get('device').get('model')
        self._device_android_version = settings.get('device').get('android_version')
        self._device_android_release = settings.get('device').get('android_release')

    def generate_android_device_id(self):
        """
        Helper to generate Android Device ID

        Returns
        -------
        str
            A random android device id
        """
        return "android-%s" % hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]