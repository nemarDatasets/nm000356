# Bellier et al. 2023: ECoG high-frequency activity while listening to a Pink Floyd song (29 patients)

**These are not raw recordings.** This dataset is a BIDS packaging of the *preprocessed* neural data released with
Bellier et al. (2023), "Music can be reconstructed from human auditory cortex activity using nonlinear decoding models",
PLoS Biology 21(8): e3002176. For each of 29 patients the release holds the authors' high-frequency activity (HFA,
70-150 Hz) estimate at 100 Hz, aligned to the 190.72 s song, plus the electrode coordinates in MNI space. The raw ECoG
was not released. `dataset_description.json` therefore declares `DatasetType: derivative`, with `GeneratedBy` and
`SourceDatasets` pointing at the authors' Zenodo record (doi:10.5281/zenodo.7876019, CC-BY-4.0).

## Participants, recording and task (from the paper)

- 29 patients with pharmacoresistant epilepsy (15 female, age 16-60), with clinical ECoG grids or strips (Ad-Tech)
  covering at least part of the superior temporal gyrus. Recorded at Albany Medical Center at 1200 Hz with g.USBamp
  and BCI2000. Approved by Albany Medical College IRB #2061 and UC Berkeley CPHS #2010-01-520; written informed
  consent. Per-patient age and sex are not in the release. `participants.tsv` gives the implantation laterality
  stored by the authors.
- Task: passive listening to *Another Brick in the Wall, Part 1* (Pink Floyd, *The Wall*, 1979). The song was
  delivered through in-ear headphones at 50-60 dB SL.

## How the HFA was computed (authors, Methods "Preprocessing - ECoG data")

The authors first notch-filtered 60 Hz and its harmonics up to 300 Hz, then high-pass filtered at 1 Hz. They
band-passed the signal into 20-Hz sub-bands from 70-90 to 130-150 Hz in 5-Hz steps and applied a median-based common
average reference to each sub-band. For some patients the reference was computed per splitter box. They took the
Hilbert envelope of each sub-band and robust-scaled it (median removed, divided by the 10th-90th percentile range).
The sub-bands were then averaged, the 10-s pads removed, and the result downsampled to 100 Hz. Samples above 7 SD were
tagged as outliers. **The HFA values are dimensionless**, so `units` is `n/a`.

## Files

- `sub-PXX/ieeg/sub-PXX_task-musiclistening_ieeg.vhdr/.vmrk/.eeg`: BrainVision, IEEE float32, 100 Hz, 19072 samples.
  Each file has one channel per electrode, with the authors' labels "1".."n". Time 0 is song onset.
- `..._channels.tsv`: electrodes the authors flagged as noisy or epileptic (`dataInfo.idxNoisyElecs`,
  `idxEpilepticElecs`) are marked `status = bad`. The paper excluded these from its analyses; their HFA is kept as
  released. `author_reference_electrode` marks `dataInfo.idxRefElec`. Column *i* of the authors' `ecog` matrix is
  matched to the *i*-th label of the coordinate file; the counts agree for all 29 patients (2668 electrodes in
  total, as in the paper). The stored flags mark 98 noisy and 151 epileptic electrodes. The paper reports removing
  106 noisy and 183 epileptic electrodes. The flags are transcribed as stored, without reconciling the counts.
- `..._events.tsv`: one `song` row (onset 0, duration 190.72 s). It also has one `outlier_samples` row per run of
  consecutive samples that the authors' `artifacts` matrix marks for a channel. These rows reconstruct that matrix
  exactly.
- `sub-PXX_space-Other_electrodes.tsv` + `_coordsystem.json`: the authors' MNI coordinates in mm and their anatomical
  labels. The BIDS coordinate system is `Other` because the release does not say which MNI template variant was used.
  The P2 coordinate structure has no `unit` field. Like all the others, it is taken as mm (its value range matches).
- `sourcedata/zenodo-7876019/`: the authors' 58 HFA and coordinate `.mat` files, byte-identical, with SHA-256 in
  `sourcedata/sourcedata_provenance.json`.

## Precision

The source stores float64 and BrainVision float32. The relative rounding error is below 1e-7; the maximum per subject
is in the conversion report. For bit-exact values, use the `.mat` files in `sourcedata/`.

## Stimulus: not included

The Zenodo record also contains `thewall1.wav` (the song) and its 32- and 128-bin auditory spectrograms
(`thewall1_stim32.mat`, `thewall1_stim128.mat`). The record's CC-BY-4.0 licence does not establish a right to
redistribute a commercial recording, so these three files are **not** part of this package. To reproduce the
stimulus-based analyses, download them from https://zenodo.org/records/7876019. Alternatively, use a commercial copy of
the song and compute the auditory spectrogram with the NSL toolbox as described in the paper, using the authors' code
at https://github.com/ludovicbellier/PF_HFAdecoding. The spectrograms are sampled at 100 Hz and have the same 19072
samples as the HFA.

## Licence and citation

CC-BY-4.0 (Zenodo record licence). Please cite Bellier et al. (2023), doi:10.1371/journal.pbio.3002176, and the data
record doi:10.5281/zenodo.7876019.
