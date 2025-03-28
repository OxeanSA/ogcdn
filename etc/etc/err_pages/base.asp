<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset="UTF-8">
    <title>Ceera: @Error </title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#111111">
    <link rel="manifest" href="{{ url_for('static', filename='net/manifest.json') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='theme/@logged/home.css') }}">
    </head>
    <body>
        {% block content %}
        {% endblock %}
        <script>
           var pathname = window.location.pathname;
           var nav = document.querySelector('.navbar-nav');
            var anchors = nav.getElementsByTagName('a');
            for (var i = 0; i < anchors.length; i += 1) {
              var href = anchors[i].getAttribute('href');
              if (href == pathname) {
                anchors[i].setAttribute('class', 'nav-item nav-link active');
                var sr_only = anchors[i].getElementsByTagName('span');
                sr_only[0].innerHTML = "(Current)";
              }
              else{
                anchors[i].setAttribute('class', 'nav-item nav-link');
              }
            }
        </script>
    </body>
</html>
