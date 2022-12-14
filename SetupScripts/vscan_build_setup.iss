; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "CAN Library"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "?? ??? ??????"
#define MyAppURL "http://www.module.ru/"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{3AE78376-C173-4AA1-A387-2C6A4595A463}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; ?????????? ?????, ? ??????? ?????????? ????????? ?????????? ????????? ?? ?????????
DefaultDirName={code:GetDefRoot}\Lib\site-packages\RC_Module\

;????????? ???????????? ???????? ????? ??? ????????? ?????????? ? ???????? ????? ????? ?????????? ???????????? ?? ?????
DisableDirPage=yes

;????????? ???????????? ???????? ??? ????? ???? ????
DisableProgramGroupPage=yes

; ?? ????????? ????? ??????????
; CreateAppDir=no

;????????????? ??????????? ?? ?????
Uninstallable=no

; ?????, ? ??????? ????? ??????????? ????? ????????? ???????????? ????? ???????.
OutputDir=../Build

; ????????? ?????? ?????? ??????? ??? ??? ??????????? ????? ?????????
OutputBaseFilename=vscan_setup

; ??????
Compression=lzma
SolidCompression=yes

; ?????? ???????????
SetupIconFile=satellite.ico

; ????????
WizardImageFile=logo_big.bmp
WizardSmallImageFile=logo.bmp

[Code]
//
// ??????? ?????????? ???? ??? ???????
//
function GetHKLM: Integer;
begin
  if IsWin64 then
    Result := HKLM64
  else
    Result := HKLM32;
end;

//
// ??????? ?????????? ???? ????????? ??????
//
function GetDefRoot(Param: String): String;
var Path: String;
begin
    if RegQueryStringValue(GetHKLM, 'SOFTWARE\Wow6432Node\Python\PythonCore\3.9\InstallPath', '',Path) then
        Result := Path
    else begin
        if RegQueryStringValue(GetHKLM, 'SOFTWARE\Python\PythonCore\3.9\InstallPath', '',Path) then
            Result := Path
        else begin
            MsgBox('Python 3.9 ?? ?????? ?? ?????? ??????????. ??????? ?????????? Python 3.9', mbInformation, MB_OK);
            abort();
        end;
    end;
end;

//
// ??????? ?????????? ???? ? ??????? ?? PythonPath
//
function FindRegeditEntry(Param: String): String;
var Path: String;
begin
    if RegQueryStringValue(GetHKLM, 'SOFTWARE\Wow6432Node\Python\PythonCore\3.9\PythonPath', '',Path) then
        Result := 'SOFTWARE\Wow6432Node\Python\PythonCore\3.9\PythonPath'
    else begin
        if RegQueryStringValue(GetHKLM, 'SOFTWARE\Python\PythonCore\3.9\PythonPath', '',Path) then
            Result := 'SOFTWARE\Python\PythonCore\3.9\PythonPath'
        else begin
            MsgBox('Python 3.9 ?? ?????? ?? ?????? ??????????. ??????? ?????????? Python 3.9', mbInformation, MB_OK);
            abort();
        end;
    end;
end;

// True - ???? ????? ?????????
function FindSubstring(_find: String; _str: String): Boolean;
var
    is_tmp: String;
    tmp_pos: Integer;
begin
    tmp_pos := pos(_find, _str)

    if tmp_pos = 0 then
        Result:= False
    else
    begin
        tmp_pos := tmp_pos + Length(_find);

        // ???? ????? ??????
        if tmp_pos > Length(_str) then
            Result := True
        // ???? ?? ????? ??????
        else
        begin
            // ???? ????????? ?????? ;
            if _str[tmp_pos] = ';' then
                Result := True
            // ???? ??? ?? ????? ?????? ? ?? ";"
            else
            begin
                // ???????? _str
                _str := Copy(_str, tmp_pos, Length(_str) - tmp_pos + 1)

                // ? ???? ??????
                Result := FindSubstring(_find, _str);
            end;
        end;
    end;
end;

//
// ??????? ????????? ???? ? ??????????
//
function AddLibraryPath(Param: String): String;
var tmp_str: String;
begin
    if Param = '' then
        // ???? ? ??????? ??? ?????? ?????? ?? ?????????, ?? ?? ????? ???????
        Result := ExpandConstant('{app}')
    else
    begin
        if FindSubstring(ExpandConstant('{app}'), Param) then
            // ???? ? ???? ??? ????????, ?? ????? ??????? ??????
            Result := Param
        else
        begin
            if Param[length(Param)] = ';' then
                tmp_str := ''
            else
                tmp_str := ';';

            Result := Param + tmp_str + ExpandConstant('{app}');
        end
    end;
end;

[Registry]
Root: HKLM; Subkey: "{code:FindRegeditEntry}\RC_MODULE"; ValueType: string; ValueName: ""; ValueData: "{code:AddLibraryPath|{olddata}}";

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
Source: "../*"; DestDir: "{app}\vs_can_lib"; Excludes: ".git, .idea, .pyc .vscode, build, __pycache__, dist, *egg-info"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Run]
Filename: "cmd.exe"; Parameters: "/c echo RC_Module/vs_can_lib > ""{app}\..\vs_can_lib.pth"" && echo RC_Module/ >> ""{app}\..\vs_can_lib.pth"""; StatusMsg: "?????????? pth-????? ??????????. ??? 1 ?? 1";



