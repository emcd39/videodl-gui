; NSIS Modern UI Installer Script for videodl
; 安装目录: %USERPROFILE%\AppData\Local\videodl
; 桌面快捷方式: videodl_gui

!define PRODUCT_NAME "videodl"
!define PRODUCT_VERSION "0.6.2"
!define PRODUCT_PUBLISHER "videodl"
!define PRODUCT_WEB_SITE "https://github.com/emcd39/videodl-gui"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\videodl_gui.exe"

; Set the installation directory to $LOCALAPPDATA\videodl
!define PRODUCT_INSTALL_DIR "$LOCALAPPDATA\${PRODUCT_NAME}"

;--------------------------------------------------------------------------------------------------
; Configuration
;--------------------------------------------------------------------------------------------------

; Request admin rights on Windows Vista and above
RequestExecutionLevel user

; Include Modern UI
!include "MUI2.nsh"

; Interface Settings
!define MUI_ABORTWARNING

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "videodl" SecMain

  ; Set output path to the installation directory
  SetOutPath "${PRODUCT_INSTALL_DIR}"

  ; Install all files from dist_gui folder
  File /r "dist_gui\videodl_gui\*.*"

  ; Create desktop shortcut
  CreateShortCut "$DESKTOP\videodl_gui.lnk" "${PRODUCT_INSTALL_DIR}\videodl_gui.exe" "" "${PRODUCT_INSTALL_DIR}\videodl_gui.exe" 0

  ; Create start menu shortcut
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME} GUI.lnk" "${PRODUCT_INSTALL_DIR}\videodl_gui.exe" "" "${PRODUCT_INSTALL_DIR}\videodl_gui.exe" 0
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "${PRODUCT_INSTALL_DIR}\uninstall.exe"

  ; Create uninstaller
  WriteUninstaller "${PRODUCT_INSTALL_DIR}\uninstall.exe"

  ; Write registry keys for Add/Remove Programs
  WriteRegStr SHCTX "${PRODUCT_DIR_REGKEY}" "" "${PRODUCT_INSTALL_DIR}\videodl_gui.exe"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "UninstallString" "${PRODUCT_INSTALL_DIR}\uninstall.exe"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "DisplayIcon" "${PRODUCT_INSTALL_DIR}\videodl_gui.exe"
  WriteRegDWORD SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "NoModify" 1
  WriteRegDWORD SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "NoRepair" 1

SectionEnd

; Uninstaller Section
Section "Uninstall"

  ; Delete files and directories
  RMDir /r "${PRODUCT_INSTALL_DIR}"

  ; Delete shortcuts
  Delete "$DESKTOP\videodl_gui.lnk"
  RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"

  ; Delete registry keys
  DeleteRegKey SHCTX "${PRODUCT_DIR_REGKEY}"
  DeleteRegKey SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"

SectionEnd

; Functions
Function .onInit

  ; Set the installation directory
  StrCpy $INSTDIR "${PRODUCT_INSTALL_DIR}"

FunctionEnd

; Descriptions
LangString DESC_SecMain ${LANG_SIMPCHINESE} "videodl 视频下载工具"
LangString DESC_SecMain ${LANG_ENGLISH} "videodl Video Downloader"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
