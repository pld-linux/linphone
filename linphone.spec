# TODO:
#  - split main package to few smaller (there is linphonec for console,
#    auto-answering machine and linphone applet for gnome)
#  - check if all this configure option I've set are really needed
#  - separate libraries that do not require gnome into subpackages for Jingle support in kopete
Summary:	Linphone Internet Phone
Summary(pl.UTF-8):	Linphone - telefon internetowy
Name:		linphone
Version:	3.4.3
Release:	1
License:	LGPL/GPL
Group:		Applications/Communications
Source0:	http://download.savannah.gnu.org/releases/linphone/stable/sources//%{name}-%{version}.tar.gz
# Source0-md5:	66e21f36d62c2094f7b4360262c46f20
Patch0:		%{name}-chdir.patch
Patch1:		%{name}-imgdir.patch
Patch2:		%{name}-nov4l.patch
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
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd oRTP
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
cd mediastreamer2
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..

%configure \
	LIBS="-lXext" \
	--with-html-dir=%{_gtkdocdir} \
	--enable-alsa \
	--disable-strict \
	--enable-ipv6
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

rm -r $RPM_BUILD_ROOT/usr/share/doc/{linphone,mediastreamer,ortp}

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
%attr(755,root,root) %{_libdir}/libmediastreamer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediastreamer.so.?
%attr(755,root,root) %{_libdir}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libortp.so.?
%{_libdir}/mediastream
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
%attr(755,root,root) %{_libdir}/libmediastreamer.so
%attr(755,root,root) %{_libdir}/libortp.so
%{_libdir}/liblinphone.la
%{_libdir}/libmediastreamer.la
%{_libdir}/libortp.la
%{_includedir}/linphone
%{_includedir}/mediastreamer2
%{_includedir}/ortp
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblinphone.a
%{_libdir}/libmediastreamer.a
%{_libdir}/libortp.a
