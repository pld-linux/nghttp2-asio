#
# Conditional build:
%bcond_without	asio		# libnghttp2_asio C++ library
%bcond_without	static_libs	# static libraries
%bcond_without	tests		# "make check" call

Summary:	HTTP/2.0 C library
Summary(pl.UTF-8):	Biblioteka C HTTP/2.0
Name:		nghttp2
Version:	0.7.5
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tatsuhiro-t/nghttp2/releases
Source0:	https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	d89aa34f33ac285be541198f287b77cb
Patch0:		%{name}-link.patch
URL:		https://github.com/tatsuhiro-t/nghttp2
%{?with_tests:BuildRequires:	CUnit >= 2.1}
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
%{?with_asio:BuildRequires:	boost-devel >= 1.54.0}
BuildRequires:	jansson-devel >= 2.5
BuildRequires:	libev-devel
BuildRequires:	libevent-devel >= 2.0.8
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.7.7
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	python >= 1:2.7
BuildRequires:	python-Cython
BuildRequires:	spdylay-devel >= 1.3.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.2.3
Requires:	jansson >= 2.5
Requires:	libevent >= 2.0.8
Requires:	libxml2 >= 1:2.7.7
Requires:	openssl >= 1.0.1
Requires:	spdylay >= 1.3.0
Requires:	zlib >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# non-function symbols std::__once_call, std::__once_callable
%define		skip_post_check_so	libnghttp2_asio.so.*

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

%package asio
Summary:	HTTP/2.0 C++ library
Summary(pl.UTF-8):	Biblioteka C++ HTTP/2.0
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl >= 1.0.1

%description asio
HTTP/2.0 C++ library.

%description asio -l pl.UTF-8
Biblioteka C++ HTTP/2.0.

%package asio-devel
Summary:	Header file for nghttp2_asio library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki nghttp2_asio
Group:		Development/Libraries
Requires:	%{name}-asio = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description asio-devel
Header file for nghttp2_asio library.

%description asio-devel -l pl.UTF-8
Plik nagłówkowy biblioteki nghttp2_asio.

%package asio-static
Summary:	Static libnghttp2_asio library
Summary(pl.UTF-8):	Statyczna biblioteka libnghttp2_asio
Group:		Development/Libraries
Requires:	%{name}-asio-devel = %{version}-%{release}

%description asio-static
Static libnghttp2_asio library.

%description asio-static -l pl.UTF-8
Statyczna biblioteka libnghttp2_asio.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-app \
	%{?with_asio:--enable-asio-lib} \
	--enable-hpack-tools \
	--enable-python-bindings \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--without-jemalloc

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnghttp2*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/nghttp2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	asio -p /sbin/ldconfig
%postun	asio -p /sbin/ldconfig

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
%attr(755,root,root) %ghost %{_libdir}/libnghttp2.so.5
%{_mandir}/man1/h2load.1*
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnghttp2.so
%dir %{_includedir}/nghttp2
%{_includedir}/nghttp2/nghttp2*.h
%{_pkgconfigdir}/libnghttp2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnghttp2.a
%endif

%files -n python-nghttp2
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/nghttp2.so
%{py_sitedir}/python_nghttp2-%{version}-py*.egg-info

%if %{with asio}
%files asio
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnghttp2_asio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnghttp2_asio.so.0

%files asio-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnghttp2_asio.so
%{_includedir}/nghttp2/asio_http2.h
%{_pkgconfigdir}/libnghttp2_asio.pc

%if %{with static_libs}
%files asio-static
%defattr(644,root,root,755)
%{_libdir}/libnghttp2_asio.a
%endif
%endif
