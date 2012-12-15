# TODO:
#  - split main package to few smaller (there is linphonec for console,
#    auto-answering machine and linphone applet for gnome)
#  - check if all this configure option I've set are really needed
#  - separate libraries that do not require gnome into subpackages for Jingle support in kopete
# - packages copies for "libmediastreamer.so.1", "libortp.so.8" libraries
#   those should be installed to private path and LD_LIBARY_PATH setup with wrappers.
#   without doing so do not stbr it to Th!
#
# Conditional build:
%bcond_with	system_ortp	# use system ortp
%bcond_with	system_mediastreamer	# use system mediastreamer

%if "%{pld_release}" == "th"
%if %{without system_ortp} || %{without system_mediastreamer}
Blocked: fix todo first
%endif
%endif
Summary:	Linphone Internet Phone
Summary(pl.UTF-8):	Linphone - telefon internetowy
Name:		linphone
Version:	3.5.2
Release:	0.1
License:	LGPL/GPL
Group:		Applications/Communications
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources/%{name}-%{version}.tar.gz
# Source0-md5:	4be6e940372dba1f6793aef849c1ff0d
Patch0:		%{name}-imgdir.patch
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
BuildRequires:	libeXosip2-devel
BuildRequires:	libgsm-devel >= 1.0.10
BuildRequires:	libosip2-devel >= 2.2.0
BuildRequires:	libsamplerate-devel >= 0.0.13
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	libv4l-devel
%{?with_system_ortp:BuildRequires:	ortp-devel}
%{?with_system_mediastreamer:BuildRequires:	mediastreamer-devel}
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRequires:	scrollkeeper
BuildRequires:	speex-devel >= 1.0.0
BuildRequires:	srtp-devel
BuildRequires:	xorg-lib-libXv-devel
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Provides:	ortp = 0.16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package devel
Summary:	Linphone Internet Phone - header files
Summary(pl.UTF-8):	Telefon internetowy Linphone - pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib-devel >= 0.9.0
Requires:	glib2-devel >= 2.0.0
Requires:	gtk-doc-common
Requires:	jack-audio-connection-kit-devel >= 0.15.0
Requires:	libgsm-devel >= 1.0.10
Requires:	libosip2-devel >= 2.2.0
Requires:	libsamplerate-devel >= 0.0.13
Requires:	lpc10-devel >= 1.5
Requires:	speex-devel >= 1.0.0
Provides:	ortp-devel = 0.16

%description devel
Development files for the Linphone Internet Phone.

%description devel -l pl.UTF-8
Pliki dla programistów używających telefonu internetowego Linphone.

%package static
Summary:	Linphone static libraries
Summary(pl.UTF-8):	Statyczne biblioteki Linphone
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	ortp-static = 0.16

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
	--disable-strict \
	--enable-static \
	--enable-ipv6 \
	%{?with_system_mediastreamer:--enable-external-mediastreamer} \
	%{?with_system_ortp:--enable-external-ortp}
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

rm -r $RPM_BUILD_ROOT/usr/share/doc/linphone
%{!?with_system_mediastreamer:rm -r $RPM_BUILD_ROOT/usr/share/doc/mediastreamer}
%{!?with_system_ortp:rm -r $RPM_BUILD_ROOT/usr/share/doc/ortp}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update
/sbin/ldconfig

%postun
/usr/bin/scrollkeeper-update
/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/liblinphone.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblinphone.so.?
%if %{without system_mediastreamer}
%attr(755,root,root) %{_libdir}/libmediastreamer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediastreamer.so.?
%{_libdir}/mediastream
%endif
%if %{without system_ortp}
%attr(755,root,root) %{_libdir}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libortp.so.?
%endif
%{_datadir}/sounds/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/linphone.png
%{_pixmapsdir}/linphone
%{_datadir}/linphone
%{_mandir}/man1/*
%lang(cs) %{_mandir}/cs/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblinphone.so
%{_includedir}/linphone
%{_pkgconfigdir}/linphone.pc
%if %{without system_mediastreamer}
%attr(755,root,root) %{_libdir}/libmediastreamer.so
%{_libdir}/libmediastreamer.la
%{_includedir}/mediastreamer2
%{_pkgconfigdir}/mediastreamer.pc
%endif
%if %{without system_ortp}
%attr(755,root,root) %{_libdir}/libortp.so
%{_libdir}/liblinphone.la
%{_libdir}/libortp.la
%{_includedir}/ortp
%{_pkgconfigdir}/ortp.pc
%endif

%files static
%defattr(644,root,root,755)
%{_libdir}/liblinphone.a
%if %{without system_mediastreamer}
%{_libdir}/libmediastreamer.a
%endif
%if %{without system_ortp}
%{_libdir}/libortp.a
%endif
