{% extends "./base.asp" %}
{% block content %}

    <div class="jumbotron">
      <h1>Page Not Found</h1>
      <p>Sorry, what you were looking for is not here.</p>
      <hr>
      <h1>Create an account</h1>
      <a href="{{url_for('main')}}">Go to signup page</a>
    </div>
{% endblock %}
