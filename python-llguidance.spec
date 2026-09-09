Name:           python-llguidance
Version:        1.7.6
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Bindings for the Low-level Guidance _llguidance_ Rust library for use within Guidance

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        MIT
URL:            https://github.com/microsoft/llguidance
Source0:        %{pypi_source llguidance}
# Vendored Rust dependencies. llguidance's crate graph pulls several crates that
# are either absent from Fedora (derivre, jsonschema, referencing, tiktoken-rs)
# or only present at incompatible versions (pyo3 0.28, tokenizers 0.21). Rather
# than package each one, the whole graph is built offline from a vendor tarball.
# It is not shipped in a lookaside cache: rust-sources.sh regenerates it with
# `cargo vendor` at build time (see that script).
Source1:        llguidance-%{version}-vendor.tar.xz

BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  cargo-rpm-macros


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'llguidance' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-llguidance
Summary:        %{summary}

%description -n python3-llguidance %_description


%prep
# -a1 unpacks the vendor tarball (Source1) into the source tree as ./vendor.
%autosetup -p1 -n llguidance-%{version} -a1
# Build the Rust crate graph from the vendored sources, fully offline. This
# replaces the cargo buildrequires generator: no per-crate BuildRequires are
# needed because every dependency is supplied by ./vendor.
%cargo_prep -v vendor


%generate_buildrequires
# Only the Python-side build requirements (maturin, ...). The Rust deps come
# from the vendor tree, so the cargo buildrequires generator is intentionally
# absent.
%pyproject_buildrequires


%build
export RUSTFLAGS='%{build_rustflags}'
%pyproject_wheel


%install
%pyproject_install
# Automatically extracted from wheel
%pyproject_save_files -l llguidance


%check
# llguidance.{hf,cli,llamacpp,mlx,numpy,torch} are optional integration shims
# that import heavy frameworks (transformers, huggingface_hub, llama_cpp, mlx,
# numpy, torch) at module top level. Those are only needed by users wiring
# llguidance to that backend, are not build dependencies, and are absent from
# the build root, so skip them in the build-time import check. The core modules
# and llguidance.tiktoken import cleanly.
%pyproject_check_import -e 'llguidance.hf' -e 'llguidance.cli' -e 'llguidance.llamacpp' -e 'llguidance.mlx' -e 'llguidance.numpy' -e 'llguidance.torch'


%files -n python3-llguidance -f %{pyproject_files}


%changelog
%autochangelog
