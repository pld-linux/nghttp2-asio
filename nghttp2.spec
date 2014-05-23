#
# Conditional build:
%bcond_without	tests		# don't perform "make check"
%bcond_without	static_libs	# don't build static library

Summary:	HTTP/2.0 C library
Summary(pl.UTF-8):	Biblioteka C HTTP/2.0
Name:		nghttp2
Version:	0.4.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tatsuhiro-t/nghttp2/releases
Source0:	https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	ae6f5ebe15bd461893d220662575bad6
URL:		https://github.com/tatsuhiro-t/nghttp2
%{?with_tests:BuildRequires:	CUnit >= 2.1}
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
%{?with_tests:BuildRequires:	jansson-devel >= 2.5}
BuildRequires:	libevent-devel >= 2.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.7.7
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	python >= 1:2.7
BuildRequires:	python-Cython
BuildRequires:	spdylay-devel >= 1.2.3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.2.3
Requires:	libevent >= 2.0.8
Requires:	libxml2 >= 1:2.7.7
Requires:	openssl >= 1.0.1
Requires:	spdylay >= 1.2.3
Requires:	zlib >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an experimental implementation of Hypertext Transfer Protocol
version 2.0.

%description -l pl.UTF-8
Ta biblioteka jest eksperymentalną implementacją protokołu HTTP
(Hypertext Transfer Protocol) w wersji 2.0.

%package devel
Summary:	Files needed for developing with libnghttp2
Summary(pl.UTF-8):	Pliki niezbędne do tworzenia aplikacji z użyciem libnghttp2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel >= 1.2.3

%description devel
Files needed for building applications with libnghttp2.

%description devel -l pl.UTF-8
Pliki niezbędne do tworzenia aplikacji z użyciem libnghttp2.

%package static
Summary:	Static libnghttp2 library
Summary(pl.UTF-8):	Statyczna biblioteka libnghttp2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnghttp2 library.

%description static -l pl.UTF-8
Statyczna biblioteka libnghttp2.

%package -n python-nghttp2
Summary:	Python binding to nghttp2 library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki nghttp2
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.7

%description -n python-nghttp2
Python binding to nghttp2 library.

%description -n python-nghttp2 -l pl.UTF-8
Wiązanie Pythona do biblioteki nghttp2.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnghttp2.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/nghttp2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README.rst
%attr(755,root,root) %{_bindir}/deflatehd
%attr(755,root,root) %{_bindir}/h2load
%attr(755,root,root) %{_bindir}/inflatehd
%attr(755,root,root) %{_bindir}/nghttp
%attr(755,root,root) %{_bindir}/nghttpd
%attr(755,root,root) %{_bindir}/nghttpx
%attr(755,root,root) %{_libdir}/libnghttp2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnghttp2.so.3
%{_mandir}/man1/h2load.1*
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnghttp2.so
%{_includedir}/nghttp2
%{_pkgconfigdir}/libnghttp2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnghttp2.a
%endif

%files -n python-nghttp2
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/nghttp2.so
%{py_sitedir}/python_nghttp2-0.0.0-py*.egg-info
