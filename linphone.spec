Summary:	Linphone Internet Phone
Summary(pl):	Linphone - telefon internetowy
Name:		linphone
Version:	0.7.1
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.linphone.org/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.linphone.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-core-devel
BuildRequires:	libosip-devel
BuildRequires:	scrollkeeper
Prereq:		/sbin/ldconfig
Prereq:		scrollkeeper
Requires:	applnk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME
%define		_mandir		%{_prefix}/man

%description
Linphone is a web phone: it let you phone to your friends anywhere in
the whole world, freely, simply by using the internet. The cost of the
phone call is the cost that you spend connected to the internet.

Here are the main features of linphone:
    - Works with the Gnome Desktop under linux.
    - Works as simply as a cellular phone. Two buttons, no more.
    - Understands the SIP protocol.
    - You just require a soundcard to use linphone.
    - Linphone is free software, released under the General Public
      Licence.
    - Linphone is documented: there is a complete user manual readable
      from the application that explains you all you need to know.

%description -l pl
Linphone to telefon internetowy - pozwala dzwoniæ do znajomych na
ca³ym ¶wiecie bez dodatkowych op³at, u¿ywaj±c tylko Internetu.

G³ówne cechy linphone:
 - dzia³anie ze ¶rodowiskiem GNOME
 - na¶ladowanie prostego telefonu komórkowego - tylko dwa przyciski
 - obs³uga protoko³u SIP
 - wymaga karty d¼wiêkowej
 - jest wolnodostêpnym oprogramowaniem (na licencji GPL)
 - ma dokumentacjê: pe³ny podrêcznik dostêpny z aplikacji.

%prep
%setup -q
%patch0 -p1

%build
sed -e s/AM_GNOME_GETTEXT/AM_GNU_GETTEXT/ configure.in > configure.in.tmp
mv -f configure.in.tmp configure.in
rm -f missing
#xml-i18n-toolize --copy --force
gettextize --copy --force
aclocal -I %{_aclocaldir}/gnome
autoheader
%{__autoconf}
%{__automake}
cd oRTP
autoheader
%{__autoconf}
%{__automake}
cd ..
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	linphone_sysdir=%{_sysconfdir}/CORBA/servers \
	linphone_applidir=%{_applnkdir}/Network/Communications

gzip -9nf AUTHORS BUGS ChangeLog NEWS

%find_lang %{name} --with-gnome --all-name

%post
/usr/bin/scrollkeeper-update
/sbin/ldconfig

%postun
/usr/bin/scrollkeeper-update
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/CORBA/servers/*
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_applnkdir}/Network/Communications/*
%{_datadir}/applets/Network/*
%{_pixmapsdir}/*
%{_datadir}/sounds/*
