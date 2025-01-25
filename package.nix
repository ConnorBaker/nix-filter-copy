{
  aiodns,
  aiohttp,
  buildPythonPackage,
  flit-core,
  lib,
  pyright,
  ruff,
}:
let
  inherit (lib.fileset) toSource unions;
  inherit (lib.strings) makeBinPath;
  inherit (lib.trivial) importTOML;
  pyprojectAttrs = importTOML ./pyproject.toml;
  finalAttrs = {
    pname = pyprojectAttrs.project.name;
    inherit (pyprojectAttrs.project) version;
    pyproject = true;
    src = toSource {
      root = ./.;
      fileset = unions [
        ./pyproject.toml
        ./nix_filter_copy
      ];
    };
    build-system = [ flit-core ];
    dependencies = [
      aiodns
      aiohttp
    ];
    pythonImportsCheck = [ finalAttrs.pname ];
    nativeCheckInputs = [ pyright ];
    passthru.optional-dependencies.dev = [
      pyright
      ruff
    ];
    doCheck = true;
    checkPhase =
      # preCheck
      ''
        runHook preCheck
      ''
      # Check with pyright
      + ''
        echo "Typechecking with pyright"
        pyright --warnings
      ''
      # postCheck
      + ''
        runHook postCheck
      '';
    meta = with lib; {
      inherit (pyprojectAttrs.project) description;
      homepage = pyprojectAttrs.project.urls.Homepage;
      maintainers = with maintainers; [ connorbaker ];
      mainProgram = "nix-filter-copy";
    };
  };
in
buildPythonPackage finalAttrs
