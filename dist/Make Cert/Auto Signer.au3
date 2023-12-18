#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=Icon.ico
#AutoIt3Wrapper_Outfile=Auto Signer.Exe
#AutoIt3Wrapper_Res_requestedExecutionLevel=highestAvailable
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
#include <GUIConstantsEx.au3>
#include <AutoItConstants.au3> ;for command output
#include <StaticConstants.au3> ;for centering text
#include <ButtonConstants.au3>
Opt ("TrayAutoPause",0)
$FileOpen = FileOpenDialog("Select executable to sign", @ScriptDir, "Executable (*.exe)|DLL (*.dll)|All (*.*)")
If @error Then
	MsgBox(16, "Error", "Cannot continue without selecting executable you wish to sign.")
	Exit
ElseIf StringInStr ($FileOpen,@ScriptDir) = 0 Then
	MsgBox(16, "Error", "File must be located in the same folder as the Signer tool")
	Exit
ElseIf StringInStr ($FileOpen,@ScriptDir & "\cert2spc.exe") > 0 Then
	MsgBox (16,"Error","This file is utilized by the script. Do not select it.")
	Exit
ElseIf StringInStr ($FileOpen,@ScriptDir & "\makecert.exe") > 0 Then
	MsgBox (16,"Error","This file is utilized by the script. Do not select it.")
	Exit
ElseIf StringInStr ($FileOpen,@ScriptDir & "\pvk2pfx.exe") > 0 Then
	MsgBox (16,"Error","This file is utilized by the script. Do not select it.")
	Exit
ElseIf StringInStr ($FileOpen,@ScriptDir & "\PVKIMPRT.EXE") > 0 Then
	MsgBox (16,"Error","This file is utilized by the script. Do not select it.")
	Exit
ElseIf StringInStr ($FileOpen,@ScriptDir & "\signtool.exe") > 0 Then
	MsgBox (16,"Error","This file is utilized by the script. Do not select it.")
	Exit
EndIf
$GUI = GUICreate("AutoSign", 400, 210)

$INI = @ScriptDir & "\AutoSign.ini"
$SavedSigner = IniRead($INI, "Settings", "Signer", "Your name")
$SavedPassword = IniRead($INI, "Settings", "Password", "Enter password")
$SavedTimeStamp = IniRead($INI, "Settings", "TimeStamp", "http://timestamp.globalsign.com/scripts/timstamp.dll")
$SW_SHOW = IniRead ($INI,"Settings","ShowBatchWindow","")

GUICtrlCreateGroup("Certificate Information", 5, 5, 200, 200)
GUICtrlCreateLabel("Signer ", 10, 32, 35, 20, $SS_RIGHT)
$SignerInput = GUICtrlCreateInput($SavedSigner, 50, 30, 100, 20)
$SignerSave = GUICtrlCreateButton("Save", 150, 30, 50, 20)
GUICtrlCreateLabel("Pswd ", 10, 62, 35, 20, $SS_RIGHT)
$PasswordInput = GUICtrlCreateInput($SavedPassword, 50, 60, 100, 20)
$PasswordSave = GUICtrlCreateButton("Save", 150, 60, 50, 20)
GUICtrlCreateLabel("Timestamp URL", 15, 92, 170, 20, $SS_CENTER)
$TimeStampInput = GUICtrlCreateInput($SavedTimeStamp, 15, 110, 135, 20)
$TimeStampSave = GUICtrlCreateButton("Save", 150, 110, 50, 20)

GUICtrlCreateLabel("Target ", 10, 142, 40, 20, $SS_RIGHT)
$File = GUICtrlCreateInput($FileOpen, 50, 140, 100, 20)
$FileBrowse = GUICtrlCreateButton("Browse", 150, 140, 50, 20)


GUICtrlCreateGroup("Output log", 210, 5, 185, 200)
$Log = GUICtrlCreateEdit("", 215, 30, 175, 170)

$Start = GUICtrlCreateButton("Sign selected target", 10, 170, 190, 30, $BS_CENTER)
GUICtrlSetFont(-1, 10, 800)

GUISetState(@SW_SHOW)
_CheckForFiles()
While 1
	$msg = GUIGetMsg()
	If $msg = $GUI_EVENT_CLOSE Then Exit
	If $msg = $SignerSave Then IniWrite($INI, "Settings", "Signer", GUICtrlRead($SignerInput))
	If $msg = $PasswordSave Then IniWrite($INI, "Settings", "Password", GUICtrlRead($PasswordInput))
	If $msg = $TimeStampSave Then IniWrite($INI, "Settings", "TImeStamp", GUICtrlRead($TimeStampInput))
	If $msg = $FileBrowse Then
		$FileOpen = FileOpenDialog("Select executable to sign", "", "Executable (*.exe)")
		If @error Then
			MsgBox(16, "Error", "Cannot cintinue without selecting executable you wish to sign")
		Else
			GUICtrlSetData($File, $FileOpen)
		EndIf
	EndIf
	If $msg = $Start Then _Run()
WEnd

Func _CheckForFiles()
	$Count = 0 ;add one for each found file
	If FileExists(@ScriptDir & "\capicom.dll") = 0 Then GUICtrlSetData($Log, @CRLF & "capicom.dll not found")
	If FileExists(@ScriptDir & "\cert2spc.exe") = 0 Then GUICtrlSetData($Log, @CRLF & "cert2spc.exe not found")
	If FileExists(@ScriptDir & "\makecert.exe") = 0 Then GUICtrlSetData($Log, @CRLF & "makecert.exe not found")
	If FileExists(@ScriptDir & "\pvk2pfx.exe") = 0 Then GUICtrlSetData($Log, @CRLF & "pvk2pfx.exe not found")
	If FileExists(@ScriptDir & "\PVKIMPRT.EXE") = 0 Then GUICtrlSetData($Log, @CRLF & "PVKIMPRT.EXE not found")
	If FileExists(@ScriptDir & "\signtool.exe") = 0 Then GUICtrlSetData($Log, @CRLF & "signtool.exe not found")
EndFunc   ;==>_CheckForFiles

Func _Run()
	$Executable = GUICtrlRead($File)
	If @error Then Exit
	GUICtrlSetData ($Log,"")
	DirCreate ("Certificates")
	$Password = GUICtrlRead($PasswordInput)
	$TimeStamp = GUICtrlRead($TimeStampInput)
	$Signer = GUICtrlRead($SignerInput)

	$Code1 = 'makecert.exe -r -n "CN=' & $Signer & '" -b 01/01/2013 -e 01/01/2099 -eku 1.3.6.1.5.5.7.3.3 -sv "Certificates\' & $Signer & '_cert.pvk" "Certificates\' & $Signer & '_cert.cer"'
	$Code2 = 'cert2spc.exe "Certificates\' & $Signer & '_cert.cer" "Certificates\' & $Signer & '_cert.spc"'
	$Code3 = 'pvk2pfx.exe -pvk "Certificates\' & $Signer & '_cert.pvk" -pi ' & $Password & ' -spc "Certificates\' & $Signer & '_cert.spc" -pfx "Certificates\' & $Signer & '_cert.pfx" -po ' & $Password
	$Code4 = 'signtool.exe sign /f "Certificates\' & $Signer & '_cert.pfx" /p ' & $Password & ' "' & $Executable & '"'
	$Code5 = 'signtool.exe timestamp /t "' & $TimeStamp & '" "' & $Executable & '"'

	$Run = Run('"' & @ComSpec & '" /c ' & $Code1, '', $SW_SHOW, $STDERR_CHILD + $STDOUT_CHILD)
	If WinWait("Create Private Key Password", "", 2) = 0 Then ;Wait for required window
		GUICtrlSetData($Log, GUICtrlRead($Log) & @CRLF & "$Code1 1st Required window did not open. Possibly due to existing certificate.")
	Else
		ControlSend("Create Private Key Password", "", "Edit1", $Password) ;Send password to window
		ControlSend("Create Private Key Password", "", "Edit2", $Password) ;Confirm password
		ControlClick("Create Private Key Password", "", "Button1") ;Click OK button
	EndIf
	If WinWait("Enter Private Key Password", "", 2) = 0 Then ;Wait for required window
		GUICtrlSetData($Log, GUICtrlRead($Log) & @CRLF & "$Code1 2nd Required window did not open. Terminating process")
		Return
	Else
		ControlSend("Enter Private Key Password", "", "Edit1", $Password) ;Send password to window
		ControlClick("Enter Private Key Password", "", "Button1") ;Click OK button
		ProcessWaitClose($Run)
		GUICtrlSetData($Log, GUICtrlRead($Log) & @CRLF & "$Code1=" & StdoutRead($Run))
	EndIf

	$Run = Run('"' & @ComSpec & '" /c ' & $Code2, '', $SW_SHOW, $STDERR_CHILD + $STDOUT_CHILD)
	ProcessWaitClose($Run)
	GUICtrlSetData($Log, GUICtrlRead($Log) & "$Code2=" & StdoutRead($Run))

	$Run = Run('"' & @ComSpec & '" /c ' & $Code3, '', $SW_SHOW, $STDERR_CHILD + $STDOUT_CHILD)
	ProcessWaitClose($Run)
	If StdoutRead($Run) = "" Then
		GUICtrlSetData($Log, GUICtrlRead($Log) & "$Code3=Blank. Probably OK" & @CRLF & StdoutRead($Run))
	Else
		GUICtrlSetData($Log, GUICtrlRead($Log) & "$Code3=" & @CRLF & StdoutRead($Run))
	EndIf

	$Run = Run('"' & @ComSpec & '" /c ' & $Code4, '', $SW_SHOW, $STDERR_CHILD + $STDOUT_CHILD)
	ProcessWaitClose($Run)
	GUICtrlSetData($Log, GUICtrlRead($Log) & "$Code4=" & StdoutRead($Run))

	$Run = Run('"' & @ComSpec & '" /c ' & $Code5, '', $SW_SHOW, $STDERR_CHILD + $STDOUT_CHILD)
	ProcessWaitClose($Run)
	$message = StdoutRead($Run)
	If StringInStr ($message, "Success") = 0 Then ;one space is returned if error ?
		GUICtrlSetData($Log, GUICtrlRead($Log) & "$Code5=Cannot get timestamp. Try again or change timestamp URL" & @CRLF)
	Else
		GUICtrlSetData($Log, GUICtrlRead($Log) & "$Code5=" & $message & @CRLF)
	EndIf
	GUICtrlSetData($Log, GUICtrlRead($Log) & "Finished")
EndFunc   ;==>_Run
