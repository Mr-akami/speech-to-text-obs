{
  description = "Nix for python";

  inputs = {
    nixpkgs = { url = "github:NixOS/nixpkgs/nixpkgs-unstable"; };
    flake-utils = { url = "github:numtide/flake-utils"; };
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (nixpkgs.lib) optional;
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShell = pkgs.mkShell {
          venvDir = "./.venv";
          buildInputs = [
            pkgs.python310Packages.python
            pkgs.python310Packages.venvShellHook
            pkgs.python310Packages.pyaudio
            pkgs.ffmpeg
            pkgs.portaudio
            pkgs.alsa-lib
            pkgs.alsa-lib.dev
            pkgs.alsa-utils
            pkgs.alsa-tools
            pkgs.alsa-oss
            pkgs.alsa-plugins
            pkgs.pulseaudio
            pkgs.libpulseaudio
            # this is how we add native dependencies to the shell
            # e.g. grpc libstdc++.so.6
            pkgs.stdenv.cc.cc.lib
          ];
          
          
          #shellHook = ''
          #'';
          
          postVenvCreation = ''
             unset SOURCE_DATE_EPOCH
             # pip install -r requirements.txt --editable .
          '';
          
          # Now we can execute any commands within the virtual environment.
          # This is optional and can be left out to run pip manually.
          postShellHook = ''
            if [ -z "$IN_NIX_SHELL_ZSH" ]; then
              export IN_NIX_SHELL_ZSH=1
              echo "Starting Zsh..."
              which zsh
              ls -l $(which zsh)
              exec ${pkgs.zsh}/bin/zsh --login || echo "Failed to start Zsh"
            fi
            # allow pip to install wheels
            echo "LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib" >> .venv/bin/activate
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib
            unset SOURCE_DATE_EPOCH
          '';
        };
      });
}
