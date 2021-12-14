# TF-Serving C++ Client Example with Bazel

Exmaple code to import tensorflow serving's `PredictService` using Bazel.

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
$ pip install numpy  # install numpy for tensorflow deps
$ bazel run //:test_client
INFO: Analyzed target //:test_client (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:test_client up-to-date:
  bazel-bin/test_client
INFO: Elapsed time: 5.389s, Critical Path: 5.19s
INFO: 3 processes: 1 internal, 2 darwin-sandbox.
INFO: Build completed successfully, 3 total actions
INFO: Build completed successfully, 3 total actions
Input x
        1       2       5
Output y
        2.5     3       4.5
```
