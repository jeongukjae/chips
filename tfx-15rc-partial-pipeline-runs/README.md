# Checking the usage of partial pipeline run in TFX 1.5.0rc0

This directory is to check the usage of partial pipeline run that is introduced in TFX 1.5.0rc. I copied and edited some codes from [MNIST pipeline example in TFX repository](https://github.com/tensorflow/tfx/tree/master/tfx/examples/mnist).

## To prepare

To check partial pipeline, we have to run successful pipeline for once.

```sh
pip install -r requirements.txt
# build mnist dataset to use in the pipeline
tfds build mnist
# running full pipeline will takes nearly 2 minutes.
python run_pipeline_e2e.py
```

## Run partial pipeline

```sh
$ python run_pipeline_e2e.py --with_partial_run
I1210 18:03:45.844377 4669636096 run_pipeline_e2e.py:38] Pipeline name: mnist_pipeline
I1210 18:03:45.844556 4669636096 run_pipeline_e2e.py:39] input_base for MNIST data: /Users/jeongukjae/tensorflow_datasets/mnist/3.0.1
...
... # some logs
...
I1210 18:03:48.127577 4669636096 local_dag_runner.py:88] Skipping component ImportExampleGen.
I1210 18:03:48.127788 4669636096 local_dag_runner.py:88] Skipping component StatisticsGen.
I1210 18:03:48.127947 4669636096 local_dag_runner.py:88] Skipping component SchemaGen.
I1210 18:03:48.128082 4669636096 local_dag_runner.py:88] Skipping component ExampleValidator.
I1210 18:03:48.128250 4669636096 local_dag_runner.py:88] Skipping component Transform.
I1210 18:03:48.128443 4669636096 local_dag_runner.py:88] Skipping component Trainer.
I1210 18:03:48.128583 4669636096 local_dag_runner.py:88] Skipping component Evaluator.
I1210 18:03:48.129348 4669636096 local_dag_runner.py:102] Component my_custom_component is running.
I1210 18:03:48.136124 4669636096 metadata_store.py:101] MetadataStore with DB connection initialized
I1210 18:03:48.136399 4669636096 partial_run_utils.py:130] snapshot_settings: latest_pipeline_run_strategy {
}

I1210 18:03:48.136713 4669636096 partial_run_utils.py:137] Using latest_pipeline_run_strategy.
I1210 18:03:48.136911 4669636096 partial_run_utils.py:140] Preparing to reuse artifacts.
I1210 18:03:48.138304 4669636096 partial_run_utils.py:448] base_run_id not provided. Default to latest pipeline run: 2021-12-10T18:01:19.166787
I1210 18:03:48.370673 4669636096 partial_run_utils.py:142] Artifact reuse complete.
I1210 18:03:48.371109 4669636096 launcher.py:515] Running launcher for node_info {
  type {
    name: "__main__.MyCustomComponent"
  }
  id: "my_custom_component"
}
...
... # some logs
...
I1210 18:03:48.377346 4669636096 metadata_store.py:101] MetadataStore with DB connection initialized
I1210 18:03:48.413310 4669636096 metadata_store.py:101] MetadataStore with DB connection initialized
I1210 18:03:48.414063 4669636096 launcher.py:376] Going to run a new execution 89
I1210 18:03:48.424570 4669636096 launcher.py:416] Going to run a new execution: ExecutionInfo(execution_id=89, input_dict={'evaluation': [Artifact(artifact: id: 86
...
... # some logs
...
I1210 18:03:48.425466 4669636096 run_pipeline_e2e.py:118] Running Custom Component...
I1210 18:03:48.425637 4669636096 run_pipeline_e2e.py:119] evaluation results: Artifact(artifact: id: 86
type_id: 29
uri: "./pipeline_root/Evaluator/evaluation/80"
custom_properties {
  key: "name"
  value {
    string_value: "mnist_pipeline:2021-12-10T18:01:19.166787:Evaluator:evaluation:0"
  }
}
...
... # some logs
...
I1210 18:03:48.426254 4669636096 launcher.py:463] Cleaning up stateless execution info.
I1210 18:03:48.427149 4669636096 launcher.py:558] Execution 89 succeeded.
I1210 18:03:48.427288 4669636096 launcher.py:477] Cleaning up stateful execution info.
I1210 18:03:48.428314 4669636096 launcher.py:568] Publishing output artifacts defaultdict(<class 'list'>, {}) for execution 89
I1210 18:03:48.434009 4669636096 metadata_store.py:101] MetadataStore with DB connection initialized
I1210 18:03:48.437344 4669636096 local_dag_runner.py:107] Component my_custom_component is finished.
```

As the above logs(`Skipping component *.`, `Artifact reuse complete.`) show, we can check the partial pipeline runs working properly.

If pipeline with partial runs does not have successful runs before, running the script with option `--with_partial_run` will fails with the log like `LookupError: No previous successful executions found for node_id ImportExampleGen in pipeline_run 2021-12-10T18:16:55.870408`.
