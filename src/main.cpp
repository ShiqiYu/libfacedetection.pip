#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "facedetectcnn.h"
namespace py = pybind11;

#define DETECT_BUFFER_SIZE 0x2000

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
	int * pResults = NULL; 
    pResults = facedetect_cnn(pBuffer, (unsigned char*)input_info.ptr, input_info.shape[1], input_info.shape[0], input_info.shape[0] * sizeof(float));
    std::vector<ssize_t> bbox_shape{ pResults[0], 15 };
    auto bbox_buffer = py::array_t<short>(bbox_shape, {bbox_shape[1] * sizeof(short), sizeof(short)}, (short*)(pResults + 1));
    return bbox_buffer;
}
    
PYBIND11_MODULE(yudet, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("detect", &detect, "A function that adds two numbers");
}