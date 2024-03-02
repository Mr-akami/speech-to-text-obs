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
        
        # If https://github.com/NixOS/nixpkgs/issues/6860 is released, myAlsaLib is to be replaced.
        # This is due to .so files of alsa-plugins should be alsa-lib/lib/alsa-lib
         myAlsaLib = pkgs.stdenv.mkDerivation rec {
           pname = "my-alsa-lib";
           version = "1.0";

           buildInputs = [ pkgs.alsa-lib pkgs.alsa-plugins ];

           installPhase = ''
             mkdir -p $out/lib/alsa-lib

           # no need to symbolic link because path is the same
           #  ln -s ${pkgs.alsa-plugins}/lib/alsa-lib/libasound_module_pcm_jack.so $out/lib/alsa-lib
           #  ln -s ${pkgs.alsa-plugins}/lib/alsa-lib/libasound_module_pcm_oss.so $out/lib/alsa-lib
           #  ln -s ${pkgs.alsa-plugins}/lib/alsa-lib/libasound_module_pcm_pipewire.so $out/lib/alsa-lib
           #  ln -s ${pkgs.alsa-plugins}/lib/alsa-lib/libasound_module_pcm_pulse.so $out/lib/alsa-lib
           #  ln -s ${pkgs.alsa-plugins}/lib/alsa-lib/libasound_module_pcm_upmix.so $out/lib/alsa-lib
           #  ln -s ${pkgs.alsa-plugins}/lib/alsa-lib/libasound_module_pcm_usb_stream.so $out/lib/alsa-lib
           #  ln -s ${pkgs.alsa-plugins}/lib/alsa-lib/libasound_module_pcm_vdownmix.so $out/lib/alsa-lib
           '';

           buildPhase = ":";
  
           # dummy source for nix build system
           src = pkgs.runCommandNoCC "dummy-src" {} "mkdir $out";
         };
      in
      {
        devShell = pkgs.mkShell {
          venvDir = "./.venv";
          buildInputs = [
            pkgs.python310Packages.python
            pkgs.python310Packages.pip
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
            myAlsaLib
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
            # if [ -z "$IN_NIX_SHELL_ZSH" ]; then
            #  export IN_NIX_SHELL_ZSH=1
            #  echo "Starting Zsh..."
            #  which zsh
            #  ls -l $(which zsh)
            #  exec ${pkgs.zsh}/bin/zsh --login || echo "Failed to start Zsh"
            #fi
            # allow pip to install wheels
            echo "LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib" >> .venv/bin/activate
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib
            unset SOURCE_DATE_EPOCH
          '';
        };
      });
}
