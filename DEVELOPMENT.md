# Development

Python node implementations live under `nodes/<domain>/`. Frontend extensions live in the mirrored `web/js/<domain>/` folders. The root `__init__.py` only registers stable ComfyUI node IDs, display names, and `WEB_DIRECTORY`.

## Publishing

Maintainers can publish a new registry version from a clean checkout:

```sh
./publish
./publish minor
./publish major
```

`./publish` defaults to a patch bump, commits the new `pyproject.toml` version, then runs `python -m comfy node publish`.
