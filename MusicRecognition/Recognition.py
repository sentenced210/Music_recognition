import essentia
import essentia.standard as es
import essentia.streaming as ess


def bpm_detection(file_name):
    loader = es.MonoLoader(filename=file_name)()

    bpm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm = bpm_extractor(loader)[0]

    print("BPM: = " + str(int(round(bpm))))

    return bpm


def time_signature_detection(file_name):
    loader = es.MonoLoader(filename=file_name)()

    beat_tracker = es.BeatTrackerDegara()
    ticks = beat_tracker(loader)

    beats_loudness = es.BeatsLoudness(beats=ticks)
    loudness, loudness_band_ratio = beats_loudness(loader)

    beatogram_detector = es.Beatogram()
    beatogram = beatogram_detector(loudness, loudness_band_ratio)

    meter = es.Meter()
    time_signature = meter(beatogram)

    print("Time signature:" + str(time_signature))

    return time_signature


def duration_detection(file_name):
    loader = es.MonoLoader(filename=file_name)()

    duration_detector = es.Duration()
    duration = duration_detector(loader)
    print("Duration: " + str(duration))

    return duration


def key_and_scale_detection(file_name):
    loader = ess.MonoLoader(filename=file_name)

    frame_cutter = ess.FrameCutter()

    windowing = ess.Windowing()

    spectrum = ess.Spectrum()

    spectral_peaks_detector = ess.SpectralPeaks()

    hpcp = ess.HPCP()

    key = ess.Key(usePolyphony=False, useThreeChords=False)

    pool = essentia.Pool()

    loader.audio >> frame_cutter.signal
    frame_cutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectral_peaks_detector.spectrum
    spectral_peaks_detector.magnitudes >> hpcp.magnitudes
    spectral_peaks_detector.frequencies >> hpcp.frequencies
    hpcp.hpcp >> key.pcp
    key.key >> (pool, 'tonal.key_key')
    key.scale >> (pool, 'tonal.key_scale')
    key.strength >> (pool, 'tonal.key_strength')

    essentia.run(loader)

    print(str(pool['tonal.key_key']) + " " + str(pool['tonal.key_scale']))

    return pool['tonal.key_key'], pool['tonal.key_scale']
