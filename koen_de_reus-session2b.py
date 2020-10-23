import os
import csv
from pydub import AudioSegment, silence, effects

# We have three conditions: High Frequency (HF), Low Frequency (LF), and Non-Words (NW).
# All words for each condition are stored in one .wav file.
# Your task is to:
#       split the words on the silence
#       make sure they all have the same loudness
#       save them in a folder corresponding to their condition (folder names: HF, LF, NW)

path_to_directory = "/Users/koendereus/Desktop/session2b-sound"  # add your own path here!

# This piece of code is here to help you.
# It reads a text file with information about the stimuli you are going to split (names & condition),
# and returns a dictionary named 'stimuli' with condition as key, and the word itself as value.
# Use this dictionary to name the files you have to save.
stimuli_info = open(os.path.join(path_to_directory, "lexdec_stimuli.txt"))
stimuli_reader = csv.reader(stimuli_info, delimiter=',')
headers = next(stimuli_reader, None)

# Create the dictionary
stimuli = {}
for stimulus in stimuli_reader:
    if stimulus[2] not in stimuli.keys():
        stimuli[stimulus[2]] = list()
    stimuli[stimulus[2]].append(stimulus[3])

# Put them in alphabetical order
for condition, words in stimuli.items():
    sort = sorted(words)
    stimuli[condition] = sort

# change the non-word condition name
stimuli["NW"] = stimuli.pop("none")

# Now you have the stimulus names. Let's take a look at the dictionary:
print(stimuli)

# YOUR CODE HERE.
recording_folder = "/Users/koendereus/Desktop/session2b-sound/raw"
conditions = ["HF", "LF", "NW"]

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

for condition in conditions:
    condition_folder = "/Users/koendereus/Desktop/session2b-sound/" + condition
    if not os.path.isdir(condition_folder):
        os.mkdir(condition_folder)

    recording_name = condition + '_recording.wav'
    recording_path = os.path.join(recording_folder, recording_name)
    recording_load = AudioSegment.from_wav(recording_path)

    word_list = silence.split_on_silence(recording_load, min_silence_len=200, silence_thresh=-50)

    for i in range(len(word_list)):
         word_normalised = match_target_amplitude(word_list[i], -6)
         word_normalised.export(os.path.join(condition_folder,(stimuli[condition][i]) + ".wav"))

# Some hints:
# 1. Where are the stimuli?
# 2. How loud do you want your stimuli to be? Store it in a variable
# 3. Where do you want to save your files? Make separate folders for the conditions.
# 4. Do you normalize the volume for the whole sequence or for separate words? Why (not)? Try it if you like :)
# 5. You can check whether your splitting worked by playing the sound, or by printing the length of the resulting list
# 6. Use the index of the word [in the list of words you get after splitting]
# to get the right text from the dictionary.
# 7. Recall you can plot your results to see what you have done.
# Good luck!