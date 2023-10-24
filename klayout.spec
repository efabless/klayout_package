#
# spec file for package klayout
#
# Copyright (c) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           klayout
Version:        0.28.12
Release:        0
Summary:        KLayout, viewer and editor for mask layouts
License:        GPL-2.0+
Group:          Productivity/Scientific/Electronics
Url:            http://www.klayout.de
Source0:        http://www.klayout.de/downloads/source/%{name}-%{version}.tar.gz
# BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define git_source /root/klayout
# Disable auto-detection of dependencies (to prevent including the
# so's of klayout itself)
AutoReqProv: 	no
Requires:	python3 >= 3.6.0
Requires: qt-x11 >= 4.8.5
%define buildopt -j2
%description
Mask layout viewer and editor for the chip design engineer.

For details see README.md

%prep

%if "%{git_source}" != ""
  rm -rf %{_sourcedir}
  ln -s %{git_source} %{_sourcedir}
%else
  %setup -q	
%endif

%build

TARGET="linux-release"

%if "%{git_source}" != ""
# build from git sources if possible
cd %{git_source}
%else
cd %{_sourcedir}
%endif

# clean bin dir
rm -rf %{_builddir}/bin.$TARGET

# do the actual build
./build.sh -rpath %{_libdir}/klayout \
           -bin %{_builddir}/bin.$TARGET \
           -build %{_builddir}/build.$TARGET \
	   -ruby /usr/local/bin/ruby \
	   -python /usr/bin/python3 \
           %{buildopt} 

cp -p LICENSE Changelog CONTRIB %{_builddir}
strip %{_builddir}/bin.$TARGET/*.so
strip %{_builddir}/bin.$TARGET/*/*.so
strip %{_builddir}/bin.$TARGET/*/*/*.so
strip %{_builddir}/bin.$TARGET/klayout
strip %{_builddir}/bin.$TARGET/strm*

%install

TARGET="linux-release"

# create and populate libdir
mkdir -p %{buildroot}%{_libdir}/klayout
mkdir -p %{buildroot}%{_libdir}/klayout/db_plugins
mkdir -p %{buildroot}%{_libdir}/klayout/lay_plugins
cp -pd %{_builddir}/bin.$TARGET/lib*.so* %{buildroot}%{_libdir}/klayout
cp -pd %{_builddir}/bin.$TARGET/db_plugins/lib*.so* %{buildroot}%{_libdir}/klayout/db_plugins
cp -pd %{_builddir}/bin.$TARGET/lay_plugins/lib*.so* %{buildroot}%{_libdir}/klayout/lay_plugins
chmod 644 %{buildroot}%{_libdir}/klayout/*.so*
chmod 644 %{buildroot}%{_libdir}/klayout/db_plugins/*.so*
chmod 644 %{buildroot}%{_libdir}/klayout/lay_plugins/*.so*

# create and populate bindir
mkdir -p %{buildroot}%{_bindir}
cp -pd %{_builddir}/bin.$TARGET/klayout %{_builddir}/bin.$TARGET/strm* %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/*

# other files
install -Dm644 %{_sourcedir}/etc/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm644 %{_sourcedir}/etc/logo.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# TODO: remove this? This macro does not expand to anything in SuSE 42.x
#%if 0%{?suse_version}%{?sles_version}
#%suse_update_desktop_file -n %{name}
#%endif

%files
%defattr(-,root,root)
%doc LICENSE
%doc Changelog
%doc CONTRIB
%{_bindir}/klayout
%{_bindir}/strm*
%{_libdir}/klayout/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog

