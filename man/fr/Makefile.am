
mandir = @mandir@/fr

man_MANS = \
	chage.1 \
	chfn.1 \
	chpasswd.8 \
	chsh.1 \
	expiry.1 \
	faillog.5 \
	faillog.8 \
	getspnam.3 \
	gpasswd.1 \
	groupadd.8 \
	groupdel.8 \
	groupmod.8 \
	groups.1 \
	grpck.8 \
	grpconv.8 \
	grpunconv.8 \
	gshadow.5 \
	lastlog.8 \
	login.1 \
	login.defs.5 \
	logoutd.8 \
	newgrp.1 \
	newusers.8 \
	passwd.1 \
	passwd.5 \
	pwck.8 \
	pwconv.8 \
	pwunconv.8 \
	sg.1 \
	shadow.3 \
	shadow.5 \
	su.1 \
	suauth.5 \
	useradd.8 \
	userdel.8 \
	usermod.8 \
	vigr.8 \
	vipw.8

man_nopam = \
	limits.5 \
	login.access.5 \
	porttime.5

if !USE_PAM
man_MANS += $(man_nopam)
endif

EXTRA_DIST = \
	$(man_MANS) \
	$(man_nopam) \
	id.1

include ../generate_translations.mak

