Summary:	Linphone Internet Phone
Summary(pl.UTF-8):	Linphone - telefon internetowy
Name:		linphone
# 5.0+ requires SDK v5.2, which is partially on AGPL (see DEVEL-5 branch)
Version:	4.4.11
Release:	1
License:	GPL v3+ or proprietary
Group:		Applications/Communications
#Source0Download: https://gitlab.linphone.org/BC/public/linphone-desktop/-/tags
Source0:	https://gitlab.linphone.org/BC/public/linphone-desktop/-/archive/%{version}/linphone-desktop-%{version}.tar.bz2
# Source0-md5:	89948a7412880c6393b3254fb99c50ef
Patch0:		%{name}-no-sdk.patch
Patch1:		%{name}-cmake.patch
Patch2:		%{name}-install.patch
URL:		http://www.linphone.org/
BuildRequires:	Qt5Concurrent-devel >= 5.12
BuildRequires:	Qt5Core-devel >= 5.12
BuildRequires:	Qt5DBus-devel >= 5.12
BuildRequires:	Qt5Gui-devel >= 5.12
BuildRequires:	Qt5Network-devel >= 5.12
BuildRequires:	Qt5Quick-devel >= 5.12
BuildRequires:	Qt5Quick-controls2-devel >= 5.12
# optional
BuildRequires:	Qt5Speech-devel >= 5.12
BuildRequires:	Qt5Svg-devel >= 5.12
BuildRequires:	Qt5Widgets-devel >= 5.12
BuildRequires:	bctoolbox-devel >= 0.0.3
BuildRequires:	belcard-devel >= 5.1
BuildRequires:	cmake >= 3.1
BuildRequires:	doxygen
BuildRequires:	liblinphone-devel >= 5.1
BuildRequires:	liblinphone-c++-devel >= 5.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	mediastreamer-devel >= 5.1
BuildRequires:	ortp-devel >= 5.1
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5.12
BuildRequires:	qt5-linguist >= 5.12
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	belcard >= 5.1
Requires:	liblinphone >= 5.1
Requires:	liblinphone-c++ >= 5.1
Requires:	mediastreamer >= 5.1
Requires:	ortp >= 5.1
Obsoletes:	linphoneqt < 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linphone is an open source softphone for voice and video over IP
calling and instant messaging.

It is fully SIP-based, for all calling, presence and IM features.

%description -l pl.UTF-8
Linphone to mająca otwarte źródła aplikacja do programowego
wykonywania połączeń głosowych i wideo po IP oraz komunikacji
tekstowej.

Jest w pełni oparta o SIP, zarówno w przypadku połączeń, obecności
jak i komunikacji tekstowej.

%package devel
Summary:	Header files for Linphone plugins
Summary(pl.UTF-8):	Pliki nagłówkowe dla wtyczek Linphone
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= 5.12
Requires:	Qt5Network-devel >= 5.12
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for Linphone plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla wtyczek Linphone.

%prep
%setup -q -n linphone-desktop-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# hack versions (git describe doesn't work on dist tarballs)
%{__sed} -i -e 's/set(FULL_VERSION )/set(FULL_VERSION %{version})/; /^bc_compute_full_version/d' linphone-app/CMakeLists.txt
%{__sed} -i -e 's/bc_compute_full_version(PROJECT_VERSION_BUILD)/set(PROJECT_VERSION_BUILD %{version})/' linphone-app/build/CMakeLists.txt
%{__sed} -i -e 's/bc_compute_full_version(APP_PROJECT_VERSION)/set(APP_PROJECT_VERSION %{version})/' linphone-app/cmake_builder/linphone_package/CMakeLists.txt
%{__sed} -i -e 's/LINPHONE_QT_GIT_VERSION/"%{version}"/' linphone-app/src/app/AppController.cpp
# adjust locales path
%{__sed} -i -e '/LanguagePath/ s,"[^"]*","%{_datadir}/linphone/languages",' linphone-app/src/utils/Constants.hpp

%build
install -d build
cd build
%cmake .. \
	-DLINPHONE_QT_ONLY=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/qt.conf

install -d $RPM_BUILD_ROOT%{_datadir}/linphone/languages
cp -p build/linphone-app/assets/languages/*.qm $RPM_BUILD_ROOT%{_datadir}/linphone/languages
%{__mv} $RPM_BUILD_ROOT%{_datadir}/linphone/languages/{fr_FR,fr}.qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/linphone
%attr(755,root,root) %{_libdir}/libapp-plugin.so
%{_desktopdir}/linphone.desktop
%{_iconsdir}/hicolor/*x*/apps/linphone.png
%{_iconsdir}/hicolor/scalable/apps/linphone.svg
%{_datadir}/linphone/assistant
%dir %{_datadir}/linphone/languages
%lang(da) %{_datadir}/linphone/languages/da.qm
%lang(de) %{_datadir}/linphone/languages/de.qm
%{_datadir}/linphone/languages/en.qm
%lang(es) %{_datadir}/linphone/languages/es.qm
%lang(fr) %{_datadir}/linphone/languages/fr.qm
%lang(hu) %{_datadir}/linphone/languages/hu.qm
%lang(it) %{_datadir}/linphone/languages/it.qm
%lang(ja) %{_datadir}/linphone/languages/ja.qm
%lang(lt) %{_datadir}/linphone/languages/lt.qm
%lang(pt_BR) %{_datadir}/linphone/languages/pt_BR.qm
%lang(ru) %{_datadir}/linphone/languages/ru.qm
%lang(sv) %{_datadir}/linphone/languages/sv.qm
%lang(tr) %{_datadir}/linphone/languages/tr.qm
%lang(uk) %{_datadir}/linphone/languages/uk.qm
%lang(zh_CN) %{_datadir}/linphone/languages/zh_CN.qm
%{_datadir}/linphone/linphonerc-factory

%files devel
%defattr(644,root,root,755)
%{_includedir}/LinphoneApp
