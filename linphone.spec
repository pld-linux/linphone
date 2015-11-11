# TODO:
# - --enable-tunnel (BR: pkgconfig(tunnel) >= 0.3.3)
# - fill in dependencies for !system_ortp, !system_mediastreamer
# - check if all this configure option I've set are really needed
# - separate libraries that do not require gnome into subpackages for Jingle support in kopete
# - if system_mediastreamerpackages copies for "libmediastreamer.so.1", "libortp.so.8" libraries
#   those should be installed to private path and LD_LIBARY_PATH setup with wrappers.
#   without doing so do not stbr it to Th!
#
# Conditional build:
%bcond_without	ldap			# LDAP support
%bcond_without	openssl			# SSL support
%bcond_without	static_libs		# static libraries
%bcond_without	system_ortp		# use custom ortp
%bcond_without	system_mediastreamer	# use custom mediastreamer

Summary:	Linphone Internet Phone
Summary(pl.UTF-8):	Linphone - telefon internetowy
Name:		linphone
Version:	3.9.0
Release:	1
License:	GPL v2+
Group:		Applications/Communications
Source0:	http://linphone.org/releases/sources/linphone/%{name}-%{version}.tar.gz
# Source0-md5:	9d299621d97a5e9397ec29511f5998f7
Patch0:		%{name}-sh.patch
URL:		http://www.linphone.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	belle-sip-devel >= 1.4.0
%{?with_ldap:BuildRequires:	cyrus-sasl-devel >= 2}
BuildRequires:	doxygen
BuildRequires:	ffmpeg-devel >= 0.4.5
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gtk+2-devel >= 2:2.22.0
BuildRequires:	intltool >= 0.40
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libupnp-devel < 1.7
BuildRequires:	libupnp-devel >= 1.6
BuildRequires:	libv4l-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_system_mediastreamer:BuildRequires:	mediastreamer-devel >= 2.11.0}
BuildRequires:	ncurses-devel
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.8}
%{?with_system_ortp:BuildRequires:	ortp-devel >= 0.24.0}
BuildRequires:	pkgconfig
BuildRequires:	polarssl-devel >= 1.3
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRequires:	speex-devel >= 1:1.1.6
BuildRequires:	sqlite3-devel >= 3.7.0
%{!?with_system_ortp:BuildRequires:	srtp-devel}
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	zlib-devel >= 1.2.3
%if %{without system_mediastreamer}
BuildRequires:	libgsm-devel >= 1.0.10
BuildRequires:	pulseaudio-devel
BuildRequires:	speexdsp-devel >= 1.2-beta3
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libnotify >= 0.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without system_ortp}
%define		_noautoreq_1	libortp\.so.*
%endif
%if %{without system_mediastreamer}
%define		_noautoreq_2	libmediastreamer\.so.*
%endif

%define		_noautoreq	%{?_noautoreq_1} %{?_noautoreq_2}
%define		_noautoprov	%{?_noautoreq}

%description
Linphone is a web phone: it let you phone to your friends anywhere in
the whole world, freely, simply by using the internet. The cost of the
phone call is the cost that you spend connected to the internet.

Here are the main features of linphone:
- Works with the GNOME Desktop under linux.
- Works as simply as a cellular phone. Two buttons, no more.
- Understands the SIP protocol.
- You just require a soundcard to use linphone.
- Linphone is free software, released under the General Public
  Licence.
- Linphone is documented: there is a complete user manual readable
  from the application that explains you all you need to know.

%description -l pl.UTF-8
Linphone to telefon internetowy - pozwala dzwonić do znajomych na
całym świecie bez dodatkowych opłat, używając tylko Internetu.

Główne cechy linphone:
- działanie ze środowiskiem GNOME
- naśladowanie prostego telefonu komórkowego - tylko dwa przyciski
- obsługa protokołu SIP
- wymaga karty dźwiękowej
- jest wolnodostępnym oprogramowaniem (na licencji GPL)
- ma dokumentację: pełny podręcznik dostępny z aplikacji.

%package -n linphonec
Summary:	Linphone Internet Phone console interface
Summary(pl.UTF-8):	Linphone - telefon internetowy, interfejs konsolowy
Group:		Applications/Communications
Requires:	%{name}-libs = %{version}-%{release}

%description -n linphonec
Linphonec is the console version of originally GNOME Internet phone
Linphone.

%description -n linphonec -l pl.UTF-8
Linphonec to konsolowa wersja telefonu internetowego Linphone
pochodzącego z GNOME.

%package libs
Summary:	Linphone libraries
Summary(pl.UTF-8):	Biblioteki Linphone
Group:		Libraries
Requires(post,postun):	/sbin/ldconfig
Requires:	belle-sip >= 1.4.0
Requires:	glib2 >= 1:2.26.0
Requires:	gtk+2 >= 2:2.22.0
%{?with_system_mediastreamer:Requires:	mediastreamer >= 2.11.0}
%{?with_system_ortp:Requires:	ortp >= 0.24.0}
Requires:	sqlite3 >= 3.7.0

%description libs
Linphone libraries.

%description libs -l pl.UTF-8
Biblioteki Linphone.

%package devel
Summary:	Linphone Internet Phone - header files
Summary(pl.UTF-8):	Telefon internetowy Linphone - pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	alsa-lib-devel >= 0.9.0
Requires:	belle-sip-devel >= 1.4.0
Requires:	glib2-devel >= 1:2.26.0
Requires:	gtk+2 >= 2:2.22.0
Requires:	libstdc++-devel
Requires:	libupnp-devel < 1.7
Requires:	libupnp-devel >= 1.6
Requires:	libxml2-devel >= 2.0
%{?with_system_mediastreamer:Requires:	mediastreamer-devel >= 2.11.0}
%{?with_system_ortp:Requires:	ortp-devel >= 0.24.0}
Requires:	speex-devel >= 1:1.1.6
Requires:	sqlite3-devel >= 3.7.0
Requires:	srtp-devel
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXv-devel
%if %{without system_mediastreamer}
Requires:	libgsm-devel >= 1.0.10
Requires:	speexdsp-devel >= 1.2-beta3
%endif

%description devel
Development files for the Linphone Internet Phone.

%description devel -l pl.UTF-8
Pliki dla programistów używających telefonu internetowego Linphone.

%package static
Summary:	Linphone static libraries
Summary(pl.UTF-8):	Statyczne biblioteki Linphone
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of Linphone libraries.

%description static -l pl.UTF-8
Statyczne wersje bibliotek Linphone.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%if %{without system_ortp}
cd oRTP
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%endif
%if %{without system_ortp}
cd mediastreamer2
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%endif

%configure \
	--with-html-dir=%{_gtkdocdir} \
	--enable-alsa \
	%{?with_system_mediastreamer:--enable-external-mediastreamer} \
	%{?with_system_ortp:--enable-external-ortp} \
	--enable-ipv6 \
	%{?with_ldap:--enable-ldap} \
	--disable-silent-rules \
	%{?with_openssl:--enable-ssl} \
	%{?with_static_libs:--enable-static} \
	--disable-strict

# although main configure already calls {oRTP,mediastreamer2}/configure,
# reconfigure them with different dirs
%if %{without system_ortp}
cd oRTP
%configure \
	--includedir=%{_libdir}/%{name}/include \
	--libdir=%{_libdir}/%{name} \
	--enable-ipv6 \
	%{?with_static_libs:--enable-static}
cd ..
%endif
%if %{without system_ortp}
cd mediastreamer2
%configure \
	--includedir=%{_libdir}/%{name}/include \
	--libdir=%{_libdir}/%{name} \
	--disable-libv4l \
	%{?with_static_libs:--enable-static}
cd ..
%endif

%{__make} \
	GITDESCRIBE=/bin/true \
	GIT_TAG=%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install \
	GITDESCRIBE=/bin/true \
	GIT_TAG=%{version} \
	DESTDIR=$RPM_BUILD_ROOT

install pixmaps/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%{!?with_system_mediastreamer:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/mediastreamer}
%{!?with_system_ortp:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ortp}

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{nb_NO,nb}

# the executable is missing, so the manual is useless
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/sipomatic.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/cs/man1/sipomatic.1*

# some tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/*_test

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/tutorials/%{name} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without system_mediastreamer} || %{without system_ortp}
%post libs
/sbin/ldconfig %{_libdir}/%{name}
%else
%post libs -p /sbin/ldconfig
%endif

%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/linphone
%attr(755,root,root) %{_bindir}/lp-autoanswer
%{_desktopdir}/audio-assistant.desktop
%{_desktopdir}/linphone.desktop
%{_pixmapsdir}/linphone.png
%{_pixmapsdir}/linphone
%{_iconsdir}/hicolor/48x48/actions/linphone-*.png
%{_iconsdir}/hicolor/48x48/apps/linphone.png
%{_iconsdir}/hicolor/48x48/status/linphone-*.png
%{_iconsdir}/hicolor/scalable/actions/linphone-*.svg
%{_iconsdir}/hicolor/scalable/status/linphone-*.svg
%{_datadir}/appdata/linphone.appdata.xml
%{_datadir}/linphone
%{_mandir}/man1/linphone.1*
%lang(cs) %{_mandir}/cs/man1/linphone.1*

%files -n linphonec
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/linphonec
%attr(755,root,root) %{_bindir}/linphonecsh
%{_mandir}/man1/linphonec.1*
%{_mandir}/man1/linphonecsh.1*
%lang(cs) %{_mandir}/cs/man1/linphonec.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblinphone.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblinphone.so.8
%attr(755,root,root) %{_libdir}/liblinphonetester.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblinphonetester.so.0
%if %{without system_mediastreamer} || %{without system_ortp}
%dir %{_libdir}/%{name}
%endif
%if %{without system_mediastreamer}
%attr(755,root,root) %{_libdir}/%{name}/libmediastreamer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}/libmediastreamer.so.?
%{_libdir}/%{name}/mediastream
%endif
%if %{without system_ortp}
%attr(755,root,root) %{_libdir}/%{name}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}/libortp.so.?
%endif
%{_datadir}/sounds/linphone

%files devel
%defattr(644,root,root,755)
%doc coreapi/help/doc/html
%attr(755,root,root) %{_libdir}/liblinphone.so
%attr(755,root,root) %{_libdir}/liblinphonetester.so
%attr(755,root,root) %{_bindir}/lp-gen-wrappers
%{_includedir}/linphone
%{_pkgconfigdir}/linphone.pc
%{_libdir}/liblinphone.la
%{_libdir}/liblinphonetester.la
%if %{without system_mediastreamer} || %{without system_ortp}
%dir %{_libdir}/%{name}/include
%dir %{_libdir}/%{name}/pkgconfig
%endif
%if %{without system_mediastreamer}
%attr(755,root,root) %{_libdir}/%{name}/libmediastreamer.so
%{_libdir}/%{name}/libmediastreamer.la
%{_libdir}/%{name}/include/mediastreamer2
%{_libdir}/%{name}/pkgconfig/mediastreamer.pc
%endif
%if %{without system_ortp}
%attr(755,root,root) %{_libdir}/%{name}/libortp.so
%{_libdir}/%{name}/libortp.la
%{_libdir}/%{name}/include/ortp
%{_libdir}/%{name}/pkgconfig/ortp.pc
%endif
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblinphone.a
%{_libdir}/liblinphonetester.a
%if %{without system_mediastreamer}
%{_libdir}/%{name}/libmediastreamer.a
%endif
%if %{without system_ortp}
%{_libdir}/%{name}/libortp.a
%endif
%endif
