; Inno Setup Script for Android Project Rebuilder - Windows Installer
; Requires Inno Setup 6: https://jrsoftware.org/isdl.php

[Setup]
; App Information
AppName=Android Project Rebuilder
AppVersion=1.0.0
AppPublisher=Android Rebuilder Team
AppPublisherURL=https://github.com/yourproject
AppSupportURL=https://github.com/yourproject/issues
AppUpdatesURL=https://github.com/yourproject/releases

; Installation Directories
DefaultDirName={autopf}\AndroidProjectRebuilder
DefaultGroupName=Android Project Rebuilder
DisableProgramGroupPage=yes

; Output
OutputDir=..\dist
OutputBaseFilename=AndroidProjectRebuilder-Setup-v1.0.0
SetupIconFile=..\resources\icon.ico
UninstallDisplayIcon={app}\AndroidProjectRebuilder.exe

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=2

; Visual
WizardStyle=modern
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

; Requirements
MinVersion=10.0.17763
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\AndroidProjectRebuilder.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Android Project Rebuilder"; Filename: "{app}\AndroidProjectRebuilder.exe"
Name: "{group}\{cm:UninstallProgram,Android Project Rebuilder}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Android Project Rebuilder"; Filename: "{app}\AndroidProjectRebuilder.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AndroidProjectRebuilder.exe"; Description: "{cm:LaunchProgram,Android Project Rebuilder}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // Check if WebView2 Runtime is installed (optional)
  // Most Windows 10/11 systems have it by default
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation tasks if needed
  end;
end;
