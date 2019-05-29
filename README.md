# arch_bto_17cl63
My installation instructions on installing Arch Linux with i3 on my BTO (2) notebook

Disclaimer: this document is Work In Progress. Do not use! I am not responsible for any damage or loss of business or profits or whatever. If you care about breaking things: *DO NOT USE!*

## System installation

See: https://wiki.archlinux.org/index.php/Installation_guide
 * Boot with the Arch iso
 * Set up wireless lan (lspci -k: Qualcomm Atheros QCA6174 on my notebook): https://wiki.archlinux.org/index.php/Wireless_network_configuration - Note: especially this section can be done on so many different ways, this may not be a good way!
	 * _ip link -> shows 3: wlp62s0_
	 * ip link set wlp62s0 up
	 * wpa_passphrase SSID "password" > /etc/wpa_supplicant/SSID.conf
	 * wpa_supplicant -iwlp62s0 -c /etc/wpa_supplicant/SSID.conf &
	 * _iw dev wlp62s0 scan -> shows my SSID_
	 * _iw dev wlp62s0 connect SSID (should already be happening)_
	 * systemctl restart dhcpcd
	 * ip addr (can take a while) -> should show an ip address
	 * _ping archlinux.org -> should work_
 * timedatectl set-ntp true
 * Partitioning:
	* _fdisk -l (at this time, we will be using /dev/sdb6 as installation partition)_
	* mkfs.ext4 /dev/sdb6
	* mount /dev/sdb6 /mnt
 * Installing base:
	* vi /etc/pacman.d/mirrorlist and move Belgium (because that's where I live) to the top (will be copied, so it is worth getting it right already, but can of course be edited later)
	* pacstrap /mnt base base-devel
 * Configuring:
	* genfstab -U /mnt >> /mnt/etc/fstab
 * Chroot:
	* arch-chroot /mnt
 * Locale:
	* Timezone: ln -sf /usr/share/zoneinfo/Europe/Brussels /etc/localtime
	* hwclock --systohc
	* vi /etc/locale.gen and uncomment en_US.UTF-8 UTF-8
	* locale-gen
	* vi /etc/locale.conf and write *LANG=en_US.UTF-8* in it
 * Network:
	* vi /etc/hostname and write *arch-bto2* in it
	* vi /etc/hosts and add:
		* 127.0.0.1 localhost
		* ::1 localhost
		* 127.0.1.1 arch-bto2.frixx-it arch-bto2 (replace 127.0.1.1 with the static ip if there is one - 192.168.60.52)
	* pacman -Syu wpa_supplicant dhcpcd
	* wpa_passphrase SSID "password" > /etc/wpa_supplicant/SSID.conf - note: again, this is obviously not a good way
	* systemctl enable dhcpcd@wlp62s0.service
 * passwd
 * pacman -Syu grub intel-ucode os-prober (the latter only if other osses are installed, in this case, you also need to mount them, if windows is not detected, pacman -Syu ntfs-3g might do the trick)
 * grub-install --target=i386-pc /dev/sda
 * grub-mkconfig -o /boot/grub/grub.cfg
 * reboot
 
## Create a user
 * useradd -m -G wheel dirk
 * passwd dirk
 * vi /etc/sudoers and uncomment the wheel section
 * log out and log in as dirk
 
## Video driver & i3
 * sudo vi /etc/pacman.conf and enable multilib (by uncommenting two lines)
 * sudo pacman -Syu xorg nvidia nvidia-utils lib32-nvidia-utils (I selected all the defaults)
 * sudo pacman -Syu i3-wm terminator lightdm lightdm-gtk-greeter
 * sudo systemctl enable lightdm.service
 * reboot (you should now be able to log in in i3)

## Make life a bit easier:
 * sudo pacman -Syu vim
 * sudo ln -sf /usr/bin/vim /usr/bin/vi

## Make life easier with yay:
 * sudo pacman -Syu git
 * git clone https://aur.archlinux.org/yay.git
 * cd yay
 * makepkg -cris
 * cd ..
 * rm -rf yay

# Make i3 a little more beautiful
 * yay -Syu polybar rofi
 * mkdir ~/.config/polybar
 * cp /usr/share/doc/polybar/config ~/.config/polybar/config
 * vi ~/.config/polybar/launch.sh
```#!/bin/bash
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
 * Restart i3 (win+shift+r) and the polybar should be visible
 * Useful i3 config stuff:
 	* yay -Syu pulseaudio alsa-utils (you may need to reboot for pulseaudio to work)
	* Keyboard bindings:
```bindsym XF86MonBrightnessUp exec xbacklight -inc 10 # increase screen brightness
bindsym XF86MonBrightnessDown exec xbacklight -dec 10 # decrease screen brightness
bindsym XF86AudioRaiseVolume exec amixer -D pulse -q set Master playback 5%+ unmute
bindsym XF86AudioLowerVolume exec amixer -D pulse -q set Master playback 5%- unmute
bindsym XF86AudioMute exec amixer -D pulse -q set Master toggle
```

# NetworkManager (and forticlient support)

 * yay -Syu networkmanager network-manager-applet networkmanager-forticlientvpn-git
 * Add line to i3 config: exec --no-startup-id nm-applet
 
