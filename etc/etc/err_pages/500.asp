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

    <div class="jumbotron">
      <h1>Internal Server Error</h1>
      <p>Sorry, it looks like we had a programming error or the server is overloaded</p>
      <p>We're sorry for the inconvenince, please try the link below to return to the homepage</p>
      <hr>
      <a href="{{url_for('index')}}">Go to homepage</a>
    </div>
{% endblock %}
</body>
</html>