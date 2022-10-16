{
  description = "A web app to upload files to an SFTP server";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {self, nixpkgs, flake-utils }@inp:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in rec {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.python310
            pkgs.python310Packages.paramiko
            pkgs.python310Packages.fastapi
            pkgs.python310Packages.uvicorn
            pkgs.python310Packages.python-multipart
          ];

          shellHook = ''
          '';
        };
      }
  );
}
