import propresenter
from propresenter.files.pro6Template import File as p6t
p6t("Default.pro6Template", propresenter.appDataLocation+"\\Templates")
#import propresenter.registry
'''
%PROGRAMDATA%\Renewed Vision\Bibles
%PROGRAMFILESX86%\Renewed Vision\ProPresenter 6
HKCU\Software\Renewed Vision\ProPresenter 6
		REG_SZ	InstalledLocation	C:\Program Files (x86)\Renewed Vision\ProPresenter 6
	REG_SZ	AppDataLocation	C:\ProgramData\RenewedVision\ProPresenter6\
	REG_SZ	AppDataType	ForAllUsers
	REG_DWORD	CheckedVideoDriverSettings	2
	REG_DWORD	FirstTimeRun	0

%PROGRAMDATA%\Renewed Vision\ProPresenter 6
%APPDATA%\RenewedVision\ProPresenter6
%USERPROFILE%\Documents\ProPresenter6
'''
"""
Audio.pro6pl
CCLI.pro6data
CCLIReport.pro6data
countdownTimers.pro6data
CrashReports
DefaultMedia
DVD
Mask.pro6
Media.pro6pl
messageData.pro6data
PlaylistData
PosterFrames
PowerPointData
Preferences
Props.pro6
PurchasedMedia
SocialMedia.pro6Template
StageDisplay
stageDisplayLayouts.pro6data
Template Images
Templates
Thumbnails
UISettings.pro6data
"""

files = [
    "Audio.pro6pl",
    "CCLI.pro6data",
    "CCLIReport.pro6data",
    "countdownTimers.pro6data",
    "Mask.pro6",
    "Media.pro6pl",
    "messageData.pro6data",
    "Props.pro6",
    "SocialMedia.pro6Template",
    "stageDisplayLayouts.pro6data",
    "UISettings.pro6data"
]
#print(appDataLocation)

#import propresenter.utils
#v = propresenter.utils.xmlParse("UISettings.pro6data", appDataLocation)
