# TODO:
#  - check if all this configure option I've set are really needed
#  - separate libraries that do not require gnome into subpackages for Jingle support in kopete
# - if system_mediastreamerpackages copies for "libmediastreamer.so.1", "libortp.so.8" libraries
#   those should be installed to private path and LD_LIBARY_PATH setup with wrappers.
#   without doing so do not stbr it to Th!
#
# Conditional build:
%bcond_without	system_ortp		# use custom ortp
%bcond_without	system_mediastreamer	# use custom mediastreamer

Summary:	Linphone Internet Phone
Summary(pl.UTF-8):	Linphone - telefon internetowy
Name:		linphone
Version:	3.6.0
Release:	1
License:	LGPL/GPL
Group:		Applications/Communications
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources/%{name}-%{version}.tar.gz
# Source0-md5:	9a101854bb16034b39096e18c80ceb78
Patch0:		%{name}-imgdir.patch
Patch1:		%{name}-exosip-4.0.0.patch
URL:		http://www.linphone.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel >= 0.4.5
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
BuildRequires:	jack-audio-connection-kit-devel >= 0.15.0
BuildRequires:	libeXosip2-devel >= 4.0.0
BuildRequires:	libgsm-devel >= 1.0.10
BuildRequires:	libosip2-devel >= 2.2.0
BuildRequires:	libsamplerate-devel >= 0.0.13
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	libv4l-devel
%{?with_system_ortp:BuildRequires:	ortp-devel}
%{?with_system_mediastreamer:BuildRequires:	mediastreamer-devel >= 2.9.0}
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRequires:	scrollkeeper
BuildRequires:	speex-devel >= 1.0.0
BuildRequires:	srtp-devel
BuildRequires:	xorg-lib-libXv-devel
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires:	%{name}-libs = %{version}-%{release}
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
Linphonec is the console version of  originally  Gnome  internet  phone
Linphone.

%description -n linphonec -l pl.UTF-8
Linphonec to konsolowa wersja GNOME'owego telefonu internetowego Linphone.

%package libs
Summary:	Linphone libraries
Summary(pl.UTF-8):	Biblioteki Linphone
Group:		Libraries
Requires(post,postun):	/sbin/ldconfig

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
Requires:	glib2-devel >= 2.0.0
Requires:	gtk-doc-common
Requires:	jack-audio-connection-kit-devel >= 0.15.0
Requires:	libgsm-devel >= 1.0.10
Requires:	libosip2-devel >= 2.2.0
Requires:	libsamplerate-devel >= 0.0.13
Requires:	lpc10-devel >= 1.5
Requires:	speex-devel >= 1.0.0

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

find '(' -name '*.c' -o -name '*.h' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

%patch0 -p1
%patch1 -p1

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
	--disable-strict \
	--enable-static \
	--enable-ipv6 \
	%{?with_system_mediastreamer:--enable-external-mediastreamer} \
	%{?with_system_ortp:--enable-external-ortp}

%if %{without system_ortp}
cd oRTP
%configure \
	--enable-static \
	--enable-ipv6 \
	--libdir=%{_libdir}/%{name} \
	--includedir=%{_libdir}/%{name}/include
cd ..
%endif
%if %{without system_ortp}
cd mediastreamer2
%configure \
	--enable-static \
	--disable-libv4l \
	--libdir=%{_libdir}/%{name} \
	--includedir=%{_libdir}/%{name}/include
cd ..
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install pixmaps/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}

# kill .desktop in GNOME1-specific location
#rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/apps

rm -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%{!?with_system_mediastreamer:rm -r $RPM_BUILD_ROOT/usr/share/doc/mediastreamer}
%{!?with_system_ortp:rm -r $RPM_BUILD_ROOT/usr/share/doc/ortp}

mv $RPM_BUILD_ROOT%{_localedir}/{nb_NO,nb}

# the executable is missing, so the manual is useless
rm $RPM_BUILD_ROOT%{_mandir}/man1/sipomatic.1*
rm $RPM_BUILD_ROOT%{_mandir}/cs/man1/sipomatic.1*

# some tests
rm $RPM_BUILD_ROOT%{_bindir}/*_test

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update

%if %{without system_mediastreamer} || %{without system_ortp}
%post libs
/sbin/ldconfig %{_libdir}/%{name}
%else
%post libs -p /sbin/ldconfig
%endif

%postun
/usr/bin/scrollkeeper-update

%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/linphone
%{_desktopdir}/linphone.desktop
%{_pixmapsdir}/linphone.png
%{_pixmapsdir}/linphone
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
%attr(755,root,root) %ghost %{_libdir}/liblinphone.so.?
%attr(755,root,root) %{_libdir}/liblpc2xml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblpc2xml.so.?
%attr(755,root,root) %{_libdir}/libxml2lpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxml2lpc.so.?
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
%{_datadir}/sounds/*

%files devel
%defattr(644,root,root,755)
%doc coreapi/help/doc/html
%attr(755,root,root) %{_libdir}/liblinphone.so
%attr(755,root,root) %{_libdir}/liblpc2xml.so
%attr(755,root,root) %{_libdir}/libxml2lpc.so
%{_includedir}/linphone
%{_pkgconfigdir}/linphone.pc
%{_libdir}/liblinphone.la
%{_libdir}/liblpc2xml.la
%{_libdir}/libxml2lpc.la
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

%files static
%defattr(644,root,root,755)
%{_libdir}/liblinphone.a
%{_libdir}/liblpc2xml.a
%{_libdir}/libxml2lpc.a
%if %{without system_mediastreamer}
%{_libdir}/%{name}/libmediastreamer.a
%endif
%if %{without system_ortp}
%{_libdir}/%{name}/libortp.a
%endif
