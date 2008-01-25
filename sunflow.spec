%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Name:           sunflow
Version:        0.07.2
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Sunflow is a rendering system for photo-realistic image synthesis
License:        MIT
URL:            http://sunflow.sourceforge.net
Group:          Development/Java
Source0:        http://puzzle.dl.sourceforge.net/sourceforge/sunflow/%{name}-src-v%{version}.zip
Source1:        sunflow.sh
BuildRequires:  ant
BuildRequires:  java-rpmbuild
BuildRequires:  janino
BuildRequires:  jpackage-utils >= 0:1.7.2
%if ! %{gcj_support}
BuildArch:      noarch
%endif
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif
Requires:       janino

%description
Sunflow is an open source rendering system for photo-realistic image synthesis. It is written in Java and built around a flexible ray tracing core and an extensible object-oriented design.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{name}
Group:          Development/Java

%description    manual
%{summary}.

%prep
%setup -q -n %{name}
%remove_java_binaries

%build
ln -sf $(build-classpath janino) janino.jar
export CLASSPATH=$(build-classpath janino)
%{ant} jars javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 release/sunflow.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# script
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# javadoc
install -p -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr release/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}
