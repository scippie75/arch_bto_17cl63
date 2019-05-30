# arch_bto_17cl63
My installation instructions on installing Arch Linux with i3 on my BTO x-book 17cl63 (2) notebook

Disclaimer: this document is Work In Progress. Do not use! I am not responsible for any damage or loss of business or profits or whatever. If you care about breaking things: *DO NOT USE!*

## System installation

See: https://wiki.archlinux.org/index.php/Installation_guide
 * Boot with the Arch iso
 * Set up wireless lan
  	* _lspci -k shows Qualcomm Atheros QCA6174 on my notebook_
	* wifi-menu -> select the wifi SSID and configure, close and wait a while
	* _ip addr to see if it worked_
	* _ping archlinux.org -> should work_
 * timedatectl set-ntp true
 * Partitioning:
	* _fdisk -l (at this time, we will be using /dev/sdb6 as installation partition)_
	* mkfs.ext4 /dev/sdb6
	* mount /dev/sdb6 /mnt
 * Installing base:
	* vim /etc/pacman.d/mirrorlist and move Belgium (because that's where I live) to the top (will be copied, so it is worth getting it right already, but can of course be edited later)
	* pacstrap /mnt base base-devel
 * Configuring:
	* genfstab -U /mnt >> /mnt/etc/fstab
 * Chroot:
	* arch-chroot /mnt
 * Make it easier:
 	* pacman -Syu vim
 * Locale:
	* Timezone: ln -sf /usr/share/zoneinfo/Europe/Brussels /etc/localtime
	* hwclock --systohc
	* vim /etc/locale.gen and uncomment en_US.UTF-8 UTF-8
	* locale-gen
	* vim /etc/locale.conf and write *LANG=en_US.UTF-8* in it
 * Network:
	* vim /etc/hostname and write *arch-bto2* in it
	* vim /etc/hosts and add:
		* 127.0.0.1 localhost
		* ::1 localhost
		* 127.0.1.1 arch-bto2.frixx-it arch-bto2 (replace 127.0.1.1 with the static ip if there is one - 192.168.60.52)
 * passwd
 * pacman -Syu vim grub intel-ucode os-prober (the latter only if other osses are installed, in this case, you also need to mount them, if windows is not detected, pacman -Syu ntfs-3g might do the trick)
 * grub-install --target=i386-pc /dev/sda
 * grub-mkconfig -o /boot/grub/grub.cfg

It would now be possible to reboot, but then you will have no wifi. Install netctl (pacman -Syu netctl) to ensure that wifi-menu is available. But we will use NetworkManager later on, so if you go on, you don't need it.

## Create a user
 * useradd -m -G wheel dirk
 * passwd dirk
 * vim /etc/sudoers and uncomment the wheel section
 * log in as dirk: su dirk
 
## Video driver & i3
 * sudo vim /etc/pacman.conf and enable multilib (by uncommenting two lines)
 * sudo pacman -Syu xorg nvidia nvidia-utils lib32-nvidia-utils (I selected all the defaults)
 * sudo pacman -Syu i3-wm terminator lightdm lightdm-gtk-greeter
 * sudo systemctl enable lightdm.service

It would now be possible to reboot, but then you will have no wifi. You can either install netctl to ensure that wifi-menu is available, or you could wait a while to make sure NetworkManager is installed.

## Make life a bit easier:
 * sudo ln -sf /usr/bin/vim /usr/bin/vi

## Make life easier with yay:
 * sudo pacman -Syu git
 * cd ~
 * git clone https://aur.archlinux.org/yay.git
 * cd yay
 * makepkg -cris
 * cd ..
 * rm -rf yay
 
## Make sure you have an i3 config file to edit
 * mkdir ~/.config/i3
 * cp /etc/i3/config ~/.config/i3/config
 * Edit ~/.config/i3/config and find/replace Mod1 with $mod _:%s/Mod1/$mod/g_
 * Add a line above: set $mod Mod4
 
## NetworkManager (and forticlient support)
 * yay -Syu networkmanager network-manager-applet networkmanager-fortisslvpn-git
 * sudo systemctl enable NetworkManager
 * Add line to i3 config: exec --no-startup-id nm-applet

## Pulseaudio
 * yay -Syu pulseaudio alsa-utils (you may need to reboot for pulseaudio to work, you will probably want to wait)

You should now be able to reboot and use wifi, but if you go on, you can make sure that i3 boots up nice

## Ssh
 * yay -Syu openssh

## Make i3 a little more beautiful
 * yay -Syu polybar rofi
 * mkdir ~/.config/polybar
 * cp /usr/share/doc/polybar/config ~/.config/polybar/config
 * vi ~/.config/polybar/launch.sh
```
#!/bin/bash
# Terminate already running bar instances
killall -q polybar
# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done
# Launch Polybar, using default config location ~/.config/polybar/config
polybar mybar &
echo "Polybar launched..."
```
 * chmod +x ~/.config/polybar/launch.sh
 * vi ~/.config/polybar/config and change [bar/example] to [bar/mybar], optionally other things as well
 * vi ~/.config/i3/config and add/update the following lines: bindsym $mod+space exec rofi -show run -theme arthur
 * disable the change focus between tiling/floating window binding
 * disable the whole i3bar section
 * exec_always --no-startup-id $HOME/.config/polybar/launch.sh
 * yay -Syu siji-git
 * If already in i3: restart i3 (win+shift+r) and the polybar should be visible

You can now reboot (or go on if you really want)
 
## Useful i3 config stuff:
 * Faster keyboard response:
```
exec_always --no-startup-id xset r rate 300 50
```
 * Keyboard layout US-international
```
exec --no-startup-id setxkbmap -layout us -variant altgr-intl -option nodeadkeys
```
 * Keyboard bindings:
```
bindsym XF86MonBrightnessUp exec --no-startup-id xbacklight -inc 10 # increase screen brightness
bindsym XF86MonBrightnessDown exec --no-startup-id xbacklight -dec 10 # decrease screen brightness
bindsym XF86AudioRaiseVolume exec --no-startup-id amixer -D pulse -q set Master playback 5%+ unmute
bindsym XF86AudioLowerVolume exec --no-startup-id amixer -D pulse -q set Master playback 5%- unmute
bindsym XF86AudioMute exec --no-startup-id amixer -D pulse -q set Master toggle
```

## Touchpad "tapping"
Edit /etc/X11/xorg.conf.d/30-touchpad.conf
```
Section "InputClass"
    Identifier "libinput touchpad catchall"
    Driver "libinput"
    Option "Tapping" "on"
EndSection
```

## SSD periodic TRIM
 * yay -Syu util-linux
 * sudo systemctl enable fstrim.timer
 * sudo systemctl start fstrim.timer
 
## Printer (Lexmark CX310dn & pdf)
 * yay -Syu cups cups-pdf
 * sudo usermod -aG sys dirk
 * sudo systemctl enable org.cups.cupsd.service
 * sudo systemctl start org.cupscupsd.service
 * open browser on localhost:631 and follow the user interface to add the Lexmark CX310dn printer (find the PPD in Dropbox under Linux folder)

## Thunar - file explorer
 * yay -Syu thunar thunar-archive-plugin thunar-media-tags-plugin thunar-volman tumbler ffmpegthumbnailer

## EID reader
 * yay -Syu ccid
 * sudo systemctl enable pcscd.socket
 * sudo systemctl start pcscd.socket
 * gpg --recv-key 824A5E0010A04D46 (check on https://aur.archlinux.org/packages/eid-mw/ and if this fails, try another DNS)
 * yay -Syu eid-mw
 
## Close laptop lid configuration (hangs the OS if not configured)
 * sudo vi /etc/systemd/logind.conf and change the defaults (make sure HandleLidSwitch* = lock)
 * yay -Syu xss-lock
 * add line to ~/.config/i3/config: exec --no-startup-id xss-lock -- i3lock -n (optionally with parameters like -i <image.png>)

## Bluetooth
 * yay -Syu bluez bluez-utils pulseaudio-bluetooth
 * sudo systemctl enable bluetooth.service
 * sudo systemctl start bluetooth.service
 * yay -Syu blueman
 * sudo vi /etc/pulse/system.pa and add the following lines:
```
load-module module-bluetooth-policy
load-module module-bluetooth-discover
```
I needed a reboot after this

## Nicer fonts (for example, in firefox, see https://www.reddit.com/r/archlinux/comments/5r5ep8/make_your_arch_fonts_beautiful_easily/ for more information)
 * yay -Syu ttf-dejavu ttf-liberation noto-fonts
 * sudo ln -s /etc/fonts/conf.avail/70-no-bitmaps.conf /etc/fonts/conf.d
 * sudo ln -s /etc/fonts/conf.avail/10-sub-pixel-rgb.conf /etc/fonts/conf.d
 * sudo ln -s /etc/fonts/conf.avail/11-lcdfilter-default.conf /etc/fonts/conf.d
 * vi /etc/profile.d/freetype2.sh and uncomment _export FREETYPE_PROPERTIES="truetype:interpreter-version=40"_

## Configure power management
You can add these commands to i3 config:
 * xset s 3600 3600 to let screen go blank after 1 hour
 * xset dpms 0 0 0 to prevent automatic standby, suspend, off
 * xset q for more information

## Fingerprint sensor
I don't want it... see https://wiki.archlinux.org/index.php/Fingerprint_GUI for more information

## Keyboard RGB
 * yay -Syu clevo-xsm-wmi clevo-xsm-wmi-dkms clevo-xsm-wmi-util (may not need all or even give a conflict...)
 * sudo systemctl start clevo-xsm-wmi
 * sudo systemctl enable clevo-xsm-wmi
See https://bitbucket.org/tuxedocomputers/clevo-xsm-wmi/src/master/module/ABI/testing/sysfs-driver-clevo-xsm-wmi for more information on how to manually change the colors

## Polkit
  * yay -Syu polkit lxsession
  * Make sure lxpolkit is started at boot (i3-config)
  
