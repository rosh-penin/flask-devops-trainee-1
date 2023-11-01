# flask-devops-trainee-1

### Task 1
Python scripts that checks memory usage and send alert as GET request to provided API server.
#### Install:
From project (task_1) folder
~~~sh
pip install -r requirements
~~~
#### Run:
~~~sh
python memory_monitor <http://your_address.domain> <memory_percent_alert>
~~~
There is two positional parameters and first one (address) is mandatory. If not set or set incorrectly the app will fail.
memory_percent_alert is optional parameter and can be set inside app as constant
#### Logging:
There is basic logging that stores error-leveled events to file.

### Task 2
docker-compose with nosql redis db and Flask REST api.
#### There is no installation part.
But you need docker-compose installed on your system.
#### Run:
From project folder
~~~sh
docker-compose up -d
~~~
After this API should be running on your machine on 8080 port.
#### Usage:
There is 3 endpoints:
~~~
GET http://your_address:8080/<key>
POST http://your_address:8080/<key>
PUT http://your_address:8080/<key>
~~~
POST and PUT requests requires json in their body.
### PS
There is some issues as DRY imperfection but i'll leave this as it is.