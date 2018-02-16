import os
if os.name != 'nt': raise Exception("ProPresenter 6 Python library not compatible on non-Windows environments")

appDataLocation = None

import winreg
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Renewed Vision\ProPresenter 6') as __key:
        appDataType, __dtype = winreg.QueryValueEx(__key, 'AppDataType')
        assert __dtype == winreg.REG_SZ
        if appDataType == "CustomPath":
            appDataLocation = winreg.QueryValueEx(__key, "AppDataLocation")[0]
        else:
            if appDataType == "OnlyThisUser":
                appDataLocation = os.getenv('APPDATA')
            elif appDataType == "ForAllUsers":
                appDataLocation = os.getenv('PROGRAMDATA')
            appDataLocation = os.path.join(appDataLocation, r'RenewedVision\ProPresenter6')
        assert appDataLocation != None
except FileNotFoundError:
    raise Exception(
        "Data could not be accessed!\nEither ProPresenter 6 is not installed, or has not been opened before")

from . import fileTypes
from . import settings

__playlistFile = os.path.join(appDataLocation,"PlaylistData",settings.GeneralPreferences.currentLibrary.name+".pro6pl")
playlist = fileTypes.Playlist(__playlistFile) if os.path.exists(__playlistFile) and os.path.isfile(__playlistFile) else None
