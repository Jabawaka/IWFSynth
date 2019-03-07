#ifndef H_MODULES_SKELETON_CARRIER_H
#define H_MODULES_SKELETON_CARRIER_H


#include <vector>

#include "Modules/Skeleton/Operator.hpp"
#include "Modules/Skeleton/Note.hpp"


// Carrier:
// This class represents a Carrier wave, which can be modulated by other
// operators.
class Carrier : Operator
{
    public:
        void calc();

    private:
        // Input notes:
        // This is the array of notes input to the operator that should be
        // played at the current instant.
        std::vector<Note> _notes;

        // Frequency ratio:
        // Ratio between the output frequency of the operator and the input
        // frequency in the note.
        float _freqRatio;
};

#endif // H_MODULES_SKELETON_CARRIER_H
