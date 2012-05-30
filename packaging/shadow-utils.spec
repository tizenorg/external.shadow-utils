Summary: Utilities for managing accounts and shadow password files
Name: shadow-utils
Version: 4.1.4.2
Release: 1
URL: http://pkg-shadow.alioth.debian.org/
Source0: ftp://pkg-shadow.alioth.debian.org/pub/pkg-shadow/shadow-%{version}.tar.bz2
Source1: shadow-4.0.17-login.defs
Source2: shadow-4.0.18.1-useradd
Source1001: packaging/shadow-utils.manifest 
Patch0: shadow-4.1.4.2-redhat.patch
Patch1: shadow-4.1.4.1-goodname.patch
Patch2: shadow-4.1.4.2-leak.patch
Patch3: shadow-4.1.4.2-fixes.patch
License: BSD and GPLv2+
Group: System/Base
Requires: setup

%description
The shadow-utils package includes the necessary programs for
converting UNIX password files to the shadow password format, plus
programs for managing user and group accounts. The pwconv command
converts passwords to the shadow password format. The pwunconv command
unconverts shadow passwords and generates an npasswd file (a standard
UNIX password file). The pwck command checks the integrity of password
and shadow files. The lastlog command prints out the last login times
for all users. The useradd, userdel, and usermod commands are used for
managing user accounts. The groupadd, groupdel, and groupmod commands
are used for managing group accounts.

%prep
%setup -q -n shadow-%{version}
%patch0 -p1 -b .redhat
%patch1 -p1 -b .goodname
%patch2 -p1 -b .leak
%patch3 -p1 -b .fixes

iconv -f ISO88591 -t utf-8  doc/HOWTO > doc/HOWTO.utf8
cp -f doc/HOWTO.utf8 doc/HOWTO

%build
cp %{SOURCE1001} .
%configure \
        --enable-shadowgrp \
        --without-audit \
        --with-sha-crypt \
        --without-selinux \
        --without-libcrack \
        --without-libpam \
        --disable-shared
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale MKINSTALLDIRS=`pwd`/mkinstalldirs
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
install -p -c -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/login.defs
install -p -c -m 0600 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/default/useradd


ln -s useradd $RPM_BUILD_ROOT%{_sbindir}/adduser
#ln -s %{_mandir}/man8/useradd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/adduser.8
ln -s useradd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/adduser.8
for subdir in $RPM_BUILD_ROOT/%{_mandir}/{??,??_??,??_??.*}/man* ; do
        test -d $subdir && test -e $subdir/useradd.8 && echo ".so man8/useradd.8" > $subdir/adduser.8
done

# Remove binaries we don't use.
rm $RPM_BUILD_ROOT/%{_bindir}/chfn
rm $RPM_BUILD_ROOT/%{_bindir}/chsh
rm $RPM_BUILD_ROOT/%{_bindir}/expiry
rm $RPM_BUILD_ROOT/%{_bindir}/groups
rm $RPM_BUILD_ROOT/%{_bindir}/login
rm $RPM_BUILD_ROOT/%{_bindir}/passwd
rm $RPM_BUILD_ROOT/%{_bindir}/su
rm $RPM_BUILD_ROOT/%{_sysconfdir}/login.access
rm $RPM_BUILD_ROOT/%{_sysconfdir}/limits
rm $RPM_BUILD_ROOT/%{_sbindir}/logoutd
rm $RPM_BUILD_ROOT/%{_sbindir}/nologin
rm $RPM_BUILD_ROOT/%{_sbindir}/chgpasswd
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/limits.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/limits.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/login.access.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/login.access.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/porttime.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/porttime.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/chgpasswd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/chgpasswd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man3/getspnam.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man3/getspnam.*

%find_lang shadow
find $RPM_BUILD_ROOT%{_mandir} -depth -type d -empty -delete
for dir in $(ls -1d $RPM_BUILD_ROOT%{_mandir}/{??,??_??}) ; do
    dir=$(echo $dir | sed -e "s|^$RPM_BUILD_ROOT||")
    lang=$(basename $dir)
    echo "%%lang($lang) $dir" >> shadow.lang
    echo "%%lang($lang) $dir/man*" >> shadow.lang
#    echo "%%lang($lang) $dir/man*/*" >> shadow.lang
done

%clean
rm -rf $RPM_BUILD_ROOT

%files -f shadow.lang
%manifest shadow-utils.manifest
%defattr(-,root,root)
%doc NEWS doc/HOWTO README
%dir %{_sysconfdir}/default
#%attr(0644,root,root)   %config(noreplace) %{_sysconfdir}/login.defs
%exclude %{_sysconfdir}/login.defs
%attr(0600,root,root)   %config(noreplace) %{_sysconfdir}/default/useradd
%{_bindir}/sg
%{_bindir}/chage
%exclude %{_bindir}/faillog
%{_bindir}/gpasswd
%exclude %{_bindir}/lastlog
%exclude %{_bindir}/newgrp
%exclude %{_sbindir}/adduser
%attr(0750,root,root)   %{_sbindir}/user*
%attr(0750,root,root)   %{_sbindir}/group*
%{_sbindir}/grpck
%{_sbindir}/pwck
%{_sbindir}/*conv
%exclude %{_sbindir}/chpasswd
%{_sbindir}/newusers
%{_sbindir}/vipw
%{_sbindir}/vigr
%{_mandir}/man1/chage.1*
%{_mandir}/man1/gpasswd.1*
%{_mandir}/man1/sg.1*
%{_mandir}/man1/newgrp.1*
%{_mandir}/man3/shadow.3*
%{_mandir}/man5/shadow.5*
%{_mandir}/man5/login.defs.5*
%{_mandir}/man5/gshadow.5*
%{_mandir}/man5/faillog.5*
%{_mandir}/man8/adduser.8*
%{_mandir}/man8/group*.8*
%{_mandir}/man8/user*.8*
%{_mandir}/man8/pwck.8*
%{_mandir}/man8/grpck.8*
%{_mandir}/man8/chpasswd.8*
%{_mandir}/man8/newusers.8*
%{_mandir}/man8/*conv.8*
%{_mandir}/man8/lastlog.8*
%{_mandir}/man8/faillog.8*
%{_mandir}/man8/vipw.8*
%{_mandir}/man8/vigr.8*

