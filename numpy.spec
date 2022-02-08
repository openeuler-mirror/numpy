%global modname numpy

Name:           numpy
Version:        1.17.2
Release:        1
Summary:        A fast multidimensional array facility for Python

License:        BSD and Python
URL:            http://www.numpy.org/
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  openblas-devel
BuildRequires:  lapack-devel gcc-gfortran python3-Cython

Patch0:         backport-CVE-2021-41496.patch

%description
NumPy is the fundamental package for scientific computing with Python. It contains among other things:
a powerful N-dimensional array object
sophisticated (broadcasting) functions
tools for integrating C/C++ and Fortran code
useful linear algebra, Fourier transform, and random number capabilities
Besides its obvious scientific uses, NumPy can also be used as an efficient multi-dimensional container of generic data. Arbitrary data-types can be defined. This allows NumPy to seamlessly and speedily integrate with a wide variety of databases.

%package -n python3-numpy
Summary:        A fast multidimensional array facility for Python
License:        BSD
%{?python_provide:%python_provide python3-numpy}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-cffi
BuildRequires:  python3-pytest

Provides:       python3-numpy-doc
Obsoletes:      python3-numpy-doc

%description -n python3-numpy
NumPy is the fundamental package for scientific computing with Python. It contains among other things:
a powerful N-dimensional array object
sophisticated (broadcasting) functions
tools for integrating C/C++ and Fortran code
useful linear algebra, Fourier transform, and random number capabilities
Besides its obvious scientific uses, NumPy can also be used as an efficient multi-dimensional container of generic data. Arbitrary data-types can be defined. This allows NumPy to seamlessly and speedily integrate with a wide variety of databases.

%package -n python3-numpy-f2py
Summary:        f2py for numpy
Requires:       python3-numpy = %{version}-%{release}
Requires:       python3-devel
Provides:       python3-f2py = %{version}-%{release}
%{?python_provide:%python_provide python3-numpy-f2py}

%description -n python3-numpy-f2py
This package includes a version of f2py that works properly with NumPy.

%prep
%autosetup -n %{name}-%{version} -p1

rm numpy/distutils/command/__init__.py && touch numpy/distutils/command/__init__.py

cat >> site.cfg <<EOF
[openblas]
library_dirs = %{_libdir}
openblas_libs = openblasp
EOF


%build
env OPENBLAS=%{_libdir} \
    BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python3} setup.py build


%install
env OPENBLAS=%{_libdir} \
    FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python3} setup.py install --root %{buildroot}


%check
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{python3_sitearch}" PYTHONDONTWRITEBYTECODE=1 \
    %{__python3} -c "import pkg_resources, numpy ; numpy.test(verbose=2)"
popd &> /dev/null

%files -n python3-numpy
%license LICENSE.txt
%doc THANKS.txt site.cfg.example
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}/*
%{python3_sitearch}/%{name}-*.egg-info
%exclude %{python3_sitearch}/%{name}/LICENSE.txt

%files -n python3-numpy-f2py
%{_bindir}/f2py
%{_bindir}/f2py3
%{_bindir}/f2py3**
%{python3_sitearch}/%{name}/f2py

%changelog
* Tue Feb 08 2022 huangtianhua <huangtianhua@huawei.com> - 1.17.2-1
- Upgrade to 1.17.2 to support OpenStack Train and remote python2

* Tue Jan 04 2022 yuanxin<yuanxin24@huawei.com> - 1.16.5-4
- fix CVE-2021-41496

* Tue Aug 18 2020 wenzhanli<wenzhanli2@huawei.com> - 1.16.5-3
- add release version for rebuild

* Tue Aug 18 2020 wenzhanli<wenzhanli2@huawei.com> - 1.16.5-2
- add release version 

* Tue Oct 22 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.16.5-1
- Package init
