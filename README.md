Breaking Diffie-Hellman protocol using parameter injection through MITM (Man in the Middle) attack
==================================================================================================

Abstract
--------

The Diffie Hellman public-key protocol, used widely across the world, is susceptible to a 
MITM attack in the absence of authentication. This project aims to develop a secure chat server 
which exchanges keys using Diffie-Hellman and then to develop a MITM attack on it to show  the 
"secure" chat can be intercepted.

Usage
-----

### Normal usage of chat
Run the server using `python run.py port_number`. Then, run the client using `python run.py ip_address port_number`. You can then talk between the two systems.

### Running the MITM attack
Run the server using `python run.py port_number_1`. Then run the MITM code using `python server_ip_address port_number_1 port_number_2`. Finally, run `python run.py mitm_ip_address port_number_2`.

This simulates the MITM attack. However, using other tools to jump in the middle using, for example, ARP poisoning etc, then same `ip_address` and `port_number` can be used, as if it were a real attack.

License
-------

The MIT License (MIT)

Copyright © 2015 Jay Bosamiya and Rakholiya Jenish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

