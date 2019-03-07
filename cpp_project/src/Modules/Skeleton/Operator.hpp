#ifndef H_MODULES_SKELETON_OPERATOR_H
#define H_MODULES_SKELETON_OPERATOR_H

#include <vector>

// Operator:
// This parent class defines the interface and common variables for each block
// that gets instantiated in the synth.
class Operator
{
    public:
        // Calculate current output:
        // This method calculates the output at the current instant.
        virtual void calc() = 0;

        // Get current outputs:
        // This method returns the current output samples, to be able to push
        // them to the blocks downstream.
        std::vector<float> getOuts()
        {
            return _outSamples;
        }

        // Set current inputs:
        // This method sets the input array to the provided one.
        void setIns(std::vector<float> inSamples)
        {
            _inSamples = inSamples;
        }

    protected:
        // Input samples:
        // Each operator can have one or more audio sample inputs, each of them
        // an entrance in this array. This vector should be populated at each
        // instant with the outputs from the previous blocks in the chain.
        std::vector<float> _inSamples;

        // Output samples:
        // Each operator has one or more audio sample outputs, each of them an
        // entrance in this array. This vector should be populated by the
        // object each instant.
        std::vector<float> _outSamples;

};

#endif // H_MODULES_SKELETON_OPERATOR_H
