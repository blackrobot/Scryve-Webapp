<html>
<head>
  <title>Gaelyk Login Demo</title>
  <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;"/>
  <link rel="icon" type="image/png" href="../../iui/iui-favicon.png">
  <link rel="apple-touch-icon" href="../../iui/iui-logo-touch-icon.png" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <link rel="stylesheet" href="../../iui/iui.css" type="text/css" />

  <link rel="stylesheet" href="../../css/iui-panel-list.css" type="text/css" />
  <link rel="stylesheet" title="Default" href="../../iui/t/default/default-theme.css"  type="text/css"/>
  <script type="application/x-javascript" src="../../iui/iui.js"></script>
</head>
<body>
    <div class="toolbar">
        <h1 id="pageTitle"></h1>
        <a id="backButton" class="button" href="#"></a>
    <%  if (user) {  %>
      <a class="button" target="_self" href="<%= users.createLogoutURL(request.requestURI) %>">Logout</a>
    <%  } else {  %>
      <a class="button" target="_self" href="<%= users.createLoginURL(request.requestURI) %>">Login</a>
    <%  }  %>
    </div>
<ul id="home" title="Login Demo" selected="true">
	<li><a href="#about">About Gaelyk Login Demo</a></li>
	<li>
    <%  if (user) {  %>
      User: <%= user.nickname %>
    <%  } else {  %>
      Not logged in.
    <%  }  %>
   </li>
</ul>


<div id="about" class="panel">
  <h2>Gaelyk Login Demo is powered by:</h2>
  <ul>
	<li><a target="_blank" href="http://code.google.com/p/iui/">iUI Project</a></li>
	<li><a target="_blank" href="http://code.google.com/appengine/">Google App Engine</a></li>
	<li><a target="_blank" href="http://gaelyk.appspot.com/">Gaelyk</a></li>
	<li><a target="_blank" href="http://code.google.com/p/iui/wiki/iUIOnGoogleAppEngine">iUI on GAE wiki page</a></li>
  </ul>

</div>

</body>
</html>
