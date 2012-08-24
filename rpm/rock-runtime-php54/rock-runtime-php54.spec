%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-php54
Version:        1
Release:        5%{?dist}
Summary:        php54 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-php54-core-rpmbuild
Requires:       rock-runtime-php54-composer >= 1.0.0-0.2
Requires:       rock-runtime-php54-core >= 5.4.6-1

%description
php54 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{php54_rootdir}

cat > %{buildroot}%{php54_rootdir}/rock.yml << EOF
env:
  PATH: "%{php54_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php54_rootdir}/rock.yml

%changelog
* Thu Aug 23 2012 Silas Sewell <silas@sewell.org> - 1-5
- Composer 1.0.0 alpha5
- PHP 5.4.6

* Fri Jul 20 2012 Silas Sewell <silas@sewell.org> - 1-4
- Convert env to rock.yml

* Tue Jul 17 2012 Silas Sewell <silas@sewell.org> - 1-3
- Fix various issues with core package

* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Sun Jul 08 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
