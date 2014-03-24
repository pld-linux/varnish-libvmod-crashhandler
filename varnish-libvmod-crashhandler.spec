#
# Conditional build:
%bcond_without	tests		# build without tests

%define	vmod	crashhandler
Summary:	Crash handler for Varnish
Name:		varnish-libvmod-%{vmod}
Version:	1.1.0
Release:	1
License:	BSD
Group:		Daemons
Source0:	https://github.com/varnish/libvmod-crashhandler/archive/%{version}/%{vmod}-%{version}.tar.gz
# Source0-md5:	4e0541f405565b2c91f2bc7c1393e1e3
URL:		https://github.com/varnish/libvmod-crashhandler
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python-docutils
BuildRequires:	varnish-source
%{?with_tests:BuildRequires:	varnish}
%requires_eq_to varnish varnish-source
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmoddir	%(pkg-config --variable=vmoddir varnishapi || echo ERROR)

%description
Varnish 3.0 Module that catches segfaults (SIGSEGV) and issues the
regular panic code to get a back trace.

Also includes a function to trigger a segfault forcibly. Use at your
own peril.

%prep
%setup -qc
mv libvmod-%{vmod}-*/* .

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}

VARNISHSRC=$(pkg-config --variable=srcdir varnishapi)
%configure \
	VARNISHSRC=$VARNISHSRC \
	VMODDIR=%{vmoddir} \
	--disable-static

%{__make} -j1
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/varnish/vmods/libvmod_%{vmod}.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{vmoddir}/libvmod_%{vmod}.so
%{_mandir}/man3/vmod_%{vmod}.3*
