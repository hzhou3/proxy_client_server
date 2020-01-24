Programming Assignment 3

First to set up proxy HTTP request in LAN setting.

Part A: proxyServer.py
	A simple proxy server.
	python proxyServer.py [your IP] [Port #]
	e.g. python proxyServer.py 130.74.96.125 8888

Part B: threadedServer.py
	A proxy server with multi-threading
	python threadedServer.py [your IP] [Port #]

Part C: cachedServer.py
	A proxy server with caching function (No multi-threading)
	python cachedServer.py [your IP] [Port #]

If user does not want to set up proxy service in the LAN setting, leave message[1] = message[1].replace(message[1], "Host: " + host_name) uncommented in each file.
(Line 65 in threadedServer.py, Line 72 in proxyServer.py and cachedServer.py)


