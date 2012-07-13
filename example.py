#!/usr/bin/python

from teleportd import Teleportd

tl = Teleportd('f8369c8ecb7c8e28e8194070702ee58b')

search = tl.search({'str': 'paris'})

print search