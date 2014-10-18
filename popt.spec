# based on PLD Linux spec git://git.pld-linux.org/packages/popt.git
Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.16
Release:	6
License:	X Consortium (MIT-like)
Group:		Libraries
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
# Source0-md5:	3743beefa3dd6247a73f8f7a32c14c33
URL:		http://rpm5.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't require very fresh rpm.macros to build
%define		__gettextize	gettextize --copy --force ; cp -f po/Makevars{.template,}

%description
Popt is a C library for passing command line parameters. It was heavily
influenced by the getopt() and getopt_long() functions, but it allows
more powerful argument expansion. It can parse arbitrary argv[] style
arrays and automatically set variables based on command line
arguments. It also allows command line arguments to be aliased via
configuration files and includes utility functions for parsing
arbitrary strings into argv[] arrays using shell-like rules.

%package devel
Summary:	Header file and documentation for popt development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file and documentation for popt development.

%prep
%setup -q

%{__sed} -i 's#po/Makefile.in intl/Makefile##g' configure.ac
%{__sed} -i '/AM_C_PROTOTYPES/d' configure.ac
%{__sed} -i 's/^TESTS.*/TESTS = testit.sh/' Makefile.am

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake} -i
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	pkgconfigdir=%{_pkgconfigdir}	\
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES COPYING README
%attr(755,root,root) %ghost %{_libdir}/libpopt.so.?
%attr(755,root,root) %{_libdir}/libpopt.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpopt.so
%{_includedir}/popt.h
%{_pkgconfigdir}/popt.pc
%{_mandir}/man3/popt.3*

