# select the realtime variety here
%global _with_rtai 0
%global _with_rt_preempt 0
%global _with_xenomai_kernel 1
%global _with_xenomai_user 0
%global _with_simulator 0

%global _gitrel    20121103git1fce7fb

%if 0%{?_with_rtai}
%global rt_opts --with-threads=rtai
%endif
%if 0%{?_with_rt_preempt 0}
%global rt_opts --with-threads=rt-preempt-user
%endif
%if 0%{?_with_xenomai_kernel 0}
%global xenomai_type xenomai-kernel
%global _with_xenomai 1
%endif
%if 0%{?_with_xenomai_user 0}
%global xenomai_type xenomai-user
%global _with_xenomai 1
%endif
%if 0%{?_with_simulator 0}
%global rt_opts --enable-simulator
%endif

%if 0%{?_with_xenomai}
# If kversion isn't defined on the rpmbuild line, find the
# version of the newest instelled xenomai kernel
%if 0%{!?xenomai_kversion}
%global xenomai_kversion $(rpm -q --qf='%{version}-%{release}.%{arch}' kernel | tail -1 || true)
%endif # !?xenomai_kversion
%define xenomai_kernel /boot/config-%{xenomai_kversion}
%define xenomai_kernel_headers %{_usrsrc}/kernels/%{xenomai_kversion}
%global rt_opts %{xenomai_type} \
	--with-kernel=%{xenomai_kernel} \
	--with-kernel-headers=%{xenomai_kernel_headers}
%endif # ?_with_xenomai


Name:		linuxcnc
Version:	2.6.0.pre0
Release:	0.1.%{_gitrel}%{?dist}
Summary:	a software system for computer control of machine tools

License:	GPL/LGPL
Group:		Applications/Engineering
URL:		http://www.linuxcnc.org
# git://git.mah.priv.at/emc2-dev.git rtos-integration-preview1 branch
Source0:	%{name}-%{version}.%{_gitrel}.tar.bz2

BuildRequires:  gtk2-devel libgnomeprintui22-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:	tcl-devel tk-devel bwidget libXaw-devel python-mtTkinter
BuildRequires:  lyx pth-devel dblatex libmodbus kernel-devel blt-devel
# temp. disable
#BuildRequires:  asciidoc >= 8.5
#
# any of the following?
#BuildRequires:  dietlibc-devel glibc-static
Requires:	bwidget blt
Requires:	kernel-rt

# xenomai 
%if 0%{?_with_xenomai}
BuildRequires:  kernel-xenomai == %{xenomai_kversion}
BuildRequires:  kernel-xenomai-devel
BuildRequires:  xenomai-devel

Requires:  kernel-xenomai == %{xenomai_kversion}
Requires:  xenomai
%endif

%description

LinuxCNC (the Enhanced Machine Control) is a software system for
computer control of machine tools such as milling machines and lathes.

This version is from Michael Haberler's preview that integrates RTAI,
RT_PREEMPT, Xenomai-kernel, Xenomai-User and Simulator

%package devel
Group: Development/Libraries/C and C++
Summary: Devel package for %{name}
Requires: %{name} = %{version}

%description devel
Development headers and libs for the %{name} package

%package doc
Group:		Documentation
Summary:	Documentation for %{name}

%description doc

Documentation files for LinuxCNC

%prep
%setup -q

%build
cd src
./autogen.sh
%configure  %{rt_opts} \
	    --with-tkConfig=%{_libdir}/tkConfig.sh \
	    --with-tclConfig=%{_libdir}/tclConfig.sh \
	    --enable-build-documentation
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd src
make -e install DESTDIR=$RPM_BUILD_ROOT \
     DIR='install -d -m 0755' FILE='install -m 0644' \
     EXE='install -m 0755' SETUID='install -m 0755'
# put the init file in the right place
mkdir $RPM_BUILD_ROOT/etc/rc.d
mv $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT%{_initddir}
# put the docs in the right place
mv $RPM_BUILD_ROOT/usr/share/doc/linuxcnc \
   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# put X11 app-defaults where the rest of them live
mv $RPM_BUILD_ROOT%{_sysconfdir}/X11 $RPM_BUILD_ROOT%{_datadir}/

# Set the module(s) to be executable, so that they will be stripped
# when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

%files
%defattr(-,root,root)
%attr(0755,-,-) %{_initddir}/realtime
%dir %{_sysconfdir}/linuxcnc
%{_sysconfdir}/linuxcnc/rtapi.conf
%config %{_datadir}/X11/app-defaults/*
%attr(0755,-,-) %{_bindir}/[0-9a-qs-z]*
%attr(0755,-,-) %{_bindir}/rs274
%attr(6755,root,root) %{_bindir}/rtapi_app
%{_prefix}/lib/emc2
%{python2_sitelib}/*
%{_prefix}/lib/tcltk/linuxcnc
%attr(0775,-,-) %{_libdir}/*.so*
%{_datadir}/axis
%{_datadir}/glade3
%{_datadir}/gtksourceview-2.0
%{_datadir}/linuxcnc
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/linuxcnc.mo
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/linuxcnc.mo
%lang(fi) %{_datadir}/locale/fi/LC_MESSAGES/linuxcnc.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/linuxcnc.mo
%lang(hu) %{_datadir}/locale/hu/LC_MESSAGES/linuxcnc.mo
%lang(it) %{_datadir}/locale/it/LC_MESSAGES/linuxcnc.mo
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/linuxcnc.mo
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/linuxcnc.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/linuxcnc.mo
%lang(ro) %{_datadir}/locale/ro/LC_MESSAGES/linuxcnc.mo
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/linuxcnc.mo
%lang(sk) %{_datadir}/locale/sk/LC_MESSAGES/linuxcnc.mo
%lang(sr) %{_datadir}/locale/sr/LC_MESSAGES/linuxcnc.mo
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/linuxcnc.mo
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/linuxcnc.mo
%lang(zh_HK) %{_datadir}/locale/zh_HK/LC_MESSAGES/linuxcnc.mo
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/linuxcnc.mo
%doc %{_mandir}/man[19]/*

%files devel
%{_includedir}/linuxcnc
%{_libdir}/liblinuxcnc.a
%doc %{_mandir}/man3/*

%files doc
%{_docdir}/%{name}-%{version}

%changelog
* Mon Nov  5 2012 John Morris <john@zultron.com> - 2.6.0.pre0-0.1.20121102gited5d8f8
- Update to Haberler's 2.6.0.pre0-20121103git1fce7fb with
  multiple RT systems support
- Add configuration code for xenomai, based on Zultron kernel

* Sun May  6 2012  <john@zultron.com> - 2.6.0.pre0-1
- Updated to newest git:
  - Forward-port of Michael Buesch's patches
  - Fixes to the hal stacksize, no more crash!
  - Install shared libs mode 0755 for /usr/lib/rpm/rpmdeps

* Wed Apr 25 2012  <john@zultron.com> - 2.5.0.1-1
- Initial RPM version





