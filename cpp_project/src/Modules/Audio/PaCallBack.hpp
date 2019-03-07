#ifndef H_MODULES_AUDIO_PACALLBACK_H
#define H_MODULES_AUDIO_PACALLBACK_H


#include <portaudio.h>
#include "Modules/Audio/AudioSystem.hpp"

struct PaAudioData
{
    AudioSystem *p_system;
};

PaAudioData audioData;

int paCallback
   (const void                      *inputBuffer,
    void                            *outputBuffer,
    unsigned long                    framesPerBuffer,
    const PaStreamCallbackTimeInfo  *timeInfo,
    PaStreamCallbackFlags            statusFlags,
    void                            *p_userData);


#endif // H_MODULES_AUDIO_PACALLBACK_H
