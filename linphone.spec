#
Summary:	Linphone Internet Phone
Name:		linphone
Version:	0.7.1
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.linphone.org/download/%{name}-%{version}.tar.gz
URL:		http://www.linphone.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-core-devel
Prereq:		/sbin/ldconfig
Requires:	applnk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME
%define		_mandir		%{_prefix}/man

%description
Linphone is a web phone: it let you phone to your friends anywhere in the whole
world, freely, simply by using the internet. The cost of the phone call is the
cost that you spend connected to the internet.

Here are the main features of linphone:
    * Works with the Gnome Desktop under linux.
    * Works as simply as a cellular phone. Two buttons, no more.
    * Understands the SIP protocol.
    * You just require a soundcard to use linphone.
    * Linphone is free software, released under the General Public Licence.
    * Linphone is documented: there is a complete user manual readable from the
application that explains you all you need to know.

%prep
%setup -q

%build
sed -e s/AM_GNOME_GETTEXT/AM_GNU_GETTEXT/ configure.in > configure.in.tmp
mv -f configure.in.tmp configure.in
rm -f missing
#xml-i18n-toolize --copy --force
gettextize --copy --force
aclocal -I %{_aclocaldir}/gnome
autoheader
autoconf
automake -a -c -f
%configure 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Applicationsdir=%{_applnkdir}/Network/Communications 

gzip -9nf AUTHORS NEWS README TODO

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
