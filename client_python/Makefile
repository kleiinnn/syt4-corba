PYTHON         	= /usr/bin/python
PYTHON_PATH     = lib
CPPFLAGS      	= -g -c
OMNIIDL       	= /usr/local/bin/omniidl
IDL_DIR		    = ../idl
IDL_FILE	    = $(IDL_DIR)/chat.idl

all chat_idl.py: $(IDL_FILE)
	$(OMNIIDL) -bpython -Clib $(IDL_FILE)

run: chat_idl.py $(PYTHON)
# Start Naming service with command 'omniNames -start -always' as root
	PYTHONPATH=lib $(PYTHON) client.py markus -ORBInitRef NameService=corbaloc::127.0.0.1:2809/NameService

test: chat_idl.py $(PYTHON)
	PYTHONPATH=lib:. $(PYTHON) test/test_chatroomClient.py

clean clean-up:
	rm -rf *.o
	rm -rf *.hh
	rm -rf *SK.cc
	rm -rf server
