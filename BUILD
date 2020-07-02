load("@rules_python//python:defs.bzl", "py_binary")
load("@my_deps//:requirements.bzl", "requirement")

py_library(
    name = "t",
    srcs = ["t.py"],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        ":t",
        requirement("cmake"),
        requirement("Cython"),
        requirement("nagisa"),
        requirement("python-twitter"),
        requirement("regex"),
    ]
)
