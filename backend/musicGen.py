import numpy as np
import pandas as pd

from music21 import note, stream, tempo, converter, instrument, chord
from pathlib import Path

songs = []
dir = Path("model/music")

for file in dir.rglob('*.mid'):
    songs.append(file)

def training():

    print(songs)

    notes = []
    for i,file in enumerate(songs):
        print(f'{i+1}: {file}')
        try:
            midi = converter.parse(file)
            notes_to_parse = None
            parts = instrument.partitionByInstrument(midi)
            if parts: # file has instrument parts
                notes_to_parse = parts.parts[0].recurse()
            else: # file has notes in a flat structure
                notes_to_parse = midi.flat.notes
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
        except:
            print(f'FAILED: {i+1}: {file}')

    return notes

def prepare_sequences(notes, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 32

    # Get all unique pitchnames
    pitchnames = sorted(set(item for item in notes))
    numPitches = len(pitchnames)

     # Create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        # sequence_in is a sequence_length list containing sequence_length notes
        sequence_in = notes[i:i + sequence_length]
        # sequence_out is the sequence_length + 1 note that comes after all the notes in
        # sequence_in. This is so the model can read sequence_length notes before predicting
        # the next one.
        sequence_out = notes[i + sequence_length]
        # network_input is the same as sequence_in but it containes the indexes from the notes
        # because the model is only fed the indexes.
        network_input.append([note_to_int[char] for char in sequence_in])
        # network_output containes the index of the sequence_out
        network_output.append(note_to_int[sequence_out])

    # n_patters is the length of the times it was iterated 
    # for example if i = 3, then n_patterns = 3
    # because network_input is a list of lists
    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    # Reshapes it into a n_patterns by sequence_length matrix
    print(len(network_input))
    
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    network_input = network_input / float(n_vocab)

    # OneHot encodes the network_output
    network_output = np.np_utils.to_categorical(network_output)

    return (network_input, network_output)

def oversample(network_input,network_output,sequence_length=15):

  n_patterns = len(network_input)
  # Create a DataFrame from the two matrices
  new_df = pd.concat([pd.DataFrame(network_input),pd.DataFrame(network_output)],axis=1)

  # Rename the columns to numbers and Notes
  new_df.columns = [x for x in range(sequence_length+1)]
  new_df = new_df.rename(columns={sequence_length:'Notes'})

  print(new_df.tail(20))
  print('###################################################')
  print(f'Distribution of notes in the preoversampled DataFrame: {new_df["Notes"].value_counts()}')
  # Oversampling
  oversampled_df = new_df.copy()
  #max_class_size = np.max(oversampled_df['Notes'].value_counts())
  max_class_size = 700
  print('Size of biggest class: ', max_class_size)

  class_subsets = [oversampled_df.query('Notes == ' + str(i)) for i in range(len(new_df["Notes"].unique()))] # range(2) because it is a binary class

  for i in range(len(new_df['Notes'].unique())):
    try:
      class_subsets[i] = class_subsets[i].sample(max_class_size,random_state=42,replace=True)
    except:
      print(i)

  oversampled_df = pd.concat(class_subsets,axis=0).sample(frac=1.0,random_state=42).reset_index(drop=True)

  print('###################################################')
  print(f'Distribution of notes in the oversampled DataFrame: {oversampled_df["Notes"].value_counts()}')

  # Get a sample from the oversampled DataFrame (because it may be too big, and we also have to convert it into a 3D array for the LSTM)
  sampled_df = oversampled_df.sample(n_patterns,replace=True) # 99968*32 has to be equals to (99968,32,1)

  print('###################################################')
  print(f'Distribution of notes in the oversampled post-sampled DataFrame: {sampled_df["Notes"].value_counts()}')

  # Convert the training columns back to a 3D array
  network_in = sampled_df[[x for x in range(sequence_length)]]
  network_in = np.array(network_in)
  network_in = np.reshape(networkInput, (n_patterns, sequence_length, 1))
  network_in = network_in / numPitches
  print(network_in.shape)
  print(sampled_df['Notes'].shape)
  # Converts the target column into a OneHot encoded matrix
  network_out = pd.get_dummies(sampled_df['Notes'])
  print(network_out.shape)

  return network_in,network_out

def generate_notes(model, network_input, pitchnames, n_vocab):
    """ Generate notes from the neural network based on a sequence of notes """
    # pick a random sequence from the input as a starting point for the prediction
    # Selects a random row from the network_input
    start = np.random.randint(0, len(network_input)-1)
    print(f'start: {start}')
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    # Random row from network_input
    pattern = network_input[start]
    prediction_output = []

    # generate 500 notes
    for note_index in range(500):
        # Reshapes pattern into a vector
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        # Standarizes pattern
        prediction_input = prediction_input / float(n_vocab)

        # Predicts the next note
        prediction = model.predict(prediction_input, verbose=0)

        # Outputs a OneHot encoded vector, so this picks the columns
        # with the highest probability
        index = np.argmax(prediction)
        # Maps the note to its respective index
        result = int_to_note[index]
        # Appends the note to the prediction_output
        prediction_output.append(result)

        # Adds the predicted note to the pattern
        pattern = np.append(pattern,index)
        # Slices the array so that it contains the predicted note
        # eliminating the first from the array, so the model can
        # have a sequence
        pattern = pattern[1:len(pattern)]

    return prediction_output

def genMelody(memory_description):
    melody = stream.Score()

    melody.append(tempo.MetronomeMark(number=120))

    part = stream.Part()

    noteSequence = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]

    notes = [note.Note(n) for n in noteSequence]

    for n in notes:
        part.append(n)

    melody.append(part)

    return melody

if __name__ == "__main__":
    notes = training()

    n_vocab = len(set(notes))
    networkInput, networkOutput = prepare_sequences(notes,n_vocab)
    n_patterns = len(networkInput)
    pitchnames = sorted(set(item for item in notes))
    numPitches = len(pitchnames)
    networkInputShaped,networkOutputShaped = oversample(networkInput,networkOutput,sequence_length=32)
    networkOutputShaped = np.np_utils.to_categorical(networkOutput)
    n_vocab = len(set(notes))
    pitchnames = sorted(set(item for item in notes))
    prediction_output = generate_notes(networkOutputShaped, networkInputShaped, pitchnames, n_vocab)

