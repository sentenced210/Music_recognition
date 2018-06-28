import essentia
import essentia.standard as es
import essentia.streaming as ess


def bpm_detection(file_name):
    loader = es.MonoLoader(filename=file_name)()

    bpm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm = bpm_extractor(loader)[0]
    # a = bpm_extractor(loader)[1]
    # print(len(a))
    # for i in range(len(a)):
    #     print(a[i])
    return int(bpm)


def duration_detection(file_name):
    loader = es.MonoLoader(filename=file_name)()

    duration_detector = es.Duration()
    duration = duration_detector(loader)

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

    # print(str(pool['tonal.key_key']) + " " + str(pool['tonal.key_scale']))

    return pool['tonal.key_key'], pool['tonal.key_scale']


def bar_numbers(numerator, duration, bpm):
    return int(((duration/60)*bpm)/numerator)

