# Altair Server

Python web server for the Altair hands on test

## Table of contents

1. [Building and running the app](#1-building-and-running-the-app)
2. [Technical details](#2-technical-details)
3. [Next steps](#3-next-steps)

## 1. Building and running the app

### 1.1 Deploying the full system using Docker Swarm (Recommended)

> This is the recommended way for testing the application as it doesn't need any additional configuration. Note that this
is not a production ready configuration and should only be used in one node.

The app comes with a `docker-compose.yml` file which can be used to deploy a stack of containers using Docker Swarm
spawning a server and three different clients within the same network. 

First we need to start a Docker Swarm node using:

```shell script
$ docker swarm init
```

Then we can deploy the stack using:

```shell script
$ docker stack deploy -c docker-compose.yml altair-stack

    Creating network altair-stack_altair-network
    Creating service altair-stack_altair-client-2
    Creating service altair-stack_altair-client-3
    Creating service altair-stack_altair-server
    Creating service altair-stack_altair-client-1
```
This will spawn a server, three clients, and a network which handles communication amongst them. 

As we can see the containers don't start in a specific order, and as we didn't provide internal failover for the clients,
they will fail if they start before the server. However, Swarm handles this by restarting dead containers until they are
successfully running.

We can then check the state of the services using:

```shell script
$ docker stack ps altair-stack

    ID                  NAME                             IMAGE                          NODE                DESIRED STATE       CURRENT STATE            ERROR                       PORTS
    z3l3ma728ys8        altair-stack_altair-client-1.1   prodalia/altair-client:1.0.0   docker-desktop      Running             Running 17 seconds ago                               
    ts8gl7y0qfnw        altair-stack_altair-client-3.1   prodalia/altair-client:1.0.0   docker-desktop      Running             Running 15 seconds ago                               
    mzan8v67vm1d        altair-stack_altair-client-2.1   prodalia/altair-client:1.0.0   docker-desktop      Running             Running 15 seconds ago                               
    ytg4b1phbxtk        altair-stack_altair-server.1     prodalia/altair-server:1.0.0   docker-desktop      Running             Running 17 seconds ago                               
    ngzqd8o4jlgw        altair-stack_altair-client-3.1   prodalia/altair-client:1.0.0   docker-desktop      Shutdown            Failed 21 seconds ago    "task: non-zero exit (1)"   
    7ug06lv585nm        altair-stack_altair-client-2.1   prodalia/altair-client:1.0.0   docker-desktop      Shutdown            Failed 21 seconds ago    "task: non-zero exit (1)"   
```
> Here we can see how two of the clients failed at first (as they tried to start before the server was up) but are now
> successfully running. 

We can check the logs of any of our services using `$ docker service logs <service>`:


> Note: We can use the ID (`9phs3kei28cv`) or the NAME (`altair-stack_altair-server.1`)

- Server logs:
```shell script
$ docker service logs -f 9phs3kei28cv 

    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,740 [  MainThread  ] [ INFO ] BeerDB Instance running
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,740 [  MainThread  ] [ INFO ] Instance with id 140564541893072 is observing DB updates
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,740 [  MainThread  ] [ INFO ] Instance with id 140564541893136 is observing DB updates
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,742 [  MainThread  ] [ INFO ] Started Web Service listening for connections on port 8338
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,815 [  MainThread  ] [ INFO ] 101 GET /sockets/beers (10.0.0.4) 0.47ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,815 [  MainThread  ] [ INFO ] A new tap has been connected to the system
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,818 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 1 posted a new beer (id: 0)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:57,818 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 0.70ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:59,584 [  MainThread  ] [ INFO ] 101 GET /sockets/beers (10.0.0.4) 0.35ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:59,584 [  MainThread  ] [ INFO ] A new tap has been connected to the system
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:59,586 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 2 posted a new beer (id: 1)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:53:59,587 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 0.70ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:00,094 [  MainThread  ] [ INFO ] 101 GET /sockets/beers (10.0.0.4) 0.33ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:00,094 [  MainThread  ] [ INFO ] A new tap has been connected to the system
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:00,098 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 3 posted a new beer (id: 2)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:00,099 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 1.07ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:00,824 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 1 posted a new beer (id: 3)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:00,825 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 1.27ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:02,107 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 3 posted a new beer (id: 4)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:02,108 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 1.28ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:03,833 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 1 posted a new beer (id: 5)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:03,834 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 1.12ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:04,115 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 3 posted a new beer (id: 6)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:04,116 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 1.10ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:04,840 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 1 posted a new beer (id: 7)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:04,841 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 1.24ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:08,123 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 3 posted a new beer (id: 8)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:08,124 [  MainThread  ] [ INFO ] 200 POST /api/beers (10.0.0.4) 1.04ms
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:09,595 [  MainThread  ] [ INFO ] New DB Hook Notification: Tap with id 2 posted a new beer (id: 9)!
    altair-stack_altair-server.1.ytg4b1phbxtk@docker-desktop    | 2019-09-17 18:54:09,595 [  MainThread  ] [ INFO ] {'tap 1': '40.0%', 'tap 2': '20.0%', 'tap 3': '40.0%', 'total beers': 10}
```

- Client logs:

```shell script
$ docker service logs -f qij24he6jzv0

    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:53:57,811 [  MainThread  ] [ INFO ] 
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    |  - Inet Addr: altair-server:8338 
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    |  - Tap ID: 1 
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:53:57,812 [  MainThread  ] [ INFO ] Attempting to connect to: ws://altair-server:8338/sockets/beers
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:53:57,815 [  MainThread  ] [ INFO ] Posting beer...
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:53:57,818 [  MainThread  ] [ INFO ] Tap with id 1 posted a new beer (id: 0)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:00,820 [  MainThread  ] [ INFO ] Posting beer...
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:00,821 [  MainThread  ] [ INFO ] Tap with id 2 posted a new beer (id: 1)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:00,822 [  MainThread  ] [ INFO ] Tap with id 3 posted a new beer (id: 2)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:00,825 [  MainThread  ] [ INFO ] Tap with id 1 posted a new beer (id: 3)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:03,829 [  MainThread  ] [ INFO ] Posting beer...
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:03,830 [  MainThread  ] [ INFO ] Tap with id 3 posted a new beer (id: 4)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:03,833 [  MainThread  ] [ INFO ] Tap with id 1 posted a new beer (id: 5)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:04,836 [  MainThread  ] [ INFO ] Posting beer...
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:04,838 [  MainThread  ] [ INFO ] Tap with id 3 posted a new beer (id: 6)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:04,841 [  MainThread  ] [ INFO ] Tap with id 1 posted a new beer (id: 7)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:09,850 [  MainThread  ] [ INFO ] Posting beer...
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:09,853 [  MainThread  ] [ INFO ] Tap with id 3 posted a new beer (id: 8)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:09,853 [  MainThread  ] [ INFO ] Tap with id 2 posted a new beer (id: 9)!
    altair-stack_altair-client-1.1.z3l3ma728ys8@docker-desktop    | 2019-09-17 18:54:09,854 [  MainThread  ] [ INFO ] {"tap 1": "40.0%", "tap 2": "20.0%", "tap 3": "40.0%", "total beers": 10}    
```

### 1.2 Running the server standalone mode

The app is meant to be run using a Dockerized environment. The latest image of the app is hosted in Docker Hub under 
the tag `prodalia/altair-server:latest` and it is public.

> This scripts use the altair-network so it should be created first if we want to use it `docker network create altair-network` 

The following command is used to run the app using the latest image:

```shell script
$ docker container run \
      -d \
      --name altair-server \
      --network altair-network \ 
      -p 8080:8338 \
      prodalia/altair-server
```

> The server can also be run as a python process using `$ PORT=8338 python server.py`

This will download the image and run a container named `altair-server` binding the app to the host port `8080`. This
binding can be done to any other host port, but the container port has to remain the same (`8338`) as it is the port
the Web Service will be listening to.

We can then interact with the app by running one or more [clients](https://github.com/pedro-rodalia/altair-client) or
using [postman](https://www.getpostman.com/).

The App logs detailed information about the processes, and helps understand how it works. In order to see the logs 
in real time we can do so using the command:

```shell script
$ docker container logs -f altair-server
```

The repository also contains a Dockerfile so it is possible to build new images after modifying the source code using the
following command:

```shell script
$ docker image build -t altair-server-mod .
```

### 1.3 Running the client standalone mode

The client is also meant to be run as a Docker container, and takes environment arguments so we can manually set the
`tap_id` and the `inet_addr` so it can communicate with the server. 

```shell script
$ docker run \
        -d \
        --env INET_ADDR=altair-server:8338 \
        --env TAP_ID=1 \
        --network altair-network \
        --name altair-client \
        prodalia/altair-client
```

> The client can also be run as a python process using `$ INET_ADDR=localhost:8338 TAP_ID=1 python client.py`

## 2. Technical details

### App Context

The scenario this Web App works on is something like the following:

Multiple beer taps are provided with an IoT device which can measure the amount of beer they pour on each glass and 
send this information to a centralized system. It will be the WebServer's task to identify which type of glass has been
served to the customer based on the volume the devices report for each pouring. This communication gets done using the 
HTTP protocol and a REST interface.

On the other hand, the centralized system registers connected taps and sends a signal every time a new beer is poured somewhere. 
Ideally it should not notify the tap that has triggered the operation, but we will keep it simple so the message
will be broadcasted to all connected devices. It also sends in a report with some metrics to all devices periodically.
These feedback communication is performed using the WS protocol.
 

### Basic functionality

This hands on exercise has been developed using as fewer third party libraries as possible. The only dependency required
is the **Tornado Web Framework** for python.

The main goal of this Web Service is to handle HTTP requests in a RESTful manner and notify the connected devices about
changes in the system using the WebSocket protocol. It opens a listener on port `8338` for incoming requests on the 
endpoint `http:/api/beers` and lets clients subscribe to notifications on the `ws:/socket/beers`.
 
For simplicity the app only allows the `POST`, `GET` and `DELETE` method using basic numerical ids and the database collection
only stores beers using the following model:

```json
{
  "tapId": "<integer>",
  "volume": "<double[100, 1000]>"
}
```

The complete model for a `beer` resource contains more data which is inferred from the volume (the `type` property) or 
created when saving the document (`timestamp` and `id` properties).

The three basic operations that can be performed against this API are:

- **Create a beer:** Using the `/api/beers` endpoint and the `POST` method with a valid beer model.
- **Get a list of served beers:** Using the `/api/beers` endpoint and the `GET` method. This endpoint is paginated and 
    filterable and accepts query parameters such as `page`, `page_size` and `type`.
- **Get a beer using its ID:** Using the `/api/beers/:id` endpoint and the `GET` method and a valid `ID` (it will return 
    a `404 Not Found` if there are no matches).
- **Delete a beer using its ID:**Using the `/api/beers/:id` endpoint and the `DELETE` method and a valid `ID`.

> This API not have any kind of authentication handlers or validation methods for the incoming requests, so it is not robust
and has not been hard tested.

### App structure and design

![Design](/img/design.png)

Upon initialization, the app will spawn a new DB using the BeerDB class, which is a *Singleton* for this data structure and
provides the database of its basic operations (Create, Read and Delete for simplicity). The use of the *Singleton* pattern here
is used so that it guarantees that the DB instance is unique and the collection will be preserved after multiple 
instantiations of the database across the code. The BeerDB class is also built using the *Observer* pattern, so other
classes can be attached to it and be notified when changes occur within the collection.

> The Singleton implementation used here is not thread-safe, but as no multi threaded processes are being used we can
> live with it.

Database operations are treated here as asynchronous operations as they usually are when working with real databases, 
which justifies the use of coroutines for these methods although it can be technically incorrect.

As Request Handler objects are created on each request, we need another class that subscribes to the BeerDB in order to
notify connected devices. This way, the RealTimeHandler will just store the WebSocket connections in a set and we can use 
the **Notifier** class to subscribe to the DB and broadcast messages to all the devices reading their connections from
the `taps` set.

Another design pattern used is the *Decorator pattern*, which in this context helps reuse the pagination and
serialization logic for different database read operations.

## 3. Next Steps

Most of the decisions taken while developing this App where based on simplicity and quickness, and as such there is a lot
of room for improvement. Here I list some of these improvements that would logically follow the development in order to 
build a more robust and functional app.

- Some kind of authentication method should be applied to both REST operations and WebSocket connections. While the API 
  could be public for any `GET` operation, the `POST` and `DELETE` methods should be protected.
- Connected devices only exit when they are unable to connect to the server via WebSockets. This is intended because in a
  containerized environment we could retry this connection by restarting the service instead of introducing logic within
  the client app. However, there are many other failover techniques which should be implemented both on client and server
  side in order to make this a robust system.
- Error handling is not configured. Some exceptions are raised, but exceptions coming from the Tornado Framework are not 
  mapped nor handled. However the right pattern seems to be extend the Tornado Web Handlers using a base
  class for common tasks such as error handling and user authentication and subclassing this custom handler
  for any specific request handling we want to perform. 
- App structure is something I still struggle with, and possibly could be improved.