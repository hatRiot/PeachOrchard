Peach Orchard
==

Peach Orchard is a web front-end to aggregate crash and status information for different fuzzers; it provides a centralized server and distributed nodes that centralizes all crash and status information.  Each system that runs a fuzzer can fire up an Orchard node that will send crash information back to the mothership, which will then be viewable from the web interface.  If you happen to run a dozen or so fuzzers like I do, this is a nice way to pull that information together to quickly check for any crashes.

I'm bad at web design and have implemented a simple Django app with Bootstrap3; if you're a web guy who likes doing web things, I'd love PRs.

This is similar iSEC's [PeachFarmer](https://github.com/iSECPartners/PeachFarmer) project, but whilst that only aggregates logs, this provides a way of viewing the data.  Also has the added benefit of not opening up ports on all your fuzzing machines; Peach Orchard follows a strict push-only architecture, in which all fuzzers push data up to the core server; one IP, one port.

Requirements
----
Server & Node
* Python >= 2.7.x (tested on 2.7.3)

Server:
* Django >= 1.6.x (tested on 1.6.5)

Node:
* Requests >= 2.2.x (tested on 2.2.3)


Tested on both Windows and Linux.

Action
-----

Home Page
![Home](http://i.imgur.com/m3Jwze4.jpg)

Node View
![Node](http://i.imgur.com/tq9EkX4.jpg)

Crash View
![Crash](http://i.imgur.com/f3eHtP7.jpg)


Setup
----

Pretty simple, really.  Fundamentally there are two bits of information a Peach Orchard node needs: one, how and where nodes communicate, and what nodes monitor.  The how and where can be configured in `src/core/config.py` by setting the following:

* SERVER_KEY  
  -- This is the shared key needed to authenticate a node with a server.  On initial setup, the server will generate `secret_key.py`, which contains your randomly generated 64 byte PSK.  Paste this into here.

* SERVER_IP  
  -- Location of the core server, naturally.

* MONITOR_DIR  
  -- Absolute path to your output directory.  Please keep this as a raw string, otherwise it'll be angry with your Windows paths.

To start the server, run `./start_server.sh`.  _If this is the first run, the database will be built and you'll need to create an administrative user.

To start the node, ensure `config.py` is setup correctly, then run `python node.py -f [your fuzzer] -n [your session name]`.  

Fuzzer Support
----

Currently PeachOrchard supports the following fuzzers:

* Peach
* American Fuzzy Lop (v0.45b+)

On the to-do list:

* Sulley
* SPIKE

Other requests welcome.


TODO
----

* Beef up node logging
* User authentication
* Clean up code
* Node session management (i.e. managing one node's successive fuzzing campaigns)
* Local caching for nodes if they lose connectivity to the mothership
* Crashes page that aggregates all fuzzer crash information
* Last-seen timestamp
