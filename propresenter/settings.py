import propresenter
from propresenter.files.xml import Stub as XML
class SettingsXML(XML): fileDirectory = propresenter.appDataLocation

class UISettings(SettingsXML): fileName = "UISettings.pro6data"
class StageDisplayLayouts(SettingsXML): fileName = "stageDisplayLayouts.pro6data"
class SocialMedia(SettingsXML): fileName = "SocialMedia.pro6Template"
class Props(SettingsXML): fileName = "Props.pro6"
class MessageData(SettingsXML): fileName = "messageData.pro6data"
class Media(SettingsXML): fileName = "Media.pro6pl"
class Mask(SettingsXML): fileName = "Mask.pro6"
class CountdownTimers(SettingsXML): fileName = "countdownTimers.pro6data"
class CCLIReport(SettingsXML): fileName = "CCLIReport.pro6data"
class CCLI(SettingsXML): fileName = "CCLI.pro6data"
class Audio(SettingsXML): fileName = "Audio.pro6pl"
