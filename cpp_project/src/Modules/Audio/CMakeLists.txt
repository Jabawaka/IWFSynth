add_library(Audio
    AudioSystem.cpp
    PaCallBack.cpp)

target_link_libraries(Audio
    portaudio)
