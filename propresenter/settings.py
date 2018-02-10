import propresenter
from os import path
from propresenter.files.xml import File as XML

class SettingsXML(XML):
    # Reminder that variables act as pointers instead of creating a new copy!
    fileDirectory = propresenter.appDataLocation
    fileName = None
    force_list = ()
    force_root = None

    def __init__(self):
        self._file = XML(path.join(self.fileDirectory, self.fileName), self.force_list)
        self.root = self._file.data[self.force_root] if self.force_root else self._file.data

class PreferencesXML(SettingsXML): fileDirectory = path.join(SettingsXML.fileDirectory, "Preferences")

class GeneralPreferences(PreferencesXML):
    fileName = "GeneralPreferences.pro6pref"
    force_root = "RVPreferencesGeneral"

    """
    = TODO =
    LibraryFolders
        array[RVLibraryFolder]
    SelectedLibraryFolder == RVLibraryFolder
        CloudID - ???
        CloudLibraryName - ???
        ID - UUIDv4
        IsLinked - bool
        Location - str
        Name - str
    
    MediaRepository
        Type - ???
        Path - str
    
    MediaFileSearchPaths - array[str]
    ManageMediaAutomatically - bool
    LogoPreserveAspectRatio - bool
    LogoPath - str
    AppDataType - ???
    AppDataPath - str
    AllowAutomaticDownload - bool
    
    
    = Unknown Stuff =
    MaxColumn - int
    ServerSyncSource - ???
    VersionToSkip - ???
    RevertButtonVisibility - ???
    PlayEveryFrameVideoPlayback - bool
    OpenInfoCenterAtLaunch - bool - FALSEEE
    OpenDefaultResourceHome - bool - ???
    IsSyncFileBiDirectional - bool
    IsSyncFileDown - bool
    IsSyncFileUp - bool
    IsDefaultMediaLocationSet - bool
    HighQualityVideoback - bool
    DisableCrashReport - bool
    DeinterlacedVideoPlayback - bool
    CheckForUpdates - bool
    
    
    = SKIP =
    CloudLibraryFolders
    HasMigrationOccurred
    IsWelcomeDocumentInstalled
    IsVIBSamplesInstalled
    IsTemplatesInstalled
    LastSelectedPresentationName
    LastFeedTimestamp
    IsSongSelectLogin
    SongSelectVerifier
    SongSelectTokenSecret
    SongSelectToken
    """
    class CCLI:
        @property
        def Visible(self):
            # EnableCCLIDisplay - bool
            pass
        @property
        def Number(self):
            # CCLINumber - int [str?]
            pass
        @property
        def DisplayPosition(self):
            # CCLIDisplayPosition
            pass


        pass
    CCLI = CCLI()
    # Not doing SongSelect stuff
    class SongSelect:
        pass
    SongSelect = SongSelect()
GeneralPreferences = GeneralPreferences()

class SyncPreferences(PreferencesXML):
    fileName = "SyncPreferences.pro6pref"
    force_root = "RVPreferencesSynchronization"

    @property
    def ReplaceFiles(self):
        return self.root["ReplaceFiles"].lower() == "true"
    @ReplaceFiles.setter
    def ReplaceFiles(self, state: bool):
        self.root["ReplaceFiles"] = str(state).lower()

    @property
    def Source(self):
        return self.root["Source"]
    @Source.setter
    def Source(self, source: str):
        if not path.exists(source) or path.isdir(source):
            raise ValueError("Invalid source path")
        self.root["Source"] = source
    def Source_force(self, source: str):
        self.root["Source"] = source

    @property
    def SyncLibrary(self):
        return self.root["SyncLibrary"].lower() == "true"
    @SyncLibrary.setter
    def SyncLibrary(self, state: bool):
        self.root["SyncLibrary"] = str(state).lower()

    @property
    def SyncMedia(self):
        return self.root["SyncMedia"].lower() == "true"
    @SyncMedia.setter
    def SyncMedia(self, state: bool):
        self.root["SyncMedia"] = str(state).lower()

    @property
    def SyncPlaylists(self):
        return self.root["SyncPlaylists"].lower() == "true"
    @SyncPlaylists.setter
    def SyncPlaylists(self, state: bool):
        self.root["SyncPlaylists"] = str(state).lower()

    @property
    def SyncTemplates(self):
        return self.root["SyncTemplates"].lower() == "true"
    @SyncTemplates.setter
    def SyncTemplates(self, state: bool):
        self.root["SyncTemplates"] = str(state).lower()

    @property
    def SyncMode(self):
        return self.root["SyncMode"]
    @SyncMode.setter
    def SyncMode(self, mode: str):
        if mode not in ["UpdateClient", "UpdateServer", "UpdateBoth"]:
            raise ValueError("Invalid sync mode (UpdateClient, UpdateServer, UpdateBoth)")
        self.root["SyncMode"] = mode
SyncPreferences = SyncPreferences()


"""

class AdvancedPreferences(PreferencesXML):
    fileName = "AdvancedPreferences.pro6pref"
    force_root = "RVPreferencesAdvanced"

    @property
    def AudioChannels(self):
        raise NotImplementedError
    @property
    def AudioDelay(self):
        raise NotImplementedError
    @property
    def BackgroundScaleBehavior(self):
        raise NotImplementedError
    @property
    def ForegroundScaleBehavior(self):
        raise NotImplementedError

    @property
    def IsAnamorphicOutputEnabled(self):
        return self.root["IsAnamorphicOutputEnabled"].lower() == "true"
    @IsAnamorphicOutputEnabled.setter
    def IsAnamorphicOutputEnabled(self, state: bool):
        self.root["IsAnamorphicOutputEnabled"] = str(state).lower()

    @property
    def KeyClickSuppressVideo(self):
        return self.root["KeyClickSuppressVideo"].lower() == "true"
    @KeyClickSuppressVideo.setter
    def KeyClickSuppressVideo(self, state: bool):
        self.root["KeyClickSuppressVideo"] = str(state).lower()
AdvancedPreferences = AdvancedPreferences()

class CloudPreferences(PreferencesXML):
    fileName = "CloudPreferences.pro6pref"
    force_root = "RVPreferencesCloud"
CloudPreferences = CloudPreferences()

class DisplayPreferences(PreferencesXML): fileName = "DisplayPreferences.pro6pref"
DisplayPreferences = DisplayPreferences()

class DVDPreferences(PreferencesXML): fileName = "DVDPreferences.pro6pref"
DVDPreferences = DVDPreferences()

class EdgeBlendPreferences(PreferencesXML): fileName = "EdgeBlendPreferences.pro6pref"
EdgeBlendPreferences = EdgeBlendPreferences()

class LabelsPreferences(PreferencesXML): fileName = "LabelsPreferences.pro6pref"
LabelsPreferences = LabelsPreferences()

class LiveVideoPreferences(PreferencesXML): fileName = "LiveVideoPreferences.pro6pref"
LiveVideoPreferences = LiveVideoPreferences()

class MultiScreenPreferences(PreferencesXML): fileName = "MultiScreenPreferences.pro6pref"
MultiScreenPreferences = MultiScreenPreferences()

class NetworkPreferences(PreferencesXML):
    fileName = "NetworkPreferences.pro6pref"
    force_root = "RVPreferencesNetwork"

    @property
    def IsControllerModeEnabled(self):
        return self.root["IsControllerModeEnabled"].lower() == "true"
    @IsControllerModeEnabled.setter
    def IsControllerModeEnabled(self, state: bool):
        self.root["IsControllerModeEnabled"] = str(state).lower()

    @property
    def IsMasterControlEnabled(self):
        return self.root["IsMasterControlEnabled"].lower() == "true"
    @IsMasterControlEnabled.setter
    def IsMasterControlEnabled(self, state: bool):
        self.root["IsMasterControlEnabled"] = str(state).lower()

    @property
    def IsObserverModeEnabled(self):
        return self.root["IsObserverModeEnabled"].lower() == "true"
    @IsObserverModeEnabled.setter
    def IsObserverModeEnabled(self, state: bool):
        self.root["IsObserverModeEnabled"] = str(state).lower()

    @property
    def IsProNetworkEnabled(self):
        return self.root["IsProNetworkEnabled"].lower() == "true"
    @IsProNetworkEnabled.setter
    def IsProNetworkEnabled(self, state: bool):
        self.root["IsProNetworkEnabled"] = str(state).lower()

    @property
    def IsProRemoteEnabled(self):
        return self.root["IsProRemoteEnabled"].lower() == "true"
    @IsProRemoteEnabled.setter
    def IsProRemoteEnabled(self, state: bool):
        self.root["IsProRemoteEnabled"] = str(state).lower()

    @property
    def IsSendSlidesEnabled(self):
        return self.root["IsSendSlidesEnabled"].lower() == "true"
    @IsSendSlidesEnabled.setter
    def IsSendSlidesEnabled(self, state: bool):
        self.root["IsSendSlidesEnabled"] = str(state).lower()

    @property
    def MakeArrangementsFromSeq(self):
        return self.root["MakeArrangementsFromSeq"].lower() == "true"
    @MakeArrangementsFromSeq.setter
    def MakeArrangementsFromSeq(self, state: bool):
        self.root["MakeArrangementsFromSeq"] = str(state).lower()

    @property
    def MatchSongsInLibrary(self):
        return self.root["MatchSongsInLibrary"].lower() == "true"
    @MatchSongsInLibrary.setter
    def MatchSongsInLibrary(self, state: bool):
        self.root["MatchSongsInLibrary"] = str(state).lower()

    @property
    def RemoteStageDisplayEnable(self):
        return self.root["RemoteStageDisplayEnable"].lower() == "true"
    @RemoteStageDisplayEnable.setter
    def RemoteStageDisplayEnable(self, state: bool):
        self.root["RemoteStageDisplayEnable"] = str(state).lower()

    @property
    def ShowHistoricalPlans(self):
        return self.root["ShowHistoricalPlans"].lower() == "true"
    @ShowHistoricalPlans.setter
    def ShowHistoricalPlans(self, state: bool):
        self.root["ShowHistoricalPlans"] = str(state).lower()



    @property
    def CheckPlanUpdatesMode(self):
        raise NotImplementedError

    @property
    def DownloadDocumentsMode(self):
        raise NotImplementedError

    @property
    def MasterSlaveType(self):
        raise NotImplementedError

    @property
    def ProNetworkName(self):
        raise NotImplementedError

    @property
    def ProNetworkPort(self):
        raise NotImplementedError

    @property
    def ProRemoteControllerPassword(self):
        raise NotImplementedError

    @property
    def ProRemoteObserverPassword(self):
        raise NotImplementedError

    @property
    def RemoteStageDisplayPassword(self):
        raise NotImplementedError

    @property
    def RemoteStageDisplayPort(self):
        raise NotImplementedError

    @property
    def SendSlidesName(self):
        raise NotImplementedError




    @property
    def SendSlidesPort(self):
        raise NotImplementedError


    @property
    def SlaveCollection(self):
        raise NotImplementedError


    @property
    def SlaveName(self):
        raise NotImplementedError


    @property
    def SlavePort(self):
        raise NotImplementedError


    @property
    def UploadDocumentsMode(self):
        raise NotImplementedError
NetworkPreferences=NetworkPreferences()

class SDIPreferences(PreferencesXML):
    fileName = "SDIPreferences.pro6pref"
    force_root = "RVPreferencesSDI"

    @property
    def DeviceChecked(self):
        return self.root["DeviceChecked"].lower() == "true"
    @DeviceChecked.setter
    def DeviceChecked(self, state: bool):
        self.root["DeviceChecked"] = str(state).lower()
    @property
    def IgnoreBackgroundColors(self):
        return self.root["IgnoreBackgroundColors"].lower() == "true"
    @IgnoreBackgroundColors.setter
    def IgnoreBackgroundColors(self, state: bool):
        self.root["IgnoreBackgroundColors"] = str(state).lower()

    @property
    def SelectedSSOutputDevice(self):
        raise NotImplementedError
    @property
    def SelectedSSOutputDeviceModeIndex(self):
        raise NotImplementedError

    @property
    def AlphaKeyType(self):
        raise NotImplementedError

    @property
    def AlphaKeyBlend(self):
        raise NotImplementedError
SDIPreferences = SDIPreferences()

"""
"""
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
"""
