%global		_disable_ld_no_undefined	1
%global		module		Alps

Name:		coin-or-%{module}

Summary:	COIN-OR High-Performance Parallel Search Framework
Version:	1.4.10
Release:	3%{?dist}
License:	EPL
URL:		https://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/CHiPPS/%{module}-%{version}.tgz
Source1:	%{name}.rpmlintrc
BuildRequires:	bzip2-devel
BuildRequires:	blas-devel
BuildRequires:	coin-or-Cgl-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
BuildRequires:	glpk-devel
BuildRequires:	graphviz
BuildRequires:	lapack-devel
BuildRequires:	libatlas-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	texlive-epstopdf
BuildRequires:	zlib-devel

# Properly handle DESTDIR
Patch0:		%{name}-pkgconfig.patch

# Install documentation in standard rpm directory
Patch1:		%{name}-docdir.patch

# Bad #define generated if svnversion is available
Patch2:		%{name}-svnversion.patch

%description
CHiPPS is the COIN-OR High-Performance Parallel Search Framework, a framework
for implementing parallel algorithms based on tree search. The current CHiPPS
architecture consists of three layers. The Abstract Library for Parallel Search
(ALPS) is the base layer of a hierarchy consisting of implementations of
various tree search algorithms for specific problem types. The Branch,
Constrain, and Price Software (BiCePS) is a data management layer built on
top of ALPS for implementing relaxation-based branch and bound algorithms.
The BiCePS Linear Integer Solver (BLIS) is a concretization of the BiCePS
layer for solving mixed-integer linear programs. ALPS, BiCePS, and BLIS
are sub-repostories of the CHiPPS Subversion repository.

%package	devel
Summary:	Development files for %{name}

Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mkdir bin; pushd bin; ln -sf %{_bindir}/ld.bfd ld; popd; export PATH=$PWD/bin:$PATH
CFLAGS="%{optflags} -fuse-ld=bfd" CXXFLAGS="%{optflags} -fuse-ld=bfd" \
%configure2_5x
make %{?_smp_mflags} all doxydoc

%install
export PATH=$PWD/bin:$PATH
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check
export PATH=$PWD/bin:$PATH
make test

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/alps_addlibs.txt
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%{_libdir}/*.so.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Sat Mar  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.10-3
- Correct misspelling of _smp_mflags.
- Make devel subpackage require coin-or-CoinUtils-devel.

* Sat Mar  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.10-2
- Add missing bzip2-devel and texlive-epstopdf build requires.

* Sat Mar  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.10-1
- Update to latest upstream release.

* Wed Jan  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.9-1
- Update to latest upstream release.

* Wed Jan  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.8-1
- Update to latest upstream release.

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.5-1
- Update to latest upstream release.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.2-4
- Update to run make check (#894610#c4).

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.2-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.2-2
- Rename package to coin-or-Alps.
- Do not package Thirdy party data or data without clean license.

* Sat Sep 29 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.4.2-1
- Initial coinor-Alps spec.
