# nth patchbox install

```
# do regular patchbox setup, skip through the Jack settings as we'll do those later.
# choose option to disable pulseaudio
# suggest desktop with auto-login

# then startx to get desktop
```

# nth configs

### encoder button overlay
```
wget https://raw.githubusercontent.com/okyeron/nth/main/nth-buttons-encoders-overlay.dts
sudo dtc -W no-unit_address_vs_reg -@ -I dts -O dtb -o /boot/overlays/nth-buttons-encoders-overlay.dtbo nth-buttons-encoders-overlay.dts
# ignore warning
```



### modify boot/config.txt for DAC, inputs, etc.

`sudo nano /boot/config.txt`

```
dtparam=i2c_arm=on
dtparam=spi=on
dtparam=i2s=on
dtoverlay=i2s-mmap
dtoverlay=rpi-proto

dtparam=audio=off 

# Buttons and encoders device tree
dtoverlay=nth-buttons-encoders-overlay

# MIDI UART
enable_uart=1
dtoverlay=pi3-miniuart-bt
dtoverlay=midi-uart0 

# comment out vc4-fkms-v3d
#dtoverlay=vc4-fkms-v3d
```


### blacklist onboard audio
edit  raspi-blacklist.conf 

`sudo nano /etc/modprobe.d/raspi-blacklist.conf`  
add  
```
blacklist snd_bcm2835
```

### remove pulseaudio if it's there.

`apt-get remove pulseaudio`  


### create asound.conf
sudo nano /etc/asound.conf

add  
```
pcm.!default  {
  type hw card 0
}

ctl.!default {
  type hw card 0
}
```


### need to reboot for this to take effect?
### check mixer ids  
`amixer controls`


### set default mixer values
```
amixer cset numid=13 on
amixer cset numid=4 on 
amixer cset numid=8 on 
amixer cset numid=10 on 
amixer cset numid=3 100% 

# these are 
# Output Mixer HiFi Playback Switch
# Line Capture Switch 
# ADC High Pass Filter Switch
# Playback Deemphasis Switch
# Capture Volume

```
Save alsa settings  

`sudo alsactl store` 


### re run patchbox to re-configure Jack

```
# jack settings are
snd_rpi_proto
48000
128
2
```

### Other stuff
```
sudo apt-get --allow-releaseinfo-change update
sudo apt update --allow-releaseinfo-change
sudo apt install xorg

# disable amidiauto
sudo systemctl stop amidiauto
sudo systemctl disable amidiauto

# amidiminder
git clone https://github.com/mzero/amidiminder.git
cd amidiminder
make

```
