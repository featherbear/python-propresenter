import propresenter

import winreg
import os

try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Renewed Vision\ProPresenter 6') as key:
        appDataType, dtype = winreg.QueryValueEx(key, 'AppDataType')
        assert dtype == winreg.REG_SZ
        appDataLocation = ""
        if appDataType == "CustomPath":
            appDataLocation = winreg.QueryValueEx(key, "AppDataLocation")[0]
        else:
            if appDataType == "OnlyThisUser":
                appDataLocation = os.getenv('APPDATA')
            elif appDataType == "ForAllUsers":
                appDataLocation = os.getenv('PROGRAMDATA')
            appDataLocation = os.path.join(appDataLocation, r'RenewedVision\ProPresenter6')
        assert appDataLocation != ""
        propresenter.appDataLocation = appDataLocation
except FileNotFoundError:
    raise Exception("ProPresenter 6 is not installed, or has not been opened before")
