import scipy.io.wavfile as wav
import numpy as np
import os
import pickle

# Script params
path = '/home/leonardo/Desktop/Researches/Audio DataSet/'
file_format = '.wav'

# Recovered data
count_errors = 0
count_good_files = 0
count_speakers = 0
array_length = []
audio_dataset = {}

for root, dirs, files in os.walk(path + "Speech and Speaker Datasets"):
    count_errors_by_speaker = 0
    count_good_files_by_speaker = 0
    speaker_samples = {}
    speaker_array_length = []
    print root
    for f in files:
        if f.endswith(file_format) or f.endswith(file_format.upper()):
            filename = os.path.join(root, f)
            try:
                fs, data = wav.read(filename)
                length_secs = len(data)/fs

                array_length.append(length_secs)
                speaker_array_length.append(length_secs)

                speaker_samples[count_good_files+count_errors] = {'raw_data': data, 'sample_rate': fs,
                                                                  'length(secs)': length_secs}

                print filename
                print 'Sample rate: {0}'.format(fs)
                print 'Seconds: {0} s'.format(length_secs)

                count_good_files += 1
                count_good_files_by_speaker += 1
            except ValueError:
                print '***************** ERROR **********************'
                print 'This file contains data in an unknown format: {0}'.format(filename)

                count_errors += 1
                count_errors_by_speaker += 1

    if count_good_files_by_speaker:
        speaker_array_length = np.array(speaker_array_length)
        audio_dataset[count_speakers] = {'speaker_dataset': speaker_samples,
                                         'count_bad_files': count_errors_by_speaker,
                                         'count_good_files': count_good_files_by_speaker, 'mean_length(secs)':
                                             speaker_array_length.mean(), 'standard_dev_length(secs)':
                                             speaker_array_length.std()}
        count_speakers += 1

print '\nScan of audio files finished.'
print '{folders} folders (speakers) found.\n{bad_files} files unable (bad formatted).\n' \
      '{good_files} audio files (good formatted) present.'.format(bad_files=count_errors, good_files=count_good_files,
                                                                  folders=count_speakers)
array_length = np.array(array_length)
print 'Mean length of files (seconds): {0:.2f} seconds.'.format(array_length.mean())
print 'Standard deviation length (seconds): {0:.2f} seconds.'.format(array_length.std())

print 'Storing audio dataset in \'AudioDataSet\' pickle object...'

with open('AudioDataSet.pickle', 'w') as f:
    pickle.dump(audio_dataset, f, -1)

print 'Finished!'
