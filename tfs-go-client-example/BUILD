load("@io_bazel_rules_go//go:def.bzl", "go_binary", "go_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
load("@bazel_gazelle//:def.bzl", "gazelle")

# gazelle:prefix tfs-go-client-example
gazelle(name = "gazelle")

go_binary(
    name = "main",
    srcs = ["main.go"],
    deps = [
        ":tensorflow_serving_apis_go_proto",
        ":tensorflow_core_framework_go_proto",
        "@org_golang_google_grpc//:go_default_library",
    ],
    visibility = ["//visibility:public"],
)

go_proto_library(
    name = "tensorflow_serving_apis_go_proto",
    compiler = "@io_bazel_rules_go//proto:go_grpc",
    importpath = "github.com/tensorflow/serving/tensorflow_serving/apis",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_serving_apis_proto",
    deps = [
        ":tensorflow_core_example_go_proto",
        ":tensorflow_core_framework_go_proto",
        ":tensorflow_core_protobuf_go_proto",
        ":tensorflow_serving_config_go_proto",
    ],
)

go_proto_library(
    name = "tensorflow_serving_config_go_proto",
    importpath = "github.com/tensorflow/serving/tensorflow_serving/config",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_serving_config_proto",
)

go_proto_library(
    name = "tensorflow_core_framework_go_proto",
    importpath = "github.com/tensorflow/tensorflow/tensorflow/go/core/framework",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_core_framework_proto",
)

go_proto_library(
    name = "tensorflow_core_example_go_proto",
    importpath = "github.com/tensorflow/tensorflow/tensorflow/go/core/example",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_core_example_proto",
)

go_proto_library(
    name = "tensorflow_core_protobuf_go_proto",
    importpath = "github.com/tensorflow/tensorflow/tensorflow/go/core/protobuf",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_core_protobuf_proto",
    deps = [
        ":tensorflow_core_framework_go_proto",
    ],
)
