# Pi Audio Setup

### DAC Audio Config for WM8731 DAC

### modify boot/config.txt for DAC 

`sudo nano /boot/config.txt`

```
dtparam=i2c_arm=on
dtparam=spi=on
dtparam=i2s=on
dtoverlay=i2s-mmap
dtoverlay=rpi-proto

dtparam=audio=off 
```

### blacklist onboard audio
edit  raspi-blacklist.conf 

`sudo nano /etc/modprobe.d/raspi-blacklist.conf`  
`# add`  
`blacklist snd_bcm2835`  


### create asound.conf
sudo nano /etc/asound.conf

`# add`
```
pcm.!default  {
  type hw card 0
}

ctl.!default {
  type hw card 0
}
```

### edit alsa.conf  
`sudo nano /usr/share/alsa/alsa.conf `

```
# comment out the following 
	#pcm.front cards.pcm.front
	#pcm.rear cards.pcm.rear
	#pcm.center_lfe cards.pcm.center_lfe
	#pcm.side cards.pcm.side
	#pcm.surround21 cards.pcm.surround21
	#pcm.surround40 cards.pcm.surround40
	#pcm.surround41 cards.pcm.surround41
	#pcm.surround50 cards.pcm.surround50
	#pcm.surround51 cards.pcm.surround51
	#pcm.surround71 cards.pcm.surround71
	#pcm.iec958 cards.pcm.iec958
	#pcm.hdmi cards.pcm.hdmi
	#pcm.dmix cards.pcm.dmix
	#pcm.dsnoop cards.pcm.dsnoop
	#pcm.modem cards.pcm.modem
	#pcm.phoneline cards.pcm.phoneline
```
	
`sudo /etc/init.d/alsa-utils restart`  

`sudo reboot`

## Tests

### check your device name  
`aplay -l `

### check mixer ids  
`amixer controls`


### set mixer values
# Output Mixer HiFi Playback Switch
# Line Capture Switch 
# ADC High Pass Filter Switch
# Playback Deemphasis Switch
# Capture Volume
```
amixer cset numid=13 on
amixer cset numid=4 on 
amixer cset numid=8 on 
amixer cset numid=10 on 
amixer cset numid=3 100% 
```
`sudo alsactl store` 


### restart alsa
`alsactl init`

`# or you can reboot your soundcard directly`
`sudo /etc/init.d/alsa-utils restart`

### test audio  
`# sine`  
`speaker-test -t sine -f 440 -c 2 -D hw:0,0`  
`# spoken right/left 3 times`  
`speaker-test -l 3 -t wav -c 2 -D hw:0,0`
`# test recording from inputs`  
`arecord -f dat -vv -V stereo -d 15 ~/audio-test.wav`  
`# play back recorded file`  
`aplay -vv -V stereo ~/audio-test.wav`  


### JACK

hw:CARD=sndrpiproto,DEV=0

`/usr/bin/jackd -R -P 95 -d alsa -d hw:0 -r 48000 -n 3 -p 512 -S -s &`

