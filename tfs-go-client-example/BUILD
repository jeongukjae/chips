load("@io_bazel_rules_go//go:def.bzl", "go_binary", "go_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
load("@bazel_gazelle//:def.bzl", "gazelle")

# gazelle:prefix tfs-go-client-example
gazelle(name = "gazelle")

go_binary(
    name = "main",
    srcs = ["main.go"],
    deps = [
        ":tensorflow_serving_apis",
        ":tensorflow_core_framework",
        "@org_golang_google_grpc//:go_default_library",
    ],
    visibility = ["//visibility:public"],
)

go_proto_library(
    name = "tensorflow_serving_apis",
    compiler = "@io_bazel_rules_go//proto:go_grpc",
    importpath = "tensorflow_serving/apis",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_serving_apis_proto",
    deps = [
        ":tensorflow_core_example",
        ":tensorflow_core_framework",
        ":tensorflow_core_protobuf",
        ":tensorflow_serving_config",
    ],
)

go_proto_library(
    name = "tensorflow_serving_config",
    importpath = "tensorflow_serving/config",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_serving_config_proto",
)

go_proto_library(
    name = "tensorflow_core_framework",
    importpath = "github.com/tensorflow/tensorflow/tensorflow/go/core/framework",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_core_framework_proto",
)

go_proto_library(
    name = "tensorflow_core_example",
    importpath = "github.com/tensorflow/tensorflow/tensorflow/go/core/example",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_core_example_proto",
)

go_proto_library(
    name = "tensorflow_core_protobuf",
    importpath = "github.com/tensorflow/tensorflow/tensorflow/go/core/protobuf",
    proto = "@com_github_jeongukjae_tfs_proto//:tensorflow_core_protobuf_proto",
    deps = [
        ":tensorflow_core_framework",
    ],
)
