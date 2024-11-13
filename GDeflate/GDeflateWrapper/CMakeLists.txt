cmake_minimum_required (VERSION 3.19)

project("GDeflateWrapper")

set(sources 
    "wrapper.cpp"
)

add_library(GDeflateWrapper SHARED ${sources})

target_compile_features(GDeflateWrapper PRIVATE cxx_std_17)
target_link_libraries(GDeflateWrapper PRIVATE GDeflate)
target_compile_definitions(GDeflateWrapper PRIVATE GDEFLATE_EXPORTS)