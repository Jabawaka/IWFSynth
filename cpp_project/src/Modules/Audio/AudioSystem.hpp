#ifndef H_MODULES_AUDIO_AUDIOSYSTEM_H
#define H_MODULES_AUDIO_AUDIOSYSTEM_H


#include <portaudio.h>


// AudioSystem:
// This class represents the audio system, in charge of initialising PortAudio,
// holding its callback function and handling everything related to timing.
class AudioSystem
{
    public:
        // Constructor:
        // Initialises PortAudio.
        AudioSystem();

        // Destructor:
        // Shuts down PortAudio.
        ~AudioSystem();

    private:
        // Stream:
        // Main audio stream, used to output sound directly.
        PaStream *_p_stream;

};

#endif // H_MODULES_AUDIO_AUDIOSYSTEM_H
