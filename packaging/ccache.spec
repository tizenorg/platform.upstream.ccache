#
# spec file for package ccache
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

# norootforbuild

%ifarch armv7l
%define ARCH armv7l
%define ABI eabi
%endif
%ifarch %ix86
%define ARCH i586
%endif
%ifarch x86_64
%define ARCH x86_64
%endif
%ifarch aarch64
%define ARCH aarch64
%endif
%define gcc_target %{ARCH}-tizen-linux-gnu%{?ABI}


Name:           ccache
Version:        3.2.3
Release:        1
Summary:        A Fast C/C++ Compiler Cache

License:        GPLv3+
Url:            http://ccache.samba.org/
Group:          Development/Languages/C and C++
Source0:        http://samba.org/ftp/ccache/%{name}-%{version}.tar.bz2
Source1001: 	ccache.manifest
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:  zlib-devel
Provides:       distcc:/usr/bin/ccache

%description
ccache is a compiler cache. It speeds up recompilation by caching the result of
previous compilations and detecting when the same compilation is being done
again. Supported languages are C, C++, Objective-C and Objective-C++.

%prep
%setup -q
cp %{SOURCE1001} .

%build
./autogen.sh
%configure --bindir=%{_prefix}/local/bin
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

gcc_version=`gcc --version | sed -ne '1s/.* //p'`
for compiler in c{c,++} g{cc,++} %{gcc_target}-g{cc,++} %{gcc_target}-c++ %{gcc_target}-gcc-${gcc_version} %{?clang_build:clang clang++}
do
  ln -s ccache %{buildroot}%{_prefix}/local/bin/$compiler
done
## configuration
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}/var/ccache/cache
chmod 777 %{buildroot}/var/ccache/cache
cat > %{buildroot}/etc/ccache.conf << EOF
cache_dir = /var/ccache/cache
compiler_check = content
max_size = 100G
log_file = /home/abuild/.ccache.log
EOF

%post
touch /var/ccache/timestamp

%clean
rm -rf %{buildroot}

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc AUTHORS.* GPL-3.0.txt INSTALL.* LICENSE.* MANUAL.* NEWS.* README.*
%{_prefix}/local/bin/*
/var/ccache/cache
/etc/ccache.conf

%changelog
