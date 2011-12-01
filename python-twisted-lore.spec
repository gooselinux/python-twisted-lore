%{!?python:%define python python}
%{!?python_sitearch: %define python_sitearch %(%{python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           %{python}-twisted-lore
Version:        8.2.0
Release:        3.2%{?dist}
Summary:        Documentation generator with HTML and LaTeX support
Group:          Development/Libraries
License:        MIT
URL:            http://www.twistedmatrix.com/trac/wiki/TwistedLore
Source0:        http://tmrc.mit.edu/mirror/twisted/Lore/8.2/TwistedLore-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{python}-twisted-core >= 8.2.0
BuildRequires:  %{python}-devel
Requires:       %{python}-twisted-core >= 8.2.0
Requires:       %{python}-twisted-web

# a noarch-turned-arch package should not have debuginfo
%define debug_package %{nil}

%description
Twisted is an event-based framework for internet applications.

Lore is a complete documentation system based on XHTML and can generate
documentation into other formats such as PDF, HTML.

%prep
%setup -q -n TwistedLore-%{version}

# Fix line endings
sed -i -e 's,\r$,,' doc/howto/listings/lore/*

%build
%{python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

# This is a pure python package, but extending the twisted namespace from
# python-twisted-core, which is arch-specific, so it needs to go in sitearch
%{python} setup.py install -O1 --skip-build \
    --install-purelib %{python_sitearch} --root $RPM_BUILD_ROOT

# Man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
cp -a doc/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
rm -rf doc/man

# See if there's any egg-info
if [ -f $RPM_BUILD_ROOT%{python_sitearch}/Twisted*.egg-info ]; then
    echo $RPM_BUILD_ROOT%{python_sitearch}/Twisted*.egg-info |
        sed -e "s|^$RPM_BUILD_ROOT||"
fi > egg-info

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%postun
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%files -f egg-info
%defattr(-,root,root,-)
%doc LICENSE NEWS README doc/*
%{_bindir}/lore
%{_mandir}/man1/lore.1*
%{python_sitearch}/twisted/lore/
%{python_sitearch}/twisted/plugins/twisted_lore.py*

%changelog
* Wed Jan 27 2010 David Malcolm <dmalcolm@redhat.com> - 8.2.0-3.2
- fix source URL

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 8.2.0-3.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.
- Remove no longer installed "bookify" program.

* Tue Dec 23 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0.
- Merge back changes from Paul Howarth.
- Make sure the scriplets never return a non-zero exit status.

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.0-3
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.0-2
- Rebuild for Python 2.6

* Wed May 21 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- Update to 0.3.0 release

* Fri Mar 07 2008 Jesse Keating <jkeating@redhat.com> - 0.2.0-6
- Handle the egg, drop the pyver stuff.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.0-5
- Autorebuild for GCC 4.3

* Wed Jan 03 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.0-4
- add python-devel BR
- add docs

* Wed Nov 01 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.0-3
- fix end-of-line on some files

* Tue Sep 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.0-2
- no longer ghost .pyo files
- rebuild dropin.cache

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.0-1
- remove noarch

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-2
- disttag

* Fri Mar 25 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- final release

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a2
- prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- prep for split

