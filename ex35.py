# -*- coding:utf-8 -*-

frmo sys import exit

def gold_room():
	print "This is full of gold. How mych do you take?"

	choice = raw_input("> ")
	if "0" in choice or "1" in choice:
		how_much = int(choice)
	else:
		dead("Man, learn to type a number.")

	if how_much < 50:
		print "Nice, you're not greedy, you win!"
		exit(0)
	else:
		dead("You greedy bastard!")

def bear_room():
	 print "There is a bear here."
	 print "The bear has a bunch of honey."
	 print "The fat bear is in front of another door."
	 
