%bcond_with gui

%global commit0 eafd478ae81ac1d4a757bbc1a80f4b9568e6aaca
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%if 0%{?rhel} && 0%{?rhel} < 7
%global py26 1
%endif

Name:           rmlint
Version:        2.6.1
Release:        2%{?commit0:.git%{shortcommit0}}%{?dist}
Summary:        rmlint finds space waste and other broken things on your filesystem and offers to remove it.
Group:          Applications/System
License:        GPLv3
URL:            http://rmlint.rtfd.org
Source0:        https://github.com/sahib/%{name}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

%if 0%{?py26}
Patch0:         0001-python-2.6-compat.patch
Patch1:         0002-allow-old-glib2.patch
%endif

Requires:       glib2
Requires:       libblkid
Requires:       elfutils-libelf
Requires:       json-glib
BuildRequires:  scons
%if 0%{?py26}
BuildRequires:  python27-virtualenv
%else
BuildRequires:  python-sphinx
%endif
BuildRequires:  gettext
BuildRequires:  libblkid-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  glib2-devel
BuildRequires:  json-glib-devel

%description
rmlint finds space waste and other broken things and offers to remove it. It is
especially an extremely fast tool to remove duplicates from your filesystem.

%global debug_package %{nil}

%if %{with gui}
%package gui
Summary:        rmlint gui
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Requires:       pygobject3
Requires:       gtk3
Requires:       librsvg2
BuildRequires:  python36u

%description gui
rmlint gui
%endif

%prep 
%autosetup -n %{name}-%{?commit0}%{?!commit0:%{version}} -p1

%build
%if 0%{?py26}
virtualenv-2.7 venv
. venv/bin/activate
pip install sphinx
%endif
scons config
scons --prefix=%{buildroot}%{_prefix} --actual-prefix=%{_prefix} --libdir=%{_libdir}

%install
%if 0%{?py26}
. venv/bin/activate
%endif
# Build rmlint, install it into BUILDROOT/<name>-<version>/,
# but take care rmlint thinks it's installed to /usr (--actual_prefix)
scons install --prefix=%{buildroot}%{_prefix} --actual-prefix=%{_prefix} --libdir=%{_libdir}
%if 0%{?py26}
rm -rf venv
%endif

# Find all rmlint.mo files and put them in rmlint.lang
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%doc README.rst COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Sep 06 2017 Frankie Dintino <fdintino@gmail.com> - 2.6.1-1
- Update version to 2.6.1
* Sun May 10 2015 Christopher Pahl <sahib@online.de> - 2.2.0-1
- Update version to 2.2.0
* Sun Jan 11 2015 Christopher Pahl <sahib@online.de> - 2.0.0-4
- Fix rpm for lib separation.
* Sat Dec 20 2014 Christopher Pahl <sahib@online.de> - 2.0.0-3
- Use autosetup instead of setup -q
* Fri Dec 19 2014 Christopher Pahl <sahib@online.de> - 2.0.0-2
- Updated wrong dependency list
* Mon Dec 01 2014 Christopher Pahl <sahib@online.de> - 2.0.0-1
- Initial release of RPM package 