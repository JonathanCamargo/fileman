# fileman

Lightweight file management utilities used across personal automation projects.

Provides:

- `FileManager` — class for enumerating files in a structured directory hierarchy (folder levels), filtering by extension/scope, and modifying file lists.
- `mkdirfile(path)` — make the parent directory of a file path (or the path itself if no extension), `exist_ok=True`.
- Path helpers — `downloadspath()`, `dropboxpath()`, `temppath()`, `keyspath()`, `loadKeys()`, `fileparts()`.

## Install

From a local checkout (editable):

```
pip install -e path/to/fileman
```

From git:

```
pip install git+https://github.com/JonathanCamargo/fileman.git
```

## Usage

```python
from fileman import FileManager, mkdirfile
from fileman.paths import loadKeys, downloadspath

fm = FileManager(Root="/data", PathStructure=["Date", "Trial"], Ext="csv")
files = fm.fileList()

mkdirfile("/tmp/new/folder/output.txt")  # ensures /tmp/new/folder exists

keys = loadKeys()  # reads keys.json from your Dropbox
```

## License

MIT — see [LICENSE](LICENSE).
