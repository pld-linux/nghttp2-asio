#
# Conditional build:
%bcond_without	static_libs	# static libraries

%define		gitref	e877868abe06a83ed0a6ac6e245c07f6f20866b5
%define		snap	20220811
%define		rel	1

Summary:	HTTP/2.0 C++ library
Summary(pl.UTF-8):	Biblioteka C++ HTTP/2.0
Name:		nghttp2-asio
Version:	0.1.0
Release:	0.%{snap}.%{rel}
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	https://github.com/nghttp2/nghttp2-asio/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	55e61a2019a4b2839b1ad20a528ba3a7
URL:		https://nghttp2.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.54.0
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	nghttp2-devel >= 1.43.0
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig >= 1:0.20
Requires:	nghttp2-libs >= 1.43.0
Requires:	openssl >= 1.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HTTP/2.0 C++ library.

%description -l pl.UTF-8
Biblioteka C++ HTTP/2.0.

%package devel
Summary:	Header file for nghttp2_asio library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki nghttp2_asio
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel >= 6:5
Requires:	nghttp2-devel >= 1.43.0

%description devel
Header file for nghttp2_asio library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki nghttp2_asio.

%package static
Summary:	Static libnghttp2_asio library
Summary(pl.UTF-8):	Statyczna biblioteka libnghttp2_asio
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libnghttp2_asio library.

%description static -l pl.UTF-8
Statyczna biblioteka libnghttp2_asio.

%prep
%setup -q -n %{name}-%{gitref}

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

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnghttp2_asio.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_libdir}/libnghttp2_asio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnghttp2_asio.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnghttp2_asio.so
%{_includedir}/nghttp2/asio_http2.h
%{_includedir}/nghttp2/asio_http2_client.h
%{_includedir}/nghttp2/asio_http2_server.h
%{_pkgconfigdir}/libnghttp2_asio.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnghttp2_asio.a
%endif
