%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-python27
Version:        1
Release:        8%{?dist}
Summary:        python27 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-python27-core-rpmbuild
Requires:       rock-runtime-python27-core >= 2.7.5-1
Requires:       rock-runtime-python27-virtualenv >= 1.10-1

%description
python27 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python27_rootdir}

cat << EOF > %{buildroot}%{python27_rootdir}/rock.yml
env:
  PATH: "%{python27_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python27_rootdir}/rock.yml

%changelog
* Sun Aug 04 2013 RockStack <packages@rockstack.org> - 1-8
- Python 2.7.5
- virtualenv 1.10

* Tue Apr 09 2013 RockStack <packages@rockstack.org> - 1-7
- Python 2.7.4
- virtualenv 1.9.1

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1-6
- Update to virtualenv 1.8.4

* Wed Sep 12 2012 RockStack <packages@rockstack.org> - 1-5
- Update to virtualenv 1.8.2

* Fri Jul 20 2012 RockStack <packages@rockstack.org> - 1-4
- Convert env to rock.yml

* Wed Jul 18 2012 RockStack <packages@rockstack.org> - 1-3
- Update to virtualenv 1.7.2

* Tue Jul 10 2012 RockStack <packages@rockstack.org> - 1-2
- Add env file
- Add explicit requires

* Mon May 14 2012 RockStack <packages@rockstack.org> - 1-1
- Initial build
