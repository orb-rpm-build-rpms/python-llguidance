Name:           python-llguidance
Version:        1.7.6
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Bindings for the Low-level Guidance _llguidance_ Rust library for use within Guidance

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        MIT
URL:            https://github.com/microsoft/llguidance
Source:         %{pypi_source llguidance}

BuildRequires:  python3-devel
BuildRequires:  gcc


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'llguidance' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-llguidance
Summary:        %{summary}

%description -n python3-llguidance %_description


%prep
%autosetup -p1 -n llguidance-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# Automatically extracted from wheel
%pyproject_save_files -l llguidance


%check
%pyproject_check_import


%files -n python3-llguidance -f %{pyproject_files}


%changelog
%autochangelog
