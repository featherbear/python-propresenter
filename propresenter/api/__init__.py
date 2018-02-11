class Connection():
    def __init__(self):
        # https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/
        import ctypes
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                title = buff.value

                def getClassName(hwnd):
                    resultString = ctypes.create_string_buffer(64)
                    ctypes.windll.user32.GetClassNameA(hwnd, resultString, len(resultString))
                    return resultString.value

                if title.startswith("ProPresenter") and b"ProPresenter.exe" in getClassName(hwnd):
                    # print("Found ProPresenter!")
                    self._hwnd = hwnd
            return True
        EnumWindows(EnumWindowsProc(foreach_window), 0)

        if not self._hwnd:
            raise Exception("ProPresenter not running! Or an error has occured")
        self._PostMessage = ctypes.windll.user32.PostMessageA

    def _sendKey(self, keyCode: int):
        # https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731%28v=vs.85%29.aspx?f=255&MSPPError=-2147217396
        self._PostMessage(self._hwnd, 0x0100, keyCode, 0)  # WM_KEYDOWN
        self._PostMessage(self._hwnd, 0x0101, keyCode, 0)  # WM_KEYUP

    def exit(self):
        """
        Won't actually close ProPresenter, because a confirmation dialogue box appears
        """
        self._PostMessage(self._hwnd, 0x0010, 0, 0)  # WM_CLOSE

    def clearAll(self):
        self._sendKey(0x70)
    def clearSlide(self):
        self._sendKey(0x71)
    def clearBackground(self):
        self._sendKey(0x72)
    def clearProps(self):
        self._sendKey(0x73)
    def clearAudio(self):
        self._sendKey(0x74)

    def showLogo(self):
        self._sendKey(0x75)
    def showLiveVideo(self):
        self._sendKey(0x76)

    def toggleOutput(self):
        raise NotImplementedError
        pass
    def toggleStageDisplay(self):
        raise NotImplementedError
        pass

    def prev(self):
        self._sendKey(0x25)
    def next(self):
        self._sendKey(0x27)

