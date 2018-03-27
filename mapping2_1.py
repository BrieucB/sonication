#!/usr/bin/python
# -*- coding: utf-8 -*-

# INPUT : datafile.dat
# OUPUT : song_1.mid

from midiutil import MIDIFile
import random as ra

f_in=open("datafile.dat", "r")

song=MIDIFile(numTracks=9, adjust_origin=False)

duration=1
mes=4
t=0

rate_min=0.0
rate_max=100.0
pitch_min=[50.0, 50.0, 60.0, 60.0, 50.0, 40.0] # violoncelle, voix, trompette, violon tremolo, flute, basson
pitch_max=[70.0, 70.0, 80.0, 90.0, 90.0, 60.0]

a=[(pitch_min[k]-pitch_max[k])/(rate_min-rate_max) for k in range(6)]
m=[pitch_max[k] - rate_max*a[k] for k in range(6)]

def find_nearest_number(l, n): # pour trouver la note de la gamme la plus proche (en dessous)
	k=0
	while((n>l[k]) and (k<len(l)-1)):
		k+=1
		
	return l[k];
	
def create_gamme(mode, note):
	mineur=[2,1,2,2,1,3,1]
	majeur=[2,2,1,2,2,2,1]
	gamme=[note]
	if(mode==0):
		for i in range(9):
			for k in mineur:
				note+=k
				gamme.append(note)
	else:
		for i in range(9):
			for k in majeur:
				note+=k
				gamme.append(note)
	return(gamme)
	
gammes=[]

gammes.append(create_gamme(1, 41)) # I maj
gammes.append(create_gamme(0, 38)) # VI min
gammes.append(create_gamme(1, 43)) # II maj
gammes.append(create_gamme(1, 36)) # V maj 
#print("Gammes utilisees :")
#for k in range(4):
#	print(gammes[k])

for line in f_in:
	w=line.split()
	t+=1 # time
	d=float(w[3]) # distance between 2 points
	pan=float(w[5]) # panoramic
	r=float(w[7]) # colors rate
	o=float(w[8])
	y=float(w[9])
	g=float(w[10])
	b=float(w[11])
	p=float(w[12])
	volume=float(w[13])
		
	if(volume<10):
		volume=0
	else:
		volume=300.0/d
	
	n=(int(t)/mes)%mes
	
	if(0):
		if(n==0):
			song.addProgramChange(6, 6, 0, 1)
			song.addNote(6, 6, gammes[n][2+7], t, 8*duration, 80)
			song.addProgramChange(7, 7, 0, 1)
			song.addNote(7, 7, gammes[n][4+7], t+0.1, 8*duration, 80)
			song.addProgramChange(8, 8, 0, 1)
			song.addNote(8, 8, gammes[n][7+7], t+0.2, 8*duration, 80)
		elif(n==1):
			song.addProgramChange(6, 6, 0, 1)
			song.addNote(6, 6, gammes[n][4+7], t, 8*duration, 80)
			song.addProgramChange(7, 7, 0, 1)
			song.addNote(7, 7, gammes[n][7+7], t+0.1, 8*duration, 80)
			song.addProgramChange(8, 8, 0, 1)
			song.addNote(8, 8, gammes[n][9+7], t+0.2, 8*duration, 80)
		elif(n==2):
			song.addProgramChange(6, 6, 0, 1)
			song.addNote(6, 6, gammes[n][0+7], t, 8*duration, 80)
			song.addProgramChange(7, 7, 0, 1)
			song.addNote(7, 7, gammes[n][2+7], t+0.1, 8*duration, 80)
			song.addProgramChange(8, 8, 0, 11)
			song.addNote(8, 8, gammes[n][4+7], t+0.2, 8*duration, 80)
		else:
			song.addProgramChange(6, 6, 0, 1)
			song.addNote(6, 6, gammes[n][4+7], t, 8*duration, 80)
			song.addProgramChange(7, 7, 0, 1)
			song.addNote(7, 7, gammes[n][7+7], t+0.1, 8*duration, 80)
			song.addProgramChange(8, 8, 0, 1)
			song.addNote(8, 8, gammes[n][9+7], t+0.2, 8*duration, 80)
		
		
	rand=([r,o,y,g,b,p]).index(max([r,o,y,g,b,p]))
		
	for num, instru, col in zip([0,1,2,3,4,5], [42,52,56,49,75,70], [r,o,y,g,b,p]):
		if(col!=0):
			if((num==rand)&(d<10)):
				col=int(col*a[num]+m[num])
				col=find_nearest_number(gammes[n], col)
				song.addProgramChange(num, num, 0, instru)
				song.addControllerEvent(num, num, t, 10, pan)
				song.addNote(num, num, col, t, duration-0.5, volume)
				
				bend=ra.randrange(-5,5)
				col=int(col*a[num]+m[num])
				col=find_nearest_number(gammes[n], col+bend)
				song.addProgramChange(num, num, 0, instru)
				song.addControllerEvent(num, num, t+0.5, 10, pan)
				song.addNote(num, num, col, t+0.5, duration-0.5, volume)
			else:
				col=int(col*a[num]+m[num])
				col=find_nearest_number(gammes[n], col)
				song.addProgramChange(num, num, 0, instru)
				song.addControllerEvent(num, num, t, 10, pan)
				song.addNote(num, num, col, t, duration, volume)
			
		
with open("song_1.mid", "wb") as output_file:
    song.writeFile(output_file)
    
f_in.close()
    
