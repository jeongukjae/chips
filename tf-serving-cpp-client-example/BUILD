load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")

buildifier(name = "buildifier")

cc_binary(
    name = "test_client",
    srcs = ["test_client.cc"],
    deps = [
        "@com_github_tensorflow_serving//tensorflow_serving/apis:prediction_service_cc_proto",
        "@com_github_grpc_grpc//:grpc",
    ],
)
