{% extends "./base.asp" %}
{% block content %}

    <div class="jumbotron">
      <h1>Access to the page is restricted!</h1>
      <p>Sorry, what you were looking for is not there.</p>
      <hr>
      <h1>Contact ©Ceera for more!</h1>
      <a href="{{url_for('main')}}">Back to application</a>
    </div>
{% endblock %}
