Summary: Manipulate system time per process for testing purposes
Name: libfaketime
Version: 0.9.6
Release: 3%{?dist}
License: GPLv2+
Url: http://www.code-wizards.com/projects/%{name}/
Source: http://www.code-wizards.com/projects/%{name}/%{name}-%{version}.tar.gz
Group: System Environment/Libraries
Patch1: libfaketime-0.9.5-fix-infinite-recursion-on-real_clock_gettime.patch
Patch2: libfaketime-0.9.6-boottime.patch

%description
libfaketime intercepts various system calls which programs use to
retrieve the current date and time. It can then report faked dates and
times (as specified by you, the user) to these programs. This means you
can modify the system time a program sees without having to change the
time system- wide.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
# work around from upstream for autodetecting glibc version bug on i686
sed -i -e 's/__asm__(".symver timer_gettime_22/\/\/__asm__(".symver timer_gettime_22/' src/libfaketime.c
sed -i -e 's/__asm__(".symver timer_settime_22/\/\/__asm__(".symver timer_settime_22/' src/libfaketime.c


%build
cd src ; CFLAGS="%{optflags} -Wno-strict-aliasing" make %{?_smp_mflags} \
         PREFIX="%{_prefix}" LIBDIRNAME="/%{_lib}/faketime" all

%check
make %{?_smp_mflags} -C test all

%install
make PREFIX="%{_prefix}" DESTDIR=%{buildroot} LIBDIRNAME="/%{_lib}/faketime" install
rm -r %{buildroot}/%{_docdir}/faketime
# needed for stripping/debug package
chmod a+rx %{buildroot}/%{_libdir}/faketime/*.so.*

%files
%{_bindir}/faketime
%dir %attr(0755, root, root) %{_libdir}/faketime/
%attr(0755, root, root) %{_libdir}/faketime/libfaketime*so.*
%doc README COPYING NEWS README README.developers
%{_mandir}/man1/*

%changelog
* Wed Oct 12 2016 Paul Wouters <pwouters@redhat.com> - 0.9.6-4
- Add support for CLOCK_BOOTTIME (patch by Mario Pareja <pareja.mario@gmail.com>)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 28 2014 Paul Wouters <pwouters@redhat.com> - 0.9.6-1
- Upgraded to 0.9.6 which adds option to disable monotonic time faking
- fix permissions for symbol stripping for debug package

* Tue Oct 15 2013 Paul Wouters <pwouters@redhat.com> - 0.9.5-4
- Infinite recursion patch is still needed, make test causes
  segfaults otherwise.

* Mon Oct 14 2013 Paul Wouters <pwouters@redhat.com> - 0.9.5-3
- Work around from upstream for autodetecting glibc version bug on i686

* Mon Oct 14 2013 Paul Wouters <pwouters@redhat.com> - 0.9.5-2
- Remove use of ifarch for _lib macro for multilib

* Sun Oct 13 2013 Paul Wouters <pwouters@redhat.com> - 0.9.5-1
- Initial package
