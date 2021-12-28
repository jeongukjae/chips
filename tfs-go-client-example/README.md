# TF-Serving Golang Client Example with Bazel

Exmaple code to import tensorflow serving's `PredictService` using Bazel.

I stored all required protobuf files in [this repository](https://github.com/jeongukjae/tensorflow-serving-apis-proto), and this example uses it. If you find a better way to import the required proto files, please let me know.

## Run

### Set up TF serving server

```sh
docker run -it --rm -p 8500:8500 \
    -v "$(pwd)/example_model:/models/:ro" \
    -e MODEL_NAME=half_plus_two \
    tensorflow/serving
```

### Build and run test client

```sh
$ bazel run //:main
INFO: Analyzed target //:main (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:main up-to-date:
  bazel-bin/main_/main
INFO: Elapsed time: 0.146s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
INFO: Build completed successfully, 1 total action
2021/12/29 04:24:30 Input x
2021/12/29 04:24:30     1.000000
2021/12/29 04:24:30     2.000000
2021/12/29 04:24:30     5.000000
2021/12/29 04:24:30 Response: {"model_spec":{"name":"half_plus_two","VersionChoice":{"Version":{"value":123}},"signature_name":"serving_default"},"outputs":{"y":{"dtype":1,"tensor_shape":{"dim":[{"size":1},{"size":3}]},"float_val":[2.5,3,4.5]}}}
2021/12/29 04:24:30 Output y
2021/12/29 04:24:30     2.500000
2021/12/29 04:24:30     3.000000
2021/12/29 04:24:30     4.500000
```
