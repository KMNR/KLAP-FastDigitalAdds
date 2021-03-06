; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "KLAP Add Shortcut"
#define MyAppVersion "0.2"
#define MyAppPublisher "KMNR (Stephen Jackson)"
#define MyAppURL "klap.kmnr.org"
#define MyAppExeName "digital_add.exe"

#expr Exec("python setup.py py2exe")

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{CF714F12-EA72-4562-92FA-82B58753D937}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\digital_add.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ContextItem.reg"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\python27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCR; Subkey: "Directory\shell\AddToKlap"; ValueType: string; ValueName: ""; ValueData: "Add To KLAP"; Flags: uninsdeletekey 
Root: HKCR; Subkey: "Directory\shell\AddToKlap\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey
Root: HKCR; Subkey: "Directory\Background\shell\AddToKlap"; ValueType: string; ValueName: ""; ValueData: "Add To KLAP"; Flags: uninsdeletekey 
Root: HKCR; Subkey: "Directory\Background\shell\AddToKlap\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%V"""; Flags: uninsdeletekey