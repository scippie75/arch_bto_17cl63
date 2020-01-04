/# arch_bto_17cl63
My installation instructions on installing Arch Linux with i3 on my BTO x-book 17cl63 (2) notebook

Disclaimer: this document is Work In Progress. Do not use! I am not responsible for any damage or loss of business or profits or whatever. If you care about not breaking things: *DO NOT USE!*

## System installation

For encrypted disk: https://www.howtoforge.com/tutorial/how-to-install-arch-linux-with-full-disk-encryption/

For encrypted partition: https://www.howtoforge.com/tutorial/how-to-encrypt-a-linux-partition-with-dm-crypt-luks/

For auto-mounting an encrypted partition: https://blog.tinned-software.net/automount-a-luks-encrypted-volume-on-system-start/

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
 * yay -Syu pulseaudio alsa-utils pulseaudio-alsa (you may need to reboot for pulseaudio to work, you will probably want to wait)

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
 -* vi ~/.config/i3/config and add/update the following lines: bindsym $mod+space exec rofi -show run -theme arthur-
 * vi ~/.config/i3/config and add/update the following lines: bindsym $mod+space exec --no-startup-id rofi -show run -lines 3 -eh 2 -width 100 -padding 800 -opacity "85" -bw 0 -bc "$bg-color" -bg "$bg-color" -fg "$text-color" -hlbg "$bg-color" -hlfg "#9575cd" -font "System San Francisco Display 18"
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

## Shift-numpad keys the microsoft-way (not temporary numlock)
 * Edit /etc/X11/xorg.conf.d/40-keyboard.conf
```
Section "InputClass"
        Identifier "libinput keyboard catchall"
        Driver "libinput"
	Option "XkbOptions" "numpad:microsoft"
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

## Polkit
  * yay -Syu polkit lxsession
  * Make sure lxpolkit is started at boot (i3-config)

## Thunar - file explorer
 * yay -Syu thunar thunar-archive-plugin thunar-media-tags-plugin thunar-volman tumbler ffmpegthumbnailer gvfs gvfs-smb
 * yay -Syu exfat-utils
 * yay -Syu gnome-icon-theme gnome-icon-theme-extras gnome-icon-theme-symbolic

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

## Nicer fonts (for example, in firefox)
_see https://www.reddit.com/r/archlinux/comments/5r5ep8/make_your_arch_fonts_beautiful_easily/ for more information)_
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
 * yay -Syu clevo-xsm-wmi-util
 * sudo systemctl start clevo-xsm-wmi
 * sudo systemctl enable clevo-xsm-wmi
See https://bitbucket.org/tuxedocomputers/clevo-xsm-wmi/src/master/module/ABI/testing/sysfs-driver-clevo-xsm-wmi for more information on how to manually change the colors

## Uniform look between QT and GTK applications
 * yay -Syu gtk3 gnome-themes-extra adwaita-qt4 adwaita-qt5 breeze breeze-gtk lxappearance
 * qtconfig-qt4 -> select adwaita/breeze
 * lxappearance
 
## My simple .vimrc config file for developers
```
syntax on
set tabstop=2 shiftwidth=2 expandtab
set autoindent
set number
map <F5> :tabp<CR>
map <F6> :tabn<CR>
map <F9> :!./m<CR>
map <F10> :!./%<CR>
au BufRead *.fs set ft=
au BufRead *.vs set ft=

" Show tabs in light color
hi SpecialKey ctermfg=lightgray
set listchars=tab:>-
set list
```
## More vim stuff
 * yay -Syu vim-a -> this makes an easy switcher between c/h file, add *map <F8> :A<CR>* in .vimrc
 * yay -Syu vim-airline powerline powerline-fonts -> this makes a nice toolbar, add *let g:airline_powerline_fonts = 1* to .vimrc

## Correct syntax highlighting in vim for c11 and c++11
 * see https://www.vim.org/scripts/script.php?script_id=3797

## Powerline in bash
 * yay -Syu powerline powerline-fonts
 * Change ~/.bashrc:
```
powerline-daemon -q
POWERLINE_BASH_CONTINUATION=1
POWERLINE_BASH_SELECT=1
. /usr/share/powerline/bindings/bash/powerline.sh
```

## Fonts

Here are several fonts I found interesting to have:
 * yay -Syu terminus-font bdf-unifont font-bh-ttf ttf-croscore ttf-dejavu noto-fonts ttf-liberation ttf-ubuntu-font-family ttf-ms-fonts ttf-vista-fonts ttf-anonymous-pro ttf-freefont ttf-freefont ttf-tahoma

## New additions (need to be tested and placed in the correct place)

* yay -Syu playerctl
* Add following to i3 config:
	bindsym XF86AudioPlay exec playerctl play
	bindsym XF86AudioPause exec playerctl pause
	bindsym XF86AudioNext exec playerctl next
	bindsym XF86AudioPrevious exec playerctl previous
* yay -Syu arandr
* run arandr and set up monitors, save to file ~/.screenlayout/...
* cat ~/.screenlayout/... and copy this
* Add following to i3 config: exec_always --no-startup-id [paste]
* Download font awesome: https://github.com/FortAwesome/Font-Awesome/releases
* Unzip and copy .ttf files to ~/.fonts
* Open the font awesome cheat sheet and copy/paste the icon you wish to a workspace description
* Download font YosemitySanFransisco: https://github.com/supermarin/YosemiteSanFranciscoFont
* Unzip and copy .ttf files to ~/.fonts
* Change font line in i3 config to: font pango:System San Fransisco Display 11
* Start lxappearance (yay -Syu lx-appearance if not already installed) and change the font to SFNS Display 11
* Install font infinality for nicer font rendering: yay -Syu fontconfig-infinality
* Remove polybar if installed (remove startup line in i3 config)
* yay -Syu i3blocks
* Add the following above the bar section in the i3 config
	set $bg-color                  #2f343f
	set $inactive-bg-color         #2f343f
	set $text-color                #f3f4f5
	set $inactive-text-color       #676e7d
	set $urgent-bg-color           #e53935
	set $ugly                      #ff00ff
 * Use them
	# colors                border             background         text                 indicator
	client.focused          $bg-color          $bg-color          $text-color          $ugly
	client.unfocused        $inactive-bg-color $inactive-bg-color $inactive-text-color $ugly
	client.focused_inactive $inactive-bg-color $inactive-bg-color $inactive-text-color $ugly
	client.urgent           $urgent-bg-color   $urgent-bg-color   $text-color          $ugly
 * Add this to hide the (now ugly) edge borders by adding this to the i3 config: hide_edge_borders both
 * Change the bar section in i3 config to
 	bar {
		status_command i3blocks -c $HOME/.config/i3/i3blocks.conf
		position top
		colors {
			background $bg-color
			separator #757575
			# Bar colors       border             background         text
			focused_workspace  $bg-color          $bg-color          $text-color
			inactive_workspace $inactive-bg-color $inactive-bg-color $inactive-text-color
			urgent_workspace   $urgent-bg-color   $urgent-bg-color   $text-color
		}
	}
 * Copy default config file for i3blocks: cp /etc/i3blocks.conf ~/.config/i3/.
 * vim ~/.config/i3/i3blocks.conf and configure it
 -* Install arc-firefox-theme (https://github.com/horst3180/arc-firefox-theme) by going to the website, click releases and click the arc-darker-firefox-theme-....xpi and allow firefox to install it...-
 * The firefox theme seems to have been replaced to: https://www.reddit.com/r/firefox/comments/8q1725/color_arcdarker/
 * Install arc-theme (https://github.com/horst3180/Arc-theme) with yay -Syu arc-gtk-theme (or gtk-theme-arc-git (AUR))
 * Install moka icon theme: yay -Syu moka-icon-theme
 * Start lxappearance and select the Arc-Darker theme, go to icon themes tab and select Moka (or Faba which looks better in my opinion)
 
 
