#ifndef H_MODULES_SKELETON_NOTE_H
#define H_MODULES_SKELETON_NOTE_H



// Note:
// This structure represents a note, defined by its frequency and the time at
// which the note starts.
struct Note
{
    // Frequency:
    // Frequency in Hz of the note.
    float freq_Hz;

    // Actuation time:
    // Time at which the note starts, used to apply envelopes and other time
    // dependant effects.
    float actTime_s;
};

#endif // H_MODULES_SKELETON_NOTE_H
