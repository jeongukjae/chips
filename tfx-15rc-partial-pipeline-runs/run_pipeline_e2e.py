"""
MNIST Pipeline example code.
"""

import os

import tensorflow_model_analysis as tfma
import tfx
from absl import app, flags, logging
from tfx import components
from tfx.orchestration import pipeline
from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.proto import example_gen_pb2, trainer_pb2

FLAGS = flags.FLAGS
flags.DEFINE_string("pipeline_name", "mnist_pipeline", help="name of this pipeline")
flags.DEFINE_string("pipeline_root", "./pipeline_root", help="root directory for this pipeline")
flags.DEFINE_string("pipeline_metadata", "./pipeline_root/metadata.sqlite", help="metadata path for this pipeline")
flags.DEFINE_string("mnist_base_path", os.path.join(os.getenv("HOME"), "tensorflow_datasets", "mnist", "3.0.1"), help="name of this pipeline")


def main(_):
    LocalDagRunner().run(_create_pipeline())


def _create_pipeline() -> pipeline.Pipeline:
    """Implements MNIST classification example in TFX"""
    logging.info(f"Pipeline name: {FLAGS.pipeline_name}")
    logging.info(f"input_base for MNIST data: {FLAGS.mnist_base_path}")

    module_file = os.path.join(os.path.dirname(__file__), "mnist_utils_native_keras.py")

    # Brings data into the pipeline
    example_gen = components.ImportExampleGen(
        input_base=FLAGS.mnist_base_path,
        input_config=example_gen_pb2.Input(
            splits=[
                example_gen_pb2.Input.Split(
                    name="train",
                    pattern="*-train.tfrecord-*",
                ),
                example_gen_pb2.Input.Split(
                    name="eval",
                    pattern="*-test.tfrecord-*",
                ),
            ]
        ),
    )

    # Computes statistics over data for visualization and example validation.
    statistics_gen = components.StatisticsGen(examples=example_gen.outputs["examples"])

    # Generates schema based on statistics files.
    schema_gen = components.SchemaGen(statistics=statistics_gen.outputs["statistics"], infer_feature_shape=True)

    # Performs anomaly detection based on statistics and data schema.
    example_validator = components.ExampleValidator(statistics=statistics_gen.outputs["statistics"], schema=schema_gen.outputs["schema"])

    # Performs transformations and feature engineering in training and serving.
    transform = components.Transform(examples=example_gen.outputs["examples"], schema=schema_gen.outputs["schema"], module_file=module_file)

    trainer = components.Trainer(
        module_file=module_file,
        examples=transform.outputs["transformed_examples"],
        transform_graph=transform.outputs["transform_graph"],
        schema=schema_gen.outputs["schema"],
        train_args=trainer_pb2.TrainArgs(num_steps=5000),
        eval_args=trainer_pb2.EvalArgs(num_steps=100),
    )

    # Uses TFMA to compute evaluation statistics over features of a model and
    # performs quality validation of a candidate model.
    eval_config = tfma.EvalConfig(
        model_specs=[tfma.ModelSpec(label_key="label")],
        slicing_specs=[tfma.SlicingSpec()],
        metrics_specs=[
            tfma.MetricsSpec(
                metrics=[tfma.MetricConfig(class_name="SparseCategoricalAccuracy", threshold=tfma.MetricThreshold(value_threshold=tfma.GenericValueThreshold(lower_bound={"value": 0.8})))]
            )
        ],
    )

    # Uses TFMA to compute the evaluation statistics over features of a model.
    evaluator = components.Evaluator(examples=example_gen.outputs["examples"], model=trainer.outputs["model"], eval_config=eval_config)

    return pipeline.Pipeline(
        pipeline_name=FLAGS.pipeline_name,
        pipeline_root=FLAGS.pipeline_root,
        enable_cache=True,
        components=[
            example_gen,
            statistics_gen,
            schema_gen,
            example_validator,
            transform,
            trainer,
            evaluator,
        ],
        metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(FLAGS.pipeline_metadata),
    )


if __name__ == "__main__":
    app.run(main)
