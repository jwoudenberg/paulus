{
  description = "paulus";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in rec {
        packages.paulus = pkgs.writers.writePython3Bin "paulus" { }
          (builtins.readFile ./main.py);

        defaultPackage = packages.paulus;

        devShell = pkgs.mkShell {
          buildInputs = [ pkgs.python39 pkgs.python39Packages.flake8 ];
        };
      });
}
