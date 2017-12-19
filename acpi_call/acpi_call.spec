%global commitdate 20130606
%global commit ac67445bc75ec4fcf46ceb195fb84d74ad350d51
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global srcname acpi_call

%define module acpi_call
%define version 1.1.0

Summary: %{module} %{version} dkms package
Name: %{module}
Version: %{version}
Release: 2dkms
License: GPLv2
Group: System Environment/Kernel
Requires: dkms >= 1.00
Requires: bash
Requires: kernel-devel
URL: https://github.com/mkottman/acpi_call

Source0: https://github.com/mkottman/%{srcname}/archive/%{commit}/%{srcname}-%{version}-%{shortcommit}.tar.gz
Source1: dkms.conf
Patch0: patch-for-kernel-4.12.patch

%description
This package contains %{module} module wrapped for
the DKMS framework.

%prep
rm -rf %{module}-%{version}
%setup -q -c -T -a 0
%patch0 -p1
mv acpi_call-ac67445bc75ec4fcf46ceb195fb84d74ad350d51/ %{module}-%{version}/
cp %{SOURCE1} %{module}-%{version}/

%install
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

mkdir -p $RPM_BUILD_ROOT/usr/src/%{module}-%{version}/
cp -rf %{module}-%{version}/* $RPM_BUILD_ROOT/usr/src/%{module}-%{version}/

mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{module}/
cp %{module}-%{version}/README.md $RPM_BUILD_ROOT/usr/share/doc/%{module}/

%clean
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
/usr/src/%{module}-%{version}/
/usr/share/doc/%{module}/

%pre

%post
dkms add -m %{module} -v %{version} --rpm_safe_upgrade

	if [ `uname -r | grep -c "BOOT"` -eq 0 ] && [ -e /lib/modules/`uname -r`/build/include ]; then
		dkms build -m %{module} -v %{version}
		dkms install -m %{module} -v %{version}
	elif [ `uname -r | grep -c "BOOT"` -gt 0 ]; then
		echo -e ""
		echo -e "Module build for the currently running kernel was skipped since you"
		echo -e "are running a BOOT variant of the kernel."
	else
		echo -e ""
		echo -e "Module build for the currently running kernel was skipped since the"
		echo -e "kernel headers for this kernel do not seem to be installed."
	fi
exit 0

%preun
echo -e
echo -e "Uninstall of %{module} module (version %{version}) beginning:"
dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade
exit 0
