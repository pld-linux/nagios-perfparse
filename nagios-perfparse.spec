# TODO
# - devel/static packagages needed? what for?
#
# Conditional build:
%bcond_without	mysql		# skip building of mysql storage
%bcond_with	pgsql		# use pgsql storage (broken)
%bcond_with	devel		# build devel packages
#
Summary:	Add-On for Nagios®
Name:		nagios-perfparse
Version:	0.105.6
Release:	0.5
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/perfparse/perfparse-%{version}.tar.gz
# Source0-md5:	d5fbca1184d9e831b14ed7088f295772
URL:		http://perfparse.sourceforge.net/
BuildRequires:	zlib-devel
BuildRequires:	glib-devel
BuildRequires:	gd-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
Requires:	nagios-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc/nagios
%define		_sbindir	/usr/%{_lib}/nagios/cgi

%description
PerfParse facilitates the storage and analysis of binary performance
data produced by Nagios and produces high-quality accurate graphs of
live data from standard Nagios plugins. A permanent history of plugin
results can then be viewed with advanced analysis tools.

%package devel
Summary:	Development libraries for perfparse library
Group:		Development/Libraries

%description devel
This is the package containing the development libaries files for perfparse.

%package storage-mysql
Summary:	mysql storage module for perfparse
Group:		Development/Libraries

%description storage-mysql
mysql storage module for perfparse.

%package storage-pgsql
Summary:	pgsql storage module for perfparse
Group:		Development/Libraries

%description storage-pgsql
pgsql storage module for perfparse.

%package static
Summary:	Static perfparse libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libraries for perfparse.

%prep
%setup -q -n perfparse-%{version}

%build
%configure \
	--with-data-source=nagios \
	--with-db=%{?with_mysql:mysql}%{?with_pgsql:postgresql}%{!?with_mysql:%{!?with_pgsql:none}}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{without devel}
rm -f $RPM_BUILD_ROOT/usr/lib/lib*.{la,a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	storage-mysql -p /sbin/ldconfig
%postun	storage-mysql -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%{_sysconfdir}/nagios_perfparse.cfg
%{_sysconfdir}/perfparse.cfg.example

%attr(755,root,root) %{_bindir}/perfparse-log2any
%attr(755,root,root) %{_bindir}/perfparse.sh.example
%attr(755,root,root) %{_bindir}/perfparse_nagios_command.pl
%attr(755,root,root) %{_bindir}/perfparse_nagios_pipe_command.pl
%attr(755,root,root) %{_bindir}/perfparsed

%attr(755,root,root) %{_libdir}/libpp_common.so.0.0.0
%attr(755,root,root) %{_libdir}/libpp_storage_file_output.so.0.0.0
%attr(755,root,root) %{_libdir}/libpp_storage_gnuplot.so.0.0.0
%attr(755,root,root) %{_libdir}/libpp_storage_print.so.0.0.0
%attr(755,root,root) %{_libdir}/libpp_storage_socket_output.so.0.0.0
%attr(755,root,root) %{_libdir}/libpp_storage_stdout.so.0.0.0
%attr(755,root,root) %{_libdir}/libnagios_perfdata_parser.so.0.0.0

%if %{with mysql} || %{with pgsql}
%attr(755,root,root) %{_bindir}/check_perfparse_version
%attr(755,root,root) %{_bindir}/perfparse-db-purge
%attr(755,root,root) %{_bindir}/perfparse-db-tool

%attr(755,root,root) %{_sbindir}/perfchart.png
%attr(755,root,root) %{_sbindir}/perfgant.png
%attr(755,root,root) %{_sbindir}/perfparse.cgi
%endif

%{_datadir}/locale/de/LC_MESSAGES/perfparse.mo
%{_datadir}/locale/fr/LC_MESSAGES/perfparse.mo
%{_datadir}/perfparse/images/dec0.png
%{_datadir}/perfparse/images/dec1.png
%{_datadir}/perfparse/images/inc0.png
%{_datadir}/perfparse/images/inc1.png
%{_datadir}/perfparse/images/perfgraph-sm.png
%{_datadir}/perfparse/images/perfparse-logo-sm.png
%{_datadir}/perfparse/images/perfparse-logo.png

%if %{with mysql}
%files storage-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpp_mysql.so.0.0.0
%attr(755,root,root) %{_libdir}/libpp_storage_mysql.so.0.0.0
%endif

%if %{with devel}
%files devel
%defattr(644,root,root,755)
%{_libdir}/libpp_common.la
%{_libdir}/libpp_storage_file_output.la
%{_libdir}/libpp_storage_gnuplot.la
%{_libdir}/libpp_storage_print.la
%{_libdir}/libpp_storage_socket_output.la
%{_libdir}/libpp_storage_stdout.la
%{_libdir}/libnagios_perfdata_parser.la

%if %{with mysql}
%{_libdir}/libpp_mysql.la
%{_libdir}/libpp_storage_mysql.la
%endif

%files static
%defattr(644,root,root,755)
%{_libdir}/libpp_common.a
%{_libdir}/libpp_storage_file_output.a
%{_libdir}/libpp_storage_gnuplot.a
%{_libdir}/libpp_storage_print.a
%{_libdir}/libpp_storage_socket_output.a
%{_libdir}/libpp_storage_stdout.a
%{_libdir}/libnagios_perfdata_parser.a

%if %{with mysql}
%{_libdir}/libpp_mysql.a
%{_libdir}/libpp_storage_mysql.a
%endif
%endif
