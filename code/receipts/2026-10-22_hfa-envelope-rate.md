# Receipt: Cutoffs n/a for the 100 Hz HFA envelope

**Claim**: every recording stores the authors' HFA envelope at 100 Hz (Nyquist 50 Hz). The 70/150 Hz `low_cutoff`/`high_cutoff` of all 2668 channels.tsv rows describe the carrier band, not filters on the stored signal, so both become n/a. The resampling to 100 Hz does low-pass filter, but its cutoff is not reported, so `high_cutoff` n/a means "not reported".

**PR**: nemarDatasets/nm000356#3; this receipt is on top of head 27a8c0b6.

## Source

- NEMAR nm000356 `origin/main` 88001609c84afb98ad77eefa5efee95b8cbea95a: all 29 `sub-PXX/ieeg/*_ieeg.{vhdr,eeg}` and `*_channels.tsv`. Each `.eeg` sha256 equals its git-annex key and each `.vhdr` equals its git blob (column `vhdr+eeg == main`).
- Upstream: Zenodo record 7876019 (doi:10.5281/zenodo.7876019, revision 3), the 29 `P*_HFA_data.mat` files. Each file's md5 equals the Zenodo API checksum and its sha256 equals `sourcedata/sourcedata_provenance.json` at `origin/main`.
- Rate statements. Zenodo record: "HFA and both auditory spectrograms have a sampling rate of 100 Hz, and are temporally aligned (duration of 190.72 s)." (printed by the script from the API record). Paper (Bellier et al. 2023, PLoS Biol, PMC10427021, Methods "Preprocessing—ECoG data"): "Finally, we removed the 10-second pads, down-sampled data to 100 Hz to match the stimulus spectrogram’s sampling rate". Each source file stores `dataInfo.fs` = 100.
- Resampling path (answers the maintainer's question). Authors' code linked from the Zenodo record, [PF_HFAdecoding@3483b2f](https://github.com/ludovicbellier/PF_HFAdecoding/blob/3483b2ff3e543a6a582034471fc1d7d1254e6376/PF_preprocessingECoG.m): `fsOut = 100` (L26). After the Hilbert envelope, robust scaling, averaging and pad removal it calls `cfg.resamplefs = fsOut; data = ft_resampledata(cfg, data);` with no other options (L257-260). The paper gives the FieldTrip "version from May 11, 2021". `ft_resampledata.m` as of that date ([fieldtrip@55772ea](https://github.com/fieldtrip/fieldtrip/blob/55772ea30172e0509e729188ffd2f544f9582895/ft_resampledata.m), its last change before 2021-05-11) defaults to `cfg.method = 'resample'` (L113-115) and calls MATLAB `resample(...,fsres,fsorig)` (L229/231). Its help text says "the data is filtered prior to resampling to avoid aliassing" (L27). Neither the paper nor the code states that filter's cutoff.
- Low-pass on the raw ECoG (ieeg.json `SoftwareFilters.lowpass`, added with this receipt). The same file, [PF_preprocessingECoG.m@3483b2f](https://github.com/ludovicbellier/PF_HFAdecoding/blob/3483b2ff3e543a6a582034471fc1d7d1254e6376/PF_preprocessingECoG.m) (sha256 `cc72dfae…db8310`), sets `LPcutoff = 250; % low-pass filter cutoff` (L29). It then low-passes in the call that also applies the 60 Hz band-stops and the 1 Hz high-pass, before the HFA sub-band filtering: `cfg.lpfilter = 'yes'; cfg.lpfreq = LPcutoff; data = ft_preprocessing(cfg, data);` (L151-159). The code sets no filter type, order or direction. FieldTrip at its last commit on or before 2021-05-11 ([9bd43ed](https://github.com/fieldtrip/fieldtrip/tree/9bd43ed6310d1db7bda3a1e2c10ec43739c31e87); `ft_resampledata.m` is identical to 55772ea) defaults to `lpfilttype = 'but'` and `lpfiltdir = 'twopass'` (`private/preproc.m` L185, L189) and to order 6 for 'but' (`preproc/ft_preproc_lowpassfilter.m` L152-155). The paper's Methods ("We filtered out power-line noise, using a range of notch filters centered at 60 Hz and harmonics up to 300 Hz (Butterworth, fourth order, 2 Hz bandwidth), and removed slow drifts with a 1-Hz high-pass filter (Butterworth, fourth order).") do not mention it. This filter acts on the raw ECoG upstream of the envelope, so it is not a `high_cutoff` of the stored 100 Hz series.

## Method

- Reader: MNE 1.13.2 `read_raw_brainvision`. The header unit is `n/a`, so MNE applies no scaling; values are compared as float32. scipy 1.18.1 `loadmat` reads the source files.
- Per recording: header sampling rate and sample count; channel count vs channels.tsv rows; the `low_cutoff/high_cutoff` values at `origin/main`; the source's `dataInfo.fs`; and whether float32(`ecog`) equals the stored data sample for sample.

## Result

| subject | header Hz | samples | s | channels | tsv rows | tsv low/high | vhdr+eeg == main | source | md5 == Zenodo | sha256 == provenance | dataInfo.fs | float32(ecog) == stored |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sub-P01 | 100 | 19072 | 190.72 | 64 | 64 | 70/150 | True | P1_HFA_data.mat | True | True | 100 | True |
| sub-P02 | 100 | 19072 | 190.72 | 64 | 64 | 70/150 | True | P2_HFA_data.mat | True | True | 100 | True |
| sub-P03 | 100 | 19072 | 190.72 | 64 | 64 | 70/150 | True | P3_HFA_data.mat | True | True | 100 | True |
| sub-P04 | 100 | 19072 | 190.72 | 99 | 99 | 70/150 | True | P4_HFA_data.mat | True | True | 100 | True |
| sub-P05 | 100 | 19072 | 190.72 | 93 | 93 | 70/150 | True | P5_HFA_data.mat | True | True | 100 | True |
| sub-P06 | 100 | 19072 | 190.72 | 83 | 83 | 70/150 | True | P6_HFA_data.mat | True | True | 100 | True |
| sub-P07 | 100 | 19072 | 190.72 | 101 | 101 | 70/150 | True | P7_HFA_data.mat | True | True | 100 | True |
| sub-P08 | 100 | 19072 | 190.72 | 76 | 76 | 70/150 | True | P8_HFA_data.mat | True | True | 100 | True |
| sub-P09 | 100 | 19072 | 190.72 | 109 | 109 | 70/150 | True | P9_HFA_data.mat | True | True | 100 | True |
| sub-P10 | 100 | 19072 | 190.72 | 97 | 97 | 70/150 | True | P10_HFA_data.mat | True | True | 100 | True |
| sub-P11 | 100 | 19072 | 190.72 | 96 | 96 | 70/150 | True | P11_HFA_data.mat | True | True | 100 | True |
| sub-P12 | 100 | 19072 | 190.72 | 111 | 111 | 70/150 | True | P12_HFA_data.mat | True | True | 100 | True |
| sub-P13 | 100 | 19072 | 190.72 | 94 | 94 | 70/150 | True | P13_HFA_data.mat | True | True | 100 | True |
| sub-P14 | 100 | 19072 | 190.72 | 58 | 58 | 70/150 | True | P14_HFA_data.mat | True | True | 100 | True |
| sub-P15 | 100 | 19072 | 190.72 | 120 | 120 | 70/150 | True | P15_HFA_data.mat | True | True | 100 | True |
| sub-P16 | 100 | 19072 | 190.72 | 60 | 60 | 70/150 | True | P16_HFA_data.mat | True | True | 100 | True |
| sub-P17 | 100 | 19072 | 190.72 | 59 | 59 | 70/150 | True | P17_HFA_data.mat | True | True | 100 | True |
| sub-P18 | 100 | 19072 | 190.72 | 128 | 128 | 70/150 | True | P18_HFA_data.mat | True | True | 100 | True |
| sub-P19 | 100 | 19072 | 190.72 | 98 | 98 | 70/150 | True | P19_HFA_data.mat | True | True | 100 | True |
| sub-P20 | 100 | 19072 | 190.72 | 71 | 71 | 70/150 | True | P20_HFA_data.mat | True | True | 100 | True |
| sub-P21 | 100 | 19072 | 190.72 | 109 | 109 | 70/150 | True | P21_HFA_data.mat | True | True | 100 | True |
| sub-P22 | 100 | 19072 | 190.72 | 134 | 134 | 70/150 | True | P22_HFA_data.mat | True | True | 100 | True |
| sub-P23 | 100 | 19072 | 190.72 | 98 | 98 | 70/150 | True | P23_HFA_data.mat | True | True | 100 | True |
| sub-P24 | 100 | 19072 | 190.72 | 60 | 60 | 70/150 | True | P24_HFA_data.mat | True | True | 100 | True |
| sub-P25 | 100 | 19072 | 190.72 | 76 | 76 | 70/150 | True | P25_HFA_data.mat | True | True | 100 | True |
| sub-P26 | 100 | 19072 | 190.72 | 81 | 81 | 70/150 | True | P26_HFA_data.mat | True | True | 100 | True |
| sub-P27 | 100 | 19072 | 190.72 | 36 | 36 | 70/150 | True | P27_HFA_data.mat | True | True | 100 | True |
| sub-P28 | 100 | 19072 | 190.72 | 79 | 79 | 70/150 | True | P28_HFA_data.mat | True | True | 100 | True |
| sub-P29 | 100 | 19072 | 190.72 | 250 | 250 | 70/150 | True | P29_HFA_data.mat | True | True | 100 | True |

29 recordings, 2668 channels.tsv rows; header rate 100 Hz (Nyquist 50 Hz); source dataInfo.fs 100. 150 Hz and 70 Hz both lie above the 50 Hz Nyquist of the stored 100 Hz series, so neither can be a filter on it. These 2668 rows are the ones this PR sets to n/a.

## Coverage

29 of 29 recordings (2668 of 2668 channels.tsv rows), all 29 source HFA files.

## Reproduce

```
uv run --no-project --with mne==1.13.2 --with scipy --with pandas python code/receipts/2026-10-22_hfa-envelope-rate.py <nm000356 root> <nm000356 git clone> <zenodo dir>
```

Run on 2026-10-22 as Slurm job 13448953. The root was `/checkpoint/brainai2/shared/studies/Bellier2023Music/download/nm000356` (NEMAR download), plus a git clone of nemarDatasets/nm000356 (`origin/main` above) and a directory holding the 29 Zenodo `P*_HFA_data.mat` files and `https://zenodo.org/api/records/7876019` saved as `zenodo_7876019_record.json`.
