
%define pecl_name geoip

Name:		rock-runtime-php54-geoip
Version:	1.0.8
Release:	3%{?dist}
Summary:	Extension to map IP addresses to geographic places
Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/package/%{pecl_name}
Source0:	http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://bugs.php.net/bug.php?id=59804
Patch1:		geoip-tests.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf
BuildRequires:  rock-runtime-php54-core-rpmbuild >= 5.4.11-1
BuildRequires:	GeoIP-devel

Requires:  rock-runtime-php54-core >= 5.4.11-1

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
This PHP extension allows you to find the location of an IP address 
City, State, Country, Longitude, Latitude, and other information as 
all, such as ISP and connection type. It makes use of Maxminds geoip
database

%prep
%setup -c -q
[ -f package2.xml ] || %{__mv} package.xml package2.xml
%{__mv} package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml

# Upstream often forget this
extver=$(sed -n '/#define PHP_GEOIP_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_geoip.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cd %{pecl_name}-%{version}
%patch1 -p0 -b .tests


%build
cd %{pecl_name}-%{version}
%{php54_rootdir}%{_bindir}/phpize
%configure --prefix=%{php54_rootdir}%{_prefix} \
           --with-php-config=%{php54_rootdir}%{_bindir}/php-config
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot} INSTALL="install -p"

%{__mkdir_p} %{buildroot}%{php54_libdir}/php.d
%{__cat} > %{buildroot}%{php54_libdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%{__mkdir_p} %{buildroot}%{php54_pecl_xmldir}
%{__install} -p -m 644 %{pecl_name}.xml %{buildroot}%{php54_pecl_xmldir}/%{name}.xml


#broken on el5 ppc
#%check
#cd %{pecl_name}-%{version}

#TEST_PHP_EXECUTABLE=%{_bindir}/php \
#REPORT_EXIT_STATUS=1 \
#NO_INTERACTION=1 \
#%{_bindir}/php run-tests.php \
#    -n -q \
#    -d extension_dir=modules \
#    -d extension=%{pecl_name}.so


%clean
%{__rm} -rf %{buildroot}


%if 0%{?php54_pecl_install:1}
%post
%{php54_pecl_install} %{php54_pecl_xmldir}/%{name}.xml >/dev/null || :
%endif

%if 0%{?php54_pecl_uninstall:1}
%postun
if [ $1 -eq 0 ]  ; then
%{php54_pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/{README,ChangeLog}
%config(noreplace) %{php54_libdir}/php.d/%{pecl_name}.ini
%{php54_extdir}/%{pecl_name}.so
%{php54_pecl_xmldir}/%{name}.xml

%changelog
* Sun Oct 28 2012 Curt Zirzow <czirzow@shutterstock.com> - 1.0.8-4
- namespace for rock runtime php54

* Sun Oct 28 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.8-3
- Fix php spec file macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8 for php 5.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Remi Collet <remi@fedoraproject.org> - 1.0.7-7
- fix segfault when build with latest GeoIP (#746417)
- run test suite during build
- add patch for tests, https://bugs.php.net/bug.php?id=59804
- add filter to avoid private-shared-object-provides geoip.so

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.7-6
- Fix bugzilla #715693

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.7-3
- rebuild for new PHP 5.3.0 ABI (20090626)

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.7-2
- Fix timestamps on installed files

* Sun Jun 14 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.7-1
- Initial RPM package
