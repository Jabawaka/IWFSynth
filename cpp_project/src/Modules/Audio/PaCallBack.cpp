#include <portaudio.h>

#include "Modules/Audio/PaCallBack.hpp"


int paCallBack
   (const void                      *inputBuffer,
    void                            *outputBuffer,
    unsigned long                    framesPerBuffer,
    const PaStreamCallbackTimeInfo  *timeInfo,
    PaStreamCallbackFlags            statusFlags,
    void                            *p_userData)
{
    return 0;
}
