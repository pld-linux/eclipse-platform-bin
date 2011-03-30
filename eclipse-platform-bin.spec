%bcond_without	ix86	# don't download ix86 source
%bcond_without	x86_64	# don't download x86_64 source

Summary:	Eclipse - an open extensible IDE
Summary(pl.UTF-8):	Eclipse - otwarte, rozszerzalne środowisko programistyczne
Name:		eclipse-platform-bin
Version:	3.6.2
Release:	0.1
License:	EPL v1.0
Group:		Development/Tools
%if %{with ix86}
Source0:	http://download.eclipse.org/eclipse/downloads/drops/R-3.6.2-201102101200/eclipse-platform-%{version}-linux-gtk.tar.gz
# Source0-md5:	6e68f49d0fc8954c5c35cdfc9355242f
%endif
%if %{with x86_64}
Source1:	http://download.eclipse.org/eclipse/downloads/drops/R-3.6.2-201102101200/eclipse-platform-%{version}-linux-gtk-x86_64.tar.gz
# Source1-md5:	001b3b657ba4b7ff82d76a5d36afe1b0
%endif
Source2:	eclipse.desktop
Source3:	eclipse.ini
URL:		http://www.eclipse.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
Requires:	ant
Requires:	jdk >= 1.4
Provides:	eclipse = %{version}-%{release}
Obsoletes:	eclipse
Obsoletes:	eclipse-SDK
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		eclipse_arch	%(echo %{_target_cpu} | sed 's/i.86\\|athlon\\|pentium/x86/;s/amd64/x86_64/')
%define		no_install_post_chrpath		1

# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			libcairo.so.2

%description
Eclipse is a kind of universal tool platform - an open extensible IDE
for anything and nothing in particular.

This package provides core runtime enviroment without any additional
plugins.

%description -l pl.UTF-8
Eclipse to rodzaj uniwersalnej platformy narzędziowej - otwarte,
rozszerzalne IDE (zintegrowane środowisko programistyczne) do
wszystkiego i niczego w szczególności.

Ten pakiet dostarcza podstawowe środowisko uruchomieniowe bez żadnych
dodatkowych rozszerzeń.

%prep
%ifarch %{ix86}
%setup -q -T -c -a0
%endif
%ifarch %{x8664}
%setup -q -T -c -a1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/eclipse{,/dropins},%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_sysconfdir}/eclipse}

cd eclipse
cp -a features p2 configuration plugins \
      libcairo-swt.so eclipse \
      $RPM_BUILD_ROOT%{_libdir}/eclipse

install -p icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/eclipse-icon.xpm

install -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install -p eclipse.ini $RPM_BUILD_ROOT%{_sysconfdir}/eclipse/eclipse.ini

ln -s %{_libdir}/eclipse/eclipse $RPM_BUILD_ROOT%{_bindir}
ln -s %{_sysconfdir}/eclipse/eclipse.ini $RPM_BUILD_ROOT%{_libdir}/eclipse/eclipse.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc eclipse/{about_files,readme,*html}
%dir %{_libdir}/eclipse
%dir %{_libdir}/eclipse/dropins
%{_libdir}/eclipse/features
%{_libdir}/eclipse/p2
%{_libdir}/eclipse/configuration
%{_libdir}/eclipse/plugins
%{_libdir}/eclipse/eclipse.ini
%{_desktopdir}/eclipse.desktop
%{_pixmapsdir}/eclipse-icon.xpm
%dir %{_sysconfdir}/eclipse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/eclipse/eclipse.ini
%attr(755,root,root) %{_libdir}/eclipse/libcairo-swt.so
%attr(755,root,root) %{_libdir}/eclipse/eclipse
%attr(755,root,root) %{_bindir}/eclipse
