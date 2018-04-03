from collections import OrderedDict
from os import path

from . import utils
from .fileTypes.xml import File as XML
from .. import files as propresenter


class SettingsXML():
    _fileDirectory = propresenter.appDataLocation
    _fileName = None
    _forceList = ()
    _forceRoot = None

    def __new__(cls, *args, **kwargs):
        _obj = super().__new__(cls)
        _obj._file = XML(path.join(cls._fileDirectory, cls._fileName), cls._forceList)
        _obj._root = _obj._file._data[cls._forceRoot] if cls._forceRoot else cls._file._data
        return _obj

    def save(self):
        self._file.save()


class PreferencesXML(SettingsXML): _fileDirectory = path.join(SettingsXML._fileDirectory, "Preferences")


class GeneralPreferences(PreferencesXML):
    _fileName = "GeneralPreferences.pro6pref"
    _forceRoot = "RVPreferencesGeneral"
    _forceList = ("RVLibraryFolder", "a:string")

    class _libraryObj:
        def __init__(self, path):
            self._root = path

        def __repr__(self):
            return 'Library("%s")' % self.name

        @property
        def name(self):
            return self._root["Name"]["#text"]

        @name.setter
        def name(self, name):
            self._root["Name"]["#text"] = name

        @property
        def location(self):
            return self._root["Location"]["#text"]

        @location.setter
        def location(self, path):
            self._root["Location"]["#text"] = path

        @property
        def id(self):
            return self._root["ID"]["#text"]

        @id.setter
        def id(self, id):
            self._root["ID"]["#text"] = id

        @property
        def cloudId(self):
            return self._root["CloudID"]["#text"]

        @cloudId.setter
        def cloudId(self, id):
            self._root["CloudID"]["#text"] = id

        @property
        def cloudLibraryName(self):
            return "" if "@i:nil" in self._root["CloudLibraryName"] else self._root["CloudLibraryName"]["#text"]

        @cloudLibraryName.setter
        def cloudLibraryName(self, id):
            if "@i:nil" in self._root["CloudLibraryName"]: del self._root["CloudLibraryName"]["@i:nil"]
            self._root["CloudLibraryName"]["#text"] = id

        @property
        def isLinked(self):
            return self._root["IsLinked"]["#text"].lower() == "true"

        @isLinked.setter
        def isLinked(self, state):
            self._root["IsLinked"]["#text"] = str(state).lower()

        pass

    def createLibrary(self, *, cloudID: int = 0, cloudLibraryName: str = None,
                      ID: str = utils.UUID.generateUUID(), isLinked: bool = False, location: str,
                      name: str):
        return {
            "CloudID": {"#text": cloudID},
            "CloudLibraryName": {"#text": cloudLibraryName} if cloudLibraryName else {"@i:nil": True},
            "ID": {"#text": ID},
            "IsLinked": {"#text": isLinked},
            "Location": {"#text": location},
            "Name": {"#text": name}
        }

    @property
    def currentLibrary(self):
        return self._libraryObj(self._root["SelectedLibraryFolder"])

    @currentLibrary.setter
    def currentLibrary(self, obj):
        if type(obj) == str:
            obj = self.libraries[obj]
            if obj is None:
                raise ValueError("Could not find a library with the given ID")
            self.currentLibrary = obj._root
        elif type(obj) in [dict, OrderedDict]:
            if not all(["CloudID" in obj, "CloudLibraryName" in obj, "ID" in obj, "IsLinked" in obj, "Location" in obj,
                        "Name" in obj]):
                raise ValueError("Missing values in library object")
            self._root["SelectedLibraryFolder"] = obj
        else:
            print(obj)
            print(type(obj))
            raise Exception("Bad argument")

            # Find the UUID

    def __init__(self):
        class logo:
            @property
            def path(this):
                return self._root["LogoPath"]["#text"]

            @path.setter
            def path(this, path):
                self._root["LogoPath"]["#text"] = path

            @property
            def preserveAspectRatio(this):
                return self._root["LogoPreserveAspectRatio"]["#text"].lower() == "true"

            @preserveAspectRatio.setter
            def preserveAspectRatio(this, state):
                self._root["LogoPreserveAspectRatio"]["#text"] = str(state).lower()

        self.logo = logo()

        class mediaRepository:
            @property
            def path(this):
                return self._root["MediaRepositoryPath"]["#text"]

            @path.setter
            def path(this, path):
                self._root["MediaRepositoryPath"]["#text"] = path

            @property
            def type(this):
                return self._root["MediaRepositoryType"]["#text"]

            @type.setter
            def type(this, type):
                if type not in ["CustomPath", "OnlyThisUser", "ForAllUsers"]:
                    raise ValueError("Invalid type (ForAllUsers, OnlyThisUser, CustomPath)")
                self._root["MediaRepositoryType"]["#text"] = type

            @property
            def autoManage(this):
                return self._root["ManageMediaAutomatically"]["#text"] == "true"

            @autoManage.setter
            def autoManage(this, state: bool):
                self._root["ManageMediaAutomatically"]["#text"] = str(type).lower()

        self.mediaRepository = mediaRepository()

        class mediaSearchPaths(list):
            def __repr__(self):
                return str([p["#text"] for p in self])

            def __init__(this):
                list.__init__(this, self._root["MediaFileSearchPaths"]["a:string"])

            def add(self):
                raise NotImplementedError

        self.mediaSearchPaths = mediaSearchPaths()

        class libraries(list):
            @staticmethod
            def add(*, cloudID: int = 0, cloudLibraryName: str = None,
                    ID: str = utils.UUID.generateUUID(), isLinked: bool = False, location: str,
                    name: str):
                self._root["LibraryFolders"].append({
                    self.createLibrary(**locals())
                })
                return self._libraryObj(self._root["LibraryFolders"][-1])

            def __repr__(this):
                return str([self._libraryObj(p) for p in this])

            def __init__(this):
                list.__init__(this, self._root["LibraryFolders"]["RVLibraryFolder"])

            def __getitem__(this, item):
                if type(item) == int:
                    return self._libraryObj(list.__getitem__(this, item))
                elif utils.UUID.validUUID(item):
                    item = item.upper()
                    if item not in [s["ID"]["#text"].upper() for s in this]:
                        return None
                    return self._libraryObj(next(filter(lambda element: element["ID"]["#text"].upper() == item, this)))
                else:
                    raise ValueError("Invalid UUIDv4")

        self.libraries = libraries()

        class CCLI:
            @property
            def visible(this):
                return self._root["EnableCCLIDisplay"]["#text"].lower() == "true"

            @visible.setter
            def visible(this, state):
                self._root["EnableCCLIDisplay"]["#text"] = str(state).lower()

            @property
            def number(this):
                return "" if "@i:nil" in self._root["CCLINumber"] else self._root["CCLINumber"]["#text"]

            @number.setter
            def number(this, number: str):
                self._root["CCLINumber"]["#text"] = number

            @property
            def displayPosition(this):
                return self._root["CCLIDisplayPosition"]["#text"]

            @displayPosition.setter
            def displayPosition(this, position):
                if position in []:
                    self._root["CCLIDisplayPosition"]["#text"] = position
                raise NotImplementedError

        self.CCLI = CCLI()

        '''
        NOT IMPLEMENTING APPDATA

        appData confusion
        1) Loads from registry
            AppDataLocation takes precedence over AppDataType (<-- probably only just for the radio buttons)
        2) Overwrite contents of GeneralPreferences
            AppDataLocation -> AppDataPath
            AppDataType -> AppDataType
        '''

    """
    = Unknown Stuff =
    AllowAutomaticDownload - bool
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

    # Not doing SongSelect stuff
    @property
    def SongSelect(self):
        raise NotImplementedError

    @property
    def CloudLibraryFolders(self):
        raise NotImplementedError


GeneralPreferences = GeneralPreferences()


class SyncPreferences(PreferencesXML):
    _fileName = "SyncPreferences.pro6pref"
    _forceRoot = "RVPreferencesSynchronization"

    @property
    def ReplaceFiles(self):
        return self._root["ReplaceFiles"].lower() == "true"

    @ReplaceFiles.setter
    def ReplaceFiles(self, state: bool):
        self._root["ReplaceFiles"] = str(state).lower()

    @property
    def Source(self):
        return self._root["Source"]

    @Source.setter
    def Source(self, source: str):
        if not path.exists(source) or path.isdir(source):
            raise ValueError("Invalid source path")
        self._root["Source"] = source

    def Source_force(self, source: str):
        self._root["Source"] = source

    @property
    def SyncLibrary(self):
        return self._root["SyncLibrary"].lower() == "true"

    @SyncLibrary.setter
    def SyncLibrary(self, state: bool):
        self._root["SyncLibrary"] = str(state).lower()

    @property
    def SyncMedia(self):
        return self._root["SyncMedia"].lower() == "true"

    @SyncMedia.setter
    def SyncMedia(self, state: bool):
        self._root["SyncMedia"] = str(state).lower()

    @property
    def SyncPlaylists(self):
        return self._root["SyncPlaylists"].lower() == "true"

    @SyncPlaylists.setter
    def SyncPlaylists(self, state: bool):
        self._root["SyncPlaylists"] = str(state).lower()

    @property
    def SyncTemplates(self):
        return self._root["SyncTemplates"].lower() == "true"

    @SyncTemplates.setter
    def SyncTemplates(self, state: bool):
        self._root["SyncTemplates"] = str(state).lower()

    @property
    def SyncMode(self):
        return self._root["SyncMode"]

    @SyncMode.setter
    def SyncMode(self, mode: str):
        if mode not in ["UpdateClient", "UpdateServer", "UpdateBoth"]:
            raise ValueError("Invalid sync mode (UpdateClient, UpdateServer, UpdateBoth)")
        self._root["SyncMode"] = mode


# SyncPreferences = SyncPreferences()


"""

class AdvancedPreferences(PreferencesXML):
    _fileName = "AdvancedPreferences.pro6pref"
    _forceRoot = "RVPreferencesAdvanced"

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
    _fileName = "CloudPreferences.pro6pref"
    _forceRoot = "RVPreferencesCloud"
CloudPreferences = CloudPreferences()

class DisplayPreferences(PreferencesXML): _fileName = "DisplayPreferences.pro6pref"
DisplayPreferences = DisplayPreferences()

class DVDPreferences(PreferencesXML): _fileName = "DVDPreferences.pro6pref"
DVDPreferences = DVDPreferences()

class EdgeBlendPreferences(PreferencesXML): _fileName = "EdgeBlendPreferences.pro6pref"
EdgeBlendPreferences = EdgeBlendPreferences()

class LabelsPreferences(PreferencesXML): _fileName = "LabelsPreferences.pro6pref"
LabelsPreferences = LabelsPreferences()

class LiveVideoPreferences(PreferencesXML): _fileName = "LiveVideoPreferences.pro6pref"
LiveVideoPreferences = LiveVideoPreferences()

class MultiScreenPreferences(PreferencesXML): _fileName = "MultiScreenPreferences.pro6pref"
MultiScreenPreferences = MultiScreenPreferences()

class NetworkPreferences(PreferencesXML):
    _fileName = "NetworkPreferences.pro6pref"
    _forceRoot = "RVPreferencesNetwork"

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
    _fileName = "SDIPreferences.pro6pref"
    _forceRoot = "RVPreferencesSDI"

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
class UISettings(SettingsXML): _fileName = "UISettings.pro6data"
class StageDisplayLayouts(SettingsXML): _fileName = "stageDisplayLayouts.pro6data"
class SocialMedia(SettingsXML): _fileName = "SocialMedia.pro6Template"
class Props(SettingsXML): _fileName = "Props.pro6"
class MessageData(SettingsXML): _fileName = "messageData.pro6data"
class Media(SettingsXML): _fileName = "Media.pro6pl"
class Mask(SettingsXML): _fileName = "Mask.pro6"
class CountdownTimers(SettingsXML): _fileName = "countdownTimers.pro6data"
class CCLIReport(SettingsXML): _fileName = "CCLIReport.pro6data"
class CCLI(SettingsXML): _fileName = "CCLI.pro6data"
class Audio(SettingsXML): _fileName = "Audio.pro6pl"
"""
