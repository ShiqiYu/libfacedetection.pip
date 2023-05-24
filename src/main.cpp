#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "facedetectcnn.h"
#include <iostream>
namespace py = pybind11;

#define DETECT_BUFFER_SIZE 0x9000

py::array_t<short> detect(py::array_t<unsigned char> &input){
    py::buffer_info input_info = input.request();
    if (input_info.ndim != 3)
        throw std::runtime_error("3-channel image must be 3 dims");
    if (input_info.shape[2] != 3)
        throw std::runtime_error("3-channel image must be 3 dims");

    unsigned char * pBuffer = (unsigned char *)malloc(DETECT_BUFFER_SIZE);
    if(!pBuffer)
    {
        throw std::runtime_error("Can not alloc buffer.");
    }
	int * pResults = nullptr; 
    pResults = facedetect_cnn(pBuffer, (unsigned char*)input_info.ptr, int(input_info.shape[1]), int(input_info.shape[0]), int(input_info.shape[1] * input_info.shape[2]));
    
    std::vector<py::ssize_t> bbox_shape{ pResults[0], 16 };
    py::array_t<short> bbox_buffer = py::array_t<short>(
        bbox_shape, 
        {bbox_shape[1] * sizeof(short), sizeof(short)}, 
        (short*)(pResults + 1));
    return bbox_buffer;
}


PYBIND11_MODULE(yuface, m) {
    m.doc() = "A tiny and fast face detector"; // optional module docstring
    m.def("detect", &detect, "The main detetion function");
}