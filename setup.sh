#!/bin/sh
  curl http://localhost:5001/init_syn/0
  curl http://localhost:5001/init_syn/1
  curl http://localhost:5001/init_syn/2
  curl http://localhost:5001/init_syn/3
  curl http://localhost:5002/init_syn/0
  curl -k http://localhost:5002/init_syn/1
  curl -k http://localhost:5002/init_syn/2
  curl -k http://localhost:5002/init_syn/3
  curl -k http://localhost:5003/init_syn/0
  curl -k http://localhost:5003/init_syn/1
  curl -k http://localhost:5003/init_syn/2
  curl -k http://localhost:5003/init_syn/3
