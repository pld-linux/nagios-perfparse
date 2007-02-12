# Conditional build:
%bcond_with	mysql		# skip building of mysql storage
%bcond_with	pgsql		# use pgsql storage (broken)
#
Summary:	Add-On for Nagios(R)
Summary(pl.UTF-8):   Dodatek perfparse dla Nagiosa
Name:		nagios-perfparse
Version:	0.105.6
Release:	0.15
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/perfparse/perfparse-%{version}.tar.gz
# Source0-md5:	d5fbca1184d9e831b14ed7088f295772
Source1:	perfparse.cfg
URL:		http://perfparse.sourceforge.net/
BuildRequires:	zlib-devel
BuildRequires:	glib2-devel
BuildRequires:	gd-devel
BuildRequires:	pkgconfig
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{!?with_mysql:Obsoletes:	%{name}-storage-mysql}
Requires:	nagios-common >= 2.0-0.b3.36
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc/nagios
%define		_sbindir	/usr/%{_lib}/nagios/cgi

%description
PerfParse facilitates the storage and analysis of binary performance
data produced by Nagios and produces high-quality accurate graphs of
live data from standard Nagios plugins. A permanent history of plugin
results can then be viewed with advanced analysis tools.

%description -l pl.UTF-8
PerfParse ułatwia przechowywanie i analizę binarnych danych
dotyczących wydajności stworzonych przez Nagiosa oraz tworzy dokładne
wykresy żywych danych ze standardowych wtyczek Nagiosa. Ciągła
historia wyników wtyczki może być przeglądana zaawansowanymi
narzędziami do analizy.

%package storage-mysql
Summary:	mysql storage module for perfparse
Summary(pl.UTF-8):   Moduł przechowywania danych mysql dla perfparse
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description storage-mysql
mysql storage module for perfparse.

%description storage-mysql -l pl.UTF-8
Moduł przechowywania danych mysql dla perfparse.

%package storage-pgsql
Summary:	pgsql storage module for perfparse
Summary(pl.UTF-8):   Moduł przechowywania danych pgsql dla perfparse
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description storage-pgsql
pgsql storage module for perfparse.

%description storage-pgsql -l pl.UTF-8
Moduł przechowywania danych pgsql dla perfparse.

%prep
%setup -q -n perfparse-%{version}

%build
%configure \
	--with-data-source=nagios \
	--with-db=%{?with_mysql:mysql}%{?with_pgsql:postgresql}%{!?with_mysql:%{!?with_pgsql:none}}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/plugins

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/nagios_perfparse.cfg
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/plugins/perfparse.cfg
mv $RPM_BUILD_ROOT%{_sysconfdir}/perfparse.cfg{.example,}

# don't see reason for devel and static libs
rm -f $RPM_BUILD_ROOT/usr/lib/lib*.{la,a}

%find_lang perfparse

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	storage-mysql -p /sbin/ldconfig
%postun	storage-mysql -p /sbin/ldconfig

%files -f perfparse.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO scripts/*.sql
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugins/perfparse.cfg
%attr(640,root,nagios-data) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/perfparse.cfg

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

%dir %{_datadir}/perfparse
%dir %{_datadir}/perfparse/images
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
