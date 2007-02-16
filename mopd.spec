Summary:	The Maintenance Operations Protocol (MOP) loader daemon
Name:		mopd
Version:	2.5.3
Release:	0.2
License:	BSD
Group:		Networking/Daemons
#Source0:	http://linux-vax.sourceforge.net/download/mopd-linux.tar.gz
#Source0:	ftp://ftp.stacken.kth.se/pub/OS/NetBSD/mopd/
Source0:	ftp://ftp3.ds.pg.gda.pl/people/macro/mopd/%{name}-%{version}.tar.gz
# Source0-md5:	b2bbea45c885309682c24e3f8674ac45
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-linux.patch
Patch1:		%{name}-vax-linux.patch
Patch2:		%{name}-proto.patch
Patch3:		%{name}-select.patch
Patch4:		%{name}-aout.patch
Patch5:		%{name}-syslog.patch
Patch6:		%{name}-mcast.patch
Patch7:		%{name}-elf.patch
Patch8:		%{name}-pmax.patch
Patch9:		%{name}-bind.patch
Patch10:	%{name}-eaddr.patch
Patch11:	%{name}-length.patch
Patch12:	%{name}-fddi.patch
Patch13:	%{name}-pf.patch
Patch14:	%{name}-freebsd-put.patch
Patch15:	%{name}-253patched-254.patch
Patch16:	%{name}-debian254.patch
Patch17:	%{name}-alpha.patch
Patch18:	%{name}-gcc34.patch
Patch19:	%{name}-gcc4.patch
Patch20:	%{name}-pld.patch
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	elfutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Maintenance Operations Protocol (MOP) loader daemon services MOP
load requests on one or all Ethernet and FDDI interfaces. Normally, a
filename (ending in .SYS) is included in the load request; if no
filename is given, mopd must know what image to load. When it receives
a request, mopd checks to see if the file exists in /var/lib/mop. If
the filename isn't given, the MAC address of the target is used as a
filename (e.g., 08002b09f4de.SYS, which might be a soft link to
another file). Mopd supports files in ELF, a.out and a few Digital
formats.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

%build
%{__make} -j1 CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,8},/var/lib/mop}

install mopd/mopd $RPM_BUILD_ROOT%{_sbindir}/mopd
install mopchk/mopchk $RPM_BUILD_ROOT%{_bindir}/mopchk
install mopprobe/mopprobe $RPM_BUILD_ROOT%{_bindir}/mopprobe
install moptrace/moptrace $RPM_BUILD_ROOT%{_bindir}/moptrace

install mopd/mopd.8 $RPM_BUILD_ROOT%{_mandir}/man8/mopd.8
install mopchk/mopchk.1 $RPM_BUILD_ROOT%{_mandir}/man1/mopchk.1
install mopprobe/mopprobe.1 $RPM_BUILD_ROOT%{_mandir}/man1/mopprobe.1
install moptrace/moptrace.1 $RPM_BUILD_ROOT%{_mandir}/man1/moptrace.1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mopd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mopd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mopd
%service mopd restart "MOP daemon"

%preun
if [ "$1" = 0 ]; then
	%service mopd stop
	/sbin/chkconfig --del mopd
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) %config(noreplace) /etc/rc.d/init.d/mopd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mopd
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir /var/lib/mop
%{_mandir}/man1/*
%{_mandir}/man8/*
