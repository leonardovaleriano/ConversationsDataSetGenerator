import pickle
import random
from scikits import audiolab as audlib
import numpy as np

audio_dataset = pickle.load(open('AudioDataSet.pickle', 'rb'))

amount_of_speakers = [2, 3, 5, 7, 10]

# Defines how many speaker change points will exist, 'fast' means many small speaker segments, leading to many speaker \
# changes, while 'slow' means big speaker segments, more homogeneous speech, leading to few speaker changes. The pair \
# describes the interval of duration in seconds, according to the classification of frequency.
speaker_turn_frequencies = [{'fast': (0.8, 5)}, {'moderate': (5, 12)}, {'slow': (10, 60*30)}]

# Approximated durations (in seconds) of the conversations.
conversations_duration = [3*60, 5*60, 10*60, 20*60]

# Listing speakers
speaker_ids = []
for key, value in audio_dataset.iteritems():
    speaker_ids.append(key)

# Preparing Conversations Data Set
chosen_speaker_ids = []
conversation_id = 0
for amount in amount_of_speakers:
    chosen_speaker_ids = random.sample(speaker_ids, min(amount, speaker_ids.__len__()))

    for duration in conversations_duration:
        for freq in speaker_turn_frequencies:
            interval = freq.values()[0]

            # Listing speakers utterances
            utterances_ids = {}
            for speaker_id in chosen_speaker_ids:
                speaker_samples = audio_dataset[speaker_id].get('speaker_dataset')
                for key, dict_value in speaker_samples.iteritems():
                    if interval[0] <= dict_value['length(secs)'] <= interval[1]:
                        utterances_ids[speaker_id] = utterances_ids[speaker_id] + [key] \
                            if utterances_ids.has_key(speaker_id) else [key]

            print 'Amount: {amount} speakers; Relative Duration: {duration}; Conversation Style: {style}'.format(
                amount=amount, duration=duration, style=freq.keys()[0])

            # Generating conversation
            current_size = 0
            fs = None
            current_data = np.array([])
            change_points = []
            while current_size < duration:
                for speaker_id, speaker_utt_ids in utterances_ids.iteritems():
                    chosen_utt = random.choice(speaker_utt_ids)
                    speaker_samples = audio_dataset[speaker_id].get('speaker_dataset')
                    current_data = np.concatenate((current_data, speaker_samples[chosen_utt].get('raw_data')), axis=0)
                    current_size += speaker_samples[chosen_utt].get('length(secs)')
                    change_points.append(len(current_data))
                    fs = speaker_samples[chosen_utt].get('sample_rate')

            if len(change_points):
                change_points.pop()

            if len(change_points) > 1:
                conversations_dataset = {'id': conversation_id, 'speakers_utterances': utterances_ids,
                                         'speakers_turns': change_points, 'audio_data': current_data,
                                         'length(secs)': current_size, 'sample_rate': fs, 'amount_speakers': amount,
                                         'conversation_style': freq.keys()[0]}
                audlib.wavwrite(np.array(current_data), '{0}.wav'.format(conversation_id), fs)
                conversation_id += 1

                with open('ConversationDataSet.pickle', 'ab') as f:
                    pickle.dump(conversations_dataset, f, -1)
