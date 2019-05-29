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
 
