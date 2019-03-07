#include <iostream>
#include <portaudio.h>

#include "Modules/Audio/AudioSystem.hpp"
#include "Modules/Audio/PaCallBack.hpp"


AudioSystem::AudioSystem()
{
    int error = Pa_Initialize();
    if(error != paNoError)
    {
        std::cout << "Could not initalise PortAudio library" << std::endl;
    }

    error = Pa_OpenDefaultStream
       (&_p_stream,
        0, 2, paFloat32,
        44100, paFramesPerBufferUnspecified,
        paCallback,
        &audioData);

    if(error != paNoError)
    {
        std::cout << "Could not open PortAudio Stream" << std::endl;
    }
}

AudioSystem::~AudioSystem()
{
    int error;

    error = Pa_CloseStream(_p_stream);
    if(error != paNoError)
    {
        std::cout << "Could not close the PortAudio Stream" << std::endl;
    }

    error = Pa_Terminate();
    if(error != paNoError)
    {
        std::cout << "Could not terminate PortAudio library" << std::endl;
    }
}
