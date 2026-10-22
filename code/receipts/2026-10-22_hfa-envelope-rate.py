"""Sampling rate of the stored HFA in nm000356 vs the 70/150 Hz channels.tsv cut-offs.

Usage: python 2026-10-22_hfa-envelope-rate.py <nm000356 root> <nm000356 git clone> <zenodo dir>

<nm000356 root> holds the BIDS files read, <nm000356 git clone> gives origin/main (sidecars,
git-annex keys), <zenodo dir> holds Zenodo 7876019's P*_HFA_data.mat files and its API record
as zenodo_7876019_record.json.
"""

import hashlib
import html
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import mne
import numpy as np
import pandas as pd
import scipy.io

REF = "origin/main"


def digest(path: Path, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        while chunk := f.read(1 << 24):
            h.update(chunk)
    return h.hexdigest()


def git(clone: Path, *args: str) -> bytes:
    out = subprocess.run(["git", "-C", clone, *args], capture_output=True)
    assert out.returncode == 0, out.stderr.decode()
    return out.stdout


def same_as_main(root: Path, clone: Path, rel: Path) -> bool:
    """File equals origin/main: sha256 = git-annex key, or bytes = git blob."""
    blob = git(clone, "show", f"{REF}:{rel}")
    if blob.startswith(b"/annex/objects/SHA256E-"):
        return blob.decode().split("--")[1].split(".")[0] == digest(root / rel)
    return blob == (root / rel).read_bytes()


def markdown(table: pd.DataFrame) -> str:
    lines = ["| " + " | ".join(table.columns) + " |", "|---" * table.shape[1] + "|"]
    for row in table.itertuples(index=False):
        cells = (f"{v:g}" if isinstance(v, float) else str(v) for v in row)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main(root: Path, clone: Path, zenodo: Path) -> None:
    print(f"mne {mne.__version__}, numpy {np.__version__}, scipy {scipy.__version__}")
    print(f"{REF} of the clone: {git(clone, 'rev-parse', REF).decode().strip()}")
    record = json.loads((zenodo / "zenodo_7876019_record.json").read_text())
    md5 = {f["key"]: f["checksum"].removeprefix("md5:") for f in record["files"]}
    text = html.unescape(re.sub(r"<[^>]+>", " ", record["metadata"]["description"]))
    sentences = re.split(r"(?<=\.)\s+(?=[A-Z])", " ".join(text.split()))
    rate = next(s for s in sentences if "sampling rate" in s)
    print(f"Zenodo {record['doi']} (revision {record['revision']}): {rate}")
    prov = git(clone, "show", f"{REF}:sourcedata/sourcedata_provenance.json")
    sha = {c["file"]: c["sha256"] for c in json.loads(prov)["copied"]}

    rows = []
    for vhdr in sorted(root.glob("sub-*/ieeg/*_ieeg.vhdr")):
        rel = vhdr.relative_to(root)
        tsv_rel = str(rel).replace("_ieeg.vhdr", "_channels.tsv")
        channels = pd.read_csv(
            io.BytesIO(git(clone, "show", f"{REF}:{tsv_rel}")), sep="\t", dtype=str
        )
        cutoffs = channels.low_cutoff + "/" + channels.high_cutoff
        raw = mne.io.read_raw_brainvision(vhdr, preload=True, verbose="error")
        mat = zenodo / f"P{int(rel.parts[0].removeprefix('sub-P'))}_HFA_data.mat"
        src = scipy.io.loadmat(mat, squeeze_me=True, struct_as_record=False)
        stored = np.float32(raw.get_data())
        rows.append(
            {
                "subject": rel.parts[0],
                "header Hz": raw.info["sfreq"],
                "samples": raw.n_times,
                "s": raw.n_times / raw.info["sfreq"],
                "channels": len(raw.ch_names),
                "tsv rows": len(channels),
                "tsv low/high": "; ".join(sorted(cutoffs.unique())),
                "vhdr+eeg == main": all(
                    same_as_main(root, clone, rel.with_suffix(s))
                    for s in (".vhdr", ".eeg")
                ),
                "source": mat.name,
                "md5 == Zenodo": digest(mat, "md5") == md5[mat.name],
                "sha256 == provenance": digest(mat) == sha[mat.name],
                "dataInfo.fs": src["dataInfo"].fs,
                "float32(ecog) == stored": np.array_equal(
                    np.float32(src["ecog"].T), stored
                ),
            }
        )
    table = pd.DataFrame(rows)
    print("\n" + markdown(table))
    rates = "/".join(f"{v:g}" for v in sorted(table["header Hz"].unique()))
    src_rates = "/".join(f"{v:g}" for v in sorted(table["dataInfo.fs"].unique()))
    print(
        f"\n{len(table)} recordings, {table['tsv rows'].sum()} channels.tsv rows; header "
        f"rate {rates} Hz (Nyquist {float(rates) / 2:g} Hz); source dataInfo.fs {src_rates}"
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
