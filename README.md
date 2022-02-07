# Velvere

<p>The API illustrates the "brain" of an intelligent greenhouse, able to take information from the environment and manipulate it according to the needs of the plant.</p>
<h2> The main functionalities </h2>
<ul>
	<li>Authentification service</li>
	<li>Handling of information taken from sensors (humidity, temperature, fertilizer)</li>
</ul>
<p>Source of inspiration: <a href="https://github.com/CryceTruly/bookmarker-api">here</a></p>
<h2> Communication protocols used </h2>
<ul>
	<li>Http</li>
	<li>Mqtt</li>
</ul>
<h2>Development</h2>
<p>For the development I used the <a href="https://flask.palletsprojects.com/en/2.0.x/">Flask</a> framework and for the database, <a href="https://docs.sqlalchemy.org/en/14/">SQLAlchemy</a>.</p>
<h2>Some photos from mqtt subscriber</h2>
<img src= "photos/img1.png"/>
<p>For Mqtt I used a public broker: broker.hivemq.com</p>

<h2>Schema Database</h2>
<img src = "photos/database_schema.jpeg" />